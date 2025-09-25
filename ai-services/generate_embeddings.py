#!/usr/bin/env python3
"""
生成知识库文本的向量嵌入
"""
import os
import asyncio
import asyncpg
from sentence_transformers import SentenceTransformer
import numpy as np

async def generate_embeddings():
    """生成知识库的向量嵌入"""
    
    # 数据库连接配置
    DB_CONFIG = {
        'host': 'ai-loan-postgresql',
        'port': 5432,
        'database': 'ai_loan_rag',
        'user': 'ai_loan',
        'password': 'ai_loan123'
    }
    
    # 初始化嵌入模型
    print("正在加载嵌入模型...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("嵌入模型加载完成")
    
    try:
        # 连接数据库
        print("正在连接数据库...")
        conn = await asyncpg.connect(**DB_CONFIG)
        print("数据库连接成功")
        
        # 获取所有需要生成嵌入的记录
        print("正在获取知识库记录...")
        records = await conn.fetch("SELECT id, title, content FROM knowledge_base WHERE embedding IS NULL")
        print(f"找到 {len(records)} 条记录需要生成嵌入")
        
        # 为每条记录生成嵌入
        for record in records:
            record_id = record['id']
            title = record['title']
            content = record['content']
            
            # 组合标题和内容
            text = f"{title} {content}"
            
            # 生成嵌入向量
            print(f"正在为记录 {record_id} 生成嵌入...")
            embedding = model.encode(text)
            
            # 转换为PostgreSQL向量格式
            embedding_str = '[' + ','.join(map(str, embedding)) + ']'
            
            # 更新数据库
            await conn.execute(
                "UPDATE knowledge_base SET embedding = $1::VECTOR(384) WHERE id = $2",
                embedding_str, record_id
            )
            
            print(f"记录 {record_id} 嵌入更新完成")
        
        print("所有嵌入生成完成！")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        if 'conn' in locals():
            await conn.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    asyncio.run(generate_embeddings())
