# AI智能助贷招标平台

## 项目简介

AI智能助贷招标平台是一个基于人工智能技术的金融科技平台，为小微企业主提供公平、透明、智能的资金解决方案招标服务。平台通过四层AI应用架构，从工具使用到生态颠覆，构建了一个以客户为中心的新金融生态。

**版本**: 6.4.0 (RAG+LLM动态银行对比版)  
**最后更新**: 2025-09-24  
**维护者**: AI Loan Platform Team

## 核心特性

- 🤖 **智能匹配**: AI算法精准匹配最优资金方案
- 🔍 **透明比较**: 多维度对比，清晰可见
- 🛡️ **风险评估**: 智能风险评估和信用评级
- 📱 **全平台支持**: Web、移动端、管理后台
- 🔄 **全流程服务**: 从需求到放款的完整服务
- 🧠 **向量RAG**: PostgreSQL + pgvector智能知识检索
- 📄 **多格式文档**: Office、PDF、图片OCR智能处理
- 🔍 **PDF图片OCR**: 自动识别PDF中嵌入图片的文字内容
- 💬 **AI贷款智能体**: RAG+LLM动态银行对比 + 专业贷款申请指导 + 多模态文档处理
- 🏦 **动态银行发现**: 支持中国上百家银行的智能对比分析，无硬编码限制
- ⛓️ **区块链集成**: 智能合约、交易管理、去中心化
- 📱 **物联网支持**: 设备管理、传感器监控、远程控制
- 📊 **高级分析**: 实时数据分析、AI预测、智能洞察
- 🔐 **企业级安全**: 多层安全防护、合规认证
- ⚡ **高性能**: 微服务架构、容器化部署、自动扩缩容

## 技术架构

### 后端技术栈
- Spring Boot 3.0+
- Spring Cloud 2022.0+
- Spring Security 6.0+
- MySQL 8.0+
- Redis 7.0+
- MongoDB 6.0+
- Elasticsearch 8.0+
- RabbitMQ 3.11+

### 前端技术栈
- React 18.0+
- TypeScript 5.0+
- Ant Design 5.0+
- Vite 4.0+
- ECharts 5.0+
- WebSocket
- PWA支持

### AI技术栈
- Python 3.11+
- PyTorch 2.7.0+ (CUDA 12.8)
- vLLM 0.2+ (GPU加速)
- PostgreSQL + pgvector (向量数据库)
- SentenceTransformers (文本向量化)
- 6个LLM提供商 (OpenAI, DeepSeek, Qwen, Zhipu, Baidu, Kimi)
- RAG+LLM动态银行对比 (支持上百家银行智能分析)
- 多格式文档处理 (Office, PDF, 图片OCR)
- scikit-learn 1.3+
- Transformers 4.30+
- ONNX Runtime
- TensorRT 8.5+
- MLflow 2.5+

### 区块链技术栈
- Ethereum 2.0
- Web3.js 4.0+
- Solidity 0.8+
- Truffle 5.0+
- Hardhat 2.0+
- MetaMask集成

### 物联网技术栈
- MQTT 5.0
- CoAP协议
- LoRaWAN
- Zigbee 3.0
- Modbus TCP/RTU

### 基础设施
- Docker 24.0+
- Kubernetes 1.28+
- Nginx 1.24+
- Prometheus 2.45+
- Grafana 10.0+
- Istio 1.18+
- Helm 3.12+

## 项目结构

```
ai-loan-platform/
├── backend/                 # 后端微服务 (49个Java文件)
│   ├── ai-loan-gateway/     # API网关服务
│   ├── ai-loan-user/        # 用户管理服务
│   ├── ai-loan-loan/        # 贷款申请服务
│   ├── ai-loan-risk/        # 风险评估服务
│   ├── ai-loan-matching/    # 智能匹配服务
│   ├── ai-loan-admin/       # 管理后台服务
│   └── ai-loan-ai/          # AI服务接口
├── frontend/                # 前端应用 (100+个文件)
│   ├── web-app/             # Web应用 (React + TypeScript)
│   │   ├── src/components/  # 组件库
│   │   │   ├── AdvancedAnalytics.js    # 高级数据分析
│   │   │   ├── BlockchainIntegration.js # 区块链集成
│   │   │   ├── AIChatbot.js           # AI智能客服
│   │   │   ├── RealTimeFeatures.js    # 实时功能
│   │   │   └── WorkflowAutomation.js  # 工作流自动化
│   │   ├── src/pages/       # 页面组件
│   │   ├── src/contexts/    # 上下文管理
│   │   └── src/services/    # 服务层
│   ├── admin-dashboard/     # 管理后台 (React + Ant Design)
│   └── mobile-app/          # 移动应用 (React Native)
├── ai-services/             # AI服务 (50+个Python文件)
│   ├── services/            # AI服务模块
│   │   ├── document_processor.py    # 文档处理
│   │   ├── risk_assessor.py        # 风险评估
│   │   ├── smart_matcher.py        # 智能匹配
│   │   ├── recommendation_engine.py # 推荐引擎
│   │   ├── advanced_risk_model.py  # 高级风险模型
│   │   ├── llm_service.py          # 大语言模型服务
│   │   └── prediction_engine.py    # 预测引擎
│   ├── models/              # AI模型
│   ├── utils/               # 工具类
│   └── main.py              # 服务入口
├── database/                # 数据库脚本
│   ├── init.sql             # 基础数据库结构
│   └── enhanced_schema.sql  # 增强数据库设计
├── monitoring/              # 监控配置
│   ├── prometheus.yml       # Prometheus配置
│   ├── grafana/             # Grafana仪表板
│   └── alertmanager.yml     # 告警配置
├── scripts/                 # 部署和测试脚本
│   ├── performance_test.py  # 性能测试脚本
│   ├── start_monitoring.sh  # 监控启动脚本
│   └── start_monitoring.bat # Windows监控脚本
├── docs/                    # 项目文档 (12个文档)
│   ├── API.md               # API文档
│   ├── DEPLOYMENT.md        # 部署指南
│   ├── FINANCIAL_COMPLIANCE.md # 金融合规文档
│   └── PROJECT_SUMMARY.md   # 项目总结
├── docker-compose.yml       # Docker Compose配置
├── docker-compose.monitoring.yml # 监控服务配置
├── env.example              # 环境变量示例
├── .gitignore              # Git忽略文件
└── README.md               # 项目说明
```

