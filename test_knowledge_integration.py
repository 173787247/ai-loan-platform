#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI客服知识集成功能
"""

import requests
import json

def test_knowledge_integration():
    """测试知识集成功能"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🚀 测试AI客服知识集成功能")
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
    
    # 2. 测试知识库搜索
    print("\n🔍 测试知识库搜索...")
    search_queries = [
        "银行个人信用贷款对比分析",
        "招商银行 工商银行 建设银行 对比"
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
    
    # 3. 测试AI客服回答
    print("\n🤖 测试AI客服回答...")
    test_questions = [
        "请帮我对比招商银行、工商银行、建设银行的个人信用贷款产品",
        "贷款申请需要什么材料？",
        "贷款审核流程是什么？"
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
                
                # 检查回复是否包含具体信息
                if "对比" in question and "利率对比" in response:
                    print("✅ 包含银行对比信息")
                elif "材料" in question and ("身份证" in response or "收入证明" in response):
                    print("✅ 包含申请材料信息")
                elif "审核" in question and ("流程" in response or "步骤" in response):
                    print("✅ 包含审核流程信息")
                else:
                    print("❌ 回复过于通用，未使用知识库信息")
            else:
                print(f"❌ 消息发送失败: {r2.status_code}")
                print(f"错误信息: {r2.text}")
        except Exception as e:
            print(f"❌ 消息发送异常: {e}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    test_knowledge_integration()
