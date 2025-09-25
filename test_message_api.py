#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_message_api():
    """测试发送消息API"""
    print("🔍 测试发送消息API...")
    
    # 先创建会话
    session_data = {
        "user_id": "1",
        "chatbot_role": "general"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/chat/session",
            json=session_data,
            timeout=10
        )
        print(f"✅ 创建会话状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('data', {}).get('session_id')
            print(f"✅ 会话ID: {session_id}")
            
            # 发送消息
            message_data = {
                "message": "你好",
                "user_id": "1",
                "user_role": "admin",
                "username": "admin"
            }
            
            response = requests.post(
                f"http://localhost:8000/api/v1/chat/message",
                json=message_data,
                timeout=10
            )
            print(f"✅ 发送消息状态: {response.status_code}")
            print(f"✅ 响应内容: {response.text}")
            
        else:
            print(f"❌ 创建会话失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_message_api()
