"""
AI智能助贷招标平台 - AI服务主程序

@author AI Loan Platform Team
@version 1.0.0
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
import uvicorn
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv

from services.document_processor import DocumentProcessor
from services.document_rag import DocumentRAGService
from services.risk_assessor import RiskAssessor
from services.smart_matcher import SmartMatcher
from services.recommendation_engine import RecommendationEngine
from services.ai_model_manager import AIModelManager
from services.ai_chatbot import AIChatbot, ChatbotRole
from services.llm_provider import llm_provider_manager
from services.vector_rag import vector_rag_service
from services.enhanced_web_search import enhanced_web_search_service
from services.universal_bank_search import universal_bank_search_service
from services.real_web_search import real_web_search_service
from services.credit_api_service import credit_api_service
from loguru import logger

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="AI智能助贷招标平台 - AI服务",
    description="提供文档处理、风险评估、智能匹配和推荐服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化服务"""
    try:
        # 初始化向量RAG服务
        await vector_rag_service.initialize()
        logger.info("向量RAG服务初始化成功")
        
        # 初始化LLM提供商
        await llm_provider_manager.initialize()
        logger.info("LLM提供商初始化成功")
        
        # 初始化增强版网络搜索服务
        await enhanced_web_search_service.initialize()
        logger.info("增强版网络搜索服务初始化成功")
        
        # 初始化通用银行搜索服务
        await universal_bank_search_service.initialize()
        logger.info("通用银行搜索服务初始化成功")
        
        # 初始化真正的外网搜索服务
        await real_web_search_service.initialize()
        logger.info("真正的外网搜索服务初始化成功")
        
        logger.info("AI服务启动完成")
    except Exception as e:
        logger.error(f"服务初始化失败: {e}")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    try:
        await vector_rag_service.close()
        logger.info("向量RAG服务已关闭")
        
        await enhanced_web_search_service.close()
        logger.info("增强版网络搜索服务已关闭")
        
        await universal_bank_search_service.close()
        logger.info("通用银行搜索服务已关闭")
        
        await real_web_search_service.close()
        logger.info("真正的外网搜索服务已关闭")
        
        logger.info("AI服务已关闭")
    except Exception as e:
        logger.error(f"服务关闭失败: {e}")

