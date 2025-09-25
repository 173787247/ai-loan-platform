#!/usr/bin/env python3
"""
测试光大银行信息获取
"""

import requests
import json
import time

def test_guangda_bank():
    """测试光大银行信息获取"""
    print("🏦 测试光大银行信息获取...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    # 1. 测试光大银行信息搜索
    print("\n1. 测试光大银行信息搜索...")
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/web/search/bank',
            json={
                'bank_name': '光大银行',
                'query': '贷款产品'
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 光大银行信息搜索成功")
            print(f"📊 银行: {data['data']['bank_name']}")
            print(f"📞 客服: {data['data']['contact']}")
            print(f"🌐 官网: {data['data']['website']}")
            print(f"📝 产品数量: {len(data['data']['products'])}")
            print(f"🔄 数据来源: {data['data']['source']}")
            
            # 显示产品信息
            for i, product in enumerate(data['data']['products'], 1):
                print(f"  {i}. {product['title']}")
                print(f"     描述: {product['description']}")
                print(f"     利率: {product['rate']}")
                print(f"     额度: {product['amount']}")
                print(f"     期限: {product['term']}")
                print(f"     特点: {', '.join(product['features'])}")
                print()
        else:
            print(f"❌ 光大银行信息搜索失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 光大银行信息搜索异常: {e}")
    
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
            
            # 测试光大银行问题
            questions = [
                "请介绍一下光大银行",
                "光大银行有什么贷款产品？",
                "光大银行的贷款利率是多少？",
                "光大银行的客服电话是多少？",
                "光大银行和招商银行有什么区别？"
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
                    print(f"🤖 AI回答: {answer}")
                else:
                    print(f"❌ 问答失败: {response.status_code}")
                    print(f"错误信息: {response.text}")
        else:
            print(f"❌ 聊天会话创建失败: {response.status_code}")
    except Exception as e:
        print(f"❌ AI聊天机器人测试异常: {e}")
    
    # 3. 测试其他银行
    print("\n3. 测试其他银行...")
    banks = ["民生银行", "兴业银行", "浦发银行"]
    
    for bank in banks:
        try:
            response = requests.post(
                'http://localhost:8000/api/v1/web/search/bank',
                json={
                    'bank_name': bank,
                    'query': '贷款产品'
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {bank}: {len(data['data']['products'])}个产品")
            else:
                print(f"❌ {bank}: 搜索失败")
        except Exception as e:
            print(f"❌ {bank}: 异常 - {e}")
    
    print("\n🎉 光大银行测试完成！")

if __name__ == "__main__":
    test_guangda_bank()
