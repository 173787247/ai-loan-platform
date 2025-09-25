#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_frontend_api():
    """测试前端API连接"""
    print("🔍 测试前端API连接...")
    
    # 测试主页面
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ 主页面状态: {response.status_code}")
        if "AI助贷招标平台" in response.text:
            print("✅ 页面内容正常")
        else:
            print("❌ 页面内容异常")
    except Exception as e:
        print(f"❌ 主页面连接失败: {e}")
        return
    
    # 测试AI服务
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=10)
        print(f"✅ AI服务状态: {response.status_code}")
    except Exception as e:
        print(f"❌ AI服务连接失败: {e}")
    
    # 测试创建会话
    try:
        session_data = {
            "user_id": "1",
            "chatbot_role": "general"
        }
        response = requests.post(
            "http://localhost:8000/api/v1/chat/session",
            json=session_data,
            timeout=10
        )
        print(f"✅ 创建会话状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 会话ID: {result.get('data', {}).get('session_id', 'N/A')}")
        else:
            print(f"❌ 创建会话失败: {response.text}")
    except Exception as e:
        print(f"❌ 创建会话异常: {e}")
    
    # 测试发送消息
    try:
        message_data = {
            "message": "你好",
            "user_id": "1",
            "user_role": "admin",
            "username": "admin"
        }
        response = requests.post(
            "http://localhost:8000/api/v1/chat/message",
            json=message_data,
            timeout=10
        )
        print(f"✅ 发送消息状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI回复: {result.get('data', {}).get('response', 'N/A')[:50]}...")
        else:
            print(f"❌ 发送消息失败: {response.text}")
    except Exception as e:
        print(f"❌ 发送消息异常: {e}")

if __name__ == "__main__":
    test_frontend_api()
