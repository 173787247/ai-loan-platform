# Cloudflare Tunnel 设置脚本
# 免费、安全的内网穿透方案

Write-Host "🚀 设置Cloudflare Tunnel..." -ForegroundColor Green

# 检查是否已安装cloudflared
if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Host "📥 下载cloudflared..." -ForegroundColor Yellow
    
    # 创建临时目录
    $tempDir = "$env:TEMP\cloudflared"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    
    # 下载cloudflared
    $cloudflaredUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    $cloudflaredExe = "$tempDir\cloudflared.exe"
    
    try {
        Invoke-WebRequest -Uri $cloudflaredUrl -OutFile $cloudflaredExe
        Copy-Item $cloudflaredExe -Destination "$env:USERPROFILE\cloudflared.exe" -Force
        
        Write-Host "✅ cloudflared安装完成" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ cloudflared下载失败: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "请手动下载: https://github.com/cloudflare/cloudflared/releases" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "🔧 启动Cloudflare Tunnel..." -ForegroundColor Green

# 创建配置文件
$configContent = @"
tunnel: ai-loan-platform
credentials-file: $env:USERPROFILE\.cloudflared\ai-loan-platform.json

ingress:
  - hostname: ai-loan-platform.your-domain.com
    service: http://localhost:3000
  - hostname: ai-loan-admin.your-domain.com
    service: http://localhost:3001
  - hostname: ai-loan-api.your-domain.com
    service: http://localhost:8000
  - service: http_status:404
"@

$configDir = "$env:USERPROFILE\.cloudflared"
New-Item -ItemType Directory -Path $configDir -Force | Out-Null
$configContent | Out-File -FilePath "$configDir\config.yml" -Encoding UTF8

Write-Host "📝 配置文件已创建: $configDir\config.yml" -ForegroundColor Cyan
Write-Host "🔑 请先运行: cloudflared tunnel login" -ForegroundColor Yellow
Write-Host "🏗️ 然后运行: cloudflared tunnel create ai-loan-platform" -ForegroundColor Yellow
Write-Host "🚀 最后运行: cloudflared tunnel run ai-loan-platform" -ForegroundColor Yellow
