"""
API稳定性管理器
提供重试机制、熔断器、限流等稳定性保障
"""

import asyncio
import time
import json
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid
import threading
from collections import defaultdict, deque

class CircuitState(Enum):
    """熔断器状态"""
    CLOSED = "closed"      # 正常状态
    OPEN = "open"          # 熔断状态
    HALF_OPEN = "half_open"  # 半开状态

class RateLimitType(Enum):
    """限流类型"""
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"

@dataclass
class CircuitBreakerConfig:
    """熔断器配置"""
    failure_threshold: int = 5      # 失败阈值
    success_threshold: int = 3      # 成功阈值
    timeout: int = 60               # 熔断超时时间（秒）
    half_open_max_calls: int = 3    # 半开状态最大调用数

@dataclass
class RateLimitConfig:
    """限流配置"""
    limit_type: RateLimitType = RateLimitType.SLIDING_WINDOW
    max_requests: int = 100         # 最大请求数
    window_size: int = 60           # 时间窗口（秒）
    burst_size: int = 10            # 突发请求数
    refill_rate: float = 1.0        # 补充速率

@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 3            # 最大重试次数
    base_delay: float = 1.0         # 基础延迟（秒）
    max_delay: float = 60.0         # 最大延迟（秒）
    exponential_base: float = 2.0   # 指数退避基数
    jitter: bool = True             # 是否添加抖动

