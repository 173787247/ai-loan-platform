@echo off
echo 🚀 启动AI智能助贷招标平台 (简化版)
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
echo 🚀 启动核心服务...
docker-compose -f docker-compose.simple.yml up -d

echo.
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

echo.
echo ✅ 服务启动完成！
echo.
echo 📋 访问地址：
echo   - Web应用: http://localhost:3000
echo   - MySQL: localhost:3306
echo   - Redis: localhost:6379
echo.
echo 📊 查看服务状态：
echo   docker-compose -f docker-compose.simple.yml ps
echo.
echo 🛑 停止服务：
echo   docker-compose -f docker-compose.simple.yml down
echo.
pause
