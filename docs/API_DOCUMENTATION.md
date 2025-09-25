# AI助贷招标平台 - API文档

## 📋 概述

本文档详细描述了AI助贷招标平台的RESTful API接口，包括认证、用户管理、风险评估、智能匹配等核心功能。

## 🔗 基础信息

- **Base URL**: `http://localhost:8080/api/v1`
- **Content-Type**: `application/json`
- **认证方式**: JWT Token
- **API版本**: v1.0.0

## 🔐 认证接口

### 用户登录
```http
POST /auth/login
```

**请求参数**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "userType": "admin",
      "fullName": "系统管理员",
      "permissions": ["all"]
    }
  },
  "message": "登录成功"
}
```

### 用户注册
```http
POST /auth/register
```

**请求参数**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "userType": "borrower|lender|admin",
  "fullName": "string"
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 2,
      "username": "newuser",
      "email": "newuser@example.com",
      "userType": "borrower",
      "fullName": "新用户"
    }
  },
  "message": "注册成功"
}
```

### 用户登出
```http
POST /auth/logout
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "message": "登出成功"
}
```

## 👤 用户管理接口

### 获取用户信息
```http
GET /users/profile
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "userType": "admin",
    "fullName": "系统管理员",
    "avatar": "👨‍💼",
    "permissions": ["all"],
    "lastLogin": "2025-09-21T16:00:00Z"
  }
}
```

### 更新用户信息
```http
PUT /users/profile
```

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "fullName": "string",
  "email": "string",
  "avatar": "string"
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "userType": "admin",
    "fullName": "更新后的姓名",
    "avatar": "👨‍💼"
  },
  "message": "用户信息更新成功"
}
```

### 获取用户列表（管理员）
```http
GET /users?page=1&size=10&userType=borrower
```

**请求头**:
```
Authorization: Bearer <token>
```

**查询参数**:
- `page`: 页码（默认1）
- `size`: 每页数量（默认10）
- `userType`: 用户类型过滤
- `status`: 状态过滤

**响应示例**:
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 2,
        "username": "borrower1",
        "email": "borrower1@example.com",
        "userType": "borrower",
        "fullName": "张三",
        "status": "active",
        "createdAt": "2025-09-21T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 25,
      "totalPages": 3
    }
  }
}
```

## 💰 贷款管理接口

### 创建贷款申请
```http
POST /loans
```

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "amount": 1000000,
  "term": 12,
  "purpose": "string",
  "description": "string",
  "collateral": {
    "type": "real_estate",
    "value": 2000000,
    "description": "string"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "amount": 1000000,
    "term": 12,
    "purpose": "企业扩张",
    "status": "pending",
    "createdAt": "2025-09-21T16:00:00Z"
  },
  "message": "贷款申请提交成功"
}
```

### 获取贷款列表
```http
GET /loans?page=1&size=10&status=pending
```

**请求头**:
```
Authorization: Bearer <token>
```

**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `status`: 状态过滤
- `userType`: 用户类型过滤

**响应示例**:
```json
{
  "success": true,
  "data": {
    "loans": [
      {
        "id": 1,
        "borrower": {
          "id": 2,
          "username": "borrower1",
          "fullName": "张三"
        },
        "amount": 1000000,
        "term": 12,
        "purpose": "企业扩张",
        "status": "pending",
        "riskScore": 75,
        "createdAt": "2025-09-21T16:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 50,
      "totalPages": 5
    }
  }
}
```

### 获取贷款详情
```http
GET /loans/{id}
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "borrower": {
      "id": 2,
      "username": "borrower1",
      "fullName": "张三",
      "email": "borrower1@example.com"
    },
    "amount": 1000000,
    "term": 12,
    "purpose": "企业扩张",
    "description": "用于扩大生产规模",
    "status": "pending",
    "riskScore": 75,
    "riskLevel": "medium",
    "collateral": {
      "type": "real_estate",
      "value": 2000000,
      "description": "商业地产"
    },
    "createdAt": "2025-09-21T16:00:00Z",
    "updatedAt": "2025-09-21T16:00:00Z"
  }
}
```

### 更新贷款状态
```http
PUT /loans/{id}/status
```

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "status": "approved|rejected|pending",
  "reason": "string"
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "approved",
    "reason": "风险评估通过",
    "updatedAt": "2025-09-21T16:30:00Z"
  },
  "message": "贷款状态更新成功"
}
```

## 🤖 AI风险评估接口

### 提交风险评估
```http
POST /ai/risk-assessment
```

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "loanId": 1,
  "borrowerInfo": {
    "creditScore": 750,
    "annualRevenue": 5000000,
    "businessAge": 5,
    "industry": "technology"
  },
  "financialData": {
    "assets": 10000000,
    "liabilities": 3000000,
    "cashFlow": 500000
  },
  "marketData": {
    "industryRisk": "low",
    "marketTrend": "growing"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "assessmentId": "assess_123456",
    "riskScore": 75,
    "riskLevel": "medium",
    "recommendation": "建议批准，但需要增加担保",
    "factors": [
      {
        "factor": "信用评分",
        "score": 85,
        "weight": 0.3,
        "description": "信用记录良好"
      },
      {
        "factor": "行业风险",
        "score": 70,
        "weight": 0.2,
        "description": "科技行业风险适中"
      }
    ],
    "confidence": 0.85,
    "createdAt": "2025-09-21T16:00:00Z"
  }
}
```

### 获取风险评估结果
```http
GET /ai/risk-assessment/{assessmentId}
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "assessmentId": "assess_123456",
    "loanId": 1,
    "riskScore": 75,
    "riskLevel": "medium",
    "recommendation": "建议批准，但需要增加担保",
    "factors": [...],
    "confidence": 0.85,
    "createdAt": "2025-09-21T16:00:00Z"
  }
}
```

## 🔄 智能匹配接口

### 启动智能匹配
```http
POST /ai/matching
```

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "loanId": 1,
  "criteria": {
    "maxAmount": 2000000,
    "minTerm": 6,
    "maxTerm": 24,
    "preferredIndustries": ["technology", "manufacturing"]
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "matchingId": "match_123456",
    "status": "processing",
    "estimatedTime": 30,
    "createdAt": "2025-09-21T16:00:00Z"
  }
}
```