# 全局异常处理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"请求验证错误: {exc}")
    logger.error(f"请求体: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

# 初始化AI服务
document_processor = DocumentProcessor()
document_rag = DocumentRAGService()
risk_assessor = RiskAssessor()
smart_matcher = SmartMatcher()
recommendation_engine = RecommendationEngine()
ai_model_manager = AIModelManager()
ai_chatbot = AIChatbot(vector_rag_service=vector_rag_service, llm_service=llm_provider_manager)

# 请求模型
class DocumentProcessRequest(BaseModel):
    file_path: str
    file_type: str

class DocumentUploadRequest(BaseModel):
    category: str
    metadata: Optional[Dict[str, Any]] = None

class RiskAssessmentRequest(BaseModel):
    user_id: int
    business_data: Dict[str, Any]
    market_data: Dict[str, Any]

class MatchingRequest(BaseModel):
    tender_id: int
    user_requirements: Dict[str, Any]
    available_products: List[Dict[str, Any]]

class RecommendationRequest(BaseModel):
    user_id: int
    tender_id: int
    user_preferences: Dict[str, Any]

class ModelTrainingRequest(BaseModel):
    model_name: str
    training_data: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None

class ModelPredictionRequest(BaseModel):
    model_name: str
    input_data: List[float]

class ModelEvaluationRequest(BaseModel):
    model_name: str
    test_data: Dict[str, Any]

# 响应模型
class AIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# 健康检查
@app.get("/health")
async def health_check():
    import torch
    from datetime import datetime
    
    return {
        "status": "healthy",
        "service": "ai-loan-ai-service",
            "version": "1.1.0",
        "gpu_available": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "timestamp": datetime.now().isoformat()
    }

# 文档处理接口
@app.post("/api/v1/ai/document/process", response_model=AIResponse)
async def process_document(file: UploadFile = File(...)):
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理文档
        result = document_processor.process_document(file_path, file.content_type)
        
        return AIResponse(
            success=True,
            message="文档处理成功",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档处理失败: {str(e)}")

# 风险评估接口
@app.post("/api/v1/ai/risk/assess", response_model=AIResponse)
async def assess_risk(request: RiskAssessmentRequest):
    try:
        result = risk_assessor.assess_risk(
            request.user_id,
            request.business_data,
            request.market_data
        )
        
        return AIResponse(
            success=True,
            message="风险评估完成",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"风险评估失败: {str(e)}")

# 智能匹配接口
@app.post("/api/v1/ai/match/proposals", response_model=AIResponse)
async def match_proposals(request: MatchingRequest):
    try:
        result = smart_matcher.match_proposals(
            request.tender_id,
            request.user_requirements,
            request.available_products
        )
        
        return AIResponse(
            success=True,
            message="智能匹配完成",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"智能匹配失败: {str(e)}")

# 推荐系统接口
@app.post("/api/v1/ai/recommend/solutions", response_model=AIResponse)
async def recommend_solutions(request: RecommendationRequest):
    try:
        result = recommendation_engine.recommend_solutions(
            request.user_id,
            request.tender_id,
            request.user_preferences
        )
        
        return AIResponse(
            success=True,
            message="推荐方案生成完成",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐生成失败: {str(e)}")

# 批量处理接口
@app.post("/api/v1/ai/batch/process", response_model=AIResponse)
async def batch_process(files: List[UploadFile] = File(...)):
    try:
        results = []
        
        for file in files:
            # 保存文件
            file_path = f"uploads/{file.filename}"
            os.makedirs("uploads", exist_ok=True)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # 处理文档
            result = document_processor.process_document(file_path, file.content_type)
            results.append({
                "filename": file.filename,
                "result": result
            })
        
        return AIResponse(
            success=True,
            message="批量处理完成",
            data={"results": results}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量处理失败: {str(e)}")

# 获取AI服务状态
@app.get("/api/v1/ai/status")
async def get_ai_status():
    try:
        status = {
            "document_processor": document_processor.get_status(),
            "risk_assessor": risk_assessor.get_status(),
            "smart_matcher": smart_matcher.get_status(),
            "recommendation_engine": recommendation_engine.get_status()
        }
        
        return AIResponse(
            success=True,
            message="AI服务状态获取成功",
            data=status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"状态获取失败: {str(e)}")

# AI模型管理接口
@app.post("/api/v1/ai/model/train", response_model=AIResponse)
async def train_model(request: ModelTrainingRequest):
    try:
        result = ai_model_manager.train_model(request.model_name, request.training_data)
        
        return AIResponse(
            success=result['success'],
            message=f"模型 {request.model_name} 训练{'成功' if result['success'] else '失败'}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型训练失败: {str(e)}")

@app.post("/api/v1/ai/model/predict", response_model=AIResponse)
async def predict_model(request: ModelPredictionRequest):
    try:
        import numpy as np
        input_data = np.array(request.input_data)
        result = ai_model_manager.predict(request.model_name, input_data)
        
        return AIResponse(
            success=result['success'],
            message=f"模型 {request.model_name} 预测{'成功' if result['success'] else '失败'}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型预测失败: {str(e)}")

@app.post("/api/v1/ai/model/evaluate", response_model=AIResponse)
async def evaluate_model(request: ModelEvaluationRequest):
    try:
        result = ai_model_manager.evaluate_model(request.model_name, request.test_data)
        
        return AIResponse(
            success=result['success'],
            message=f"模型 {request.model_name} 评估{'成功' if result['success'] else '失败'}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型评估失败: {str(e)}")

@app.get("/api/v1/ai/model/status")
async def get_model_status():
    try:
        status = ai_model_manager.get_model_status()
        
        return AIResponse(
            success=True,
            message="模型状态获取成功",
            data=status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型状态获取失败: {str(e)}")

@app.get("/api/v1/ai/model/insights/{model_name}")
async def get_model_insights(model_name: str):
    try:
        insights = ai_model_manager.get_training_insights(model_name)
        
        return AIResponse(
            success=True,
            message=f"模型 {model_name} 洞察获取成功",
            data=insights
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型洞察获取失败: {str(e)}")

@app.get("/api/v1/ai/model/report/{model_name}")
async def get_model_report(model_name: str):
    try:
        report = ai_model_manager.generate_model_report(model_name)
        
        return AIResponse(
            success=True,
            message=f"模型 {model_name} 报告生成成功",
            data=report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型报告生成失败: {str(e)}")

# 高级AI分析接口
@app.post("/api/v1/ai/analyze/risk-trends", response_model=AIResponse)
async def analyze_risk_trends(request: Dict[str, Any]):
    try:
        # 使用风险预测模型分析风险趋势
        import numpy as np
        
        # 模拟历史数据
        historical_data = request.get('historical_data', [])
        if not historical_data:
            # 生成模拟数据
            historical_data = np.random.rand(30, 20).tolist()
        
        # 预测未来风险趋势
        predictions = []
        for data_point in historical_data[-5:]:  # 使用最近5个数据点
            result = ai_model_manager.predict('risk_prediction', np.array(data_point))
            if result['success']:
                predictions.append({
                    'risk_level': result['prediction'],
                    'confidence': result['confidence']
                })
        
        # 分析趋势
        risk_trend = "stable"
        if len(predictions) >= 2:
            recent_risks = [p['risk_level'] for p in predictions[-2:]]
            if recent_risks[1] > recent_risks[0]:
                risk_trend = "increasing"
            elif recent_risks[1] < recent_risks[0]:
                risk_trend = "decreasing"
        
        analysis_result = {
            'risk_trend': risk_trend,
            'predictions': predictions,
            'average_confidence': np.mean([p['confidence'] for p in predictions]) if predictions else 0,
            'recommendations': ai_model_manager._get_model_recommendations('risk_prediction', {})
        }
        
        return AIResponse(
            success=True,
            message="风险趋势分析完成",
            data=analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"风险趋势分析失败: {str(e)}")

@app.post("/api/v1/ai/analyze/market-sentiment", response_model=AIResponse)
async def analyze_market_sentiment(request: Dict[str, Any]):
    try:
        # 使用市场分析模型分析市场情绪
        import numpy as np
        
        market_data = request.get('market_data', [])
        if not market_data:
            # 生成模拟市场数据
            market_data = np.random.rand(10, 10).tolist()
        
        # 分析市场情绪
        sentiment_scores = []
        for data_point in market_data:
            result = ai_model_manager.predict('market_analysis', np.array(data_point))
            if result['success']:
                sentiment_scores.append(result['prediction'])
        
        # 计算整体市场情绪
        if sentiment_scores:
            avg_sentiment = np.mean(sentiment_scores)
            if avg_sentiment == 0:
                market_sentiment = "看跌"
            elif avg_sentiment == 1:
                market_sentiment = "看涨"
            else:
                market_sentiment = "平稳"
        else:
            market_sentiment = "未知"
        
        # 计算平均置信度
        avg_confidence = 0
        if market_data:
            confidences = []
            for data_point in market_data:
                result = ai_model_manager.predict('market_analysis', np.array(data_point))
                if result['success']:
                    confidences.append(result['confidence'])
            avg_confidence = np.mean(confidences) if confidences else 0
        
        analysis_result = {
            'market_sentiment': market_sentiment,
            'sentiment_scores': sentiment_scores,
            'confidence': avg_confidence,
            'analysis_time': datetime.now().isoformat()
        }
        
        return AIResponse(
            success=True,
            message="市场情绪分析完成",
            data=analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"市场情绪分析失败: {str(e)}")

# AI智能客服接口
class ChatSessionRequest(BaseModel):
    user_id: str
    chatbot_role: str = "general"  # general, loan_specialist, risk_analyst, technical_support

class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    user_info: Optional[Dict[str, Any]] = None

@app.post("/api/v1/chat/session", response_model=AIResponse)
async def create_chat_session(request: ChatSessionRequest):
    """创建聊天会话"""
    try:
        logger.info(f"收到聊天会话创建请求: user_id={request.user_id}, chatbot_role={request.chatbot_role}")
        logger.info(f"请求数据类型: user_id={type(request.user_id)}, chatbot_role={type(request.chatbot_role)}")
        
        # 验证chatbot_role是否有效
        valid_roles = [role.value for role in ChatbotRole]
        logger.info(f"验证chatbot_role: {request.chatbot_role}, 有效值: {valid_roles}")
        if request.chatbot_role not in valid_roles:
            logger.error(f"无效的chatbot_role: {request.chatbot_role}, 有效值: {valid_roles}")
            raise HTTPException(status_code=422, detail=f"无效的chatbot_role: {request.chatbot_role}，有效值: {valid_roles}")
        
        role = ChatbotRole(request.chatbot_role)
        session_id = ai_chatbot.create_session(request.user_id, role)
        
        logger.info(f"会话创建成功: session_id={session_id}, 当前会话数: {len(ai_chatbot.sessions)}")
        logger.info(f"当前所有会话ID: {list(ai_chatbot.sessions.keys())}")
        
        return AIResponse(
            success=True,
            message="聊天会话创建成功",
            data={
                "session_id": session_id,
                "chatbot_role": request.chatbot_role,
                "created_at": datetime.now().isoformat()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"聊天会话创建失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建聊天会话失败: {str(e)}")

@app.post("/api/v1/chat/message", response_model=AIResponse)
async def send_chat_message(request: ChatMessageRequest):
    """发送聊天消息"""
    try:
        logger.info(f"收到聊天消息请求: session_id={request.session_id}, message={request.message[:50]}...")
        logger.info(f"当前会话数: {len(ai_chatbot.sessions)}")
        logger.info(f"当前所有会话ID: {list(ai_chatbot.sessions.keys())}")
        logger.info(f"请求的会话ID是否存在: {request.session_id in ai_chatbot.sessions}")
        
        result = await ai_chatbot.process_message(
            request.session_id,
            request.message,
            request.user_info
        )
        
        return AIResponse(
            success=True,
            message="消息处理成功",
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理消息失败: {str(e)}")

@app.get("/api/v1/chat/session/{session_id}/history")
async def get_chat_history(session_id: str):
    """获取聊天历史"""
    try:
        history = ai_chatbot.get_session_history(session_id)
        
        return AIResponse(
            success=True,
            message="聊天历史获取成功",
            data={
                "session_id": session_id,
                "messages": history,
                "total_messages": len(history)
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天历史失败: {str(e)}")

@app.get("/api/v1/chat/session/{session_id}/info")
async def get_session_info(session_id: str):
    """获取会话信息"""
    try:
        info = ai_chatbot.get_session_info(session_id)
        
        return AIResponse(
            success=True,
            message="会话信息获取成功",
            data=info
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话信息失败: {str(e)}")

@app.post("/api/v1/chat/cleanup")
async def cleanup_old_sessions():
    """清理旧会话"""
    try:
        cleaned_count = ai_chatbot.cleanup_old_sessions()
        
        return AIResponse(
            success=True,
            message=f"清理完成，共清理 {cleaned_count} 个旧会话",
            data={"cleaned_sessions": cleaned_count}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清理会话失败: {str(e)}")

@app.get("/api/v1/chat/knowledge/search")
async def search_knowledge(query: str, category: str = None):
    """搜索知识库"""
    try:
        if ai_chatbot.rag_kb:
            results = await ai_chatbot.rag_kb.search_knowledge_hybrid(query, max_results=10)
        else:
            results = []
        
        return AIResponse(
            success=True,
            message="知识库搜索成功",
            data={
                "query": query,
                "category": category,
                "results": results,
                "total_results": len(results)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索知识库失败: {str(e)}")

# LLM提供商管理接口
@app.get("/api/v1/llm/providers")
async def get_available_providers():
    """获取可用的LLM提供商列表"""
    try:
        providers = llm_provider_manager.get_available_providers()
        default_provider = llm_provider_manager.get_default_provider()
        
        return AIResponse(
            success=True,
            message="LLM提供商列表获取成功",
            data={
                "available_providers": providers,
                "default_provider": default_provider,
                "total_count": len(providers)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取LLM提供商列表失败: {str(e)}")

@app.post("/api/v1/llm/generate")
async def generate_llm_response(request: Dict[str, Any]):
    """生成LLM回复"""
    try:
        messages = request.get("messages", [])
        provider = request.get("provider")
        model = request.get("model")
        temperature = request.get("temperature", 0.7)
        max_tokens = request.get("max_tokens", 1000)
        
        if not messages:
            raise HTTPException(status_code=400, detail="消息内容不能为空")
        
        result = await llm_provider_manager.generate_response(
            messages=messages,
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return AIResponse(
            success=True,
            message="LLM回复生成成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"生成LLM回复失败: {e}")
        raise HTTPException(status_code=500, detail=f"生成LLM回复失败: {str(e)}")

@app.post("/api/v1/llm/test")
async def test_llm_provider(request: Dict[str, Any]):
    """测试LLM提供商"""
    try:
        provider = request.get("provider")
        model = request.get("model")
        message = request.get("message", "你好，请介绍一下你自己")
        
        messages = [
            {"role": "user", "content": message}
        ]
        
        result = await llm_provider_manager.generate_response(
            messages=messages,
            provider=provider,
            model=model,
            temperature=0.7,
            max_tokens=500
        )
        
        return AIResponse(
            success=result.get("success", False),
            message="LLM测试完成",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM测试失败: {str(e)}")

# RAG知识库管理接口
@app.post("/api/v1/rag/knowledge")
async def add_knowledge(request: Dict[str, Any]):
    """添加知识到向量数据库"""
    try:
        category = request.get("category")
        title = request.get("title")
        content = request.get("content")
        metadata = request.get("metadata", {})
        
        if not all([category, title, content]):
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        knowledge_id = await vector_rag_service.add_knowledge(
            category=category,
            title=title,
            content=content,
            metadata=metadata
        )
        
        if knowledge_id:
            return AIResponse(
                success=True,
                message="知识添加成功",
                data={"knowledge_id": knowledge_id}
            )
        else:
            raise HTTPException(status_code=500, detail="知识添加失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加知识失败: {str(e)}")

@app.get("/api/v1/rag/knowledge/{knowledge_id}")
async def get_knowledge(knowledge_id: int):
    """根据ID获取知识"""
    try:
        knowledge = await vector_rag_service.get_knowledge_by_id(knowledge_id)
        
        if knowledge:
            return AIResponse(
                success=True,
                message="知识获取成功",
                data=knowledge
            )
        else:
            raise HTTPException(status_code=404, detail="知识不存在")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识失败: {str(e)}")

@app.put("/api/v1/rag/knowledge/{knowledge_id}")
async def update_knowledge(knowledge_id: int, request: Dict[str, Any]):
    """更新知识"""
    try:
        title = request.get("title")
        content = request.get("content")
        metadata = request.get("metadata")
        
        success = await vector_rag_service.update_knowledge(
            knowledge_id=knowledge_id,
            title=title,
            content=content,
            metadata=metadata
        )
        
        if success:
            return AIResponse(
                success=True,
                message="知识更新成功",
                data={"knowledge_id": knowledge_id}
            )
        else:
            raise HTTPException(status_code=500, detail="知识更新失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新知识失败: {str(e)}")

@app.delete("/api/v1/rag/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: int):
    """删除知识"""
    try:
        success = await vector_rag_service.delete_knowledge(knowledge_id)
        
        if success:
            return AIResponse(
                success=True,
                message="知识删除成功",
                data={"knowledge_id": knowledge_id}
            )
        else:
            raise HTTPException(status_code=500, detail="知识删除失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除知识失败: {str(e)}")

@app.get("/api/v1/rag/stats")
async def get_rag_stats():
    """获取RAG知识库统计信息"""
    try:
        stats = await vector_rag_service.get_knowledge_stats()
        
        return AIResponse(
            success=True,
            message="统计信息获取成功",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

# 文档处理API
@app.post("/api/v1/rag/process-document")
async def process_document(
    file: UploadFile = File(...),
    category: str = "general",
    metadata: str = "{}"
):
    """处理并上传文档到RAG系统"""
    try:
        # 解析元数据
        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            metadata_dict = {}
        
        # 保存上传的文件
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理文档并添加到RAG系统
        result = await document_rag.process_and_add_document(
            file_path=file_path,
            file_type=file.filename.split('.')[-1].lower(),
            category=category,
            metadata=metadata_dict
        )
        
        # 清理临时文件（在处理完成后）
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"清理临时文件失败: {e}")
        
        return AIResponse(
            success=True,
            message="文档处理成功",
            data={
                "document_id": result.get("document_id", str(uuid.uuid4())),
                "filename": file.filename,
                "category": category,
                "chunks_created": result.get("indexed_chunks", 0),
                "total_chunks": result.get("total_chunks", 0),
                "content": result.get("processing_result", {}).get("text", "")[:500] + "..." if result.get("processing_result", {}).get("text") else "",
                "content_length": len(result.get("processing_result", {}).get("text", "")),
                "processing_time": result.get("processing_time", 0),
                "document_type": result.get("document_type", "unknown")
            }
        )
        
    except Exception as e:
        logger.error(f"文档处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"文档处理失败: {str(e)}")

@app.post("/api/v1/rag/batch-process")
async def batch_process_documents(
    file_paths: List[str],
    category: str = "general",
    metadata: Dict[str, Any] = {}
):
    """批量处理文档"""
    try:
        results = await document_rag.batch_process_and_add_documents(
            file_paths=file_paths,
            category=category,
            metadata=metadata
        )
        
        return AIResponse(
            success=True,
            message="批量文档处理成功",
            data=results
        )
        
    except Exception as e:
        logger.error(f"批量文档处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"批量文档处理失败: {str(e)}")

# 网络搜索API
@app.post("/api/v1/web/search/bank")
async def search_bank_info(request: Dict[str, Any]):
    """搜索银行信息"""
    try:
        bank_name = request.get("bank_name")
        query = request.get("query", "")
        
        if not bank_name:
            raise HTTPException(status_code=400, detail="银行名称不能为空")
        
        result = await enhanced_web_search_service.search_bank_info(bank_name, query)
        
        return AIResponse(
            success=True,
            message="银行信息搜索成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"搜索银行信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索银行信息失败: {str(e)}")

@app.get("/api/v1/web/search/banks")
async def search_all_banks(query: str = ""):
    """搜索所有银行信息"""
    try:
        result = await enhanced_web_search_service.search_multiple_banks(query)
        
        return AIResponse(
            success=True,
            message="多银行信息搜索成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"搜索多银行信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索多银行信息失败: {str(e)}")

@app.get("/api/v1/web/search/bank/{bank_name}/contact")
async def get_bank_contact(bank_name: str):
    """获取银行联系方式"""
    try:
        result = await enhanced_web_search_service.get_bank_contact_info(bank_name)
        
        return AIResponse(
            success=True,
            message="银行联系方式获取成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"获取银行联系方式失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取银行联系方式失败: {str(e)}")

# 通用银行搜索API
@app.post("/api/v1/web/search/universal/bank")
async def search_universal_bank(request: Dict[str, Any]):
    """通用银行搜索"""
    try:
        bank_name = request.get("bank_name")
        query = request.get("query", "")
        
        if not bank_name:
            raise HTTPException(status_code=400, detail="银行名称不能为空")
        
        result = await universal_bank_search_service.search_bank_info(bank_name, query)
        
        return AIResponse(
            success=True,
            message="通用银行搜索成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"通用银行搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"通用银行搜索失败: {str(e)}")

@app.get("/api/v1/web/search/universal/banks")
async def search_all_universal_banks(query: str = ""):
    """搜索所有银行（通用）"""
    try:
        result = await universal_bank_search_service.search_all_banks(query)
        
        return AIResponse(
            success=True,
            message="通用多银行搜索成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"通用多银行搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"通用多银行搜索失败: {str(e)}")

@app.post("/api/v1/web/search/universal/detect")
async def detect_bank_in_message(request: Dict[str, Any]):
    """检测消息中的银行名称"""
    try:
        message = request.get("message", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="消息内容不能为空")
        
        # 优先使用LLM推理
        bank_name = await universal_bank_search_service.detect_bank_name_with_llm(message)
        if not bank_name:
            # 如果LLM推理失败，使用传统方法
            bank_name = universal_bank_search_service.detect_bank_name(message)
        
        return AIResponse(
            success=True,
            message="银行名称检测成功",
            data={
                "bank_name": bank_name,
                "message": message,
                "detected": bank_name is not None
            }
        )
        
    except Exception as e:
        logger.error(f"银行名称检测失败: {e}")
        raise HTTPException(status_code=500, detail=f"银行名称检测失败: {str(e)}")

# 真正的外网搜索API
@app.post("/api/v1/web/search/real")
async def real_web_search(request: Dict[str, Any]):
    """真正的外网搜索"""
    try:
        bank_name = request.get("bank_name")
        query = request.get("query", "")
        
        if not bank_name:
            raise HTTPException(status_code=400, detail="银行名称不能为空")
        
        result = await real_web_search_service.search_bank_info(bank_name, query)
        
        return AIResponse(
            success=True,
            message="外网搜索成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"外网搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"外网搜索失败: {str(e)}")

@app.post("/api/v1/rag/search")
async def search_knowledge_advanced(request: Dict[str, Any]):
    """高级知识搜索"""
    try:
        query = request.get("query")
        category = request.get("category")
        search_type = request.get("search_type", "hybrid")  # vector, text, hybrid
        max_results = request.get("max_results", 5)
        
        if not query:
            raise HTTPException(status_code=400, detail="查询内容不能为空")
        
        if search_type == "vector":
            results = await vector_rag_service.search_knowledge_vector(
                query=query,
                category=category,
                max_results=max_results
            )
        elif search_type == "text":
            results = await vector_rag_service.search_knowledge_text(
                query=query,
                category=category,
                max_results=max_results
            )
        else:  # hybrid
            results = await vector_rag_service.search_knowledge_hybrid(
                query=query,
                category=category,
                max_results=max_results
            )
        
        return AIResponse(
            success=True,
            message="知识搜索成功",
            data={
                "query": query,
                "search_type": search_type,
                "category": category,
                "results": results,
                "total_results": len(results)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识搜索失败: {str(e)}")

# ==================== 征信API路由 ====================

@app.post("/api/v1/credit/query")
async def query_enterprise_credit(request: Dict[str, Any]):
    """查询企业信用评分"""
    try:
        company_name = request.get('company_name', '')
        provider = request.get('provider', 'jingdong')
        
        if not company_name:
            raise HTTPException(status_code=400, detail="企业名称不能为空")
        
        logger.info(f"收到征信查询请求: {company_name}, 提供商: {provider}")
        
        # 调用征信API服务
        result = credit_api_service.query_enterprise_credit(
            company_name=company_name,
            provider=provider
        )
        
        if result.get('success'):
            # 成功查询
            return AIResponse(
                success=True,
                message="征信查询成功",
                data={
                    'credit_score': result.get('data', {}).get('credit_score', 0),
                    'credit_level': result.get('data', {}).get('credit_level', '未知'),
                    'credit_source': result.get('data', {}).get('credit_source', '未知'),
                    'company_name': company_name,
                    'provider': result.get('provider', provider),
                    'quota_remaining': result.get('quota_remaining'),
                    'query_time': datetime.now().isoformat(),
                    'is_mock': result.get('data', {}).get('is_mock', False)
                }
            )
        else:
            # 查询失败，使用模拟数据
            logger.warning(f"征信API查询失败: {result.get('error')}, 使用模拟数据")
            
            # 生成模拟数据
            import random
            mock_score = random.randint(500, 800)
            mock_level = '优秀' if mock_score >= 750 else '良好' if mock_score >= 700 else '一般' if mock_score >= 650 else '较差'
            
            mock_sources = [
                '央行征信中心 (模拟)',
                '百行征信 (模拟)',
                '芝麻信用 (模拟)',
                '腾讯征信 (模拟)'
            ]
            mock_source = random.choice(mock_sources)
            
            return AIResponse(
                success=True,
                message="征信查询成功（模拟数据）",
                data={
                    'credit_score': mock_score,
                    'credit_level': mock_level,
                    'credit_source': mock_source,
                    'company_name': company_name,
                    'provider': 'mock',
                    'quota_remaining': None,
                    'query_time': datetime.now().isoformat(),
                    'is_mock': True
                }
            )
            
    except Exception as e:
        logger.error(f"征信查询异常: {e}")
        return AIResponse(
            success=False,
            message=f"征信查询失败: {str(e)}",
            data={}
        )

@app.get("/api/v1/credit/stats")
async def get_credit_usage_stats():
    """获取征信API使用统计"""
    try:
        stats = credit_api_service.get_usage_stats()
        return AIResponse(
            success=True,
            message="获取统计成功",
            data=stats
        )
    except Exception as e:
        logger.error(f"获取使用统计失败: {e}")
        return AIResponse(
            success=False,
            message=f"获取统计失败: {str(e)}",
            data={}
        )

@app.get("/api/v1/credit/providers")
async def get_credit_providers():
    """获取可用的征信提供商"""
    try:
        providers = []
        for key, config in credit_api_service.apis.items():
            providers.append({
                'id': key,
                'name': config['name'],
                'enabled': config.get('enabled', False),
                'free_quota': config['free_quota'],
                'used': credit_api_service.usage_stats[key]['used'],
                'remaining': config['free_quota'] - credit_api_service.usage_stats[key]['used']
            })
        
        return AIResponse(
            success=True,
            message="获取提供商列表成功",
            data={'providers': providers}
        )
    except Exception as e:
        logger.error(f"获取提供商列表失败: {e}")
        return AIResponse(
            success=False,
            message=f"获取提供商失败: {str(e)}",
            data={}
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
