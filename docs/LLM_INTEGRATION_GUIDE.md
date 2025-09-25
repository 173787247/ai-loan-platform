# AI助贷招标智能体 - LLM模型集成指南

## 🤖 支持的LLM模型

### 1. OpenAI模型
- **GPT-4**: 最强大的通用模型，适合复杂分析
- **GPT-3.5-turbo**: 性价比高，适合日常对话
- **GPT-4-turbo**: 更快的GPT-4版本
- **GPT-4-vision**: 支持图像分析

### 2. Anthropic Claude模型
- **Claude-3-Opus**: 最强大的Claude模型
- **Claude-3-Sonnet**: 平衡性能和成本
- **Claude-3-Haiku**: 快速响应模型

### 3. Google Gemini模型
- **Gemini-Pro**: 强大的多模态模型
- **Gemini-Pro-Vision**: 支持图像理解
- **Gemini-Ultra**: 最高性能模型

### 4. 百度文心一言
- **文心一言4.0**: 最新版本
- **文心一言3.5**: 稳定版本
- **文心一言Turbo**: 快速版本

### 5. 阿里通义千问
- **Qwen-72B**: 大参数模型
- **Qwen-14B**: 中等参数模型
- **Qwen-7B**: 小参数模型

### 6. 腾讯混元
- **混元-Pro**: 专业版本
- **混元-Standard**: 标准版本

### 7. 本地模型
- **Qwen系列**: 通义千问本地部署
- **ChatGLM系列**: 清华ChatGLM
- **DeepSeek系列**: DeepSeek模型
- **Llama系列**: Meta Llama模型

## 🔧 配置方法

### 1. 环境变量配置

创建 `.env` 文件：

```bash
# OpenAI配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic配置
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_BASE_URL=https://api.anthropic.com

# Google配置
GOOGLE_API_KEY=your_google_api_key
GOOGLE_BASE_URL=https://generativelanguage.googleapis.com/v1beta

# 百度配置
BAIDU_API_KEY=your_baidu_api_key
BAIDU_SECRET_KEY=your_baidu_secret_key
BAIDU_BASE_URL=https://aip.baidubce.com

# 本地模型配置
ENABLE_LOCAL_MODELS=true
LOCAL_MODEL_PATH=/path/to/models
```

### 2. 代码配置

```python
from ai_services.llm_integration import LLMConfig, LLMProvider, create_llm_manager

# 创建自定义配置
config = LLMConfig(
    provider=LLMProvider.OPENAI,
    model_name="gpt-4",
    api_key="your_api_key",
    temperature=0.7,
    max_tokens=2000
)

# 创建LLM管理器
manager = create_llm_manager()

# 使用LLM
response = await manager.generate("你好，请介绍一下贷款流程")
```

## 🚀 使用示例

### 1. 基础使用

```python
from ai_services.enhanced_ai_agent import EnhancedAILoanAgent, ConversationMode

# 创建智能体
agent = EnhancedAILoanAgent(llm_name="gpt-3.5-turbo")

# 开始对话
response = await agent.start_conversation(
    user_id=1, 
    mode=ConversationMode.PROFESSIONAL
)

# 智能收集用户信息
user_data = {
    "company_name": "测试公司",
    "industry": "制造业",
    "company_size": "small",
    # ... 其他信息
}
response = await agent.intelligent_collect_user_info(user_data)

# 智能风险评估
response = await agent.intelligent_risk_assessment()

# 智能匹配
response = await agent.intelligent_smart_matching()
```

### 2. 切换LLM模型

```python
# 列出可用模型
available_llms = agent.get_available_llms()
print(f"可用模型: {available_llms}")

# 切换到GPT-4
success = agent.switch_llm("gpt-4")
if success:
    print("已切换到GPT-4")
```

### 3. 自定义对话模式

```python
from ai_services.enhanced_ai_agent import ConversationMode

# 专业模式
response = await agent.start_conversation(
    user_id=1, 
    mode=ConversationMode.PROFESSIONAL
)

# 友好模式
response = await agent.start_conversation(
    user_id=1, 
    mode=ConversationMode.FRIENDLY
)

# 技术模式
response = await agent.start_conversation(
    user_id=1, 
    mode=ConversationMode.TECHNICAL
)

# 简单模式
response = await agent.start_conversation(
    user_id=1, 
    mode=ConversationMode.SIMPLE
)
```

### 4. 与LLM直接对话

```python
# 直接与LLM对话
response = await agent.chat_with_llm("请解释一下什么是信用评分？")
print(response.message)
```

## 📊 性能对比

| 模型 | 响应速度 | 准确性 | 成本 | 适用场景 |
|------|----------|--------|------|----------|
| GPT-4 | 中等 | 最高 | 高 | 复杂分析、专业咨询 |
| GPT-3.5-turbo | 快 | 高 | 中等 | 日常对话、一般咨询 |
| Claude-3-Opus | 慢 | 最高 | 高 | 深度分析、创意生成 |
| Claude-3-Sonnet | 中等 | 高 | 中等 | 平衡性能和成本 |
| Gemini-Pro | 快 | 高 | 低 | 多模态、快速响应 |
| 文心一言4.0 | 快 | 高 | 低 | 中文优化、本土化 |
| 本地模型 | 快 | 中等 | 低 | 隐私保护、离线使用 |

## 🔒 安全考虑

### 1. API密钥安全
- 使用环境变量存储API密钥
- 定期轮换API密钥
- 限制API使用权限

### 2. 数据隐私
- 敏感数据不发送到外部API
- 使用本地模型处理敏感信息
- 实施数据脱敏

### 3. 访问控制
- 限制LLM访问权限
- 监控API使用情况
- 实施速率限制

## 🛠️ 故障排除

### 1. 常见问题

**问题**: LLM模型不可用
```python
# 检查可用模型
available_llms = agent.get_available_llms()
print(f"可用模型: {available_llms}")

# 检查API密钥
import os
print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY', 'Not set')}")
```

**问题**: 响应速度慢
```python
# 调整参数
response = await agent.chat_with_llm(
    "你好",
    temperature=0.3,  # 降低随机性
    max_tokens=500    # 减少生成长度
)
```

**问题**: 成本过高
```python
# 切换到成本较低的模型
agent.switch_llm("gpt-3.5-turbo")  # 或 "gemini-pro"
```

### 2. 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
```

## 📈 最佳实践

### 1. 模型选择策略
- **复杂分析**: 使用GPT-4或Claude-3-Opus
- **日常对话**: 使用GPT-3.5-turbo或Gemini-Pro
- **成本敏感**: 使用本地模型或文心一言
- **隐私要求**: 使用本地模型

### 2. 参数调优
- **temperature**: 0.7-0.9用于创意，0.3-0.5用于准确
- **max_tokens**: 根据需求调整，避免过长
- **top_p**: 0.9用于多样性，0.7用于一致性

### 3. 错误处理
```python
try:
    response = await agent.chat_with_llm("你好")
except Exception as e:
    print(f"LLM调用失败: {e}")
    # 使用备用方案
    response = "抱歉，AI服务暂时不可用，请稍后再试。"
```

## 🔄 更新和维护

### 1. 模型更新
- 定期检查新模型版本
- 测试新模型性能
- 逐步迁移到新模型

### 2. 配置管理
- 使用配置文件管理模型参数
- 实施配置版本控制
- 定期备份配置

### 3. 监控和告警
- 监控API使用量
- 设置成本告警
- 监控响应时间

---

**文档版本**: 1.1.0  
**最后更新**: 2025-09-14  
**维护团队**: AI Loan Platform Team
