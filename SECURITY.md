# 安全配置指南

## 概述

本文档说明如何安全地配置 AI 智能助贷招标平台的环境变量和敏感信息。

## 环境变量配置

### 1. 创建环境变量文件

```bash
# 复制示例文件
cp env.example .env

# 编辑环境变量
nano .env
```

### 2. 必需的环境变量

#### AI 服务配置
```bash
# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# DeepSeek 配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# 其他 AI 服务
BAIDU_API_KEY=your_baidu_api_key_here
DASHSCOPE_API_KEY=your_dashscope_api_key_here
ZHIPU_API_KEY=your_zhipu_api_key_here
KIMI_API_KEY=your_kimi_api_key_here
```

#### 数据库配置
```bash
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=ai_loan_platform
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_mysql_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# MongoDB
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=ai_loan_platform
MONGODB_USERNAME=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password
```

## 安全最佳实践

### 1. 文件权限
```bash
# 设置 .env 文件权限（仅所有者可读写）
chmod 600 .env

# 确保 .env 文件在 .gitignore 中
echo ".env" >> .gitignore
```

### 2. 生产环境配置
- 使用强密码（至少 16 位，包含大小写字母、数字和特殊字符）
- 定期轮换 API 密钥
- 使用环境变量而不是硬编码
- 启用 HTTPS
- 配置防火墙规则

### 3. 监控和审计
- 定期检查日志文件
- 监控异常访问
- 设置告警机制
- 定期备份数据

## 常见问题

### Q: 为什么 GitHub 检测到 API Key？
A: GitHub 的秘密扫描功能会检测代码中的 API Key 模式。即使使用环境变量 `${OPENAI_API_KEY}`，扫描器也可能误报。这是正常的安全机制。

### Q: 如何避免误报？
A: 
1. 确保使用环境变量而不是硬编码
2. 在 GitHub 仓库设置中标记为误报
3. 使用 GitHub Actions Secrets 管理敏感信息

### Q: 如何安全地分享项目？
A: 
1. 确保 `.env` 文件在 `.gitignore` 中
2. 提供 `env.example` 作为模板
3. 在 README 中说明环境变量配置
4. 不要在任何文档中暴露真实的 API Key

## 紧急情况处理

如果 API Key 意外泄露：
1. 立即在服务提供商处撤销 API Key
2. 生成新的 API Key
3. 更新所有环境变量
4. 检查访问日志
5. 通知相关团队

## 联系方式

如有安全问题，请联系：
- 邮箱：security@ai-loan-platform.com
- 紧急联系：+86-xxx-xxxx-xxxx

---

**注意：本文档包含敏感信息，请妥善保管，不要公开分享。**
