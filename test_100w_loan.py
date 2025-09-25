#!/usr/bin/env python3
"""
测试100万贷款申请的AI客服回复格式
"""

import requests
import json
import time

def test_100w_loan_application():
    """测试100万贷款申请回复格式"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 测试100万贷款申请AI客服回复格式")
    print("=" * 50)
    
    # 等待AI服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(3)
    
    try:
        # 创建会话
        session_data = {
            "user_id": "admin",
            "chatbot_role": "loan_specialist"
        }
        
        response = requests.post(f"{base_url}/chat/session", json=session_data, timeout=10)
        if response.status_code == 200:
            session_id = response.json()['data']['session_id']
            print(f"✅ 会话创建成功: {session_id}")
            
            # 发送100万贷款申请问题
            message_data = {
                "session_id": session_id,
                "message": "我想申请一百万的个人信贷，申请哪一家最有利"
            }
            
            print("\n📤 发送问题: 我想申请一百万的个人信贷，申请哪一家最有利")
            print("-" * 60)
            
            response = requests.post(f"{base_url}/chat/message", 
                                   json=message_data, timeout=30)
            if response.status_code == 200:
                ai_response = response.json()['data']['response']
                print("📊 AI客服回复:")
                print("=" * 60)
                print(ai_response)
                print("=" * 60)
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
                print(f"错误信息: {response.text}")
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_100w_loan_application()
