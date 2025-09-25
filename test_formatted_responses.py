#!/usr/bin/env python3
"""
测试AI客服格式化回复效果
"""

import requests
import json
import time

def test_formatted_responses():
    """测试格式化回复效果"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 测试AI客服格式化回复效果")
    print("=" * 50)
    
    # 等待AI服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(5)
    
    try:
        # 1. 测试银行产品对比
        print("\n1️⃣ 测试银行产品对比格式化")
        print("-" * 30)
        
        # 创建会话
        session_data = {
            "user_id": "test_user",
            "chatbot_role": "loan_specialist"
        }
        
        response = requests.post(f"{base_url}/chat/session", json=session_data, timeout=10)
        if response.status_code == 200:
            session_id = response.json()['data']['session_id']
            print(f"✅ 会话创建成功: {session_id}")
            
            # 发送银行对比问题
            message_data = {
                "session_id": session_id,
                "message": "请帮我对比招商银行、工商银行、建设银行的个人信用贷款产品"
            }
            
            response = requests.post(f"{base_url}/chat/message", 
                                   json=message_data, timeout=30)
            if response.status_code == 200:
                ai_response = response.json()['data']['response']
                print("📊 银行对比回复:")
                print(ai_response)
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    try:
        # 2. 测试申请材料清单
        print("\n2️⃣ 测试申请材料清单格式化")
        print("-" * 30)
        
        # 创建新会话
        session_data = {
            "user_id": "test_user_2",
            "chatbot_role": "loan_specialist"
        }
        
        response = requests.post(f"{base_url}/chat/session", json=session_data, timeout=10)
        if response.status_code == 200:
            session_id = response.json()['data']['session_id']
            print(f"✅ 会话创建成功: {session_id}")
            
            # 发送申请材料问题
            message_data = {
                "session_id": session_id,
                "message": "贷款申请需要什么材料？"
            }
            
            response = requests.post(f"{base_url}/chat/message", 
                                   json=message_data, timeout=30)
            if response.status_code == 200:
                ai_response = response.json()['data']['response']
                print("📋 申请材料回复:")
                print(ai_response)
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    try:
        # 3. 测试审核流程
        print("\n3️⃣ 测试审核流程格式化")
        print("-" * 30)
        
        # 创建新会话
        session_data = {
            "user_id": "test_user_3",
            "chatbot_role": "loan_specialist"
        }
        
        response = requests.post(f"{base_url}/chat/session", json=session_data, timeout=10)
        if response.status_code == 200:
            session_id = response.json()['data']['session_id']
            print(f"✅ 会话创建成功: {session_id}")
            
            # 发送审核流程问题
            message_data = {
                "session_id": session_id,
                "message": "贷款审核流程是什么？"
            }
            
            response = requests.post(f"{base_url}/chat/message", 
                                   json=message_data, timeout=30)
            if response.status_code == 200:
                ai_response = response.json()['data']['response']
                print("📝 审核流程回复:")
                print(ai_response)
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("\n🎉 格式化测试完成！")

if __name__ == "__main__":
    test_formatted_responses()
