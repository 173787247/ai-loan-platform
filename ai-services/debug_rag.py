#!/usr/bin/env python3
import asyncio
import os
import sys
sys.path.append('/app')

from services.vector_rag import VectorRAGService

async def debug_rag():
    """调试RAG搜索问题"""
    try:
        # 初始化RAG服务
        rag = VectorRAGService()
        await rag.initialize()
        
        # 测试搜索
        print("测试搜索'招商银行'...")
        results = await rag.search_knowledge_hybrid('招商银行', 5)
        print(f"找到 {len(results)} 条结果")
        
        if results:
            for i, result in enumerate(results[:3]):
                print(f"结果 {i+1}:")
                print(f"  标题: {result.get('title', 'N/A')}")
                print(f"  内容: {result.get('content', 'N/A')[:100]}...")
                print(f"  相关性: {result.get('relevance_score', 'N/A')}")
                print()
        else:
            print("没有找到结果")
            
        # 测试全文搜索
        print("\n测试全文搜索...")
        text_results = await rag.search_knowledge_text('招商银行', 5)
        print(f"全文搜索找到 {len(text_results)} 条结果")
        
        if text_results:
            for i, result in enumerate(text_results[:3]):
                print(f"结果 {i+1}:")
                print(f"  标题: {result.get('title', 'N/A')}")
                print(f"  内容: {result.get('content', 'N/A')[:100]}...")
                print(f"  相关性: {result.get('relevance_score', 'N/A')}")
                print()
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_rag())
