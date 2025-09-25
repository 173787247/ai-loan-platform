#!/bin/bash

# AI智能贷款平台监控启动脚本

echo "启动AI智能贷款平台监控系统..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker未运行，请先启动Docker"
    exit 1
fi

# 创建监控网络
echo "创建监控网络..."
docker network create ai-loan-network 2>/dev/null || true

# 启动监控服务
echo "启动Prometheus..."
docker-compose -f docker-compose.monitoring.yml up -d prometheus

echo "启动Grafana..."
docker-compose -f docker-compose.monitoring.yml up -d grafana

echo "启动AlertManager..."
docker-compose -f docker-compose.monitoring.yml up -d alertmanager

echo "启动Node Exporter..."
docker-compose -f docker-compose.monitoring.yml up -d node-exporter

echo "启动cAdvisor..."
docker-compose -f docker-compose.monitoring.yml up -d cadvisor

echo "启动Jaeger..."
docker-compose -f docker-compose.monitoring.yml up -d jaeger

echo "启动ELK日志系统..."
docker-compose -f docker-compose.monitoring.yml up -d elasticsearch-logs
sleep 10
docker-compose -f docker-compose.monitoring.yml up -d logstash
docker-compose -f docker-compose.monitoring.yml up -d kibana

# 等待服务启动
echo "等待服务启动..."
sleep 30

# 检查服务状态
echo "检查服务状态..."
docker-compose -f docker-compose.monitoring.yml ps

echo ""
echo "监控服务启动完成！"
echo ""
echo "访问地址:"
echo "  Prometheus: http://localhost:9090"
echo "  Grafana: http://localhost:3000 (admin/admin123)"
echo "  AlertManager: http://localhost:9093"
echo "  Jaeger: http://localhost:16686"
echo "  Kibana: http://localhost:5601"
echo "  cAdvisor: http://localhost:8081"
echo ""
echo "请确保主应用服务也在运行: docker-compose up -d"
