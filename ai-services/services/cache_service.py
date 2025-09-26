"""
缓存服务
使用Redis实现API响应缓存和会话缓存
"""

import json
import pickle
import time
from typing import Any, Optional, Union
from loguru import logger
import os
from datetime import datetime, timedelta

# 尝试导入redis，如果失败则使用内存缓存
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis未安装，将使用内存缓存")

class CacheService:
    """缓存服务"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}  # 内存缓存作为后备
        self.cache_prefix = "ai_loan:"
        self.default_ttl = 3600  # 默认1小时过期
        
    async def initialize(self):
        """初始化缓存连接"""
        if not REDIS_AVAILABLE:
            logger.info("使用内存缓存服务")
            return
            
        try:
            redis_host = os.getenv("REDIS_HOST", "ai-loan-redis")
            redis_port = int(os.getenv("REDIS_PORT", "6379"))
            redis_db = int(os.getenv("REDIS_DB", "0"))
            redis_password = os.getenv("REDIS_PASSWORD", "")
            
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                password=redis_password if redis_password else None,
                decode_responses=False,  # 使用二进制模式以支持pickle
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # 测试连接
            self.redis_client.ping()
            logger.info("Redis缓存服务初始化成功")
            
        except Exception as e:
            logger.error(f"Redis缓存服务初始化失败: {e}")
            logger.info("回退到内存缓存")
            self.redis_client = None
    
    def _get_key(self, key: str) -> str:
        """生成带前缀的缓存键"""
        return f"{self.cache_prefix}{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        # 如果Redis不可用，使用内存缓存
        if not self.redis_client:
            cache_key = self._get_key(key)
            if cache_key in self.memory_cache:
                cache_data = self.memory_cache[cache_key]
                # 检查是否过期
                if cache_data['expires_at'] > time.time():
                    return cache_data['value']
                else:
                    # 过期则删除
                    del self.memory_cache[cache_key]
            return None
            
        try:
            cache_key = self._get_key(key)
            data = self.redis_client.get(cache_key)
            
            if data is None:
                return None
                
            # 尝试JSON反序列化
            try:
                return json.loads(data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # 如果JSON失败，尝试pickle反序列化
                return pickle.loads(data)
                
        except Exception as e:
            logger.error(f"获取缓存失败 {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存数据"""
        cache_key = self._get_key(key)
        ttl = ttl or self.default_ttl
        
        # 如果Redis不可用，使用内存缓存
        if not self.redis_client:
            try:
                self.memory_cache[cache_key] = {
                    'value': value,
                    'expires_at': time.time() + ttl
                }
                return True
            except Exception as e:
                logger.error(f"设置内存缓存失败 {key}: {e}")
                return False
            
        try:
            # 优先使用JSON序列化
            try:
                data = json.dumps(value, ensure_ascii=False).encode('utf-8')
            except (TypeError, ValueError):
                # 如果JSON失败，使用pickle序列化
                data = pickle.dumps(value)
            
            result = self.redis_client.setex(cache_key, ttl, data)
            return bool(result)
            
        except Exception as e:
            logger.error(f"设置缓存失败 {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存数据"""
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._get_key(key)
            result = self.redis_client.delete(cache_key)
            return bool(result)
        except Exception as e:
            logger.error(f"删除缓存失败 {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._get_key(key)
            return bool(self.redis_client.exists(cache_key))
        except Exception as e:
            logger.error(f"检查缓存存在失败 {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """清除匹配模式的缓存"""
        if not self.redis_client:
            return 0
            
        try:
            cache_pattern = self._get_key(pattern)
            keys = self.redis_client.keys(cache_pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"清除缓存模式失败 {pattern}: {e}")
            return 0
    
    async def get_stats(self) -> dict:
        """获取缓存统计信息"""
        if not self.redis_client:
            return {"status": "disconnected"}
            
        try:
            info = self.redis_client.info()
            return {
                "status": "connected",
                "used_memory": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            logger.error(f"获取缓存统计失败: {e}")
            return {"status": "error", "error": str(e)}

# 全局缓存服务实例
cache_service = CacheService()
