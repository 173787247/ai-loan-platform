#!/bin/bash

# AI智能助贷招标平台 - 部署脚本

set -e

echo "🚀 开始部署AI智能助贷招标平台..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs
mkdir -p data/mysql
mkdir -p data/redis
mkdir -p data/mongodb
mkdir -p data/elasticsearch

# 设置权限
echo "🔐 设置目录权限..."
chmod 755 data/mysql
chmod 755 data/redis
chmod 755 data/mongodb
chmod 755 data/elasticsearch

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down || true

# 构建镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 显示访问信息
echo "✅ 部署完成！"
echo ""
echo "📋 服务访问信息："
echo "  - Web应用: http://localhost:3000"
echo "  - 管理后台: http://localhost:3001"
echo "  - API网关: http://localhost:8080"
echo "  - AI服务: http://localhost:8000"
echo "  - MySQL: localhost:3306"
echo "  - Redis: localhost:6379"
echo "  - MongoDB: localhost:27017"
echo "  - Elasticsearch: http://localhost:9200"
echo ""
echo "📊 查看日志："
echo "  docker-compose logs -f"
echo ""
echo "🛑 停止服务："
echo "  docker-compose down"
echo ""
echo "🎉 部署成功！请访问 http://localhost:3000 开始使用"
