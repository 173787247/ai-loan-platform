#!/usr/bin/env python3
"""
测试通用银行搜索功能
"""

import requests
import json
import time

def test_universal_bank_search():
    """测试通用银行搜索功能"""
    print("🌐 测试通用银行搜索功能...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    # 1. 测试银行名称检测
    print("\n1. 测试银行名称检测...")
    test_messages = [
        "请介绍一下光大银行",
        "民生银行有什么贷款产品？",
        "我想了解交通银行的利率",
        "中信银行的客服电话是多少？",
        "华夏银行怎么样？",
        "我想申请广发银行的贷款",
        "平安银行和招商银行哪个好？",
        "邮储银行的申请条件是什么？",
        "北京银行有什么特色？",
        "上海银行的贷款额度是多少？"
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
    
    # 2. 测试已知银行搜索
    print("\n2. 测试已知银行搜索...")
    known_banks = ["光大银行", "民生银行", "交通银行", "中信银行", "华夏银行"]
    
    for bank in known_banks:
        try:
            response = requests.post(
                'http://localhost:8000/api/v1/web/search/universal/bank',
                json={
                    'bank_name': bank,
                    'query': '贷款产品'
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                products = data['data']['products']
                source = data['data']['source']
                print(f"✅ {bank}: {len(products)}个产品，来源: {source}")
            else:
                print(f"❌ {bank}: 搜索失败")
        except Exception as e:
            print(f"❌ {bank}: 异常 - {e}")
    
    # 3. 测试未知银行搜索
    print("\n3. 测试未知银行搜索...")
    unknown_banks = ["地方银行", "农商银行", "城商银行", "村镇银行"]
    
    for bank in unknown_banks:
        try:
            response = requests.post(
                'http://localhost:8000/api/v1/web/search/universal/bank',
                json={
                    'bank_name': bank,
                    'query': '贷款产品'
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                products = data['data']['products']
                source = data['data']['source']
                print(f"✅ {bank}: {len(products)}个产品，来源: {source}")
            else:
                print(f"❌ {bank}: 搜索失败")
        except Exception as e:
            print(f"❌ {bank}: 异常 - {e}")
    
    # 4. 测试AI聊天机器人
    print("\n4. 测试AI聊天机器人...")
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
                "请介绍一下交通银行",
                "中信银行有什么贷款产品？",
                "华夏银行的贷款利率是多少？",
                "广发银行的客服电话是多少？",
                "平安银行和招商银行有什么区别？",
                "地方银行有什么特色？"
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
    
    # 5. 测试多银行搜索
    print("\n5. 测试多银行搜索...")
    try:
        response = requests.get(
            'http://localhost:8000/api/v1/web/search/universal/banks?query=贷款产品',
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
    
    print("\n🎉 通用银行搜索功能测试完成！")

if __name__ == "__main__":
    test_universal_bank_search()
