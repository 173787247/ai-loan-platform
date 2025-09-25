# AI智能助贷招标平台 - Spring Boot应用构建脚本
# 版本: 1.1.0
# 最后更新: 2025-09-13

Write-Host "🚀 开始构建Spring Boot应用..." -ForegroundColor Green

# 检查Java环境
Write-Host "🔍 检查Java环境..." -ForegroundColor Yellow
try {
    $javaVersion = java -version 2>&1 | Select-String "version"
    Write-Host "✅ Java环境: $javaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Java环境，请先安装Java 11+" -ForegroundColor Red
    exit 1
}

# 检查Maven环境
Write-Host "🔍 检查Maven环境..." -ForegroundColor Yellow
try {
    $mavenVersion = mvn -version 2>&1 | Select-String "Apache Maven"
    Write-Host "✅ Maven环境: $mavenVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Maven环境，请先安装Maven" -ForegroundColor Red
    exit 1
}

# 构建API网关
Write-Host "🔨 构建API网关服务..." -ForegroundColor Yellow
Set-Location "backend/ai-loan-gateway"
try {
    mvn clean package -DskipTests
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ API网关构建成功" -ForegroundColor Green
    } else {
        Write-Host "❌ API网关构建失败" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ API网关构建异常: $_" -ForegroundColor Red
    exit 1
}
Set-Location "../.."

# 构建用户服务
Write-Host "🔨 构建用户服务..." -ForegroundColor Yellow
Set-Location "backend/ai-loan-user"
try {
    mvn clean package -DskipTests
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 用户服务构建成功" -ForegroundColor Green
    } else {
        Write-Host "❌ 用户服务构建失败" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ 用户服务构建异常: $_" -ForegroundColor Red
    exit 1
}
Set-Location "../.."

Write-Host "🎉 所有Spring Boot应用构建完成！" -ForegroundColor Green
Write-Host "📦 构建产物位置:" -ForegroundColor Cyan
Write-Host "   - API网关: backend/ai-loan-gateway/target/ai-loan-gateway-1.1.0.jar" -ForegroundColor Cyan
Write-Host "   - 用户服务: backend/ai-loan-user/target/ai-loan-user-1.1.0.jar" -ForegroundColor Cyan