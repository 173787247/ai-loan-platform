# 部署指南

## 环境要求

### 系统要求
- **操作系统**: Linux (Ubuntu 20.04+), macOS 12+, Windows 11+
- **内存**: 最低 16GB，推荐 32GB+ (AI服务需要更多内存)
- **存储**: 最低 100GB 可用空间 (包含AI模型和区块链数据)
- **网络**: 稳定的互联网连接，支持WebSocket和MQTT
- **GPU**: 可选，用于AI加速 (NVIDIA RTX 3060+ 推荐)

### 软件要求
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Kubernetes**: 1.28+ (生产环境)
- **Java**: 17+ (如果本地运行)
- **Node.js**: 18+ (如果本地运行)
- **Python**: 3.9+ (如果本地运行)
- **NVIDIA Container Toolkit**: 2.0+ (GPU支持)

## 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/173787247/ai-loan-platform.git
cd ai-loan-platform
```

### 2. 配置环境变量

复制环境变量模板：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```bash
# 数据库配置
MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=ai_loan_platform
MYSQL_USER=ai_loan
MYSQL_PASSWORD=ai_loan123

# Redis配置
REDIS_PASSWORD=redis123

# MongoDB配置
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=mongo123
MONGO_DATABASE=ai_loan_analytics

# Elasticsearch配置
ELASTICSEARCH_PASSWORD=elastic123

# JWT配置
JWT_SECRET=ai-loan-platform-secret-key-2025-v6
JWT_EXPIRATION=86400

# AI服务配置
AI_SERVICE_URL=http://ai-service:8000
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key

# 区块链配置
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your-project-id
PRIVATE_KEY=your-private-key
CONTRACT_ADDRESS=0x...

# 物联网配置
MQTT_BROKER_URL=mqtt://localhost:1883
MQTT_USERNAME=mqtt_user
MQTT_PASSWORD=mqtt_pass

# 监控配置
PROMETHEUS_RETENTION_TIME=30d
GRAFANA_ADMIN_PASSWORD=admin123
```

### 3. 启动服务

#### 开发环境
```bash
# 启动简化版本（不包含AI服务）
docker-compose -f docker-compose.simple.yml up -d

# 启动最小化版本（仅核心服务）
docker-compose -f docker-compose.minimal.yml up -d
```

#### 生产环境
```bash
# 启动完整服务栈（包含AI和区块链服务）
docker-compose -f docker-compose.gpu.yml up -d

# 启动监控服务
docker-compose -f docker-compose.monitoring.yml up -d
```

#### 使用部署脚本
```bash
# Linux/macOS
./scripts/deploy.sh

# Windows
.\scripts\deploy.bat
```

### 4. 验证部署

检查服务状态：

```bash
# 检查所有服务状态
docker-compose ps

# 检查特定服务日志
docker-compose logs ai-loan-gateway
docker-compose logs ai-service
docker-compose logs web-app
```

访问服务：
- **Web应用**: http://localhost:3000
- **管理后台**: http://localhost:3001
- **API文档**: http://localhost:8080/swagger-ui.html
- **监控面板**: http://localhost:9090 (Prometheus)
- **可视化监控**: http://localhost:3001 (Grafana)
- **区块链浏览器**: http://localhost:3002

## 生产环境部署

### 1. 使用Kubernetes

```bash
# 创建命名空间
kubectl apply -f k8s/namespace.yaml

# 部署数据库
kubectl apply -f k8s/mysql-deployment.yaml

# 部署应用服务
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ai-service-deployment.yaml
```

### 2. 使用Docker Swarm

```bash
# 初始化Swarm
docker swarm init

