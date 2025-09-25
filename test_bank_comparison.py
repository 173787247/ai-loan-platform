#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI客服多银行贷款对比功能
"""

import requests
import json

def test_bank_comparison():
    """测试多银行贷款对比功能"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🚀 测试AI客服多银行贷款对比功能")
    print("=" * 60)
    
    # 1. 创建聊天会话
    print("\n📞 创建聊天会话...")
    session_data = {
        "user_id": "test_user_123",
        "role": "borrower"
    }
    
    try:
        r1 = requests.post(f"{base_url}/chat/session", json=session_data, timeout=10)
        if r1.status_code == 200:
            session_id = r1.json()['data']['session_id']
            print(f"✅ 会话创建成功: {session_id}")
        else:
            print(f"❌ 会话创建失败: {r1.status_code}")
            return
    except Exception as e:
        print(f"❌ 会话创建异常: {e}")
        return
    
    # 2. 测试多银行对比问题
    test_questions = [
        "请帮我对比招商银行、工商银行、建设银行的个人信用贷款产品",
        "AI客服怎么协助我申请招商银行贷款需要提供什么资料",
        "怎么协助我审核不同银行的贷款要求？",
        "请对比一下各大银行的贷款利率和条件"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 测试问题 {i}: {question}")
        print("-" * 50)
        
        message_data = {
            "message": question,
            "user_id": "test_user_123",
            "session_id": session_id,
            "metadata": {"has_files": False}
        }
        
        try:
            r2 = requests.post(f"{base_url}/chat/message", json=message_data, timeout=30)
            if r2.status_code == 200:
                response = r2.json()['data']['response']
                print(f"🤖 AI回复:\n{response}")
            else:
                print(f"❌ 消息发送失败: {r2.status_code}")
                print(f"错误信息: {r2.text}")
        except Exception as e:
            print(f"❌ 消息发送异常: {e}")
        
        print("\n" + "="*60)
    
    # 3. 测试知识库搜索
    print("\n🔍 测试知识库搜索...")
    search_queries = [
        "工商银行 个人信用贷款",
        "建设银行 个人信用贷款", 
        "银行 贷款 对比",
        "贷款利率 条件"
    ]
    
    for query in search_queries:
        print(f"\n📚 搜索: {query}")
        try:
            r = requests.post(f"{base_url}/rag/search", json={'query': query, 'limit': 3}, timeout=10)
            if r.status_code == 200:
                results = r.json()['data']['results']
                print(f"找到 {len(results)} 条结果:")
                for j, result in enumerate(results[:3], 1):
                    title = result.get('title', '未知标题')
                    content = result.get('content', '')[:100]
                    print(f"  {j}. {title}: {content}...")
            else:
                print(f"❌ 搜索失败: {r.status_code}")
        except Exception as e:
            print(f"❌ 搜索异常: {e}")

if __name__ == "__main__":
    test_bank_comparison()
