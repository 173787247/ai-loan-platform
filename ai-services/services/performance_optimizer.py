#!/usr/bin/env python3
"""
性能优化服务
提供缓存、连接池、异步处理等性能优化功能
"""

import asyncio
import time
import psutil
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from functools import wraps
import weakref

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """性能指标"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read: int
    disk_io_write: int
    network_sent: int
    network_recv: int
    active_connections: int
    response_time_avg: float
    error_rate: float

class ConnectionPoolManager:
    """连接池管理器"""
    
    def __init__(self):
        self.pools = {}
        self.metrics = {}
    
    async def create_pool(self, name: str, pool_config: Dict[str, Any]):
        """创建连接池"""
        try:
            import asyncpg
            
            pool = await asyncpg.create_pool(
                **pool_config,
                min_size=pool_config.get('min_size', 5),
                max_size=pool_config.get('max_size', 20),
                max_queries=pool_config.get('max_queries', 50000),
                max_inactive_connection_lifetime=pool_config.get('max_inactive_connection_lifetime', 300.0),
                command_timeout=pool_config.get('command_timeout', 60),
                server_settings={
                    'jit': 'off',
                    'application_name': f'ai_loan_{name}'
                }
            )
            
            self.pools[name] = pool
            self.metrics[name] = {
                'created_at': datetime.now(),
                'total_connections': 0,
                'active_connections': 0,
                'idle_connections': 0,
                'total_queries': 0,
                'failed_queries': 0
            }
            
            logger.info(f"连接池 {name} 创建成功")
            return pool
            
        except Exception as e:
            logger.error(f"创建连接池 {name} 失败: {e}")
            raise
    
    async def get_pool(self, name: str) -> Optional[Any]:
        """获取连接池"""
        return self.pools.get(name)
    
    async def close_pool(self, name: str):
        """关闭连接池"""
        if name in self.pools:
            await self.pools[name].close()
            del self.pools[name]
            logger.info(f"连接池 {name} 已关闭")
    
    async def get_pool_status(self, name: str) -> Dict[str, Any]:
        """获取连接池状态"""
        if name not in self.pools:
            return {"status": "not_found"}
        
        pool = self.pools[name]
        metrics = self.metrics[name]
        
        return {
            "status": "active",
            "size": pool.get_size(),
            "min_size": pool.get_min_size(),
            "max_size": pool.get_max_size(),
            "idle_size": pool.get_idle_size(),
            "metrics": metrics
        }

class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.cache = {}
        self.ttl = {}
        self.access_count = {}
        self.max_size = 1000
        self.cleanup_interval = 300  # 5分钟清理一次
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key not in self.cache:
            return None
        
        # 检查TTL
        if key in self.ttl and datetime.now() > self.ttl[key]:
            await self.delete(key)
            return None
        
        # 更新访问计数
        self.access_count[key] = self.access_count.get(key, 0) + 1
        
        return self.cache[key]
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """设置缓存"""
        # 检查缓存大小
        if len(self.cache) >= self.max_size:
            await self._evict_least_used()
        
        self.cache[key] = value
        self.ttl[key] = datetime.now() + timedelta(seconds=ttl)
        self.access_count[key] = 0
    
    async def delete(self, key: str):
        """删除缓存"""
        self.cache.pop(key, None)
        self.ttl.pop(key, None)
        self.access_count.pop(key, None)
    
    async def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.ttl.clear()
        self.access_count.clear()
    
    async def _evict_least_used(self):
        """淘汰最少使用的缓存项"""
        if not self.access_count:
            return
        
        # 找到访问次数最少的项
        least_used_key = min(self.access_count.keys(), key=lambda k: self.access_count[k])
        await self.delete(least_used_key)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": sum(self.access_count.values()) / max(len(self.cache), 1),
            "keys": list(self.cache.keys())[:10]  # 显示前10个键
        }

class AsyncTaskManager:
    """异步任务管理器"""
    
    def __init__(self):
        self.tasks = {}
        self.task_metrics = {}
    
    async def submit_task(self, task_id: str, coro, priority: int = 1):
        """提交异步任务"""
        try:
            task = asyncio.create_task(coro)
            self.tasks[task_id] = {
                'task': task,
                'priority': priority,
                'created_at': datetime.now(),
                'status': 'running'
            }
            
            # 监控任务完成
            asyncio.create_task(self._monitor_task(task_id, task))
            
            return task
            
        except Exception as e:
            logger.error(f"提交任务 {task_id} 失败: {e}")
            raise
    
    async def _monitor_task(self, task_id: str, task):
        """监控任务状态"""
        try:
            await task
            self.tasks[task_id]['status'] = 'completed'
            self.tasks[task_id]['completed_at'] = datetime.now()
        except Exception as e:
            self.tasks[task_id]['status'] = 'failed'
            self.tasks[task_id]['error'] = str(e)
            logger.error(f"任务 {task_id} 执行失败: {e}")
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        if task_id not in self.tasks:
            return {"status": "not_found"}
        
        task_info = self.tasks[task_id]
        return {
            "status": task_info['status'],
            "priority": task_info['priority'],
            "created_at": task_info['created_at'].isoformat(),
            "completed_at": task_info.get('completed_at', '').isoformat() if task_info.get('completed_at') else None,
            "error": task_info.get('error')
        }
    
    async def cancel_task(self, task_id: str):
        """取消任务"""
        if task_id in self.tasks:
            self.tasks[task_id]['task'].cancel()
            self.tasks[task_id]['status'] = 'cancelled'

class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        self.connection_pool_manager = ConnectionPoolManager()
        self.cache_manager = CacheManager()
        self.task_manager = AsyncTaskManager()
        self.metrics_history = []
        self.max_history = 1000
        self._monitor_task = None
    
    async def initialize(self):
        """初始化性能优化器"""
        if self._monitor_task is None:
            self._monitor_task = asyncio.create_task(self._monitor_performance())
            logger.info("性能监控已启动")
    
    async def _monitor_performance(self):
        """性能监控循环"""
        while True:
            try:
                metrics = await self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # 保持历史记录在限制范围内
                if len(self.metrics_history) > self.max_history:
                    self.metrics_history = self.metrics_history[-self.max_history:]
                
                # 检查性能告警
                await self._check_performance_alerts(metrics)
                
                await asyncio.sleep(60)  # 每分钟收集一次
                
            except Exception as e:
                logger.error(f"性能监控异常: {e}")
                await asyncio.sleep(60)
    
    async def _collect_metrics(self) -> PerformanceMetrics:
        """收集性能指标"""
        try:
            # 系统指标
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            
            # 连接池指标
            active_connections = 0
            for pool_name in self.connection_pool_manager.pools:
                pool_status = await self.connection_pool_manager.get_pool_status(pool_name)
                active_connections += pool_status.get('idle_size', 0)
            
            # 响应时间（简化计算）
            response_time_avg = 0.0
            if self.metrics_history:
                recent_metrics = self.metrics_history[-10:]  # 最近10次
                response_times = [m.response_time_avg for m in recent_metrics if m.response_time_avg > 0]
                response_time_avg = sum(response_times) / len(response_times) if response_times else 0.0
            
            # 错误率（简化计算）
            error_rate = 0.0
            
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / 1024 / 1024,
                disk_io_read=disk_io.read_bytes if disk_io else 0,
                disk_io_write=disk_io.write_bytes if disk_io else 0,
                network_sent=network_io.bytes_sent if network_io else 0,
                network_recv=network_io.bytes_recv if network_io else 0,
                active_connections=active_connections,
                response_time_avg=response_time_avg,
                error_rate=error_rate
            )
            
        except Exception as e:
            logger.error(f"收集性能指标失败: {e}")
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                disk_io_read=0,
                disk_io_write=0,
                network_sent=0,
                network_recv=0,
                active_connections=0,
                response_time_avg=0.0,
                error_rate=0.0
            )
    
    async def _check_performance_alerts(self, metrics: PerformanceMetrics):
        """检查性能告警"""
        alerts = []
        
        # CPU使用率告警
        if metrics.cpu_percent > 80:
            alerts.append(f"CPU使用率过高: {metrics.cpu_percent:.1f}%")
        
        # 内存使用率告警
        if metrics.memory_percent > 85:
            alerts.append(f"内存使用率过高: {metrics.memory_percent:.1f}%")
        
        # 响应时间告警
        if metrics.response_time_avg > 5.0:
            alerts.append(f"平均响应时间过长: {metrics.response_time_avg:.2f}秒")
        
        # 错误率告警
        if metrics.error_rate > 0.05:
            alerts.append(f"错误率过高: {metrics.error_rate:.2%}")
        
        if alerts:
            logger.warning(f"性能告警: {'; '.join(alerts)}")
    
    def performance_decorator(self, operation_name: str):
        """性能监控装饰器"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    logger.info(f"{operation_name} 执行时间: {execution_time:.3f}秒")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"{operation_name} 执行失败 (耗时: {execution_time:.3f}秒): {e}")
                    raise
            return async_wrapper
        return decorator
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        if not self.metrics_history:
            return {"status": "no_data"}
        
        latest_metrics = self.metrics_history[-1]
        recent_metrics = self.metrics_history[-10:] if len(self.metrics_history) >= 10 else self.metrics_history
        
        # 计算趋势
        cpu_trend = self._calculate_trend([m.cpu_percent for m in recent_metrics])
        memory_trend = self._calculate_trend([m.memory_percent for m in recent_metrics])
        
        return {
            "current": {
                "cpu_percent": latest_metrics.cpu_percent,
                "memory_percent": latest_metrics.memory_percent,
                "memory_used_mb": latest_metrics.memory_used_mb,
                "active_connections": latest_metrics.active_connections,
                "response_time_avg": latest_metrics.response_time_avg,
                "error_rate": latest_metrics.error_rate
            },
            "trends": {
                "cpu_trend": cpu_trend,
                "memory_trend": memory_trend
            },
            "cache_stats": self.cache_manager.get_stats(),
            "pools": {
                name: await self.connection_pool_manager.get_pool_status(name)
                for name in self.connection_pool_manager.pools
            },
            "timestamp": latest_metrics.timestamp.isoformat()
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """计算趋势"""
        if len(values) < 2:
            return "stable"
        
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            return "increasing"
        elif second_avg < first_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    async def optimize_performance(self):
        """执行性能优化"""
        try:
            # 清理过期缓存
            await self.cache_manager.clear()
            
            # 优化连接池
            for pool_name in self.connection_pool_manager.pools:
                pool_status = await self.connection_pool_manager.get_pool_status(pool_name)
                if pool_status.get('idle_size', 0) > pool_status.get('size', 0) * 0.5:
                    logger.info(f"连接池 {pool_name} 空闲连接过多，考虑减少池大小")
            
            logger.info("性能优化完成")
            
        except Exception as e:
            logger.error(f"性能优化失败: {e}")

# 全局实例
performance_optimizer = PerformanceOptimizer()
