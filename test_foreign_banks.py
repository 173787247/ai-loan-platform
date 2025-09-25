#!/usr/bin/env python3
"""
测试国外银行问题
"""

import requests
import json
import time

def test_foreign_banks():
    """测试国外银行问题"""
    print("🏦 测试国外银行问题...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    # 1. 测试银行名称检测
    print("\n1. 测试银行名称检测...")
    test_messages = [
        "介绍一下国外有哪些银行在中国有业务？",
        "国外银行在中国有业务吗",
        "请介绍一下花旗银行",
        "汇丰银行有什么贷款产品？"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(
                'http://localhost:8000/api/v1/web/search/universal/detect',
                json={'message': message},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                bank_name = data['data']['bank_name']
                detected = data['data']['detected']
                print(f"✅ '{message}' -> {bank_name if detected else '未检测到银行'}")
            else:
                print(f"❌ 检测失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 检测异常: {e}")
    
    # 2. 测试AI聊天机器人
    print("\n2. 测试AI聊天机器人...")
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
            
            # 测试国外银行问题
            test_questions = [
                "介绍一下国外有哪些银行在中国有业务？",
                "国外银行在中国有业务吗",
                "请介绍一下花旗银行"
            ]
            
            for question in test_questions:
                print(f"\n📝 问题: {question}")
                response = requests.post(
                    'http://localhost:8000/api/v1/chat/message',
                    json={
                        'session_id': session_id,
                        'message': question,
                        'user_id': '2'
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data['data']['response']
                    print(f"🤖 AI回答: {answer}")
                else:
                    print(f"❌ 问答失败: {response.status_code}")
                    print(f"错误信息: {response.text}")
        else:
            print(f"❌ 聊天会话创建失败: {response.status_code}")
    except Exception as e:
        print(f"❌ AI聊天机器人测试异常: {e}")
    
    print("\n🎉 国外银行测试完成！")

if __name__ == "__main__":
    test_foreign_banks()
