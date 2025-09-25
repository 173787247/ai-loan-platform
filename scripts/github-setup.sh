#!/bin/bash

# AI智能助贷招标平台 - GitHub仓库设置脚本

set -e

echo "🚀 设置GitHub仓库..."

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "📁 初始化Git仓库..."
    git init
fi

# 添加所有文件
echo "📝 添加文件到Git..."
git add .

# 提交更改
echo "💾 提交更改..."
git commit -m "Initial commit: AI智能助贷招标平台

- 完整的四层AI应用架构
- Spring Boot微服务后端
- React前端应用
- Python AI服务
- Docker容器化部署
- Kubernetes配置
- 完整的文档和API"

# 设置远程仓库
echo "🔗 设置远程仓库..."
echo "请先在GitHub上创建仓库，然后运行以下命令："
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/ai-loan-platform.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "或者使用SSH："
echo "git remote add origin git@github.com:YOUR_USERNAME/ai-loan-platform.git"
echo "git branch -M main"
echo "git push -u origin main"

echo "✅ GitHub仓库设置完成！"
echo ""
echo "📋 下一步："
echo "1. 在GitHub上创建新仓库：https://github.com/new"
echo "2. 仓库名称：ai-loan-platform"
echo "3. 描述：AI智能助贷招标平台 - 基于四层AI应用架构的金融科技平台"
echo "4. 选择Public或Private"
echo "5. 不要初始化README、.gitignore或LICENSE（我们已经有了）"
echo "6. 运行上面显示的git命令"
