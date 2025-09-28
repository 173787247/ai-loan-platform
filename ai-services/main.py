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
from services.loan_agent import LoanAgent
from services.loan_rfq_service import LoanRFQService
from services.cache_service import cache_service
from services.universal_bank_search import universal_bank_search_service
from services.real_web_search import real_web_search_service
from services.credit_api_service import credit_api_service
from services.conversation_enhancer import ConversationEnhancer
from services.knowledge_enhancer import KnowledgeEnhancer
from services.personalization_engine import PersonalizationEngine
from services.multi_turn_dialog import MultiTurnDialogManager
from services.advanced_risk_engine import AdvancedRiskEngine
from services.advanced_pricing_engine import AdvancedPricingEngine
from services.approval_workflow_engine import ApprovalWorkflowEngine
from services.compliance_checker import ComplianceChecker
from services.third_party_integrator import third_party_integrator
from services.data_sync_manager import data_sync_manager
from services.api_stability_manager import api_stability_manager
from services.monitoring_system import system_monitor
from services.performance_optimizer import performance_optimizer
from services.advanced_ocr import advanced_ocr_service
from middleware.error_handler import ErrorHandler, PerformanceMiddleware, LoggingMiddleware
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
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 添加性能监控中间件
app.middleware("http")(PerformanceMiddleware.performance_middleware)

# 添加日志中间件
app.middleware("http")(LoggingMiddleware.logging_middleware)

