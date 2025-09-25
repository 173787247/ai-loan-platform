#!/usr/bin/env python3
"""
测试AI服务原始响应内容
"""

import requests
import json

def test_raw_response():
    """测试AI服务原始响应"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 测试AI服务原始响应内容")
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
            
            response = requests.post(f"{base_url}/chat/message", 
                                   json=message_data, timeout=30)
            if response.status_code == 200:
                ai_response = response.json()['data']['response']
                
                print("\n📊 原始响应内容:")
                print("=" * 60)
                print(repr(ai_response))
                print("=" * 60)
                
                print("\n📊 显示格式:")
                print("=" * 60)
                print(ai_response)
                print("=" * 60)
                
                # 分析换行符
                lines = ai_response.split('\n')
                print(f"\n📈 分析结果:")
                print(f"  • 总行数: {len(lines)}")
                print(f"  • 换行符数量: {ai_response.count('\\n')}")
                
                # 显示前10行
                print(f"\n📋 前10行内容:")
                for i, line in enumerate(lines[:10]):
                    print(f"  {i+1:2d}: {repr(line)}")
                    
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_raw_response()
