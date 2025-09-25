# API文档

## 概述

AI智能助贷招标平台提供RESTful API接口，支持用户管理、招标管理、风险评估、智能匹配、区块链集成、物联网设备管理、高级分析等功能。

## 基础信息

- **Base URL**: `http://localhost:8080/api/v1`
- **认证方式**: JWT Token / OAuth 2.0
- **数据格式**: JSON
- **字符编码**: UTF-8
- **API版本**: v6.0.0
- **支持协议**: HTTP/HTTPS, WebSocket, MQTT

## 认证

### 获取Token

```http
POST /api/v1/users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 使用Token

在请求头中添加Authorization字段：

```http
Authorization: Bearer <token>
```

## 用户管理

### 用户注册

```http
POST /api/v1/users/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "user@example.com",
  "phone": "13800138000",
  "password": "password123",
  "companyName": "测试科技有限公司",
  "companyType": "科技",
  "companyAddress": "北京市朝阳区",
  "businessLicense": "91110000123456789X"
}
```

### 获取用户信息

```http
GET /api/v1/users/{userId}
Authorization: Bearer <token>
```

### 更新用户信息

```http
PUT /api/v1/users/{userId}
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "newusername",
  "email": "newemail@example.com",
  "phone": "13900139000",
  "companyName": "新公司名称"
}
```

## 招标管理

### 创建招标

```http
POST /api/v1/tenders
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "流动资金招标",
  "description": "企业流动资金需求",
  "amount": 1000000,
  "termMonths": 12,
  "purpose": "生产经营",
  "repaymentType": "等额本息",
  "interestRateMin": 5.0,
  "interestRateMax": 8.0
}
```

### 获取招标列表

```http
GET /api/v1/tenders?page=0&size=10&status=PUBLISHED
Authorization: Bearer <token>
```

### 获取招标详情

```http
GET /api/v1/tenders/{tenderId}
Authorization: Bearer <token>
```

### 发布招标

```http
POST /api/v1/tenders/{tenderId}/publish
Authorization: Bearer <token>
```

## 方案管理

### 获取方案列表

```http
GET /api/v1/tenders/{tenderId}/proposals
Authorization: Bearer <token>
```

### 选择方案

```http
POST /api/v1/proposals/{proposalId}/select
Authorization: Bearer <token>
```

### 获取方案详情

```http
GET /api/v1/proposals/{proposalId}
Authorization: Bearer <token>
```

## 风险评估

### 评估用户风险

```http
POST /api/v1/risk/assess
Authorization: Bearer <token>
Content-Type: application/json

{
  "userId": 1,
  "businessData": {
    "revenue": 1000000,
    "profit": 100000,
    "assets": 5000000
  },
  "marketData": {
    "industry": "科技",
    "region": "北京"
  }
}
```

### 获取风险报告

```http
GET /api/v1/risk/report/{userId}
Authorization: Bearer <token>
```

## 智能匹配

### 匹配方案

```http
POST /api/v1/match/proposals
Authorization: Bearer <token>
Content-Type: application/json

{
  "tenderId": 1,
  "userRequirements": {
    "amount": 1000000,
    "termMonths": 12,
    "interestRateMax": 8.0
  }
}
```

### 获取推荐方案

```http
GET /api/v1/match/recommendations/{tenderId}
Authorization: Bearer <token>
```

## AI服务

### 文档处理

```http
POST /api/v1/ai/document/process
Content-Type: multipart/form-data

file: <file>
```

### 风险评估

```http
POST /api/v1/ai/risk/assess
Content-Type: application/json

{
  "userId": 1,
  "businessData": {...},
  "marketData": {...}
}
```

### 智能匹配

```http
POST /api/v1/ai/match/proposals
Content-Type: application/json

{
  "tenderId": 1,
  "userRequirements": {...},
  "availableProducts": [...]
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 响应格式

所有API响应都遵循以下格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {...},
  "timestamp": 1640995200000
}
```

## 区块链API

### 智能合约管理

#### 部署智能合约
```http
POST /api/v1/blockchain/contracts/deploy
Authorization: Bearer <token>
Content-Type: application/json

{
  "contractName": "LoanContract",
  "contractCode": "pragma solidity ^0.8.0; ...",
  "constructorArgs": ["arg1", "arg2"]
}
```

#### 获取合约列表
```http
GET /api/v1/blockchain/contracts
Authorization: Bearer <token>
```

#### 执行合约方法
```http
POST /api/v1/blockchain/contracts/{contractId}/execute
Authorization: Bearer <token>
Content-Type: application/json

