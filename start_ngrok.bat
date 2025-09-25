@echo off
echo 🚀 启动AI助贷平台内网穿透...
echo.
echo 📋 请先下载ngrok: https://ngrok.com/download
echo 📋 解压ngrok.exe到当前目录
echo.
echo 🔧 启动主应用内网穿透...
ngrok.exe http 3000
echo.
echo ✅ 请使用ngrok显示的https://xxxxx.ngrok.io地址从公司访问
pause