# 设置错误处理器
ErrorHandler.setup_error_handlers(app)

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化服务"""
    try:
        # 初始化缓存服务
        await cache_service.initialize()
        logger.info("缓存服务初始化成功")
        
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
        
        # 初始化文档RAG服务
        await document_rag.initialize()
        logger.info("文档RAG服务初始化成功")
        
        # 初始化AI增强服务
        knowledge_enhance_result = knowledge_enhancer.enhance_knowledge_base()
        if knowledge_enhance_result.get("success"):
            logger.info(f"知识库增强成功，新增 {knowledge_enhance_result.get('enhanced_count', 0)} 条知识")
        else:
            logger.warning("知识库增强失败")
        
        logger.info("AI增强服务初始化完成")
        
        # 初始化集成服务
        await third_party_integrator.initialize()
        await data_sync_manager.initialize()
        await system_monitor.start_monitoring()
        
        # 初始化性能优化器
        await performance_optimizer.initialize()
        await performance_optimizer.connection_pool_manager.create_pool(
            "main_db", 
            {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "port": int(os.getenv("POSTGRES_PORT", "5432")),
                "database": os.getenv("POSTGRES_DB", "ai_loan_rag"),
                "user": os.getenv("POSTGRES_USER", "ai_loan"),
                "password": os.getenv("POSTGRES_PASSWORD", "ai_loan123"),
                "min_size": 5,
                "max_size": 20
            }
        )
        
        # 配置API稳定性管理器
        from services.api_stability_manager import CircuitBreakerConfig, RateLimitConfig
        api_stability_manager.add_circuit_breaker("ai_chatbot", CircuitBreakerConfig())
        api_stability_manager.add_circuit_breaker("rag_search", CircuitBreakerConfig())
        api_stability_manager.add_rate_limiter("ai_chatbot", RateLimitConfig(max_requests=100, window_size=60))
        api_stability_manager.add_rate_limiter("rag_search", RateLimitConfig(max_requests=200, window_size=60))
        
        logger.info("集成服务初始化完成")
        
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

# 全局贷款智能体实例
loan_agent = LoanAgent(
    llm_service=llm_provider_manager,
    rag_service=vector_rag_service,
    risk_service=None,  # 待实现
    pricing_service=None  # 待实现
)

# 全局助贷招标服务实例
loan_rfq_service = LoanRFQService()

# 全局AI增强服务实例
conversation_enhancer = ConversationEnhancer(llm_service=llm_provider_manager)
knowledge_enhancer = KnowledgeEnhancer(vector_rag_service=vector_rag_service)
personalization_engine = PersonalizationEngine()
multi_turn_dialog_manager = MultiTurnDialogManager(
    conversation_enhancer=conversation_enhancer,
    knowledge_enhancer=knowledge_enhancer
)

# 全局业务服务实例
advanced_risk_engine = AdvancedRiskEngine()
advanced_pricing_engine = AdvancedPricingEngine()
approval_workflow_engine = ApprovalWorkflowEngine()
compliance_checker = ComplianceChecker()

# 全局集成服务实例
# third_party_integrator 已在模块中初始化
# data_sync_manager 已在模块中初始化
# api_stability_manager 已在模块中初始化
# system_monitor 已在模块中初始化

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

# 学习状态监控接口
@app.get("/api/v1/learning/status")
async def get_learning_status():
    """获取学习状态"""
    try:
        if ai_chatbot and ai_chatbot.smart_learning:
            status = await ai_chatbot.smart_learning.get_learning_status()
            return {
                "success": True,
                "data": status
            }
        else:
            return {
                "success": False,
                "error": "智能学习系统未启用"
            }
    except Exception as e:
        logger.error(f"获取学习状态失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/v1/learning/trigger")
async def trigger_learning(request: dict):
    """手动触发学习"""
    try:
        query = request.get("query", "")
        if not query:
            return {
                "success": False,
                "error": "查询内容不能为空"
            }
        
        if ai_chatbot and ai_chatbot.smart_learning:
            result = await ai_chatbot.smart_learning.trigger_learning(query)
            return {
                "success": True,
                "data": result
            }
        else:
            return {
                "success": False,
                "error": "智能学习系统未启用"
            }
    except Exception as e:
        logger.error(f"触发学习失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# 自主机器学习接口
@app.post("/api/v1/autonomous-learning/start")
async def start_autonomous_learning():
    """启动自主机器学习"""
    try:
        if ai_chatbot and ai_chatbot.autonomous_learning:
            await ai_chatbot.autonomous_learning.start_autonomous_learning()
            return {
                "success": True,
                "message": "自主机器学习已启动"
            }
        else:
            return {
                "success": False,
                "error": "自主机器学习系统未启用"
            }
    except Exception as e:
        logger.error(f"启动自主机器学习失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/v1/autonomous-learning/status")
async def get_autonomous_learning_status():
    """获取自主机器学习状态"""
    try:
        if ai_chatbot and ai_chatbot.autonomous_learning:
            status = await ai_chatbot.autonomous_learning.get_learning_status()
            return {
                "success": True,
                "data": status
            }
        else:
            return {
                "success": False,
                "error": "自主机器学习系统未启用"
            }
    except Exception as e:
        logger.error(f"获取自主机器学习状态失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/v1/autonomous-learning/stop")
async def stop_autonomous_learning():
    """停止自主机器学习"""
    try:
        if ai_chatbot and ai_chatbot.autonomous_learning:
            await ai_chatbot.autonomous_learning.stop_learning()
            return {
                "success": True,
                "message": "自主机器学习已停止"
            }
        else:
            return {
                "success": False,
                "error": "自主机器学习系统未启用"
            }
    except Exception as e:
        logger.error(f"停止自主机器学习失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# 银行清单学习接口
@app.post("/api/v1/bank-list-learning/start")
async def start_bank_list_learning():
    """启动银行清单学习"""
    try:
        if ai_chatbot and ai_chatbot.bank_list_learning:
            await ai_chatbot.bank_list_learning.start_bank_list_learning()
            return {
                "success": True,
                "message": "银行清单学习已启动"
            }
        else:
            return {
                "success": False,
                "error": "银行清单学习系统未启用"
            }
    except Exception as e:
        logger.error(f"启动银行清单学习失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/v1/bank-list-learning/status")
async def get_bank_list_learning_status():
    """获取银行清单学习状态"""
    try:
        if ai_chatbot and ai_chatbot.bank_list_learning:
            status = await ai_chatbot.bank_list_learning.get_learning_status()
            return {
                "success": True,
                "data": status
            }
        else:
            return {
                "success": False,
                "error": "银行清单学习系统未启用"
            }
    except Exception as e:
        logger.error(f"获取银行清单学习状态失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/v1/bank-list-learning/bank-list")
async def get_bank_list():
    """获取银行清单"""
    try:
        if ai_chatbot and ai_chatbot.bank_list_learning:
            bank_list = await ai_chatbot.bank_list_learning.get_bank_list()
            return {
                "success": True,
                "data": bank_list
            }
        else:
            return {
                "success": False,
                "error": "银行清单学习系统未启用"
            }
    except Exception as e:
        logger.error(f"获取银行清单失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/v1/bank-list-learning/stop")
async def stop_bank_list_learning():
    """停止银行清单学习"""
    try:
        if ai_chatbot and ai_chatbot.bank_list_learning:
            await ai_chatbot.bank_list_learning.stop_learning()
            return {
                "success": True,
                "message": "银行清单学习已停止"
            }
        else:
            return {
                "success": False,
                "error": "银行清单学习系统未启用"
            }
    except Exception as e:
        logger.error(f"停止银行清单学习失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# 智能贷款推荐接口
@app.post("/api/v1/loan-recommendation/analyze")
async def analyze_user_and_recommend(user_info: dict):
    """分析用户画像并推荐贷款产品"""
    try:
        if ai_chatbot and ai_chatbot.loan_recommendation:
            # 分析用户画像
            user_profile = await ai_chatbot.loan_recommendation.analyze_user_profile(user_info)
            
            # 计算产品评分
            scored_products = await ai_chatbot.loan_recommendation.calculate_product_scores(user_profile)
            
            # 生成推荐报告
            recommendation_report = await ai_chatbot.loan_recommendation.generate_recommendation_report(
                user_profile, scored_products
            )
            
            return {
                "success": True,
                "data": {
                    "user_profile": user_profile,
                    "scored_products": scored_products[:10],  # 返回前10个产品
                    "recommendation_report": recommendation_report
                }
            }
        else:
            return {
                "success": False,
                "error": "智能贷款推荐系统未启用"
            }
    except Exception as e:
        logger.error(f"贷款推荐分析失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/v1/loan-recommendation/products")
async def get_all_products():
    """获取所有银行产品信息"""
    try:
        if ai_chatbot and ai_chatbot.loan_recommendation:
            products = ai_chatbot.loan_recommendation.bank_products_db
            return {
                "success": True,
                "data": products
            }
        else:
            return {
                "success": False,
                "error": "智能贷款推荐系统未启用"
            }
    except Exception as e:
        logger.error(f"获取产品信息失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/v1/loan-recommendation/compare")
async def compare_products(products_to_compare: dict):
    """对比多个产品"""
    try:
        if ai_chatbot and ai_chatbot.loan_recommendation:
            product_names = products_to_compare.get("products", [])
            user_info = products_to_compare.get("user_info", {})
            
            # 分析用户画像
            user_profile = await ai_chatbot.loan_recommendation.analyze_user_profile(user_info)
            
            # 获取指定产品的评分
            all_scored_products = await ai_chatbot.loan_recommendation.calculate_product_scores(user_profile)
            
            # 筛选指定产品
            compared_products = []
            for product in all_scored_products:
                product_key = f"{product['bank_name']}-{product['product_name']}"
                if product_key in product_names:
                    compared_products.append(product)
            
            # 按评分排序
            compared_products.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "success": True,
                "data": {
                    "user_profile": user_profile,
                    "compared_products": compared_products,
                    "comparison_summary": {
                        "best_product": compared_products[0] if compared_products else None,
                        "total_products": len(compared_products)
                    }
                }
            }
        else:
            return {
                "success": False,
                "error": "智能贷款推荐系统未启用"
            }
    except Exception as e:
        logger.error(f"产品对比失败: {e}")
        return {
            "success": False,
            "error": str(e)
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

@app.get("/api/v1/cache/stats")
async def get_cache_stats():
    """获取缓存统计信息"""
    try:
        stats = await cache_service.get_stats()
        return AIResponse(
            success=True,
            message="缓存统计信息获取成功",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取缓存统计信息失败: {str(e)}")

@app.post("/api/v1/cache/clear")
async def clear_cache(request: Dict[str, Any]):
    """清除缓存"""
    try:
        pattern = request.get("pattern", "*")
        cleared_count = await cache_service.clear_pattern(pattern)
        return AIResponse(
            success=True,
            message=f"缓存清除成功，共清除 {cleared_count} 个键",
            data={"cleared_count": cleared_count}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除缓存失败: {str(e)}")

# 文档处理API
@app.options("/api/v1/rag/process-document")
async def process_document_options():
    """处理文档上传的OPTIONS请求"""
    return {"message": "OK"}

# 贷款智能体API端点
@app.post("/api/v1/loan-agent/chat")
async def loan_agent_chat(request: dict):
    """贷款智能体对话接口"""
    try:
        user_id = request.get("user_id")
        message = request.get("message")
        session_id = request.get("session_id")
        
        if not user_id or not message:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        result = await loan_agent.process_message(user_id, message, session_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "贷款智能体对话成功",
                "data": result
            }
        )
        
    except Exception as e:
        logger.error(f"贷款智能体对话失败: {e}")
        raise HTTPException(status_code=500, detail=f"贷款智能体对话失败: {str(e)}")

@app.get("/api/v1/loan-agent/profile/{user_id}")
async def get_loan_profile(user_id: str):
    """获取用户贷款档案"""
    try:
        if user_id in loan_agent.profiles:
            profile = loan_agent.profiles[user_id]
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "获取用户档案成功",
                    "data": {
                        "profile": profile.__dict__,
                        "status": profile.status.value,
                        "next_actions": loan_agent._get_next_actions(profile)
                    }
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "用户档案不存在"
                }
            )
            
    except Exception as e:
        logger.error(f"获取用户档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取用户档案失败: {str(e)}")

@app.post("/api/v1/loan-agent/reset/{user_id}")
async def reset_loan_profile(user_id: str):
    """重置用户贷款档案"""
    try:
        if user_id in loan_agent.profiles:
            del loan_agent.profiles[user_id]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "用户档案重置成功"
            }
        )
        
    except Exception as e:
        logger.error(f"重置用户档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"重置用户档案失败: {str(e)}")

# 助贷招标API端点
@app.post("/api/v1/rfq/create")
async def create_rfq(request: dict):
    """创建贷款招标需求"""
    try:
        borrower_profile = request.get("borrower_profile")
        if not borrower_profile:
            raise HTTPException(status_code=400, detail="缺少借款人档案信息")
        
        result = await loan_rfq_service.create_rfq(borrower_profile)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "RFQ创建成功",
                "data": result
            }
        )
        
    except Exception as e:
        logger.error(f"创建RFQ失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建RFQ失败: {str(e)}")

@app.post("/api/v1/rfq/{rfq_id}/publish")
async def publish_rfq(rfq_id: str, request: dict = None):
    """发布RFQ"""
    try:
        deadline_hours = request.get("deadline_hours", 72) if request else 72
        result = await loan_rfq_service.publish_rfq(rfq_id, deadline_hours)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "RFQ发布成功",
                "data": result
            }
        )
        
    except Exception as e:
        logger.error(f"发布RFQ失败: {e}")
        raise HTTPException(status_code=500, detail=f"发布RFQ失败: {str(e)}")

@app.post("/api/v1/rfq/{rfq_id}/bid")
async def submit_bid(rfq_id: str, request: dict):
    """提交投标方案"""
    try:
        lender_id = request.get("lender_id")
        bid_data = request.get("bid_data")
        
        if not lender_id or not bid_data:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        result = await loan_rfq_service.submit_bid(rfq_id, lender_id, bid_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "投标提交成功",
                "data": result
            }
        )
        
    except Exception as e:
        logger.error(f"提交投标失败: {e}")
        raise HTTPException(status_code=500, detail=f"提交投标失败: {str(e)}")

@app.get("/api/v1/rfq/{rfq_id}/bids")
async def get_rfq_bids(rfq_id: str):
    """获取RFQ的所有投标"""
    try:
        result = await loan_rfq_service.get_rfq_bids(rfq_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "获取投标列表成功",
                "data": result
            }
        )
        
    except Exception as e:
        logger.error(f"获取投标列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取投标列表失败: {str(e)}")

@app.post("/api/v1/rfq/{rfq_id}/award/{bid_id}")
async def award_bid(rfq_id: str, bid_id: str):
    """中标投标方案"""
    try:
        result = await loan_rfq_service.award_bid(rfq_id, bid_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "中标成功",
                "data": result
            }
        )
        
    except Exception as e:
        logger.error(f"中标处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"中标处理失败: {str(e)}")

# AI增强服务API
@app.post("/api/v1/ai/enhanced-chat")
async def enhanced_chat(request: Dict[str, Any]):
    """增强AI聊天接口"""
    try:
        user_id = request.get("user_id")
        message = request.get("message")
        session_id = request.get("session_id")
        
        if not user_id or not message:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        # 更新用户交互记录
        personalization_engine.update_user_interaction(user_id, {
            "query": message,
            "query_type": "chat",
            "timestamp": datetime.now().isoformat()
        })
        
        # 使用多轮对话管理器
        if session_id not in multi_turn_dialog_manager.dialog_contexts:
            multi_turn_dialog_manager.start_dialog(session_id, user_id, message)
        
        dialog_response = multi_turn_dialog_manager.process_message(session_id, message)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "增强AI聊天成功",
                "data": {
                    "response": dialog_response.response_text,
                    "next_state": dialog_response.next_state.value,
                    "suggested_questions": dialog_response.suggested_questions,
                    "follow_up_actions": dialog_response.follow_up_actions,
                    "confidence": dialog_response.confidence,
                    "requires_clarification": dialog_response.requires_clarification
                }
            }
        )
        
    except Exception as e:
        logger.error(f"增强AI聊天失败: {e}")
        raise HTTPException(status_code=500, detail=f"增强AI聊天失败: {str(e)}")

@app.get("/api/v1/ai/personalized-recommendations/{user_id}")
async def get_personalized_recommendations(user_id: str, max_recommendations: int = 5):
    """获取个性化推荐"""
    try:
        recommendations = personalization_engine.generate_personalized_recommendations(
            user_id, max_recommendations
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "个性化推荐获取成功",
                "data": {
                    "recommendations": [
                        {
                            "id": rec.id,
                            "title": rec.title,
                            "description": rec.description,
                            "category": rec.category.value,
                            "relevance_score": rec.relevance_score,
                            "confidence": rec.confidence,
                            "reason": rec.reason,
                            "action_url": rec.action_url,
                            "metadata": rec.metadata
                        }
                        for rec in recommendations
                    ],
                    "total_count": len(recommendations)
                }
            }
        )
        
    except Exception as e:
        logger.error(f"获取个性化推荐失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取个性化推荐失败: {str(e)}")

@app.get("/api/v1/ai/enhanced-knowledge/search")
async def search_enhanced_knowledge(query: str, category: str = None, max_results: int = 5):
    """搜索增强知识库"""
    try:
        results = knowledge_enhancer.search_enhanced_knowledge(
            query, category, max_results
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "增强知识库搜索成功",
                "data": {
                    "results": results,
                    "total_count": len(results)
                }
            }
        )
        
    except Exception as e:
        logger.error(f"增强知识库搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"增强知识库搜索失败: {str(e)}")

@app.get("/api/v1/ai/dialog-summary/{session_id}")
async def get_dialog_summary(session_id: str):
    """获取对话摘要"""
    try:
        summary = multi_turn_dialog_manager.get_dialog_summary(session_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "对话摘要获取成功",
                "data": summary
            }
        )
        
    except Exception as e:
        logger.error(f"获取对话摘要失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取对话摘要失败: {str(e)}")

@app.get("/api/v1/ai/user-profile/{user_id}")
async def get_user_profile(user_id: str):
    """获取用户画像"""
    try:
        profile = personalization_engine.get_user_profile(user_id)
        
        if not profile:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "用户画像不存在"
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "用户画像获取成功",
                "data": {
                    "user_id": profile.user_id,
                    "profile_type": profile.profile_type.value,
                    "interests": [interest.value for interest in profile.interests],
                    "risk_tolerance": profile.risk_tolerance,
                    "income_range": profile.income_range,
                    "age_group": profile.age_group,
                    "preferred_banks": profile.preferred_banks,
                    "interaction_count": len(profile.interaction_history),
                    "last_activity": profile.last_activity.isoformat(),
                    "behavior_patterns": profile.behavior_patterns
                }
            }
        )
        
    except Exception as e:
        logger.error(f"获取用户画像失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取用户画像失败: {str(e)}")

# 高级风控服务API
@app.post("/api/v1/risk/advanced-assessment")
async def advanced_risk_assessment(request: Dict[str, Any]):
    """高级风险评估"""
    try:
        assessment = advanced_risk_engine.assess_risk(request)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "高级风险评估完成",
                "data": {
                    "overall_risk_score": assessment.overall_risk_score,
                    "risk_level": assessment.risk_level.value,
                    "approval_recommendation": assessment.approval_recommendation,
                    "risk_factors": {factor.value: score for factor, score in assessment.risk_factors.items()},
                    "risk_explanations": {factor.value: explanation for factor, explanation in assessment.risk_explanations.items()},
                    "mitigation_suggestions": assessment.mitigation_suggestions,
                    "confidence_score": assessment.confidence_score,
                    "assessment_timestamp": assessment.assessment_timestamp.isoformat(),
                    "model_version": assessment.model_version
                }
            }
        )
        
    except Exception as e:
        logger.error(f"高级风险评估失败: {e}")
        raise HTTPException(status_code=500, detail=f"高级风险评估失败: {str(e)}")

@app.get("/api/v1/risk/model-info")
async def get_risk_model_info():
    """获取风控模型信息"""
    try:
        model_info = advanced_risk_engine.get_risk_model_info()
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "风控模型信息获取成功",
                "data": model_info
            }
        )
    except Exception as e:
        logger.error(f"获取风控模型信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取风控模型信息失败: {str(e)}")

# 高级定价服务API
@app.post("/api/v1/pricing/calculate")
async def calculate_pricing(request: Dict[str, Any]):
    """计算贷款定价"""
    try:
        loan_request = request.get("loan_request", {})
        risk_assessment = request.get("risk_assessment", {})
        pricing_strategy = request.get("pricing_strategy", "risk_based")
        
        from services.advanced_pricing_engine import PricingStrategy
        strategy = PricingStrategy(pricing_strategy)
        
        pricing_result = advanced_pricing_engine.calculate_pricing(loan_request, risk_assessment, strategy)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "贷款定价计算完成",
                "data": {
                    "base_interest_rate": pricing_result.base_interest_rate,
                    "final_interest_rate": pricing_result.final_interest_rate,
                    "monthly_payment": pricing_result.monthly_payment,
                    "total_interest": pricing_result.total_interest,
                    "total_amount": pricing_result.total_amount,
                    "fees": {fee.value: amount for fee, amount in pricing_result.fees.items()},
                    "total_fees": pricing_result.total_fees,
                    "apr": pricing_result.apr,
                    "pricing_strategy": pricing_result.pricing_strategy.value,
                    "risk_adjustment": pricing_result.risk_adjustment,
                    "market_adjustment": pricing_result.market_adjustment,
                    "profit_margin": pricing_result.profit_margin,
                    "confidence_score": pricing_result.confidence_score,
                    "pricing_timestamp": pricing_result.pricing_timestamp.isoformat(),
                    "model_version": pricing_result.model_version
                }
            }
        )
        
    except Exception as e:
        logger.error(f"贷款定价计算失败: {e}")
        raise HTTPException(status_code=500, detail=f"贷款定价计算失败: {str(e)}")

@app.post("/api/v1/pricing/optimize")
async def optimize_pricing(request: Dict[str, Any]):
    """优化定价方案"""
    try:
        loan_request = request.get("loan_request", {})
        risk_assessment = request.get("risk_assessment", {})
        target_profit_margin = request.get("target_profit_margin", 0.05)
        
        pricing_scenarios = advanced_pricing_engine.optimize_pricing(loan_request, risk_assessment, target_profit_margin)
        
        scenarios_data = []
        for scenario in pricing_scenarios:
            scenarios_data.append({
                "strategy": scenario.pricing_strategy.value,
                "interest_rate": scenario.final_interest_rate,
                "monthly_payment": scenario.monthly_payment,
                "total_interest": scenario.total_interest,
                "apr": scenario.apr,
                "profit_margin": scenario.profit_margin,
                "confidence_score": scenario.confidence_score
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "定价方案优化完成",
                "data": {
                    "scenarios": scenarios_data,
                    "recommended": scenarios_data[0] if scenarios_data else None
                }
            }
        )
        
    except Exception as e:
        logger.error(f"定价方案优化失败: {e}")
        raise HTTPException(status_code=500, detail=f"定价方案优化失败: {str(e)}")

# 审批流程服务API
@app.post("/api/v1/approval/process")
async def process_approval(request: Dict[str, Any]):
    """处理贷款审批"""
    try:
        application_data = request.get("application_data", {})
        risk_assessment = request.get("risk_assessment", {})
        
        decision = approval_workflow_engine.process_application(application_data, risk_assessment)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "审批处理完成",
                "data": {
                    "decision_id": decision.decision_id,
                    "application_id": decision.application_id,
                    "status": decision.status.value,
                    "approval_level": decision.approval_level.value,
                    "decision_reason": decision.decision_reason,
                    "conditions": decision.conditions,
                    "risk_factors": decision.risk_factors,
                    "approval_amount": decision.approval_amount,
                    "approved_term": decision.approved_term,
                    "special_conditions": decision.special_conditions,
                    "decision_timestamp": decision.decision_timestamp.isoformat(),
                    "decision_officer": decision.decision_officer,
                    "confidence_score": decision.confidence_score
                }
            }
        )
        
    except Exception as e:
        logger.error(f"审批处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"审批处理失败: {str(e)}")

@app.get("/api/v1/approval/status/{application_id}")
async def get_approval_status(application_id: str):
    """获取审批状态"""
    try:
        decision = approval_workflow_engine.get_approval_status(application_id)
        
        if not decision:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "审批记录不存在"
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "审批状态获取成功",
                "data": {
                    "decision_id": decision.decision_id,
                    "status": decision.status.value,
                    "approval_level": decision.approval_level.value,
                    "decision_reason": decision.decision_reason,
                    "decision_timestamp": decision.decision_timestamp.isoformat(),
                    "decision_officer": decision.decision_officer
                }
            }
        )
        
    except Exception as e:
        logger.error(f"获取审批状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取审批状态失败: {str(e)}")

# 合规检查服务API
@app.post("/api/v1/compliance/check")
async def check_compliance(request: Dict[str, Any]):
    """执行合规检查"""
    try:
        application_data = request.get("application_data", {})
        risk_assessment = request.get("risk_assessment", {})
        
        compliance_report = compliance_checker.check_compliance(application_data, risk_assessment)
        
        checks_data = []
        for check in compliance_report.checks:
            checks_data.append({
                "rule_type": check.rule_type.value,
                "compliance_level": check.compliance_level.value,
                "is_compliant": check.is_compliant,
                "violation_details": check.violation_details,
                "risk_score": check.risk_score,
                "recommendations": check.recommendations
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "合规检查完成",
                "data": {
                    "report_id": compliance_report.report_id,
                    "application_id": compliance_report.application_id,
                    "overall_compliance_score": compliance_report.overall_compliance_score,
                    "compliance_level": compliance_report.compliance_level.value,
                    "checks": checks_data,
                    "critical_violations": compliance_report.critical_violations,
                    "recommendations": compliance_report.recommendations,
                    "report_timestamp": compliance_report.report_timestamp.isoformat(),
                    "requires_manual_review": compliance_report.requires_manual_review
                }
            }
        )
        
    except Exception as e:
        logger.error(f"合规检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"合规检查失败: {str(e)}")

# 第三方服务集成API
@app.post("/api/v1/third-party/credit-report")
async def get_credit_report(request: Dict[str, Any]):
    """获取征信报告"""
    try:
        user_id = request.get("user_id")
        id_number = request.get("id_number")
        
        if not user_id or not id_number:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        response = await third_party_integrator.get_credit_report(user_id, id_number)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": response.success,
                "message": "征信报告获取完成",
                "data": {
                    "service_name": response.service_name,
                    "data": response.data,
                    "response_time": response.response_time,
                    "timestamp": response.timestamp.isoformat(),
                    "request_id": response.request_id
                }
            }
        )
        
    except Exception as e:
        logger.error(f"征信报告获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"征信报告获取失败: {str(e)}")

@app.post("/api/v1/third-party/verify-identity")
async def verify_identity(request: Dict[str, Any]):
    """身份验证"""
    try:
        id_number = request.get("id_number")
        name = request.get("name")
        phone = request.get("phone")
        
        if not all([id_number, name, phone]):
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        response = await third_party_integrator.verify_identity(id_number, name, phone)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": response.success,
                "message": "身份验证完成",
                "data": {
                    "service_name": response.service_name,
                    "data": response.data,
                    "response_time": response.response_time,
                    "timestamp": response.timestamp.isoformat(),
                    "request_id": response.request_id
                }
            }
        )
        
    except Exception as e:
        logger.error(f"身份验证失败: {e}")
        raise HTTPException(status_code=500, detail=f"身份验证失败: {str(e)}")

@app.get("/api/v1/third-party/service-status")
async def get_service_status():
    """获取第三方服务状态"""
    try:
        status_info = await third_party_integrator.get_service_status()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "服务状态获取成功",
                "data": status_info
            }
        )
        
    except Exception as e:
        logger.error(f"服务状态获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"服务状态获取失败: {str(e)}")

# 数据同步API
@app.post("/api/v1/sync/add-task")
async def add_sync_task(request: Dict[str, Any]):
    """添加同步任务"""
    try:
        from services.data_sync_manager import DataSource, SyncType
        
        source = DataSource(request.get("source", "database"))
        target = DataSource(request.get("target", "cache"))
        sync_type = SyncType(request.get("sync_type", "real_time"))
        data_key = request.get("data_key")
        data = request.get("data", {})
        priority = request.get("priority", 1)
        
        if not data_key:
            raise HTTPException(status_code=400, detail="缺少data_key参数")
        
        task_id = await data_sync_manager.add_sync_task(
            source, target, sync_type, data_key, data, priority
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "同步任务添加成功",
                "data": {"task_id": task_id}
            }
        )
        
    except Exception as e:
        logger.error(f"同步任务添加失败: {e}")
        raise HTTPException(status_code=500, detail=f"同步任务添加失败: {str(e)}")

@app.get("/api/v1/sync/status")
async def get_sync_status():
    """获取同步状态"""
    try:
        status_info = await data_sync_manager.get_sync_status()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "同步状态获取成功",
                "data": status_info
            }
        )
        
    except Exception as e:
        logger.error(f"同步状态获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"同步状态获取失败: {str(e)}")

@app.get("/api/v1/sync/task/{task_id}")
async def get_task_details(task_id: str):
    """获取任务详情"""
    try:
        task_details = await data_sync_manager.get_task_details(task_id)
        
        if not task_details:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "任务不存在"
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "任务详情获取成功",
                "data": task_details
            }
        )
        
    except Exception as e:
        logger.error(f"任务详情获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"任务详情获取失败: {str(e)}")

# API稳定性API
@app.get("/api/v1/stability/metrics")
async def get_stability_metrics():
    """获取API稳定性指标"""
    try:
        metrics = api_stability_manager.get_all_metrics()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "稳定性指标获取成功",
                "data": metrics
            }
        )
        
    except Exception as e:
        logger.error(f"稳定性指标获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"稳定性指标获取失败: {str(e)}")

@app.get("/api/v1/stability/health")
async def get_stability_health():
    """获取API稳定性健康状态"""
    try:
        health_info = api_stability_manager.health_check()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "稳定性健康检查完成",
                "data": health_info
            }
        )
        
    except Exception as e:
        logger.error(f"稳定性健康检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"稳定性健康检查失败: {str(e)}")

# 监控系统API
@app.get("/api/v1/monitoring/system-status")
async def get_system_status():
    """获取系统状态"""
    try:
        status_info = system_monitor.get_system_status()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "系统状态获取成功",
                "data": status_info
            }
        )
        
    except Exception as e:
        logger.error(f"系统状态获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"系统状态获取失败: {str(e)}")

@app.get("/api/v1/monitoring/metrics")
async def get_monitoring_metrics():
    """获取监控指标"""
    try:
        metrics_summary = system_monitor.get_metrics_summary()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "监控指标获取成功",
                "data": metrics_summary
            }
        )
        
    except Exception as e:
        logger.error(f"监控指标获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"监控指标获取失败: {str(e)}")

@app.get("/api/v1/monitoring/alerts")
async def get_monitoring_alerts():
    """获取监控告警"""
    try:
        alert_summary = system_monitor.get_alert_summary()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "监控告警获取成功",
                "data": alert_summary
            }
        )
        
    except Exception as e:
        logger.error(f"监控告警获取失败: {e}")
        raise HTTPException(status_code=500, detail=f"监控告警获取失败: {str(e)}")

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
        
        response_data = AIResponse(
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
        
        return response_data
        
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
        elif search_type == "simple":
            results = await vector_rag_service.search_knowledge_simple(
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

# 性能优化API
@app.get("/api/v1/performance/summary")
async def get_performance_summary():
    """获取性能摘要"""
    try:
        summary = await performance_optimizer.get_performance_summary()
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "性能摘要获取成功",
                "data": summary
            }
        )
    except Exception as e:
        logger.error(f"获取性能摘要失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取性能摘要失败: {str(e)}")

@app.post("/api/v1/performance/optimize")
async def optimize_performance():
    """执行性能优化"""
    try:
        await performance_optimizer.optimize_performance()
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "性能优化完成"
            }
        )
    except Exception as e:
        logger.error(f"性能优化失败: {e}")
        raise HTTPException(status_code=500, detail=f"性能优化失败: {str(e)}")

@app.get("/api/v1/performance/cache/stats")
async def get_cache_stats():
    """获取缓存统计"""
    try:
        stats = performance_optimizer.cache_manager.get_stats()
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "缓存统计获取成功",
                "data": stats
            }
        )
    except Exception as e:
        logger.error(f"获取缓存统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取缓存统计失败: {str(e)}")

@app.post("/api/v1/performance/cache/clear")
async def clear_cache():
    """清空缓存"""
    try:
        await performance_optimizer.cache_manager.clear()
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "缓存清空成功"
            }
        )
    except Exception as e:
        logger.error(f"清空缓存失败: {e}")
        raise HTTPException(status_code=500, detail=f"清空缓存失败: {str(e)}")

# 高级OCR API
@app.post("/api/v1/ocr/recognize")
async def recognize_text(request: Dict[str, Any]):
    """OCR文字识别"""
    try:
        image_path = request.get("image_path")
        engines = request.get("engines", ["paddleocr", "tesseract"])
        language = request.get("language", "chi_sim+eng")
        
        if not image_path or not os.path.exists(image_path):
            raise HTTPException(status_code=400, detail="图片路径无效")
        
        # 转换引擎名称
        ocr_engines = []
        for engine in engines:
            if engine == "paddleocr":
                ocr_engines.append(OCREngine.PADDLEOCR)
            elif engine == "tesseract":
                ocr_engines.append(OCREngine.TESSERACT)
            elif engine == "baidu":
                ocr_engines.append(OCREngine.BAIDU)
        
        # 执行OCR识别
        results = await advanced_ocr_service.recognize_text(
            image_path, 
            ocr_engines, 
            language
        )
        
        # 获取最佳结果
        best_result = await advanced_ocr_service.get_best_result(results)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "OCR识别完成",
                "data": {
                    "text": best_result.text if best_result else "",
                    "confidence": best_result.confidence if best_result else 0.0,
                    "engine": best_result.engine if best_result else "none",
                    "processing_time": best_result.processing_time if best_result else 0.0,
                    "all_results": [
                        {
                            "text": result.text,
                            "confidence": result.confidence,
                            "engine": result.engine,
                            "processing_time": result.processing_time
                        }
                        for result in results
                    ]
                }
            }
        )
        
    except Exception as e:
        logger.error(f"OCR识别失败: {e}")
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
