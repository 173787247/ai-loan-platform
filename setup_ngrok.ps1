# 内网穿透设置脚本
# 使用ngrok进行内网穿透

Write-Host "🚀 设置内网穿透..." -ForegroundColor Green

# 检查是否已安装ngrok
if (-not (Get-Command ngrok -ErrorAction SilentlyContinue)) {
    Write-Host "📥 下载ngrok..." -ForegroundColor Yellow
    
    # 创建临时目录
    $tempDir = "$env:TEMP\ngrok"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    
    # 下载ngrok
    $ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    $ngrokZip = "$tempDir\ngrok.zip"
    
    try {
        Invoke-WebRequest -Uri $ngrokUrl -OutFile $ngrokZip
        Expand-Archive -Path $ngrokZip -DestinationPath $tempDir -Force
        
        # 复制到系统路径
        Copy-Item "$tempDir\ngrok.exe" -Destination "$env:USERPROFILE\ngrok.exe" -Force
        
        Write-Host "✅ ngrok安装完成" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ ngrok下载失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "请手动下载: https://ngrok.com/download" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "🔧 启动内网穿透..." -ForegroundColor Green

# 启动ngrok隧道
Write-Host "主应用: http://localhost:3000" -ForegroundColor Cyan
Write-Host "管理后台: http://localhost:3001" -ForegroundColor Cyan
Write-Host "AI服务: http://localhost:8000" -ForegroundColor Cyan

# 启动主应用隧道
Start-Process -FilePath "ngrok" -ArgumentList "http", "3000" -WindowStyle Minimized

Write-Host "✅ 内网穿透已启动" -ForegroundColor Green
Write-Host "📱 请查看ngrok控制台获取公网访问地址" -ForegroundColor Yellow
Write-Host "🌐 通常格式为: https://xxxxx.ngrok.io" -ForegroundColor Yellow
