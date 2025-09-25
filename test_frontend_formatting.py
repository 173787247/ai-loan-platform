#!/usr/bin/env python3
"""
测试前端格式化显示效果
"""

import requests
import json
import time

def test_frontend_formatting():
    """测试前端格式化显示"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 测试前端格式化显示效果")
    print("=" * 50)
    
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
                print("📊 AI客服回复 (原始格式):")
                print("=" * 60)
                print(repr(ai_response))  # 使用repr显示原始字符串，包括换行符
                print("=" * 60)
                
                print("\n📊 AI客服回复 (显示格式):")
                print("=" * 60)
                print(ai_response)
                print("=" * 60)
                
                # 检查换行符
                line_count = ai_response.count('\n')
                print(f"\n📈 格式统计:")
                print(f"  • 总字符数: {len(ai_response)}")
                print(f"  • 换行符数量: {line_count}")
                print(f"  • 行数: {len(ai_response.split('\\n'))}")
                
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
                print(f"错误信息: {response.text}")
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_frontend_formatting()
