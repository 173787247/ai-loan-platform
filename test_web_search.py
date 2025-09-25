#!/usr/bin/env python3
"""
测试增强版网络搜索功能
"""

import requests
import json
import time

def test_web_search():
    """测试网络搜索功能"""
    print("🔍 测试增强版网络搜索功能...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    # 1. 测试银行信息搜索
    print("\n1. 测试银行信息搜索...")
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/web/search/bank',
            json={
                'bank_name': '招商银行',
                'query': '贷款产品'
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 招商银行信息搜索成功")
            print(f"📊 银行: {data['data']['bank_name']}")
            print(f"📞 客服: {data['data']['contact']}")
            print(f"🌐 官网: {data['data']['website']}")
            print(f"📝 产品数量: {len(data['data']['products'])}")
            print(f"🔄 数据来源: {data['data']['source']}")
            
            # 显示产品信息
            for i, product in enumerate(data['data']['products'][:3], 1):
                print(f"  {i}. {product['title']} - {product['description']}")
                print(f"     利率: {product['rate']}, 额度: {product['amount']}")
        else:
            print(f"❌ 银行信息搜索失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 银行信息搜索异常: {e}")
    
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
            
            # 测试招商银行问题
            questions = [
                "介绍一下招商银行",
                "招商银行有什么贷款产品？",
                "招商银行的贷款利率是多少？",
                "招商银行的客服电话是多少？"
            ]
            
            for question in questions:
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
                    answer = data['response']
                    print(f"🤖 AI回答: {answer[:200]}...")
                else:
                    print(f"❌ 问答失败: {response.status_code}")
        else:
            print(f"❌ 聊天会话创建失败: {response.status_code}")
    except Exception as e:
        print(f"❌ AI聊天机器人测试异常: {e}")
    
    # 3. 测试多银行搜索
    print("\n3. 测试多银行搜索...")
    try:
        response = requests.get(
            'http://localhost:8000/api/v1/web/search/banks?query=贷款产品',
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 多银行搜索成功")
            print(f"📊 搜索银行数: {data['data']['total_banks']}")
            print(f"✅ 成功银行数: {data['data']['successful_banks']}")
            
            for bank_name, bank_data in data['data']['banks'].items():
                if not bank_data.get('error'):
                    print(f"  {bank_name}: {len(bank_data.get('products', []))}个产品")
        else:
            print(f"❌ 多银行搜索失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 多银行搜索异常: {e}")
    
    print("\n🎉 网络搜索功能测试完成！")

if __name__ == "__main__":
    test_web_search()
