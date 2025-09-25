@echo off
echo ========================================
echo AI智能助贷招标平台 - GPU版本启动
echo ========================================

echo 检查Docker状态...
docker --version
if %errorlevel% neq 0 (
    echo 错误: Docker未安装或未启动
    pause
    exit /b 1
)

echo 检查NVIDIA GPU支持...
docker run --rm --gpus all nvidia/cuda:11.2-base-ubuntu20.04 nvidia-smi
if %errorlevel% neq 0 (
    echo 警告: GPU支持可能不可用，将使用CPU模式
)

echo 启动基础服务...
docker-compose up -d mysql redis mongodb elasticsearch rabbitmq

echo 等待基础服务启动...
timeout /t 10 /nobreak

echo 启动AI服务 (GPU版本)...
docker-compose -f docker-compose.gpu.yml up -d ai-service

echo 启动Web应用...
docker-compose up -d web-app gateway user-service

echo ========================================
echo 服务启动完成！
echo ========================================
echo 演示页面: http://localhost:8089
echo Web应用: http://localhost:3000
echo API网关: http://localhost:8080
echo AI服务: http://localhost:8000
echo ========================================

pause
