#!/usr/bin/env python3
"""
测试AI智能客服修复结果
"""

import requests
import json

def test_ai_service():
    """测试AI服务修复结果"""
    print("🔍 测试AI智能客服修复结果...")
    
    # 1. 测试API健康状态
    print("\n1. 测试API健康状态...")
    try:
        response = requests.get('http://localhost:8000/api/v1/rag/stats', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API健康检查通过: {data['data']['total_count']}条知识记录")
        else:
            print(f"❌ API健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return False

    # 2. 测试创建聊天会话
    print("\n2. 测试创建聊天会话...")
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/chat/session',
            json={'user_id': '2', 'chatbot_role': 'general'},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 聊天会话创建成功: {data['data']['session_id']}")
            session_id = data['data']['session_id']
        else:
            print(f"❌ 聊天会话创建失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 聊天会话创建异常: {e}")
        return False

    # 3. 测试发送消息
    print("\n3. 测试发送消息...")
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/chat/message',
            json={
                'session_id': session_id,
                'message': '什么是个人信用贷款？',
                'user_id': '2'
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 消息发送成功: {data['data']['response'][:100]}...")
            return True
        else:
            print(f"❌ 消息发送失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 消息发送异常: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_service()
    if success:
        print("\n🎉 AI智能客服修复成功！")
        print("✅ 用户ID类型问题已修复")
        print("✅ 向量搜索问题已修复")
        print("✅ 聊天会话创建正常")
        print("✅ 消息发送正常")
    else:
        print("\n❌ AI智能客服仍有问题，需要进一步调试")
