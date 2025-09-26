"""
统一错误处理中间件
"""

import traceback
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Union
import time

class ErrorHandler:
    """错误处理器"""
    
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        """HTTP异常处理器"""
        logger.warning(f"HTTP异常: {exc.status_code} - {exc.detail} - {request.url}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "type": "HTTPException",
                    "code": exc.status_code,
                    "message": exc.detail,
                    "timestamp": time.time()
                }
            }
        )
    
    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        """通用异常处理器"""
        error_id = f"ERR_{int(time.time())}"
        logger.error(f"未处理异常 [{error_id}]: {str(exc)}")
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": "InternalServerError",
                    "code": 500,
                    "message": "服务器内部错误",
                    "error_id": error_id,
                    "timestamp": time.time()
                }
            }
        )
    
    @staticmethod
    async def validation_exception_handler(request: Request, exc: Exception):
        """验证异常处理器"""
        logger.warning(f"验证异常: {str(exc)} - {request.url}")
        
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "type": "ValidationError",
                    "code": 422,
                    "message": "请求参数验证失败",
                    "details": str(exc),
                    "timestamp": time.time()
                }
            }
        )
    
    @staticmethod
    def setup_error_handlers(app):
        """设置错误处理器"""
        app.add_exception_handler(HTTPException, ErrorHandler.http_exception_handler)
        app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)
        
        # 添加验证异常处理器（如果使用Pydantic）
        try:
            from pydantic import ValidationError
            app.add_exception_handler(ValidationError, ErrorHandler.validation_exception_handler)
        except ImportError:
            pass
        
        logger.info("错误处理器设置完成")

class PerformanceMiddleware:
    """性能监控中间件"""
    
    @staticmethod
    async def performance_middleware(request: Request, call_next):
        """性能监控中间件"""
        start_time = time.time()
        
        # 记录请求开始
        logger.info(f"请求开始: {request.method} {request.url}")
        
        try:
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录请求完成
            logger.info(f"请求完成: {request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
            
            # 添加性能头
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"请求失败: {request.method} {request.url} - {str(e)} - {process_time:.3f}s")
            raise

class LoggingMiddleware:
    """日志中间件"""
    
    @staticmethod
    async def logging_middleware(request: Request, call_next):
        """日志中间件"""
        # 记录请求信息
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        logger.info(f"请求: {client_ip} - {request.method} {request.url} - {user_agent}")
        
        response = await call_next(request)
        
        # 记录响应信息
        logger.info(f"响应: {response.status_code} - {request.method} {request.url}")
        
        return response
