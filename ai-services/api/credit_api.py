"""
征信API端点
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import os
from loguru import logger

from services.credit_api_service import credit_api_service

router = APIRouter(prefix="/api/v1/credit", tags=["征信查询"])

class CreditQueryRequest(BaseModel):
    """征信查询请求"""
    company_name: str
    provider: Optional[str] = "jingdong"  # 默认使用京东万象

class CreditQueryResponse(BaseModel):
    """征信查询响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    provider: str
    quota_remaining: Optional[int] = None
    query_time: str

class UsageStatsResponse(BaseModel):
    """使用统计响应"""
    success: bool
    stats: Dict[str, Any]

@router.post("/query", response_model=CreditQueryResponse)
async def query_enterprise_credit(request: CreditQueryRequest):
    """查询企业信用评分"""
    try:
        logger.info(f"收到征信查询请求: {request.company_name}, 提供商: {request.provider}")
        
        # 调用征信API服务
        result = credit_api_service.query_enterprise_credit(
            company_name=request.company_name,
            provider=request.provider
        )
        
        if result.get('success'):
            # 成功查询
            return CreditQueryResponse(
                success=True,
                data=result.get('data', {}),
                provider=result.get('provider', request.provider),
                quota_remaining=result.get('quota_remaining'),
                query_time=result.get('query_time', '')
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
            
            return CreditQueryResponse(
                success=True,
                data={
                    'credit_score': mock_score,
                    'credit_level': mock_level,
                    'credit_source': mock_source,
                    'company_name': request.company_name,
                    'query_time': result.get('query_time', ''),
                    'is_mock': True
                },
                provider='mock',
                quota_remaining=None,
                query_time=result.get('query_time', '')
            )
            
    except Exception as e:
        logger.error(f"征信查询异常: {e}")
        raise HTTPException(status_code=500, detail=f"征信查询失败: {str(e)}")

@router.get("/stats", response_model=UsageStatsResponse)
async def get_usage_stats():
    """获取API使用统计"""
    try:
        stats = credit_api_service.get_usage_stats()
        return UsageStatsResponse(
            success=True,
            stats=stats
        )
    except Exception as e:
        logger.error(f"获取使用统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")

@router.post("/reset-stats")
async def reset_usage_stats(provider: Optional[str] = None):
    """重置使用统计"""
    try:
        credit_api_service.reset_usage_stats(provider)
        return {"success": True, "message": "统计已重置"}
    except Exception as e:
        logger.error(f"重置统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"重置失败: {str(e)}")

@router.get("/providers")
async def get_available_providers():
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
        
        return {
            "success": True,
            "providers": providers
        }
    except Exception as e:
        logger.error(f"获取提供商列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取提供商失败: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "credit-api",
        "timestamp": "2025-09-23T15:00:00Z"
    }
