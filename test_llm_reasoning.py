#!/usr/bin/env python3
"""
直接测试LLM推理
"""

import requests
import json
import time

def test_llm_reasoning():
    """直接测试LLM推理"""
    print("🤖 直接测试LLM推理...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    test_messages = [
        "介绍一下国外有哪些银行在中国有业务？",
        "国外银行在中国有业务吗",
        "请介绍一下花旗银行",
        "汇丰银行有什么贷款产品？"
    ]
    
    for message in test_messages:
        print(f"\n📝 测试消息: {message}")
        try:
            response = requests.post(
                'http://localhost:8000/api/v1/web/search/universal/detect',
                json={'message': message},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                bank_name = data['data']['bank_name']
                detected = data['data']['detected']
                print(f"✅ 检测结果: {bank_name if detected else '未检测到银行'}")
            else:
                print(f"❌ 检测失败: {response.status_code}")
                print(f"错误信息: {response.text}")
        except Exception as e:
            print(f"❌ 检测异常: {e}")
    
    print("\n🎉 LLM推理测试完成！")

if __name__ == "__main__":
    test_llm_reasoning()
