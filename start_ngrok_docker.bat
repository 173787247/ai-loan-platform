@echo off
echo 🚀 启动Docker版本的ngrok内网穿透...
echo.

echo 📋 请先注册ngrok账号获取authtoken:
echo 1. 访问: https://ngrok.com/signup
echo 2. 注册免费账号
echo 3. 获取authtoken
echo.

set /p authtoken=请输入您的ngrok authtoken: 

if "%authtoken%"=="" (
    echo ❌ 需要authtoken才能使用ngrok
    echo 请访问 https://ngrok.com/signup 注册获取
    pause
    exit /b 1
)

echo.
echo 🔧 设置环境变量...
set NGROK_AUTHTOKEN=%authtoken%

echo.
echo 🐳 启动Docker容器...
docker-compose -f docker-compose.ngrok.yml up -d

echo.
echo ✅ ngrok已启动！
echo 📱 访问 http://localhost:4040 查看ngrok状态
echo 🌐 使用显示的https://xxxxx.ngrok.io地址让朋友访问
echo.
echo 按任意键停止ngrok...
pause

echo.
echo 🛑 停止ngrok...
docker-compose -f docker-compose.ngrok.yml down