{
  "method": "createLoan",
  "parameters": ["0x123...", 1000000, 12]
}
```

### 交易管理

#### 获取交易列表
```http
GET /api/v1/blockchain/transactions?page=0&size=10
Authorization: Bearer <token>
```

#### 获取交易详情
```http
GET /api/v1/blockchain/transactions/{txHash}
Authorization: Bearer <token>
```

#### 发送交易
```http
POST /api/v1/blockchain/transactions/send
Authorization: Bearer <token>
Content-Type: application/json

{
  "to": "0x123...",
  "value": "1000000000000000000",
  "data": "0x..."
}
```

## 物联网API

### 设备管理

#### 注册设备
```http
POST /api/v1/iot/devices
Authorization: Bearer <token>
Content-Type: application/json

{
  "deviceId": "device001",
  "deviceType": "sensor",
  "location": "office",
  "capabilities": ["temperature", "humidity"]
}
```

#### 获取设备列表
```http
GET /api/v1/iot/devices?status=online&type=sensor
Authorization: Bearer <token>
```

#### 控制设备
```http
POST /api/v1/iot/devices/{deviceId}/control
Authorization: Bearer <token>
Content-Type: application/json

{
  "action": "turn_on",
  "parameters": {"brightness": 80}
}
```

### 传感器数据

#### 获取传感器数据
```http
GET /api/v1/iot/sensors/{deviceId}/data?startTime=2025-01-01&endTime=2025-01-02
Authorization: Bearer <token>
```

#### 实时数据订阅
```http
WebSocket: ws://localhost:8080/api/v1/iot/sensors/{deviceId}/stream
```

## 高级分析API

### 数据分析

#### 获取分析报告
```http
GET /api/v1/analytics/reports?type=loan&period=30d
Authorization: Bearer <token>
```

#### 生成预测分析
```http
POST /api/v1/analytics/predictions
Authorization: Bearer <token>
Content-Type: application/json

{
  "type": "loan_volume",
  "timeRange": "next_30_days",
  "parameters": {
    "marketTrend": "up",
    "seasonality": true
  }
}
```

#### 获取实时指标
```http
GET /api/v1/analytics/metrics/realtime
Authorization: Bearer <token>
```

### 数据可视化

#### 获取图表数据
```http
GET /api/v1/analytics/charts/{chartId}/data?timeRange=7d
Authorization: Bearer <token>
```

#### 导出数据
```http
POST /api/v1/analytics/export
Authorization: Bearer <token>
Content-Type: application/json

{
  "format": "excel",
  "dataType": "loan_analysis",
  "timeRange": "30d"
}
```

## AI服务API

### 大语言模型

#### 文本生成
```http
POST /api/v1/ai/llm/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "分析这个贷款申请的风险",
  "model": "gpt-4",
  "maxTokens": 1000
}
```

#### 文档分析
```http
POST /api/v1/ai/llm/analyze-document
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <document_file>
```

### 智能客服

#### 发送消息
```http
POST /api/v1/ai/chatbot/message
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "如何申请贷款？",
  "sessionId": "session123"
}
```

#### 获取对话历史
```http
GET /api/v1/ai/chatbot/sessions/{sessionId}/history
Authorization: Bearer <token>
```

## 工作流API

### 工作流管理

#### 创建工作流
```http
POST /api/v1/workflows
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "贷款审批流程",
  "description": "自动化贷款审批工作流",
  "steps": [
    {
      "name": "风险评估",
      "type": "ai_analysis",
      "config": {"model": "risk_v2"}
    }
  ]
}
```

#### 执行工作流
```http
POST /api/v1/workflows/{workflowId}/execute
Authorization: Bearer <token>
Content-Type: application/json

{
  "inputData": {
    "loanApplication": {...}
  }
}
```

## 分页

支持分页的接口使用以下参数：

- `page`: 页码（从0开始）
- `size`: 每页大小（默认10）

响应格式：

```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "content": [...],
    "totalElements": 100,
    "totalPages": 10,
    "size": 10,
    "number": 0,
    "first": true,
    "last": false
  }
}
```

## WebSocket连接

### 实时数据流
```javascript
const ws = new WebSocket('ws://localhost:8080/api/v1/ws/realtime');
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('实时数据:', data);
};
```

### 区块链事件监听
```javascript
const ws = new WebSocket('ws://localhost:8080/api/v1/ws/blockchain');
ws.onmessage = function(event) {
  const event = JSON.parse(event.data);
  console.log('区块链事件:', event);
};
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 429 | 请求频率限制 |
| 500 | 服务器内部错误 |
| 502 | 区块链网络错误 |
| 503 | 物联网设备离线 |
| 504 | AI服务超时 |
