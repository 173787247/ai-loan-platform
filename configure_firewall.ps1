# Windows防火墙配置脚本
# 需要管理员权限运行

Write-Host "🔧 配置Windows防火墙规则..." -ForegroundColor Green
Write-Host ""

# 检查是否以管理员权限运行
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ 需要管理员权限才能配置防火墙规则" -ForegroundColor Red
    Write-Host "请右键点击PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "或者手动在Windows防火墙中添加以下规则:" -ForegroundColor Cyan
    Write-Host "1. 打开Windows Defender防火墙" -ForegroundColor White
    Write-Host "2. 点击'高级设置'" -ForegroundColor White
    Write-Host "3. 选择'入站规则' -> '新建规则'" -ForegroundColor White
    Write-Host "4. 选择'端口' -> 'TCP' -> '特定本地端口'" -ForegroundColor White
    Write-Host "5. 添加端口: 3000, 3001, 8000, 8080" -ForegroundColor White
    Write-Host "6. 选择'允许连接'" -ForegroundColor White
    Write-Host "7. 应用到所有网络配置文件" -ForegroundColor White
    Write-Host "8. 命名为'AI助贷平台端口'" -ForegroundColor White
    pause
    exit 1
}

Write-Host "✅ 检测到管理员权限，开始配置防火墙规则..." -ForegroundColor Green
Write-Host ""

# 配置防火墙规则
$ports = @(
    @{Port=3000; Name="AI助贷平台-主应用"},
    @{Port=3001; Name="AI助贷平台-管理后台"},
    @{Port=8000; Name="AI助贷平台-AI服务"},
    @{Port=8080; Name="AI助贷平台-API网关"}
)

foreach ($rule in $ports) {
    try {
        # 检查规则是否已存在
        $existingRule = Get-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue
        
        if ($existingRule) {
            Write-Host "⚠️  规则已存在: $($rule.Name) (端口 $($rule.Port))" -ForegroundColor Yellow
        } else {
            # 创建新的防火墙规则
            New-NetFirewallRule -DisplayName $rule.Name -Direction Inbound -Protocol TCP -LocalPort $rule.Port -Action Allow -Profile Any
            Write-Host "✅ 已创建规则: $($rule.Name) (端口 $($rule.Port))" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "❌ 创建规则失败: $($rule.Name) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔍 验证防火墙规则..." -ForegroundColor Yellow

# 验证规则
foreach ($rule in $ports) {
    $firewallRule = Get-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue
    if ($firewallRule) {
        $status = if ($firewallRule.Enabled -eq "True") { "启用" } else { "禁用" }
        Write-Host "✅ $($rule.Name): $status (端口 $($rule.Port))" -ForegroundColor Green
    } else {
        Write-Host "❌ $($rule.Name): 规则不存在" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎯 防火墙配置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📋 现在请测试远程访问:" -ForegroundColor Cyan
Write-Host "从公司访问: http://192.3.23.66:3000" -ForegroundColor White
Write-Host ""
Write-Host "如果仍然无法访问，请检查:" -ForegroundColor Yellow
Write-Host "1. 路由器端口转发是否正确配置" -ForegroundColor White
Write-Host "2. 路由器是否需要重启" -ForegroundColor White
Write-Host "3. 网络提供商是否限制入站连接" -ForegroundColor White
Write-Host ""

pause
