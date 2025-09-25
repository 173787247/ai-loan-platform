@echo off
chcp 65001 >nul
echo 🚀 启动AI智能助贷招标平台 (GPU版本)
echo.

echo 📋 检查Docker状态...
docker --version
if %errorlevel% neq 0 (
    echo ❌ Docker未安装或未启动，请先启动Docker Desktop
    pause
    exit /b 1
)

echo.
echo 🔍 检查Docker Desktop是否运行...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Docker Desktop未运行，请先启动Docker Desktop
    echo 💡 启动Docker Desktop后，再次运行此脚本
    pause
    exit /b 1
)

echo.
echo 🔍 检查NVIDIA Docker支持...
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ NVIDIA Docker支持未检测到，将使用CPU版本
    set USE_GPU=false
) else (
    echo ✅ 检测到NVIDIA GPU支持
    set USE_GPU=true
)

echo.
echo 🚀 启动服务...
if "%USE_GPU%"=="true" (
    echo 使用GPU版本启动...
    docker-compose -f docker-compose.gpu.yml up -d
) else (
    echo 使用CPU版本启动...
    docker-compose -f docker-compose.yml up -d
)

echo.
echo ⏳ 等待服务启动...
timeout /t 30 /nobreak >nul

echo.
echo ✅ 服务启动完成！
echo.
echo 📋 访问地址：
echo   - Web应用: http://localhost:3000
echo   - API网关: http://localhost:8080
echo   - AI服务: http://localhost:8000
echo   - MySQL: localhost:3306
echo   - Redis: localhost:6379
echo   - MongoDB: localhost:27017
echo   - Elasticsearch: http://localhost:9200
echo.
echo 📊 查看服务状态：
if "%USE_GPU%"=="true" (
    docker-compose -f docker-compose.gpu.yml ps
) else (
    docker-compose -f docker-compose.yml ps
)
echo.
echo 🛑 停止服务：
if "%USE_GPU%"=="true" (
    echo docker-compose -f docker-compose.gpu.yml down
) else (
    echo docker-compose -f docker-compose.yml down
)
echo.
pause