### 获取匹配结果
```http
GET /ai/matching/{matchingId}
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "matchingId": "match_123456",
    "status": "completed",
    "matches": [
      {
        "lenderId": 3,
        "lenderName": "银行A",
        "matchScore": 92,
        "offeredAmount": 1000000,
        "offeredRate": 0.08,
        "offeredTerm": 12,
        "conditions": ["需要担保", "定期报告"]
      }
    ],
    "createdAt": "2025-09-21T16:00:00Z",
    "completedAt": "2025-09-21T16:01:00Z"
  }
}
```

## 📊 监控和统计接口

### 获取系统统计
```http
GET /monitoring/stats
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "totalLoans": 1250,
    "activeLoans": 180,
    "totalAmount": 50000000,
    "avgRiskScore": 72,
    "successRate": 0.85,
    "processingTime": 2.5,
    "systemHealth": {
      "cpuUsage": 45.2,
      "memoryUsage": 67.8,
      "diskUsage": 23.1,
      "networkLatency": 12
    }
  }
}
```

### 获取风险分布
```http
GET /monitoring/risk-distribution
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "distribution": [
      {
        "level": "low",
        "count": 450,
        "percentage": 36
      },
      {
        "level": "medium",
        "count": 350,
        "percentage": 28
      },
      {
        "level": "high",
        "count": 450,
        "percentage": 36
      }
    ]
  }
}
```

### 获取贷款趋势
```http
GET /monitoring/loan-trend?period=6months
```

**请求头**:
```
Authorization: Bearer <token>
```

**查询参数**:
- `period`: 时间周期（1month, 3months, 6months, 1year）

**响应示例**:
```json
{
  "success": true,
  "data": {
    "trend": [
      {
        "month": "2025-03",
        "total": 120,
        "approved": 100,
        "rejected": 20
      },
      {
        "month": "2025-04",
        "total": 135,
        "approved": 115,
        "rejected": 20
      }
    ]
  }
}
```

## 🔔 通知接口

### 获取通知列表
```http
GET /notifications?page=1&size=10
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "id": 1,
        "type": "info",
        "title": "贷款申请已提交",
        "message": "您的贷款申请已成功提交，正在审核中",
        "read": false,
        "createdAt": "2025-09-21T16:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 25,
      "totalPages": 3
    }
  }
}
```

### 标记通知为已读
```http
PUT /notifications/{id}/read
```

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "message": "通知已标记为已读"
}
```

## 📁 文件上传接口

### 上传文件
```http
POST /files/upload
```

**请求头**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**请求参数**:
- `file`: 文件（支持PDF, DOC, DOCX, XLS, XLSX, JPG, PNG）
- `type`: 文件类型（financial_report, identity_document, collateral_document）

**响应示例**:
```json
{
  "success": true,
  "data": {
    "fileId": "file_123456",
    "filename": "financial_report.pdf",
    "size": 1024000,
    "type": "financial_report",
    "url": "https://api.example.com/files/file_123456",
    "uploadedAt": "2025-09-21T16:00:00Z"
  }
}
```

## ❌ 错误处理

### 错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      }
    ]
  },
  "timestamp": "2025-09-21T16:00:00Z"
}
```

### 常见错误码

| 错误码 | HTTP状态码 | 描述 |
|--------|------------|------|
| VALIDATION_ERROR | 400 | 请求参数验证失败 |
| UNAUTHORIZED | 401 | 未授权访问 |
| FORBIDDEN | 403 | 权限不足 |
| NOT_FOUND | 404 | 资源不存在 |
| CONFLICT | 409 | 资源冲突 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

## 🔒 安全说明

### 认证机制
- 使用JWT Token进行身份认证
- Token有效期为24小时
- 支持Token刷新机制

### 权限控制
- 基于角色的访问控制（RBAC）
- 细粒度权限管理
- API级别的权限验证

### 数据安全
- 所有敏感数据加密传输
- 用户密码使用bcrypt加密
- 支持HTTPS协议

## 📝 使用示例

### JavaScript示例
```javascript
// 用户登录
const login = async (username, password) => {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  if (data.success) {
    localStorage.setItem('token', data.data.token);
    return data.data.user;
  }
  throw new Error(data.error.message);
};

// 获取贷款列表
const getLoans = async (page = 1, size = 10) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`/api/v1/loans?page=${page}&size=${size}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  return data.data;
};
```

### Python示例
```python
import requests

# 用户登录
def login(username, password):
    response = requests.post(
        'http://localhost:8080/api/v1/auth/login',
        json={'username': username, 'password': password}
    )
    data = response.json()
    if data['success']:
        return data['data']['token']
    raise Exception(data['error']['message'])

# 获取贷款列表
def get_loans(token, page=1, size=10):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'http://localhost:8080/api/v1/loans?page={page}&size={size}',
        headers=headers
    )
    return response.json()['data']
```

## 📞 技术支持

如有API使用问题，请联系技术支持团队：

- **邮箱**: support@ai-loan-platform.com
- **电话**: 400-123-4567
- **工作时间**: 周一至周五 9:00-18:00

---

**文档版本**: v1.0.0  
**最后更新**: 2025年9月21日  
**维护团队**: AI助贷平台开发组
