# 🔐 环境变量设置指南

## 📋 概述

本指南将帮助您配置AI助贷招标平台的环境变量，特别是各种LLM API密钥的设置。

## 🚀 快速开始

### 1. 创建环境变量文件

```bash
# 复制模板文件
cp env.template .env

# 编辑环境变量文件
nano .env  # 或使用您喜欢的编辑器
```

### 2. 配置LLM API密钥

在`.env`文件中填入您的API密钥：

```bash
# 示例：配置DeepSeek API
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# 设置默认提供商
DEFAULT_LLM_PROVIDER=deepseek
```

## 🔑 支持的LLM提供商

### 1. OpenAI
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

**获取API密钥**：
- 访问 [OpenAI Platform](https://platform.openai.com/)
- 注册/登录账户
- 在API Keys页面创建新密钥

### 2. DeepSeek
```bash
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

**获取API密钥**：
- 访问 [DeepSeek Platform](https://platform.deepseek.com/)
- 注册/登录账户
- 在API管理页面创建密钥

### 3. 通义千问 (Qwen)
```bash
QWEN_API_KEY=sk-your-qwen-api-key-here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL=qwen-turbo
```

**获取API密钥**：
- 访问 [阿里云DashScope](https://dashscope.aliyun.com/)
- 注册/登录阿里云账户
- 开通DashScope服务并获取API Key

### 4. 智谱AI (GLM)
```bash
ZHIPU_API_KEY=your-zhipu-api-key-here
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZHIPU_MODEL=glm-4
```

**获取API密钥**：
- 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
- 注册/登录账户
- 在控制台获取API Key

### 5. 百度文心一言
```bash
BAIDU_API_KEY=your-baidu-api-key-here
BAIDU_SECRET_KEY=your-baidu-secret-key-here
BAIDU_BASE_URL=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat
BAIDU_MODEL=ernie-bot-turbo
```

**获取API密钥**：
- 访问 [百度智能云](https://cloud.baidu.com/)
- 开通文心一言服务
- 在API Key管理页面获取密钥

### 6. 月之暗面 (Kimi)
```bash
KIMI_API_KEY=sk-your-kimi-api-key-here
KIMI_BASE_URL=https://api.moonshot.cn/v1
KIMI_MODEL=moonshot-v1-8k
```

**获取API密钥**：
- 访问 [月之暗面开放平台](https://platform.moonshot.cn/)
- 注册/登录账户
- 在API管理页面创建密钥

## ⚙️ 配置说明

### 默认提供商设置
```bash
# 设置默认使用的LLM提供商
DEFAULT_LLM_PROVIDER=deepseek  # 可选: openai, deepseek, qwen, zhipu, baidu, kimi
```

### 模型配置
每个提供商支持不同的模型，您可以根据需要选择：

- **OpenAI**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
- **DeepSeek**: `deepseek-chat`, `deepseek-coder`
- **通义千问**: `qwen-turbo`, `qwen-plus`, `qwen-max`
- **智谱AI**: `glm-4`, `glm-3-turbo`
- **百度文心一言**: `ernie-bot-turbo`, `ernie-bot`
- **月之暗面**: `moonshot-v1-8k`, `moonshot-v1-32k`

## 🔒 安全注意事项

### 1. 保护API密钥
- **永远不要**将`.env`文件提交到Git仓库
- 使用强密码和复杂的API密钥
- 定期轮换API密钥
- 限制API密钥的权限范围

### 2. 环境隔离
```bash
# 开发环境
.env.development

# 生产环境
.env.production

# 测试环境
.env.test
```

### 3. 访问控制
- 限制API密钥的IP白名单
- 设置API调用频率限制
- 监控API使用情况

## 🧪 测试配置

### 1. 检查可用提供商
```bash
curl http://localhost:8000/api/v1/llm/providers
```

### 2. 测试特定提供商
```bash
curl -X POST http://localhost:8000/api/v1/llm/test \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "deepseek",
    "model": "deepseek-chat",
    "message": "你好，请介绍一下你自己"
  }'
```

### 3. 测试AI智能客服
```bash
# 创建会话
curl -X POST http://localhost:8000/api/v1/chat/session \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "chatbot_role": "general"
  }'

# 发送消息
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_id_from_above",
    "message": "我想了解贷款产品"
  }'
```

## 🐳 Docker环境变量

### 1. 在Docker Compose中设置
```yaml
services:
  ai-service-prod:
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - DEFAULT_LLM_PROVIDER=${DEFAULT_LLM_PROVIDER}
    env_file:
      - .env
```

### 2. 在Dockerfile中设置
```dockerfile
# 复制环境变量文件
COPY .env /app/.env

# 设置环境变量
ENV DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
```

## 🔧 故障排除

### 1. 常见问题

**问题**: API密钥无效
```bash
# 检查API密钥格式
echo $DEEPSEEK_API_KEY

# 检查API密钥是否包含特殊字符
# 确保没有多余的空格或换行符
```

**问题**: 网络连接失败
```bash
# 检查网络连接
ping api.deepseek.com

# 检查防火墙设置
# 确保允许HTTPS连接
```

**问题**: 模型不存在
```bash
# 检查模型名称是否正确
# 查看提供商支持的模型列表
curl http://localhost:8000/api/v1/llm/providers
```

### 2. 日志调试
```bash
# 查看AI服务日志
docker logs ai-loan-ai-service-prod

# 查看详细日志
docker logs ai-loan-ai-service-prod -f
```

### 3. 环境变量验证
```bash
# 检查环境变量是否正确加载
docker exec ai-loan-ai-service-prod env | grep -E "(DEEPSEEK|OPENAI|QWEN)"
```

## 📚 更多资源

- [OpenAI API文档](https://platform.openai.com/docs)
- [DeepSeek API文档](https://platform.deepseek.com/api-docs)
- [通义千问API文档](https://help.aliyun.com/zh/dashscope/)
- [智谱AI API文档](https://open.bigmodel.cn/dev/api)
- [百度文心一言API文档](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/4lilb2lpf)
- [月之暗面API文档](https://platform.moonshot.cn/docs)

## 🆘 获取帮助

如果您在配置过程中遇到问题，可以：

1. 查看项目README文档
2. 检查GitHub Issues
3. 联系开发团队
4. 查看API提供商官方文档

---

**配置完成后，您的AI智能客服系统就可以使用真实的LLM服务了！** 🚀✨
