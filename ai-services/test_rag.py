#!/usr/bin/env python3
import asyncio
import sys
sys.path.append('/app')

async def test_rag():
    try:
        from services.vector_rag import VectorRAGService
        rag = VectorRAGService()
        await rag.initialize()
        
        results = await rag.search_knowledge_hybrid('招商银行', 5)
        print(f"找到 {len(results)} 条结果")
        
        for i, result in enumerate(results):
            print(f"\n结果 {i+1}:")
            print(f"标题: {result.get('title', 'N/A')}")
            print(f"内容: {result.get('content', 'N/A')[:200]}...")
            print(f"类型: {type(result)}")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_rag())
