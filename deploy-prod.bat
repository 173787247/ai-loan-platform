@echo off
REM AI助贷招标平台 - 生产环境部署脚本 (Windows)
REM 作者: AI Loan Platform Team
REM 版本: 1.0.0

setlocal enabledelayedexpansion

echo 🚀 开始生产环境部署...

REM 检查Docker和Docker Compose
:check_prerequisites
echo [INFO] 检查前置条件...

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker 未安装，请先安装 Docker Desktop
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose 未安装，请先安装 Docker Compose
    exit /b 1
)

echo [SUCCESS] 前置条件检查通过

REM 创建必要的目录
:create_directories
echo [INFO] 创建必要的目录...

if not exist "data\mysql" mkdir data\mysql
if not exist "data\redis" mkdir data\redis
if not exist "data\mongodb" mkdir data\mongodb
if not exist "data\elasticsearch" mkdir data\elasticsearch
if not exist "data\ai-models" mkdir data\ai-models
if not exist "data\ai-uploads" mkdir data\ai-uploads
if not exist "logs\nginx" mkdir logs\nginx
if not exist "logs\applications" mkdir logs\applications

echo [SUCCESS] 目录创建完成

REM 设置环境变量
:setup_environment
echo [INFO] 设置环境变量...

if not exist ".env.prod" (
    echo [WARNING] 未找到 .env.prod 文件，使用默认配置
    copy env.prod.example .env.prod
    echo [WARNING] 请编辑 .env.prod 文件以配置生产环境参数
)

echo [SUCCESS] 环境变量设置完成

REM 构建镜像
:build_images
echo [INFO] 构建Docker镜像...

echo [INFO] 构建AI服务镜像...
docker-compose -f docker-compose.prod.yml build ai-service

echo [INFO] 构建网关服务镜像...
docker-compose -f docker-compose.prod.yml build gateway

echo [INFO] 构建其他服务镜像...
docker-compose -f docker-compose.prod.yml build user-service loan-service risk-service matching-service admin-service

echo [INFO] 构建前端应用镜像...
docker-compose -f docker-compose.prod.yml build web-app admin-app

echo [SUCCESS] 镜像构建完成

REM 启动服务
:start_services
echo [INFO] 启动生产环境服务...

echo [INFO] 启动数据库服务...
docker-compose -f docker-compose.prod.yml up -d mysql redis mongodb elasticsearch

echo [INFO] 等待数据库启动...
timeout /t 30 /nobreak >nul

echo [INFO] 启动AI服务...
docker-compose -f docker-compose.prod.yml up -d ai-service

echo [INFO] 等待AI服务启动...
timeout /t 20 /nobreak >nul

echo [INFO] 启动后端服务...
docker-compose -f docker-compose.prod.yml up -d user-service loan-service risk-service matching-service admin-service

echo [INFO] 等待后端服务启动...
timeout /t 30 /nobreak >nul

echo [INFO] 启动网关服务...
docker-compose -f docker-compose.prod.yml up -d gateway

echo [INFO] 等待网关启动...
timeout /t 20 /nobreak >nul

echo [INFO] 启动前端应用...
docker-compose -f docker-compose.prod.yml up -d web-app admin-app

echo [INFO] 启动Nginx负载均衡器...
docker-compose -f docker-compose.prod.yml up -d nginx

echo [SUCCESS] 所有服务启动完成

REM 健康检查
:health_check
echo [INFO] 执行健康检查...

curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] AI服务健康检查通过
) else (
    echo [ERROR] AI服务健康检查失败
)

curl -f http://localhost:8080/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] 网关健康检查通过
) else (
    echo [WARNING] 网关健康检查失败，可能正在启动中
)

curl -f http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] 前端应用健康检查通过
) else (
    echo [WARNING] 前端应用健康检查失败，可能正在启动中
)

curl -f http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] 管理后台健康检查通过
) else (
    echo [WARNING] 管理后台健康检查失败，可能正在启动中
)

REM 显示服务状态
:show_status
echo [INFO] 服务状态:
docker-compose -f docker-compose.prod.yml ps

echo.
echo [INFO] 访问地址:
echo   前端应用: http://localhost:3000
echo   管理后台: http://localhost:3001
echo   API网关: http://localhost:8080
echo   AI服务: http://localhost:8000
echo   Nginx: http://localhost:80

echo.
echo [SUCCESS] 生产环境部署完成！
echo 请访问 http://localhost:3000 查看应用

endlocal
