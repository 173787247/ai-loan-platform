# AI助贷招标平台 - 生产环境部署指南

## 📋 概述

本文档详细介绍了AI助贷招标平台的生产环境部署流程，包括系统架构、配置说明、部署步骤和监控维护。

## 🏗️ 系统架构

### 微服务架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx LB      │    │   API Gateway   │    │   AI Service    │
│   Port: 80/443  │────│   Port: 8080    │────│   Port: 8000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web App       │    │  User Service   │    │  Loan Service   │
│   Port: 3000    │    │   Port: 8081    │    │   Port: 8082    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Admin App      │    │  Risk Service   │    │Matching Service │
│   Port: 3001    │    │   Port: 8083    │    │   Port: 8084    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 数据存储
- **MySQL**: 主数据库 (Port: 3306)
- **Redis**: 缓存和会话存储 (Port: 6379)
- **MongoDB**: 文档存储 (Port: 27017)
- **Elasticsearch**: 搜索引擎 (Port: 9200)

## 🚀 快速部署

### 1. 环境准备

#### 系统要求
- **操作系统**: Linux (Ubuntu 20.04+) / Windows 10+ / macOS
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **内存**: 最低 8GB，推荐 16GB+
- **存储**: 最低 50GB 可用空间
- **GPU**: 可选，用于AI服务加速

#### 安装Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Windows/macOS
# 下载并安装 Docker Desktop
```

### 2. 配置环境

#### 复制环境配置文件
```bash
cp env.prod.example .env.prod
```

#### 编辑生产环境配置
```bash
nano .env.prod
```

关键配置项：
```env
# 数据库密码（生产环境请使用强密码）
MYSQL_ROOT_PASSWORD=your-strong-password
MYSQL_PASSWORD=your-strong-password

# JWT密钥（生产环境请使用随机生成的密钥）
JWT_SECRET=your-super-secret-jwt-key

# 域名配置
REACT_APP_API_BASE_URL=https://your-domain.com/api
REACT_APP_AI_SERVICE_URL=https://your-domain.com/ai
```

### 3. 部署服务

#### 使用部署脚本（推荐）
```bash
# Linux/macOS
chmod +x deploy-prod.sh
./deploy-prod.sh

# Windows
deploy-prod.bat
```

#### 手动部署
```bash
# 1. 构建镜像
docker-compose -f docker-compose.prod.yml build

# 2. 启动数据库服务
docker-compose -f docker-compose.prod.yml up -d mysql redis mongodb elasticsearch

# 3. 等待数据库启动
sleep 30

# 4. 启动AI服务
docker-compose -f docker-compose.prod.yml up -d ai-service

# 5. 启动后端服务
docker-compose -f docker-compose.prod.yml up -d user-service loan-service risk-service matching-service admin-service

# 6. 启动网关
docker-compose -f docker-compose.prod.yml up -d gateway

# 7. 启动前端应用
docker-compose -f docker-compose.prod.yml up -d web-app admin-app

# 8. 启动Nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

## 🔧 配置说明

### Nginx配置
- **负载均衡**: 自动分发请求到后端服务
- **SSL终止**: 支持HTTPS配置
- **静态资源缓存**: 优化前端资源加载
- **健康检查**: 自动检测服务状态

### 网关配置
- **路由管理**: 统一API入口
- **认证授权**: JWT令牌验证
- **限流控制**: 防止API滥用
- **监控日志**: 请求追踪和性能监控

### AI服务配置
- **GPU加速**: 自动检测和使用GPU
- **模型管理**: 支持模型热更新
- **性能监控**: 实时监控模型性能
- **容错处理**: 自动重试和降级

## 📊 监控和维护

### 1. 服务监控

#### 使用监控脚本
```bash
# 执行一次监控检查
chmod +x monitor-prod.sh
./monitor-prod.sh

# 实时监控
./monitor-prod.sh realtime

# 生成监控报告
./monitor-prod.sh report
```

#### 手动检查
```bash
# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看服务日志
docker-compose -f docker-compose.prod.yml logs -f [service-name]

# 查看资源使用情况
docker stats
```

### 2. 性能测试

#### 运行API测试
```bash
python test-prod-api.py
```

测试包括：
- 服务健康检查
- API响应时间
- 负载测试
- 错误率统计

### 3. 日志管理

#### 日志位置
- **应用日志**: `logs/applications/`
- **Nginx日志**: `logs/nginx/`
- **Docker日志**: `docker logs [container-name]`

#### 日志轮转
```bash
# 配置logrotate
sudo nano /etc/logrotate.d/ai-loan-platform
```

## 🔒 安全配置

### 1. 网络安全
- 配置防火墙规则
- 使用HTTPS加密
- 限制端口访问
- 设置访问控制列表

### 2. 数据安全
- 数据库加密存储
- 敏感信息环境变量化
- 定期备份数据
- 访问日志审计

### 3. 应用安全
- JWT令牌安全配置
- API限流和防刷
- 输入验证和过滤
- 错误信息脱敏

## 📈 性能优化

### 1. 数据库优化
- 配置连接池
- 创建适当索引
- 定期清理历史数据
- 监控慢查询

### 2. 缓存策略
- Redis缓存热点数据
- 静态资源CDN加速
- 数据库查询缓存
- 会话状态缓存

### 3. 负载均衡
- Nginx负载均衡配置
- 服务实例水平扩展
- 健康检查配置
- 故障转移机制

## 🚨 故障排除

### 常见问题

#### 1. 服务启动失败
```bash
# 检查容器日志
docker logs [container-name]

# 检查端口占用
netstat -tuln | grep :[port]

# 检查资源使用
docker stats
```

#### 2. 数据库连接失败
```bash
# 检查数据库状态
docker exec -it ai-loan-mysql-prod mysql -u root -p

# 检查网络连接
docker network ls
docker network inspect ai-loan-platform_ai-loan-network
```

#### 3. AI服务异常
```bash
# 检查GPU状态
nvidia-smi

# 检查AI服务日志
docker logs ai-loan-ai-service-prod

# 重启AI服务
docker-compose -f docker-compose.prod.yml restart ai-service
```

### 应急处理

#### 1. 服务降级
```bash
# 停止非关键服务
docker-compose -f docker-compose.prod.yml stop [service-name]

# 启用维护模式
echo "系统维护中" > maintenance.html
```

#### 2. 数据恢复
```bash
# 从备份恢复数据库
docker exec -i ai-loan-mysql-prod mysql -u root -p < backup.sql

# 恢复文件数据
tar -xzf data-backup.tar.gz
```

## 📞 技术支持

### 联系方式
- **技术支持**: tech-support@ai-loan-platform.com
- **紧急联系**: emergency@ai-loan-platform.com
- **文档更新**: docs@ai-loan-platform.com

### 版本信息
- **当前版本**: v6.0.0
- **最后更新**: 2025-09-22
- **兼容性**: Docker 20.10+, Docker Compose 2.0+

---

**注意**: 生产环境部署前请仔细阅读本文档，并根据实际环境调整配置参数。建议在测试环境充分验证后再部署到生产环境。
