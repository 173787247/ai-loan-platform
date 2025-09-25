#!/usr/bin/env python3
import requests
import time
import json

def test_auto_session():
    """测试AI客服自动创建会话功能"""
    base_url = "http://localhost:3000"
    
    print("🧪 测试AI客服自动创建会话功能...")
    
    # 1. 测试前端页面是否可访问
    try:
        response = requests.get(f"{base_url}/ai-chatbot", timeout=10)
        if response.status_code == 200:
            print("✅ 前端页面可访问")
        else:
            print(f"❌ 前端页面访问失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 前端页面访问失败: {e}")
        return
    
    # 2. 测试API服务
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI服务正常运行")
        else:
            print(f"❌ AI服务异常: {response.status_code}")
    except Exception as e:
        print(f"❌ AI服务连接失败: {e}")
    
    print("\n🎯 测试完成！")
    print("请手动访问 http://localhost:3000 验证：")
    print("1. 登录后点击'AI智能客服'")
    print("2. 检查是否自动创建了会话")
    print("3. 检查输入框是否立即可用")

if __name__ == "__main__":
    test_auto_session()
