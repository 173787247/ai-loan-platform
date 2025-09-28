"""
向量化RAG服务
使用PostgreSQL + pgvector进行向量搜索
"""

import asyncio
import asyncpg
import numpy as np
from typing import List, Dict, Any, Optional
from loguru import logger
import os
import json
from datetime import datetime
import hashlib
from .cache_service import cache_service

class VectorRAGService:
    """向量化RAG服务"""
    
    def __init__(self):
        self.db_config = {
            "host": os.getenv("POSTGRES_HOST", "ai-loan-postgresql"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "database": os.getenv("POSTGRES_DB", "ai_loan_rag"),
            "user": os.getenv("POSTGRES_USER", "ai_loan"),
            "password": os.getenv("POSTGRES_PASSWORD", "ai_loan123")
        }
        self.connection_pool = None
        self.embedding_model = None
        self._initialize_embedding_model()
    
    def _initialize_embedding_model(self):
        """初始化嵌入模型"""
        try:
            # 使用sentence-transformers作为嵌入模型
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            # 注意：all-MiniLM-L6-v2生成384维向量，需要调整PostgreSQL schema
            logger.info("嵌入模型初始化成功")
        except ImportError:
            logger.warning("sentence-transformers未安装，使用简单文本匹配")
            self.embedding_model = None
        except Exception as e:
            logger.error(f"嵌入模型初始化失败: {e}")
            self.embedding_model = None
    
    async def initialize(self):
        """初始化数据库连接池"""
        try:
            self.connection_pool = await asyncpg.create_pool(
                host=self.db_config["host"],
                port=self.db_config["port"],
                database=self.db_config["database"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                min_size=10,  # 增加最小连接数
                max_size=50,  # 增加最大连接数
                max_queries=50000,  # 每个连接最大查询数
                max_inactive_connection_lifetime=300.0,  # 非活跃连接最大生存时间
                command_timeout=60,  # 命令超时时间
                server_settings={
                    'jit': 'off',  # 关闭JIT以提高连接速度
                    'application_name': 'ai_loan_rag'
                }
            )
            logger.info("PostgreSQL连接池初始化成功 - 配置: min=10, max=50")
        except Exception as e:
            logger.error(f"PostgreSQL连接池初始化失败: {e}")
            raise
    
    def is_initialized(self):
        """检查服务是否已初始化"""
        return self.connection_pool is not None
    
    async def close(self):
        """关闭数据库连接池"""
        if self.connection_pool:
            await self.connection_pool.close()
            logger.info("PostgreSQL连接池已关闭")
    
    def _get_embedding(self, text: str) -> List[float]:
        """获取文本的向量嵌入"""
        if self.embedding_model:
            try:
                embedding = self.embedding_model.encode(text)
                return embedding.tolist()
            except Exception as e:
                logger.error(f"生成嵌入向量失败: {e}")
                return None
        else:
            # 简单的文本向量化（基于词频）
            words = text.lower().split()
            word_count = {}
            for word in words:
                word_count[word] = word_count.get(word, 0) + 1
            
            # 创建固定长度的向量（1536维，匹配OpenAI）
            vector = [0.0] * 1536
            for i, (word, count) in enumerate(word_count.items()):
                if i < 1536:
                    vector[i] = count / len(words)
            
            return vector
    
    async def add_knowledge(self, category: str, title: str, content: str, metadata: Dict[str, Any] = None) -> int:
        """添加知识到向量数据库"""
        try:
            embedding = self._get_embedding(content)
            if not embedding:
                logger.warning("无法生成嵌入向量，跳过添加")
                return None
            
            async with self.connection_pool.acquire() as conn:
                # 将embedding转换为PostgreSQL vector格式
                embedding_str = '[' + ','.join(map(str, embedding)) + ']'
                query = """
                INSERT INTO knowledge_base (category, title, content, embedding, metadata)
                VALUES ($1, $2, $3, $4::VECTOR(384), $5)
                RETURNING id
                """
                result = await conn.fetchval(
                    query, 
                    category, 
                    title, 
                    content, 
                    embedding_str, 
                    json.dumps(metadata) if metadata else None
                )
                logger.info(f"知识添加成功: {title} (ID: {result})")
                return result
        except Exception as e:
            logger.error(f"添加知识失败: {e}")
            return None
    
    async def search_knowledge_vector(
        self, 
        query: str, 
        category: str = None, 
        similarity_threshold: float = 0.7,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """使用向量搜索知识库"""
        try:
            query_embedding = self._get_embedding(query)
            if not query_embedding:
                logger.warning("无法生成查询向量，使用文本搜索")
                return await self.search_knowledge_text(query, category, max_results)
            
            async with self.connection_pool.acquire() as conn:
                # 将embedding转换为PostgreSQL vector格式
                embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
                if category:
                    query_sql = """
                    SELECT id, category, title, content, 
                           1 - (embedding <=> $1::VECTOR(384)) as similarity_score, metadata
                    FROM knowledge_base 
                    WHERE category = $2 AND embedding IS NOT NULL
                    AND 1 - (embedding <=> $1::VECTOR(384)) > $3
                    ORDER BY embedding <=> $1::VECTOR(384)
                    LIMIT $4
                    """
                    results = await conn.fetch(query_sql, embedding_str, category, similarity_threshold, max_results)
                else:
                    query_sql = """
                    SELECT id, category, title, content, 
                           1 - (embedding <=> $1::VECTOR(384)) as similarity_score, metadata
                    FROM knowledge_base 
                    WHERE embedding IS NOT NULL
                    AND 1 - (embedding <=> $1::VECTOR(384)) > $2
                    ORDER BY embedding <=> $1::VECTOR(384)
                    LIMIT $3
                    """
                    results = await conn.fetch(query_sql, embedding_str, similarity_threshold, max_results)
                
                knowledge_results = []
                for row in results:
                    knowledge_results.append({
                        "id": row["id"],
                        "category": row["category"],
                        "title": row["title"],
                        "content": row["content"],
                        "similarity_score": float(row["similarity_score"]),
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
                    })
                
                logger.info(f"向量搜索完成，找到 {len(knowledge_results)} 条结果")
                return knowledge_results
                
        except Exception as e:
            logger.error(f"向量搜索失败: {e}")
            return await self.search_knowledge_text(query, category, max_results)
    
    def _generate_cache_key(self, query: str, category: str = None, max_results: int = 5, search_type: str = "text") -> str:
        """生成缓存键"""
        key_data = f"{search_type}:{query}:{category or ''}:{max_results}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def search_knowledge_text(
        self, 
        query: str, 
        category: str = None, 
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """使用ILIKE模糊搜索知识库（带缓存）"""
        # 检查缓存
        cache_key = self._generate_cache_key(query, category, max_results, "text")
        cached_result = await cache_service.get(cache_key)
        if cached_result is not None:
            logger.info(f"从缓存获取搜索结果: {query}")
            return cached_result
        
        try:
            async with self.connection_pool.acquire() as conn:
                if category:
                    query_sql = """
                    SELECT id, category, title, content, 
                           CASE 
                               WHEN content ILIKE $1 THEN 1.0
                               ELSE 0.5
                           END as relevance_score,
                           metadata
                    FROM knowledge_base 
                    WHERE category = $2 
                    AND content ILIKE $1
                    ORDER BY relevance_score DESC, id DESC
                    LIMIT $3::INTEGER
                    """
                    results = await conn.fetch(query_sql, f"%{query}%", category, max_results)
                else:
                    query_sql = """
                    SELECT id, category, title, content, 
                           CASE 
                               WHEN content ILIKE $1 THEN 1.0
                               ELSE 0.5
                           END as relevance_score,
                           metadata
                    FROM knowledge_base 
                    WHERE content ILIKE $1
                    ORDER BY relevance_score DESC, id DESC
                    LIMIT $2
                    """
                    results = await conn.fetch(query_sql, f"%{query}%", max_results)
                
                knowledge_results = []
                for row in results:
                    knowledge_results.append({
                        "id": row["id"],
                        "category": row["category"],
                        "title": row["title"],
                        "content": row["content"],
                        "similarity_score": float(row["relevance_score"]),
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
                    })
                
                logger.info(f"全文搜索完成，找到 {len(knowledge_results)} 条结果")
                
                # 存储到缓存（缓存1小时）
                await cache_service.set(cache_key, knowledge_results, ttl=3600)
                
                return knowledge_results
                
        except Exception as e:
            logger.error(f"全文搜索失败: {e}")
            return []
    
    async def search_knowledge_hybrid(
        self, 
        query: str, 
        category: str = None, 
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """混合搜索（向量+全文）"""
        try:
            # 首先尝试向量搜索
            query_embedding = self._get_embedding(query)
            if query_embedding:
                try:
                    async with self.connection_pool.acquire() as conn:
                        # 将embedding转换为PostgreSQL vector格式
                        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
                        query_sql = """
                        SELECT id, category, title, content, relevance_score, metadata
                        FROM search_knowledge_hybrid($1, $2::VECTOR(384), $3, $4)
                        """
                        results = await conn.fetch(query_sql, query, embedding_str, category or '', max_results)
                        
                        knowledge_results = []
                        for row in results:
                            knowledge_results.append({
                                "id": row["id"],
                                "category": row["category"],
                                "title": row["title"],
                                "content": row["content"],
                                "similarity_score": float(row["relevance_score"]),
                                "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
                            })
                        
                        if knowledge_results:
                            logger.info(f"混合搜索完成，找到 {len(knowledge_results)} 条结果")
                            return knowledge_results
                except Exception as e:
                    logger.warning(f"向量搜索失败，回退到文本搜索: {e}")
            
            # 回退到文本搜索
            return await self.search_knowledge_text(query, category, max_results)
                
        except Exception as e:
            logger.error(f"混合搜索失败: {e}")
            return await self.search_knowledge_text(query, category, max_results)
    
    async def get_knowledge_by_id(self, knowledge_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取知识"""
        try:
            async with self.connection_pool.acquire() as conn:
                query = """
                SELECT id, category, title, content, metadata, created_at, updated_at
                FROM knowledge_base 
                WHERE id = $1
                """
                result = await conn.fetchrow(query, knowledge_id)
                
                if result:
                    return {
                        "id": result["id"],
                        "category": result["category"],
                        "title": result["title"],
                        "content": result["content"],
                        "metadata": json.loads(result["metadata"]) if result["metadata"] else {},
                        "created_at": result["created_at"].isoformat(),
                        "updated_at": result["updated_at"].isoformat()
                    }
                return None
                
        except Exception as e:
            logger.error(f"获取知识失败: {e}")
            return None
    
    async def update_knowledge(
        self, 
        knowledge_id: int, 
        title: str = None, 
        content: str = None, 
        metadata: Dict[str, Any] = None
    ) -> bool:
        """更新知识"""
        try:
            async with self.connection_pool.acquire() as conn:
                # 构建更新查询
                update_fields = []
                params = [knowledge_id]
                param_count = 1
                
                if title:
                    param_count += 1
                    update_fields.append(f"title = ${param_count}")
                    params.append(title)
                
                if content:
                    param_count += 1
                    update_fields.append(f"content = ${param_count}")
                    params.append(content)
                    
                    # 重新生成嵌入向量
                    embedding = self._get_embedding(content)
                    if embedding:
                        param_count += 1
                        update_fields.append(f"embedding = ${param_count}")
                        params.append(embedding)
                
                if metadata:
                    param_count += 1
                    update_fields.append(f"metadata = ${param_count}")
                    params.append(json.dumps(metadata))
                
                if not update_fields:
                    return False
                
                param_count += 1
                update_fields.append(f"updated_at = ${param_count}")
                params.append(datetime.now())
                
                query = f"""
                UPDATE knowledge_base 
                SET {', '.join(update_fields)}
                WHERE id = $1
                """
                
                result = await conn.execute(query, *params)
                logger.info(f"知识更新成功: ID {knowledge_id}")
                return True
                
        except Exception as e:
            logger.error(f"更新知识失败: {e}")
            return False
    
    async def delete_knowledge(self, knowledge_id: int) -> bool:
        """删除知识"""
        try:
            async with self.connection_pool.acquire() as conn:
                query = "DELETE FROM knowledge_base WHERE id = $1"
                result = await conn.execute(query, knowledge_id)
                logger.info(f"知识删除成功: ID {knowledge_id}")
                return True
                
        except Exception as e:
            logger.error(f"删除知识失败: {e}")
            return False
    
    async def get_knowledge_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        try:
            async with self.connection_pool.acquire() as conn:
                # 总数量
                total_count = await conn.fetchval("SELECT COUNT(*) FROM knowledge_base")
                
                # 按分类统计
                category_stats = await conn.fetch("""
                    SELECT category, COUNT(*) as count 
                    FROM knowledge_base 
                    GROUP BY category 
                    ORDER BY count DESC
                """)
                
                # 有嵌入向量的数量
                embedded_count = await conn.fetchval("""
                    SELECT COUNT(*) FROM knowledge_base WHERE embedding IS NOT NULL
                """)
                
                return {
                    "total_count": total_count,
                    "embedded_count": embedded_count,
                    "category_stats": {row["category"]: row["count"] for row in category_stats}
                }
                
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}
    
    async def search_knowledge_simple(
        self, 
        query: str, 
        category: str = None, 
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """简单搜索（优先向量，回退到文本）"""
        try:
            # 首先尝试向量搜索
            vector_results = await self.search_knowledge_vector(query, category, 0.1, max_results)
            if vector_results:
                logger.info(f"向量搜索成功，找到 {len(vector_results)} 条结果")
                return vector_results
            
            # 回退到文本搜索
            logger.info("向量搜索无结果，回退到文本搜索")
            return await self.search_knowledge_text(query, category, max_results)
                
        except Exception as e:
            logger.error(f"简单搜索失败: {e}")
            return []

# 全局实例
vector_rag_service = VectorRAGService()
