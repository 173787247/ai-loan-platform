#!/usr/bin/env python3
"""
测试API响应格式
"""

import requests
import json
import time

def test_api_response():
    """测试API响应格式"""
    print("🔍 测试API响应格式...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    try:
        # 创建会话
        response = requests.post(
            'http://localhost:8000/api/v1/chat/session',
            json={'user_id': '2', 'chatbot_role': 'general'},
            timeout=10
        )
        if response.status_code == 200:
            session_id = response.json()['data']['session_id']
            print(f"✅ 聊天会话创建成功: {session_id}")
            
            # 测试问题
            response = requests.post(
                'http://localhost:8000/api/v1/chat/message',
                json={
                    'session_id': session_id,
                    'message': '请介绍一下人民银行',
                    'user_id': '2'
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API响应成功")
                print(f"📊 响应字段: {list(data.keys())}")
                print(f"📝 完整响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
            else:
                print(f"❌ 问答失败: {response.status_code}")
                print(f"错误信息: {response.text}")
        else:
            print(f"❌ 聊天会话创建失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试异常: {e}")
    
    print("\n🎉 API响应格式测试完成！")

if __name__ == "__main__":
    test_api_response()
