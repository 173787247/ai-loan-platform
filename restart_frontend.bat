@echo off
echo 正在重启前端容器...
cd /d "C:\Users\rchua\Desktop\AIFullStackDevelopment\ai-loan-platform"
docker restart ai-loan-web-app
echo 前端容器重启完成！
echo 请访问 http://localhost:3000 测试AI客服
pause
