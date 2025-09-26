#!/usr/bin/env python3
"""
RAG检索服务优化测试
测试三种搜索方法：simple, text, vector
"""

import requests
import json
import time

def test_rag_search(search_type="simple"):
    """测试RAG搜索"""
    print(f"🔍 测试RAG搜索 - {search_type}模式")
    print("-" * 40)
    
    test_queries = [
        "招商银行个人信用贷款产品",
        "工商银行经营贷款利率",
        "建设银行房贷政策",
        "个人信用贷款",
        "贷款利率"
    ]
    
    success_count = 0
    total_results = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. 测试查询: {query}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/rag/search",
                json={
                    "query": query,
                    "search_type": search_type,
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
                    
                    print(f"   ✅ 找到 {total_found} 条结果")
                    total_results += total_found
                    
                    if results:
                        success_count += 1
                        print("   结果示例:")
                        for j, result_item in enumerate(results[:2], 1):  # 只显示前2个
                            content = result_item.get("content", "")[:100]
                            score = result_item.get("similarity_score", 0)
                            print(f"     {j}. 评分:{score:.2f} - {content}...")
                    else:
                        print("   ⚠️ 未找到相关结果")
                else:
                    print(f"   ❌ 搜索失败: {result.get('message')}")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
                print(f"   响应内容: {response.text}")
        except Exception as e:
            print(f"   ❌ 搜索异常: {e}")
        
        time.sleep(0.5)
    
    print(f"\n{search_type}模式搜索结果:")
    print(f"  成功查询: {success_count}/{len(test_queries)}")
    print(f"  总结果数: {total_results}")
    
    return success_count > 0

def main():
    """主测试函数"""
    print("🚀 RAG检索服务优化测试")
    print("=" * 50)
    
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(15)
    
    # 测试健康状态
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ AI服务运行正常")
        else:
            print(f"❌ 服务健康检查失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 服务健康检查异常: {e}")
        return
    
    # 测试三种搜索模式
    search_types = ["simple", "text", "vector"]
    results = {}
    
    for search_type in search_types:
        print(f"\n{'='*20} {search_type.upper()} 模式 {'='*20}")
        results[search_type] = test_rag_search(search_type)
        time.sleep(2)
    
    # 输出总结
    print(f"\n📊 测试结果总结")
    print("=" * 50)
    for search_type, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{search_type.upper()}模式: {status}")
    
    # 推荐最佳模式
    if results.get("simple", False):
        print(f"\n💡 推荐使用: SIMPLE模式（优先向量，回退到文本）")
    elif results.get("text", False):
        print(f"\n💡 推荐使用: TEXT模式（ILIKE模糊匹配）")
    elif results.get("vector", False):
        print(f"\n💡 推荐使用: VECTOR模式（向量相似度）")
    else:
        print(f"\n⚠️ 所有模式都需要进一步优化")

if __name__ == "__main__":
    main()