@dataclass
class APICallMetrics:
    """API调用指标"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    retry_calls: int = 0
    circuit_breaker_trips: int = 0
    rate_limit_hits: int = 0
    average_response_time: float = 0.0
    last_call_time: Optional[datetime] = None

class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        self.lock = threading.Lock()
    
    def can_execute(self) -> bool:
        """检查是否可以执行"""
        with self.lock:
            if self.state == CircuitState.CLOSED:
                return True
            elif self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    return True
                return False
            elif self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls < self.config.half_open_max_calls:
                    self.half_open_calls += 1
                    return True
                return False
            return False
    
    def record_success(self):
        """记录成功"""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
                    logger.info(f"熔断器 {self.name} 恢复正常")
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0
    
    def record_failure(self):
        """记录失败"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.state == CircuitState.CLOSED:
                if self.failure_count >= self.config.failure_threshold:
                    self.state = CircuitState.OPEN
                    logger.warning(f"熔断器 {self.name} 触发熔断")
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                logger.warning(f"熔断器 {self.name} 重新熔断")
    
    def _should_attempt_reset(self) -> bool:
        """检查是否应该尝试重置"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = (datetime.now() - self.last_failure_time).total_seconds()
        return time_since_failure >= self.config.timeout
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        with self.lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
                "half_open_calls": self.half_open_calls
            }

class RateLimiter:
    """限流器"""
    
    def __init__(self, name: str, config: RateLimitConfig):
        self.name = name
        self.config = config
        self.requests = deque()
        self.tokens = config.burst_size
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def is_allowed(self) -> bool:
        """检查是否允许请求"""
        with self.lock:
            current_time = time.time()
            
            if self.config.limit_type == RateLimitType.SLIDING_WINDOW:
                return self._sliding_window_check(current_time)
            elif self.config.limit_type == RateLimitType.TOKEN_BUCKET:
                return self._token_bucket_check(current_time)
            elif self.config.limit_type == RateLimitType.FIXED_WINDOW:
                return self._fixed_window_check(current_time)
            else:
                return True
    
    def _sliding_window_check(self, current_time: float) -> bool:
        """滑动窗口检查"""
        # 移除过期请求
        while self.requests and self.requests[0] <= current_time - self.config.window_size:
            self.requests.popleft()
        
        # 检查是否超过限制
        if len(self.requests) < self.config.max_requests:
            self.requests.append(current_time)
            return True
        
        return False
    
    def _token_bucket_check(self, current_time: float) -> bool:
        """令牌桶检查"""
        # 补充令牌
        time_passed = current_time - self.last_refill
        tokens_to_add = time_passed * self.config.refill_rate
        self.tokens = min(self.config.burst_size, self.tokens + tokens_to_add)
        self.last_refill = current_time
        
        # 检查是否有可用令牌
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        
        return False
    
    def _fixed_window_check(self, current_time: float) -> bool:
        """固定窗口检查"""
        window_start = int(current_time // self.config.window_size) * self.config.window_size
        
        # 清理过期窗口
        while self.requests and self.requests[0] < window_start:
            self.requests.popleft()
        
        # 检查是否超过限制
        if len(self.requests) < self.config.max_requests:
            self.requests.append(current_time)
            return True
        
        return False
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        with self.lock:
            return {
                "name": self.name,
                "limit_type": self.config.limit_type.value,
                "max_requests": self.config.max_requests,
                "window_size": self.config.window_size,
                "current_requests": len(self.requests),
                "tokens": self.tokens if self.config.limit_type == RateLimitType.TOKEN_BUCKET else None
            }

class RetryManager:
    """重试管理器"""
    
    def __init__(self, config: RetryConfig):
        self.config = config
    
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """带重试的执行"""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(f"重试成功，尝试次数: {attempt + 1}")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                if attempt < self.config.max_retries:
                    delay = self._calculate_delay(attempt)
                    logger.warning(f"执行失败，{delay:.2f}秒后重试 (尝试 {attempt + 1}/{self.config.max_retries + 1}): {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"重试失败，已达到最大重试次数: {e}")
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """计算延迟时间"""
        delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        delay = min(delay, self.config.max_delay)
        
        if self.config.jitter:
            # 添加随机抖动
            import random
            delay *= (0.5 + random.random() * 0.5)
        
        return delay

class APIStabilityManager:
    """API稳定性管理器"""
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.retry_manager = RetryManager(RetryConfig())
        self.metrics: Dict[str, APICallMetrics] = defaultdict(APICallMetrics)
        self.lock = threading.Lock()
    
    def add_circuit_breaker(self, name: str, config: CircuitBreakerConfig):
        """添加熔断器"""
        self.circuit_breakers[name] = CircuitBreaker(name, config)
        logger.info(f"熔断器已添加: {name}")
    
    def add_rate_limiter(self, name: str, config: RateLimitConfig):
        """添加限流器"""
        self.rate_limiters[name] = RateLimiter(name, config)
        logger.info(f"限流器已添加: {name}")
    
    async def execute_with_stability(self, api_name: str, func: Callable, 
                                   *args, **kwargs) -> Any:
        """带稳定性保障的执行"""
        start_time = time.time()
        
        # 更新指标
        with self.lock:
            metrics = self.metrics[api_name]
            metrics.total_calls += 1
            metrics.last_call_time = datetime.now()
        
        try:
            # 检查熔断器
            circuit_breaker = self.circuit_breakers.get(api_name)
            if circuit_breaker and not circuit_breaker.can_execute():
                with self.lock:
                    metrics.circuit_breaker_trips += 1
                raise Exception(f"熔断器 {api_name} 处于熔断状态")
            
            # 检查限流器
            rate_limiter = self.rate_limiters.get(api_name)
            if rate_limiter and not rate_limiter.is_allowed():
                with self.lock:
                    metrics.rate_limit_hits += 1
                raise Exception(f"限流器 {api_name} 触发限流")
            
            # 执行函数（带重试）
            result = await self.retry_manager.execute_with_retry(func, *args, **kwargs)
            
            # 记录成功
            if circuit_breaker:
                circuit_breaker.record_success()
            
            with self.lock:
                metrics.successful_calls += 1
            
            return result
            
        except Exception as e:
            # 记录失败
            if circuit_breaker:
                circuit_breaker.record_failure()
            
            with self.lock:
                metrics.failed_calls += 1
            
            raise e
        
        finally:
            # 更新响应时间
            response_time = time.time() - start_time
            with self.lock:
                metrics.average_response_time = (
                    (metrics.average_response_time * (metrics.total_calls - 1) + response_time) 
                    / metrics.total_calls
                )
    
    def get_circuit_breaker_state(self, name: str) -> Optional[Dict[str, Any]]:
        """获取熔断器状态"""
        circuit_breaker = self.circuit_breakers.get(name)
        return circuit_breaker.get_state() if circuit_breaker else None
    
    def get_rate_limiter_state(self, name: str) -> Optional[Dict[str, Any]]:
        """获取限流器状态"""
        rate_limiter = self.rate_limiters.get(name)
        return rate_limiter.get_state() if rate_limiter else None
    
    def get_api_metrics(self, api_name: str) -> Dict[str, Any]:
        """获取API指标"""
        with self.lock:
            metrics = self.metrics[api_name]
            return {
                "api_name": api_name,
                "total_calls": metrics.total_calls,
                "successful_calls": metrics.successful_calls,
                "failed_calls": metrics.failed_calls,
                "retry_calls": metrics.retry_calls,
                "circuit_breaker_trips": metrics.circuit_breaker_trips,
                "rate_limit_hits": metrics.rate_limit_hits,
                "average_response_time": metrics.average_response_time,
                "success_rate": metrics.successful_calls / metrics.total_calls if metrics.total_calls > 0 else 0,
                "last_call_time": metrics.last_call_time.isoformat() if metrics.last_call_time else None
            }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """获取所有指标"""
        with self.lock:
            return {
                "circuit_breakers": {name: cb.get_state() for name, cb in self.circuit_breakers.items()},
                "rate_limiters": {name: rl.get_state() for name, rl in self.rate_limiters.items()},
                "api_metrics": {name: self.get_api_metrics(name) for name in self.metrics.keys()},
                "total_apis": len(self.metrics),
                "total_circuit_breakers": len(self.circuit_breakers),
                "total_rate_limiters": len(self.rate_limiters)
            }
    
    def reset_metrics(self, api_name: Optional[str] = None):
        """重置指标"""
        with self.lock:
            if api_name:
                if api_name in self.metrics:
                    self.metrics[api_name] = APICallMetrics()
                    logger.info(f"API {api_name} 指标已重置")
            else:
                self.metrics.clear()
                logger.info("所有API指标已重置")
    
    def update_circuit_breaker_config(self, name: str, config_updates: Dict[str, Any]):
        """更新熔断器配置"""
        if name in self.circuit_breakers:
            circuit_breaker = self.circuit_breakers[name]
            for key, value in config_updates.items():
                if hasattr(circuit_breaker.config, key):
                    setattr(circuit_breaker.config, key, value)
            logger.info(f"熔断器 {name} 配置已更新")
    
    def update_rate_limiter_config(self, name: str, config_updates: Dict[str, Any]):
        """更新限流器配置"""
        if name in self.rate_limiters:
            rate_limiter = self.rate_limiters[name]
            for key, value in config_updates.items():
                if hasattr(rate_limiter.config, key):
                    setattr(rate_limiter.config, key, value)
            logger.info(f"限流器 {name} 配置已更新")
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        healthy_breakers = sum(1 for cb in self.circuit_breakers.values() if cb.state == CircuitState.CLOSED)
        total_breakers = len(self.circuit_breakers)
        
        healthy_limiters = sum(1 for rl in self.rate_limiters.values() if rl.is_allowed())
        total_limiters = len(self.rate_limiters)
        
        return {
            "status": "healthy" if healthy_breakers == total_breakers else "degraded",
            "circuit_breakers": {
                "total": total_breakers,
                "healthy": healthy_breakers,
                "open": total_breakers - healthy_breakers
            },
            "rate_limiters": {
                "total": total_limiters,
                "healthy": healthy_limiters,
                "limited": total_limiters - healthy_limiters
            },
            "timestamp": datetime.now().isoformat()
        }

# 全局实例
api_stability_manager = APIStabilityManager()
