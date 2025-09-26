#!/usr/bin/env python3
"""
RAG检索服务最终验证
"""

import requests
import json

def test_rag_final():
    """最终RAG测试"""
    print("🚀 RAG检索服务最终验证")
    print("=" * 50)
    
    # 测试TEXT模式（推荐模式）
    print("🔍 测试TEXT模式（ILIKE模糊匹配）")
    print("-" * 40)
    
    test_queries = [
        "招商银行",
        "个人信用贷款", 
        "贷款利率",
        "工商银行",
        "建设银行"
    ]
    
    success_count = 0
    total_results = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. 查询: {query}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/rag/search",
                json={
                    "query": query,
                    "search_type": "text",
                    "max_results": 3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    results = data.get("results", [])
                    total_found = data.get("total_results", 0)
                    
                    if total_found > 0:
                        success_count += 1
                        print(f"   ✅ 找到 {total_found} 条结果")
                        total_results += total_found
                        
                        # 显示第一个结果
                        if results:
                            content = results[0].get("content", "")[:80]
                            print(f"   示例: {content}...")
                    else:
                        print(f"   ⚠️ 未找到结果")
                else:
                    print(f"   ❌ 搜索失败: {result.get('message')}")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 搜索异常: {e}")
    
    print(f"\n📊 TEXT模式测试结果:")
    print(f"  成功查询: {success_count}/{len(test_queries)}")
    print(f"  总结果数: {total_results}")
    
    # 测试VECTOR模式
    print(f"\n🔍 测试VECTOR模式（向量相似度）")
    print("-" * 40)
    
    vector_success = 0
    vector_results = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. 查询: {query}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/rag/search",
                json={
                    "query": query,
                    "search_type": "vector",
                    "max_results": 3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    results = data.get("results", [])
                    total_found = data.get("total_results", 0)
                    
                    if total_found > 0:
                        vector_success += 1
                        print(f"   ✅ 找到 {total_found} 条结果")
                        vector_results += total_found
                        
                        # 显示第一个结果
                        if results:
                            content = results[0].get("content", "")[:80]
                            score = results[0].get("similarity_score", 0)
                            print(f"   示例: 评分{score:.2f} - {content}...")
                    else:
                        print(f"   ⚠️ 未找到结果")
                else:
                    print(f"   ❌ 搜索失败: {result.get('message')}")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 搜索异常: {e}")
    
    print(f"\n📊 VECTOR模式测试结果:")
    print(f"  成功查询: {vector_success}/{len(test_queries)}")
    print(f"  总结果数: {vector_results}")
    
    # 最终总结
    print(f"\n🎯 最终验证结果")
    print("=" * 50)
    print(f"TEXT模式: {'✅ 通过' if success_count > 0 else '❌ 失败'}")
    print(f"VECTOR模式: {'✅ 通过' if vector_success > 0 else '❌ 失败'}")
    
    if success_count > 0 or vector_success > 0:
        print(f"\n🎉 RAG检索服务优化成功！")
        print(f"推荐使用: {'TEXT模式' if success_count >= vector_success else 'VECTOR模式'}")
        return True
    else:
        print(f"\n⚠️ RAG检索服务仍需进一步优化")
        return False

if __name__ == "__main__":
    test_rag_final()
