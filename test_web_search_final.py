#!/usr/bin/env python3
"""
测试外网查询功能
"""

import requests
import json
import time

def test_web_search_capabilities():
    """测试外网查询能力"""
    print("🌐 测试LLM外网查询功能...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    # 1. 测试银行信息搜索
    print("\n1. 测试银行信息搜索...")
    banks_to_test = ["光大银行", "民生银行", "兴业银行", "浦发银行"]
    
    for bank in banks_to_test:
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
                products = data['data']['products']
                print(f"✅ {bank}: {len(products)}个产品，来源: {data['data']['source']}")
            else:
                print(f"❌ {bank}: 搜索失败")
        except Exception as e:
            print(f"❌ {bank}: 异常 - {e}")
    
    # 2. 测试AI聊天机器人外网查询
    print("\n2. 测试AI聊天机器人外网查询...")
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
            
            # 测试各种银行问题
            test_questions = [
                "请介绍一下光大银行",
                "民生银行有什么贷款产品？",
                "兴业银行的贷款利率是多少？",
                "浦发银行的客服电话是多少？",
                "招商银行和光大银行有什么区别？"
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
    
    print("\n🎉 外网查询功能测试完成！")

if __name__ == "__main__":
    test_web_search_capabilities()
