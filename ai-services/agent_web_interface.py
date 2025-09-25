"""
AI助贷招标智能体Web接口
提供Web界面与智能体交互

@author AI Loan Platform Team
@version 1.1.0
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime
import uvicorn

from ai_loan_agent import AILoanAgent, UserProfile, LoanPurpose

# 创建FastAPI应用
app = FastAPI(
    title="AI助贷招标智能体",
    description="智能助贷招标平台AI智能体Web接口",
    version="1.1.0"
)

# 静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 全局智能体实例
agent = AILoanAgent()

# 请求模型
class UserInfoRequest(BaseModel):
    user_id: int
    company_name: str
    industry: str
    company_size: str
    business_age: int
    annual_revenue: float
    monthly_income: float
    credit_score: int
    management_experience: int
    risk_tolerance: str
    preferred_loan_amount: float
    preferred_term: int
    preferred_rate: float

class MessageRequest(BaseModel):
    message: str
    user_id: int

class DocumentUploadRequest(BaseModel):
    file_path: str
    file_type: str

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    await agent.initialize_services()
    print("🤖 AI助贷招标智能体Web接口已启动")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """主页"""
    return templates.TemplateResponse("agent_interface.html", {
        "request": request,
        "title": "AI助贷招标智能体"
    })

@app.post("/api/agent/start")
async def start_conversation(user_id: int):
    """开始对话"""
    try:
        response = agent.start_conversation(user_id)
        return JSONResponse(content={
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "next_action": response.next_action,
            "confidence": response.confidence,
            "timestamp": response.timestamp
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/user-info")
async def collect_user_info(request: UserInfoRequest):
    """收集用户信息"""
    try:
        user_data = request.dict()
        response = agent.collect_user_info(user_data)
        return JSONResponse(content={
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "next_action": response.next_action,
            "confidence": response.confidence,
            "timestamp": response.timestamp
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/assess-risk")
async def assess_risk():
    """风险评估"""
    try:
        response = agent.assess_risk()
        return JSONResponse(content={
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "next_action": response.next_action,
            "confidence": response.confidence,
            "timestamp": response.timestamp
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/smart-matching")
async def smart_matching():
    """智能匹配"""
    try:
        response = agent.smart_matching()
        return JSONResponse(content={
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "next_action": response.next_action,
            "confidence": response.confidence,
            "timestamp": response.timestamp
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/recommendations")
async def generate_recommendations():
    """生成推荐方案"""
    try:
        response = agent.generate_recommendations()
        return JSONResponse(content={
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "next_action": response.next_action,
            "confidence": response.confidence,
            "timestamp": response.timestamp
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/process-document")
async def process_document(request: DocumentUploadRequest):
    """处理文档"""
    try:
        response = agent.process_document(request.file_path, request.file_type)
        return JSONResponse(content={
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "next_action": response.next_action,
            "confidence": response.confidence,
            "timestamp": response.timestamp
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agent/history")
async def get_conversation_history():
    """获取对话历史"""
    try:
        history = agent.get_conversation_history()
        return JSONResponse(content={
            "success": True,
            "data": history,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/reset")
async def reset_agent():
    """重置智能体"""
    try:
        agent.reset_agent()
        return JSONResponse(content={
            "success": True,
            "message": "智能体已重置",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agent/status")
async def get_agent_status():
    """获取智能体状态"""
    try:
        return JSONResponse(content={
            "success": True,
            "data": {
                "state": agent.state.value,
                "user_profile": agent.user_profile.__dict__ if agent.user_profile else None,
                "conversation_count": len(agent.conversation_history)
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
