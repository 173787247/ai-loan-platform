"""
数据同步管理器
提供实时数据同步和一致性保证
"""

import json
import asyncio
import redis
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib
import pickle
from concurrent.futures import ThreadPoolExecutor

class SyncStatus(Enum):
    """同步状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class SyncType(Enum):
    """同步类型"""
    REAL_TIME = "real_time"
    BATCH = "batch"
    INCREMENTAL = "incremental"
    FULL_SYNC = "full_sync"

class DataSource(Enum):
    """数据源"""
    DATABASE = "database"
    CACHE = "cache"
    EXTERNAL_API = "external_api"
    FILE_SYSTEM = "file_system"
    MESSAGE_QUEUE = "message_queue"

@dataclass
class SyncTask:
    """同步任务"""
    task_id: str
    source: DataSource
    target: DataSource
    sync_type: SyncType
    data_key: str
    data: Any
    status: SyncStatus
    retry_count: int
    max_retries: int
    created_at: datetime
    updated_at: datetime
    error_message: str
    priority: int

@dataclass
class SyncConfig:
    """同步配置"""
    source_config: Dict[str, Any]
    target_config: Dict[str, Any]
    sync_interval: int  # 秒
    batch_size: int
    retry_delay: int  # 秒
    max_retries: int
    enable_compression: bool
    enable_encryption: bool

class DataSyncManager:
    """数据同步管理器"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.sync_tasks: Dict[str, SyncTask] = {}
        self.sync_configs: Dict[str, SyncConfig] = {}
        self.sync_handlers: Dict[str, Callable] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.sync_queue = asyncio.Queue()
        self.is_running = False
        self._initialize_default_configs()
    
    def _initialize_default_configs(self):
        """初始化默认配置"""
        # 数据库到缓存同步
        self.sync_configs["db_to_cache"] = SyncConfig(
            source_config={"type": "postgresql", "host": "localhost", "port": 5432},
            target_config={"type": "redis", "host": "localhost", "port": 6379},
            sync_interval=5,
            batch_size=100,
            retry_delay=10,
            max_retries=3,
            enable_compression=True,
            enable_encryption=False
        )
        
        # 缓存到外部API同步
        self.sync_configs["cache_to_api"] = SyncConfig(
            source_config={"type": "redis", "host": "localhost", "port": 6379},
            target_config={"type": "http_api", "base_url": "https://api.example.com"},
            sync_interval=10,
            batch_size=50,
            retry_delay=15,
            max_retries=5,
            enable_compression=True,
            enable_encryption=True
        )
        
        # 实时数据同步
        self.sync_configs["real_time"] = SyncConfig(
            source_config={"type": "message_queue", "host": "localhost", "port": 5672},
            target_config={"type": "redis", "host": "localhost", "port": 6379},
            sync_interval=1,
            batch_size=10,
            retry_delay=5,
            max_retries=2,
            enable_compression=False,
            enable_encryption=False
        )
    
    async def initialize(self):
        """初始化同步管理器"""
        try:
            # 初始化Redis连接
            self.redis_client = redis.Redis(
                host="ai-loan-redis",
                port=6379,
                db=0,
                decode_responses=False,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # 测试连接
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self.redis_client.ping
            )
            
            # 注册默认同步处理器
            self._register_default_handlers()
            
            logger.info("数据同步管理器初始化完成")
            
        except Exception as e:
            logger.error(f"数据同步管理器初始化失败: {e}")
            raise
    
    def _register_default_handlers(self):
        """注册默认同步处理器"""
        self.sync_handlers["db_to_cache"] = self._sync_db_to_cache
        self.sync_handlers["cache_to_api"] = self._sync_cache_to_api
        self.sync_handlers["real_time"] = self._sync_real_time
        self.sync_handlers["incremental"] = self._sync_incremental
    
    async def start_sync_service(self):
        """启动同步服务"""
        if self.is_running:
            logger.warning("同步服务已在运行")
            return
        
        self.is_running = True
        logger.info("数据同步服务启动")
        
        # 启动同步任务处理循环
        asyncio.create_task(self._sync_loop())
        
        # 启动定期同步任务
        asyncio.create_task(self._periodic_sync())
    
    async def stop_sync_service(self):
        """停止同步服务"""
        self.is_running = False
        logger.info("数据同步服务停止")
    
    async def _sync_loop(self):
        """同步任务处理循环"""
        while self.is_running:
            try:
                # 从队列获取同步任务
                task = await asyncio.wait_for(self.sync_queue.get(), timeout=1.0)
                
                # 处理同步任务
                await self._process_sync_task(task)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"同步循环异常: {e}")
                await asyncio.sleep(1)
    
    async def _periodic_sync(self):
        """定期同步任务"""
        while self.is_running:
            try:
                # 检查需要定期同步的数据
                await self._check_periodic_sync()
                await asyncio.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                logger.error(f"定期同步异常: {e}")
                await asyncio.sleep(30)
    
    async def _check_periodic_sync(self):
        """检查定期同步"""
        for config_name, config in self.sync_configs.items():
            if config.sync_interval > 0:
                # 检查是否需要同步
                last_sync_key = f"last_sync:{config_name}"
                last_sync_time = await self._get_last_sync_time(last_sync_key)
                
                if last_sync_time:
                    time_since_sync = (datetime.now() - last_sync_time).total_seconds()
                    if time_since_sync >= config.sync_interval:
                        await self._trigger_sync(config_name, SyncType.BATCH)
    
    async def _get_last_sync_time(self, key: str) -> Optional[datetime]:
        """获取最后同步时间"""
        try:
            if self.redis_client:
                timestamp_str = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.get, key
                )
                if timestamp_str:
                    return datetime.fromisoformat(timestamp_str.decode())
        except Exception as e:
            logger.error(f"获取最后同步时间失败: {e}")
        return None
    
    async def _set_last_sync_time(self, key: str, timestamp: datetime):
        """设置最后同步时间"""
        try:
            if self.redis_client:
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.set, key, timestamp.isoformat()
                )
        except Exception as e:
            logger.error(f"设置最后同步时间失败: {e}")
    
    async def add_sync_task(self, source: DataSource, target: DataSource, 
                           sync_type: SyncType, data_key: str, data: Any,
                           priority: int = 1) -> str:
        """添加同步任务"""
        task_id = str(uuid.uuid4())
        
        task = SyncTask(
            task_id=task_id,
            source=source,
            target=target,
            sync_type=sync_type,
            data_key=data_key,
            data=data,
            status=SyncStatus.PENDING,
            retry_count=0,
            max_retries=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            error_message="",
            priority=priority
        )
        
        self.sync_tasks[task_id] = task
        
        # 添加到同步队列
        await self.sync_queue.put(task)
        
        logger.info(f"同步任务已添加: {task_id}")
        return task_id
    
    async def _process_sync_task(self, task: SyncTask):
        """处理同步任务"""
        try:
            # 更新任务状态
            task.status = SyncStatus.IN_PROGRESS
            task.updated_at = datetime.now()
            
            # 获取同步处理器
            handler_key = f"{task.source.value}_to_{task.target.value}"
            handler = self.sync_handlers.get(handler_key)
            
            if not handler:
                # 尝试通用处理器
                handler = self.sync_handlers.get(task.sync_type.value)
            
            if handler:
                # 执行同步
                success = await handler(task)
                
                if success:
                    task.status = SyncStatus.COMPLETED
                    logger.info(f"同步任务完成: {task.task_id}")
                else:
                    await self._handle_sync_failure(task)
            else:
                task.error_message = f"未找到同步处理器: {handler_key}"
                await self._handle_sync_failure(task)
                
        except Exception as e:
            task.error_message = str(e)
            await self._handle_sync_failure(task)
    
    async def _handle_sync_failure(self, task: SyncTask):
        """处理同步失败"""
        task.retry_count += 1
        
        if task.retry_count < task.max_retries:
            task.status = SyncStatus.RETRYING
            logger.warning(f"同步任务失败，将重试: {task.task_id}, 错误: {task.error_message}")
            
            # 延迟后重新加入队列
            await asyncio.sleep(5)
            await self.sync_queue.put(task)
        else:
            task.status = SyncStatus.FAILED
            logger.error(f"同步任务最终失败: {task.task_id}, 错误: {task.error_message}")
    
    async def _sync_db_to_cache(self, task: SyncTask) -> bool:
        """数据库到缓存同步"""
        try:
            # 模拟数据库查询
            data = task.data
            
            # 压缩数据（如果启用）
            if self.sync_configs.get("db_to_cache", {}).enable_compression:
                data = self._compress_data(data)
            
            # 存储到缓存
            if self.redis_client:
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.set, 
                    task.data_key, pickle.dumps(data)
                )
            
            # 更新最后同步时间
            await self._set_last_sync_time("last_sync:db_to_cache", datetime.now())
            
            return True
            
        except Exception as e:
            logger.error(f"数据库到缓存同步失败: {e}")
            return False
    
    async def _sync_cache_to_api(self, task: SyncTask) -> bool:
        """缓存到API同步"""
        try:
            # 从缓存获取数据
            if self.redis_client:
                cached_data = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.get, task.data_key
                )
                
                if cached_data:
                    data = pickle.loads(cached_data)
                    
                    # 模拟API调用
                    await asyncio.sleep(0.1)  # 模拟网络延迟
                    
                    # 更新最后同步时间
                    await self._set_last_sync_time("last_sync:cache_to_api", datetime.now())
                    
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"缓存到API同步失败: {e}")
            return False
    
    async def _sync_real_time(self, task: SyncTask) -> bool:
        """实时同步"""
        try:
            # 实时同步逻辑
            data = task.data
            
            # 立即同步到目标
            if self.redis_client:
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.set, 
                    task.data_key, pickle.dumps(data)
                )
            
            return True
            
        except Exception as e:
            logger.error(f"实时同步失败: {e}")
            return False
    
    async def _sync_incremental(self, task: SyncTask) -> bool:
        """增量同步"""
        try:
            # 增量同步逻辑
            data = task.data
            
            # 计算数据哈希
            data_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
            
            # 检查数据是否已更改
            last_hash_key = f"hash:{task.data_key}"
            if self.redis_client:
                last_hash = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.get, last_hash_key
                )
                
                if last_hash and last_hash.decode() == data_hash:
                    # 数据未更改，跳过同步
                    return True
                
                # 更新数据哈希
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.redis_client.set, last_hash_key, data_hash
                )
            
            # 执行同步
            return await self._sync_db_to_cache(task)
            
        except Exception as e:
            logger.error(f"增量同步失败: {e}")
            return False
    
    def _compress_data(self, data: Any) -> bytes:
        """压缩数据"""
        import gzip
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        return gzip.compress(json_data)
    
    def _decompress_data(self, compressed_data: bytes) -> Any:
        """解压数据"""
        import gzip
        json_data = gzip.decompress(compressed_data)
        return json.loads(json_data.decode('utf-8'))
    
    async def _trigger_sync(self, config_name: str, sync_type: SyncType):
        """触发同步"""
        config = self.sync_configs.get(config_name)
        if not config:
            logger.error(f"未找到同步配置: {config_name}")
            return
        
        # 创建同步任务
        task_id = await self.add_sync_task(
            source=DataSource.DATABASE,
            target=DataSource.CACHE,
            sync_type=sync_type,
            data_key=f"sync:{config_name}",
            data={"config": config_name, "timestamp": datetime.now().isoformat()},
            priority=1
        )
        
        logger.info(f"已触发同步: {config_name}, 任务ID: {task_id}")
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """获取同步状态"""
        status_info = {
            "is_running": self.is_running,
            "total_tasks": len(self.sync_tasks),
            "pending_tasks": len([t for t in self.sync_tasks.values() if t.status == SyncStatus.PENDING]),
            "in_progress_tasks": len([t for t in self.sync_tasks.values() if t.status == SyncStatus.IN_PROGRESS]),
            "completed_tasks": len([t for t in self.sync_tasks.values() if t.status == SyncStatus.COMPLETED]),
            "failed_tasks": len([t for t in self.sync_tasks.values() if t.status == SyncStatus.FAILED]),
            "retrying_tasks": len([t for t in self.sync_tasks.values() if t.status == SyncStatus.RETRYING]),
            "queue_size": self.sync_queue.qsize(),
            "configs": {name: {
                "sync_interval": config.sync_interval,
                "batch_size": config.batch_size,
                "max_retries": config.max_retries
            } for name, config in self.sync_configs.items()}
        }
        
        return status_info
    
    async def get_task_details(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务详情"""
        task = self.sync_tasks.get(task_id)
        if not task:
            return None
        
        return {
            "task_id": task.task_id,
            "source": task.source.value,
            "target": task.target.value,
            "sync_type": task.sync_type.value,
            "data_key": task.data_key,
            "status": task.status.value,
            "retry_count": task.retry_count,
            "max_retries": task.max_retries,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
            "error_message": task.error_message,
            "priority": task.priority
        }
    
    def register_sync_handler(self, handler_key: str, handler: Callable):
        """注册同步处理器"""
        self.sync_handlers[handler_key] = handler
        logger.info(f"同步处理器已注册: {handler_key}")
    
    def update_sync_config(self, config_name: str, config_updates: Dict[str, Any]):
        """更新同步配置"""
        if config_name in self.sync_configs:
            config = self.sync_configs[config_name]
            for key, value in config_updates.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            logger.info(f"同步配置已更新: {config_name}")
    
    async def cleanup_completed_tasks(self, older_than_hours: int = 24):
        """清理已完成的任务"""
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        
        tasks_to_remove = []
        for task_id, task in self.sync_tasks.items():
            if (task.status == SyncStatus.COMPLETED and 
                task.updated_at < cutoff_time):
                tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.sync_tasks[task_id]
        
        logger.info(f"已清理 {len(tasks_to_remove)} 个已完成的任务")

# 全局实例
data_sync_manager = DataSyncManager()
