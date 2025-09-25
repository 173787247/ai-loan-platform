#!/usr/bin/env python3
import requests
import time
import json

def test_ai_chatbot():
    """测试AI客服自动创建会话功能"""
    print("🧪 测试AI客服功能...")
    
    # 等待前端启动
    print("⏳ 等待前端服务启动...")
    time.sleep(10)
    
    # 1. 测试前端页面
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ 前端页面可访问")
        else:
            print(f"❌ 前端页面访问失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 前端页面访问失败: {e}")
        return
    
    # 2. 测试AI服务
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI服务正常运行")
        else:
            print(f"❌ AI服务异常: {response.status_code}")
    except Exception as e:
        print(f"❌ AI服务连接失败: {e}")
    
    # 3. 测试创建会话API
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
        if response.status_code == 200:
            result = response.json()
            print("✅ 创建会话API正常")
            print(f"   会话ID: {result.get('data', {}).get('session_id', 'N/A')}")
        else:
            print(f"❌ 创建会话API失败: {response.status_code}")
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 创建会话API错误: {e}")
    
    # 4. 测试发送消息API（使用刚创建的会话）
    try:
        # 先创建会话
        session_data = {
            "user_id": "1",
            "chatbot_role": "general"
        }
        session_response = requests.post(
            "http://localhost:8000/api/v1/chat/session",
            json=session_data,
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_id = session_response.json().get('data', {}).get('session_id')
            
            # 使用会话ID发送消息
            message_data = {
                "message": "测试消息",
                "user_id": "1",
                "user_role": "admin",
                "username": "admin",
                "session_id": session_id
            }
            response = requests.post(
                "http://localhost:8000/api/v1/chat/message",
                json=message_data,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                print("✅ 发送消息API正常")
                print(f"   响应: {result.get('data', {}).get('response', 'N/A')[:100]}...")
            else:
                print(f"❌ 发送消息API失败: {response.status_code}")
                print(f"   响应: {response.text}")
        else:
            print(f"❌ 创建会话失败: {session_response.status_code}")
    except Exception as e:
        print(f"❌ 发送消息API错误: {e}")
    
    print("\n🎯 测试完成！")
    print("请手动访问 http://localhost:3000 验证：")
    print("1. 登录后点击'AI智能客服'")
    print("2. 检查是否自动创建了会话")
    print("3. 检查输入框是否立即可用")
    print("4. 尝试发送消息")

if __name__ == "__main__":
    test_ai_chatbot()