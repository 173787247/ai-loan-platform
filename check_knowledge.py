#!/usr/bin/env python3
"""
检查知识库内容和RAG检索情况
"""

import requests
import json

def check_knowledge_base():
    """检查知识库内容"""
    print("🔍 检查知识库内容...")
    
    # 1. 检查知识库统计
    response = requests.get('http://localhost:8000/api/v1/rag/stats', timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"📊 知识库统计: {data['data']}")
    else:
        print(f"❌ 获取统计失败: {response.status_code}")
        return
    
    # 2. 搜索招商银行相关内容
    print("\n🔍 搜索招商银行相关内容...")
    response = requests.post(
        'http://localhost:8000/api/v1/rag/search',
        json={
            'query': '招商银行',
            'search_type': 'hybrid',
            'max_results': 5
        },
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        results = data['data']['results']
        print(f"📝 搜索结果: {len(results)}条")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']} - {result['content'][:100]}...")
    else:
        print(f"❌ 搜索失败: {response.status_code}")
    
    # 3. 搜索银行相关内容
    print("\n🔍 搜索银行相关内容...")
    response = requests.post(
        'http://localhost:8000/api/v1/rag/search',
        json={
            'query': '银行',
            'search_type': 'hybrid',
            'max_results': 5
        },
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        results = data['data']['results']
        print(f"📝 搜索结果: {len(results)}条")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']} - {result['content'][:100]}...")
    else:
        print(f"❌ 搜索失败: {response.status_code}")

if __name__ == "__main__":
    check_knowledge_base()