# 部署服务栈
docker stack deploy -c docker-compose.prod.yml ai-loan-platform
```

### 3. 使用云服务

#### AWS部署

1. 使用ECS Fargate
2. 使用RDS MySQL
3. 使用ElastiCache Redis
4. 使用S3存储文件

#### 阿里云部署

1. 使用ACK (Kubernetes)
2. 使用RDS MySQL
3. 使用Redis
4. 使用OSS存储文件

## 配置说明

### 数据库配置

#### MySQL配置

```yaml
mysql:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    MYSQL_DATABASE: ${MYSQL_DATABASE}
    MYSQL_USER: ${MYSQL_USER}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  volumes:
    - mysql_data:/var/lib/mysql
    - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
```

#### Redis配置

```yaml
redis:
  image: redis:6.0-alpine
  command: redis-server --requirepass ${REDIS_PASSWORD}
  volumes:
    - redis_data:/data
```

### 应用配置

#### 后端服务配置

```yaml
# application-prod.yml
spring:
  datasource:
    url: jdbc:mysql://mysql:3306/ai_loan_platform
    username: ${MYSQL_USER}
    password: ${MYSQL_PASSWORD}
  redis:
    host: redis
    password: ${REDIS_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
```

#### 前端配置

```javascript
// config.js
const config = {
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080',
  aiServiceUrl: process.env.REACT_APP_AI_SERVICE_URL || 'http://localhost:8000'
};
```

## 监控和日志

### 日志配置

```yaml
logging:
  level:
    com.ai-loan: INFO
    org.springframework: WARN
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: logs/ai-loan-platform.log
```

### 监控配置

使用Prometheus + Grafana：

```yaml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin123
```

## 备份和恢复

### 数据库备份

```bash
# 备份MySQL
docker exec mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} ai_loan_platform > backup.sql

# 恢复MySQL
docker exec -i mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} ai_loan_platform < backup.sql
```

### 文件备份

```bash
# 备份上传文件
tar -czf uploads-backup.tar.gz uploads/

# 恢复上传文件
tar -xzf uploads-backup.tar.gz
```

## 安全配置

### SSL/TLS配置

```yaml
# nginx.conf
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    
    location / {
        proxy_pass http://frontend:80;
    }
}
```

### 防火墙配置

```bash
# 开放必要端口
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 3306  # MySQL (仅内网)
ufw allow 6379  # Redis (仅内网)
```

## 性能优化

### 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tenders_user_status ON tenders(user_id, status);
CREATE INDEX idx_proposals_tender_score ON proposals(tender_id, score);

-- 优化查询
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```

### 应用优化

```yaml
# JVM参数
JAVA_OPTS: "-Xms2g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"

# 连接池配置
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
```

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查日志
   docker-compose logs service-name
   
   # 检查端口占用
   netstat -tulpn | grep :8080
   ```

2. **数据库连接失败**
   ```bash
   # 检查数据库状态
   docker-compose exec mysql mysql -u root -p
   
   # 检查网络连接
   docker-compose exec backend ping mysql
   ```

3. **内存不足**
   ```bash
   # 检查内存使用
   docker stats
   
   # 增加内存限制
   deploy:
     resources:
       limits:
         memory: 2Gi
   ```

### 日志分析

```bash
# 查看错误日志
docker-compose logs | grep ERROR

# 查看访问日志
docker-compose logs nginx | grep "GET /"

# 实时监控日志
docker-compose logs -f
```

## 更新和维护

### 应用更新

```bash
# 拉取最新代码
git pull origin main

# 重新构建镜像
docker-compose build

# 重启服务
docker-compose up -d
```

### 数据库迁移

```bash
# 运行数据库迁移
docker-compose exec backend ./mvnw flyway:migrate
```

### 定期维护

```bash
# 清理Docker镜像
docker system prune -a

# 清理日志文件
find logs/ -name "*.log" -mtime +30 -delete

# 备份数据库
./scripts/backup.sh

# 清理区块链数据
docker-compose exec blockchain-node geth --datadir /data removedb

# 清理AI模型缓存
docker-compose exec ai-service python -c "import torch; torch.cuda.empty_cache()"
```

## 高级部署选项

### 区块链节点部署

#### 以太坊节点
```bash
# 启动以太坊节点
docker-compose -f docker-compose.blockchain.yml up -d ethereum-node