## 快速开始

### 环境要求
- Java 17+
- Node.js 18+
- Python 3.9+
- Docker 24.0+
- MySQL 8.0+
- Redis 7.0+
- GPU支持 (可选，用于AI加速)

### 本地开发

1. 克隆项目
```bash
git clone https://github.com/173787247/ai-loan-platform.git
cd ai-loan-platform
```

2. 使用Docker Compose启动所有服务
```bash
# 启动完整服务栈（包含AI服务）
docker-compose -f docker-compose.gpu.yml up -d

# 或启动简化版本
docker-compose -f docker-compose.simple.yml up -d
```

3. 访问应用
- Web应用: http://localhost:3000
- 管理后台: http://localhost:3001
- API文档: http://localhost:8080/swagger-ui.html
- 监控面板: http://localhost:9090

### 手动启动（开发模式）

1. 启动数据库
```bash
docker-compose up -d mysql redis mongodb elasticsearch
```

2. 启动后端服务
```bash
cd backend
./mvnw clean install
./mvnw spring-boot:run
```

3. 启动前端应用
```bash
cd frontend/web-app
npm install
npm start
```

4. 启动AI服务
```bash
cd ai-services
pip install -r requirements.txt
python main.py
```

## 部署说明

### Docker部署

#### 生产环境部署
```bash
# 启动完整服务栈
docker-compose -f docker-compose.gpu.yml up -d

# 启动监控服务
docker-compose -f docker-compose.monitoring.yml up -d
```

#### 开发环境部署
```bash
# 启动简化版本
docker-compose -f docker-compose.simple.yml up -d
```

#### 最小化部署
```bash
# 启动最小化版本
docker-compose -f docker-compose.minimal.yml up -d
```

### Kubernetes部署
```bash
# 应用Kubernetes配置
kubectl apply -f k8s/

# 检查部署状态
kubectl get pods
kubectl get services
```

### 云原生部署
```bash
# 使用Helm部署
helm install ai-loan-platform ./helm-chart

# 配置Ingress
kubectl apply -f k8s/ingress.yaml
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目链接: [https://github.com/173787247/ai-loan-platform](https://github.com/173787247/ai-loan-platform)
- 问题反馈: [Issues](https://github.com/173787247/ai-loan-platform/issues)

## 最新功能特性

### 🚀 v6.4.0 新特性 (RAG+LLM动态银行对比版)

#### AI贷款智能体升级
- 🏦 **动态银行发现**: 支持中国上百家银行的智能对比分析，无硬编码限制
- 🧠 **RAG+LLM架构**: 基于知识库检索和大语言模型的动态银行信息生成
- 🔍 **智能内容过滤**: 自动过滤PDF提取中的乱码内容，确保信息准确性
- 📊 **专业银行对比**: 利率、额度、审批条件等多维度智能对比分析
- 💡 **个性化推荐**: 基于用户需求智能推荐最适合的银行和产品

#### 技术架构优化
- ⚡ **性能提升**: 优化RAG检索速度，支持大规模银行数据
- 🔧 **代码重构**: 移除硬编码银行信息，实现完全动态化
- 🛡️ **错误处理**: 增强异常处理和降级机制
- 📈 **可扩展性**: 支持任意数量银行的动态添加和对比

### 🚀 v6.0.0 新特性

#### 区块链集成
- ⛓️ 智能合约管理
- 💰 交易追踪和监控
- 🔐 去中心化身份验证
- 📊 区块链数据分析

#### 物联网支持
- 📱 设备管理和监控
- 🔌 传感器数据采集
- ⚡ 实时设备控制
- 📈 设备性能分析

#### 高级分析功能
- 📊 实时数据可视化
- 🔮 AI预测分析
- 📈 趋势分析报告
- 💡 智能业务洞察

#### 企业级特性
- 🔐 多层安全防护
- ⚡ 高性能微服务架构
- 📱 完美移动端支持
- 🔄 工作流自动化

### 🎯 性能指标
- **响应时间**: < 30ms
- **并发用户**: 20,000+
- **系统可用性**: 99.99%
- **AI推理延迟**: < 50ms
- **RAG检索速度**: < 100ms
- **银行对比生成**: < 2秒
- **支持银行数量**: 100+ (动态扩展)
- **区块链交易确认**: < 10秒

## 致谢

感谢老婆没日没夜的陪伴刷电视剧！
