#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的RAG+LLM AI聊天机器人功能
"""

import requests
import json
import time

def test_ai_chatbot():
    """测试AI聊天机器人API"""
    base_url = "http://localhost:8000"
    
    # 测试消息
    test_messages = [
        "我想了解贷款产品",
        "我想个人信贷一百万人民币，帮我推荐五家对比一下",
        "哪个银行的利率最低？",
        "申请贷款需要什么材料？"
    ]
    
    print("🤖 测试新的RAG+LLM AI聊天机器人功能")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 测试消息 {i}: {message}")
        print("-" * 40)
        
        try:
            # 创建会话
            session_response = requests.post(
                f"{base_url}/api/v1/chat/session",
                json={"user_id": "test_user"},
                timeout=10
            )
            
            if session_response.status_code == 200:
                session_data = session_response.json()
                session_id = session_data.get('data', {}).get('session_id')
                print(f"✅ 会话创建成功: {session_id}")
                
                # 发送消息
                message_response = requests.post(
                    f"{base_url}/api/v1/chat/message",
                    json={
                        "session_id": session_id,
                        "message": message,
                        "user_id": "test_user"
                    },
                    timeout=30
                )
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    ai_response = response_data.get('response', '')
                    print(f"🤖 AI回复:")
                    print(ai_response)
                    
                    # 检查是否包含银行信息
                    if any(bank in ai_response for bank in ['银行', '建设银行', '工商银行', '招商银行']):
                        print("✅ 包含银行信息")
                    else:
                        print("⚠️ 未包含银行信息")
                        
                else:
                    print(f"❌ 发送消息失败: {message_response.status_code}")
                    print(message_response.text)
                    
            else:
                print(f"❌ 创建会话失败: {session_response.status_code}")
                print(session_response.text)
                
        except requests.exceptions.Timeout:
            print("⏰ 请求超时")
        except requests.exceptions.ConnectionError:
            print("🔌 连接失败，请确保AI服务正在运行")
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        print("\n" + "=" * 50)
        time.sleep(2)  # 避免请求过于频繁

if __name__ == "__main__":
    test_ai_chatbot()