# 检查节点状态
docker-compose exec ethereum-node geth attach --exec "eth.blockNumber"
```

#### 智能合约部署
```bash
# 编译智能合约
docker-compose exec truffle truffle compile

# 部署智能合约
docker-compose exec truffle truffle migrate --network development
```

### 物联网设备部署

#### MQTT Broker
```bash
# 启动MQTT Broker
docker-compose -f docker-compose.iot.yml up -d mqtt-broker

# 配置设备连接
docker-compose exec mqtt-broker mosquitto_pub -h localhost -t "device/001" -m "hello"
```

#### 设备模拟器
```bash
# 启动设备模拟器
docker-compose -f docker-compose.iot.yml up -d device-simulator

# 查看设备数据
docker-compose logs device-simulator
```

### AI服务部署

#### GPU加速部署
```bash
# 检查GPU支持
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# 启动GPU加速AI服务
docker-compose -f docker-compose.gpu.yml up -d ai-service-gpu
```

#### 模型管理
```bash
# 下载预训练模型
docker-compose exec ai-service python download_models.py

# 检查模型状态
docker-compose exec ai-service python check_models.py
```

### 微服务部署

#### 服务网格 (Istio)
```bash
# 安装Istio
curl -L https://istio.io/downloadIstio | sh -
istioctl install --set values.defaultRevision=default

# 部署到Istio
kubectl label namespace default istio-injection=enabled
kubectl apply -f k8s/istio/
```

#### 服务发现 (Consul)
```bash
# 启动Consul
docker-compose -f docker-compose.service-mesh.yml up -d consul

# 注册服务
curl -X PUT http://localhost:8500/v1/agent/service/register -d @consul-service.json
```

### 监控和告警

#### 日志聚合 (ELK Stack)
```bash
# 启动ELK Stack
docker-compose -f docker-compose.monitoring.yml up -d elasticsearch kibana logstash

# 查看日志
open http://localhost:5601
```

#### 分布式追踪 (Jaeger)
```bash
# 启动Jaeger
docker-compose -f docker-compose.monitoring.yml up -d jaeger

# 查看追踪
open http://localhost:16686
```

### 安全加固

#### SSL/TLS证书
```bash
# 生成自签名证书
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# 配置HTTPS
docker-compose -f docker-compose.secure.yml up -d
```

#### 密钥管理 (Vault)
```bash
# 启动Vault
docker-compose -f docker-compose.secure.yml up -d vault

# 初始化Vault
docker-compose exec vault vault operator init
```

## 性能调优

### 数据库优化
```sql
-- MySQL优化
SET GLOBAL innodb_buffer_pool_size = 2G;
SET GLOBAL max_connections = 1000;
SET GLOBAL query_cache_size = 256M;

-- 创建分区表
CREATE TABLE loan_transactions (
    id BIGINT AUTO_INCREMENT,
    created_at TIMESTAMP,
    amount DECIMAL(15,2),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026)
);
```

### 缓存优化
```yaml
# Redis配置优化
redis:
  command: >
    redis-server
    --maxmemory 2gb
    --maxmemory-policy allkeys-lru
    --save 900 1
    --save 300 10
    --save 60 10000
```

### 应用优化
```yaml
# JVM优化
JAVA_OPTS: >
  -Xms4g -Xmx8g
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=200
  -XX:+UseStringDeduplication
  -XX:+OptimizeStringConcat
```

## 故障恢复

### 自动故障转移
```yaml
# Docker Swarm配置
deploy:
  replicas: 3
  update_config:
    parallelism: 1
    delay: 10s
    failure_action: rollback
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
```

### 数据恢复
```bash
# 从备份恢复
./scripts/restore.sh --backup-file backup-2025-09-21.tar.gz

# 区块链数据恢复
docker-compose exec ethereum-node geth --datadir /data import blockchain-backup.json
```

### 服务健康检查
```yaml
# 健康检查配置
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```
