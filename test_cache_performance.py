#!/usr/bin/env python3
"""
测试缓存性能优化效果
"""

import requests
import time
import json

def test_cache_performance():
    """测试缓存性能"""
    print("🚀 缓存性能测试")
    print("=" * 40)
    
    # 测试查询
    test_query = "个人信用贷款"
    
    print(f"测试查询: {test_query}")
    print("-" * 30)
    
    # 第一次查询（无缓存）
    print("1. 第一次查询（无缓存）...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/rag/search",
            json={
                "query": test_query,
                "search_type": "text",
                "max_results": 3
            },
            timeout=30
        )
        
        first_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                results = data.get("results", [])
                print(f"   ✅ 找到 {len(results)} 条结果")
                print(f"   ⏱️ 响应时间: {first_time:.3f}秒")
            else:
                print(f"   ❌ 查询失败: {result.get('message')}")
                return
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 查询异常: {e}")
        return
    
    # 第二次查询（有缓存）
    print("\n2. 第二次查询（有缓存）...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/rag/search",
            json={
                "query": test_query,
                "search_type": "text",
                "max_results": 3
            },
            timeout=30
        )
        
        second_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                results = data.get("results", [])
                print(f"   ✅ 找到 {len(results)} 条结果")
                print(f"   ⏱️ 响应时间: {second_time:.3f}秒")
            else:
                print(f"   ❌ 查询失败: {result.get('message')}")
                return
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 查询异常: {e}")
        return
    
    # 性能对比
    print(f"\n📊 性能对比")
    print("-" * 30)
    print(f"第一次查询（无缓存）: {first_time:.3f}秒")
    print(f"第二次查询（有缓存）: {second_time:.3f}秒")
    
    if second_time < first_time:
        improvement = ((first_time - second_time) / first_time) * 100
        print(f"性能提升: {improvement:.1f}%")
    else:
        print("缓存可能未生效")
    
    # 测试缓存统计
    print(f"\n3. 缓存统计信息...")
    try:
        response = requests.get("http://localhost:8000/api/v1/cache/stats")
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                stats = result.get("data", {})
                print(f"   ✅ 缓存状态: {stats.get('status', 'unknown')}")
                if 'used_memory' in stats:
                    print(f"   💾 内存使用: {stats.get('used_memory', 'unknown')}")
                if 'keyspace_hits' in stats:
                    print(f"   🎯 缓存命中: {stats.get('keyspace_hits', 0)}")
            else:
                print(f"   ❌ 获取统计失败: {result.get('message')}")
        else:
            print(f"   ❌ 统计API调用失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 统计查询异常: {e}")

def test_multiple_queries():
    """测试多个查询的缓存效果"""
    print(f"\n🔄 多查询缓存测试")
    print("=" * 40)
    
    queries = [
        "招商银行个人信用贷款",
        "工商银行经营贷款利率", 
        "建设银行房贷政策",
        "个人信用贷款",  # 重复查询
        "贷款利率"  # 重复查询
    ]
    
    total_time = 0
    cache_hits = 0
    
    for i, query in enumerate(queries, 1):
        print(f"{i}. 查询: {query}")
        
        start_time = time.time()
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
            
            query_time = time.time() - start_time
            total_time += query_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    results = data.get("results", [])
                    print(f"   ✅ 找到 {len(results)} 条结果 - {query_time:.3f}秒")
                    
                    # 检查是否可能是缓存命中（响应时间很短）
                    if query_time < 0.01:  # 小于10ms可能是缓存
                        cache_hits += 1
                else:
                    print(f"   ❌ 查询失败: {result.get('message')}")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 查询异常: {e}")
    
    print(f"\n📊 多查询统计")
    print("-" * 30)
    print(f"总查询数: {len(queries)}")
    print(f"总耗时: {total_time:.3f}秒")
    print(f"平均耗时: {total_time/len(queries):.3f}秒")
    print(f"可能的缓存命中: {cache_hits}")

if __name__ == "__main__":
    test_cache_performance()
    test_multiple_queries()
