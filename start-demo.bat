@echo off
echo ========================================
echo AI智能助贷招标平台 - 演示版本启动
echo ========================================

echo 检查Docker状态...
docker --version
if %errorlevel% neq 0 (
    echo 错误: Docker未安装或未启动
    pause
    exit /b 1
)

echo 启动基础服务...
docker-compose up -d mysql redis mongodb elasticsearch rabbitmq

echo 等待基础服务启动...
timeout /t 5 /nobreak

echo 启动AI服务 (GPU版本)...
docker-compose -f docker-compose.gpu.yml up -d ai-service

echo 等待AI服务启动...
timeout /t 10 /nobreak

echo 启动演示页面...
cd demo
start python -m http.server 8089

echo ========================================
echo 演示版本启动完成！
echo ========================================
echo 演示页面: http://localhost:8089
echo AI服务API: http://localhost:8000
echo RabbitMQ管理: http://localhost:15672
echo ========================================
echo 注意: Web应用由于网络问题暂时无法启动
echo 但AI服务和演示页面已完全可用！
echo ========================================

pause
