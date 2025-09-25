# 快速远程访问解决方案
Write-Host "🚀 AI助贷平台远程访问解决方案" -ForegroundColor Green
Write-Host ""

# 检查本地服务状态
Write-Host "📋 检查本地服务状态..." -ForegroundColor Yellow
Write-Host "主应用: http://localhost:3000" -ForegroundColor Cyan
Write-Host "管理后台: http://localhost:3001" -ForegroundColor Cyan
Write-Host "AI服务: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API网关: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""

# 测试本地连接
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ 主应用本地访问正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 主应用本地访问失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔧 远程访问解决方案:" -ForegroundColor Yellow
Write-Host ""
Write-Host "方案1: 路由器端口转发 (推荐)" -ForegroundColor Cyan
Write-Host "1. 确认路由器端口转发规则已保存" -ForegroundColor White
Write-Host "2. 重启路由器" -ForegroundColor White
Write-Host "3. 从公司访问: http://192.3.23.66:3000" -ForegroundColor White
Write-Host ""
Write-Host "方案2: 使用内网穿透工具" -ForegroundColor Cyan
Write-Host "1. 下载ngrok: https://ngrok.com/download" -ForegroundColor White
Write-Host "2. 运行: ngrok http 3000" -ForegroundColor White
Write-Host "3. 使用显示的https://xxxxx.ngrok.io地址" -ForegroundColor White
Write-Host ""
Write-Host "方案3: 使用Cloudflare Tunnel" -ForegroundColor Cyan
Write-Host "1. 下载cloudflared: https://github.com/cloudflare/cloudflared/releases" -ForegroundColor White
Write-Host "2. 运行: cloudflared tunnel --url http://localhost:3000" -ForegroundColor White
Write-Host ""

# 提供简单的ngrok启动脚本
Write-Host "🚀 正在创建ngrok启动脚本..." -ForegroundColor Yellow

$ngrokScript = @"
@echo off
echo 🚀 启动AI助贷平台内网穿透...
echo.
echo 📋 请先下载ngrok: https://ngrok.com/download
echo 📋 解压到当前目录
echo.
echo 🔧 启动主应用内网穿透...
ngrok.exe http 3000
echo.
echo ✅ 请使用ngrok显示的https://xxxxx.ngrok.io地址从公司访问
pause
"@

$ngrokScript | Out-File -FilePath "start_ngrok.bat" -Encoding UTF8

Write-Host "✅ 已创建 start_ngrok.bat 脚本" -ForegroundColor Green
Write-Host "📋 使用方法:" -ForegroundColor Yellow
Write-Host "1. 下载ngrok: https://ngrok.com/download" -ForegroundColor White
Write-Host "2. 解压ngrok.exe到当前目录" -ForegroundColor White
Write-Host "3. 运行: .\start_ngrok.bat" -ForegroundColor White
Write-Host "4. 使用显示的https://xxxxx.ngrok.io地址" -ForegroundColor White
Write-Host ""

Write-Host "🎯 推荐使用方案2 (ngrok) 快速解决远程访问问题！" -ForegroundColor Green
