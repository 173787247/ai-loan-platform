#!/bin/bash

echo "🚀 AI助贷招标平台 - 环境变量设置脚本"
echo "================================================"

echo ""
echo "📋 正在创建 .env 文件..."

# 复制预设文件为 .env
cp env.preset .env

if [ $? -eq 0 ]; then
    echo "✅ .env 文件创建成功！"
    echo ""
    echo "📝 请编辑 .env 文件，填入您的API密钥："
    echo ""
    echo "1. 打开 .env 文件"
    echo "2. 找到 OPENAI_API_KEY=sk-your-openai-api-key-here"
    echo "3. 替换为您的真实OpenAI API密钥"
    echo "4. 保存文件"
    echo ""
    echo "🔧 配置完成后，运行以下命令重启AI服务："
    echo "   docker-compose -f docker-compose.prod.yml restart ai-service"
    echo ""
    echo "🧪 然后运行测试验证配置："
    echo "   python test_env_config.py"
    echo ""
    echo "📚 更多帮助请查看："
    echo "   - ENV_SETUP_GUIDE.md (详细配置指南)"
    echo "   - QUICK_START.md (快速开始指南)"
    echo ""
else
    echo "❌ .env 文件创建失败！"
    echo "请手动复制 env.preset 为 .env"
    exit 1
fi
