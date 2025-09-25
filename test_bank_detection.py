#!/usr/bin/env python3
"""
直接测试银行检测API
"""

import requests
import json
import time

def test_bank_detection():
    """直接测试银行检测API"""
    print("🔍 直接测试银行检测API...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    test_messages = [
        "花旗银行的产品能在中国销售吗",
        "请介绍一下花旗银行",
        "花旗银行有什么贷款产品？",
        "花旗银行的利率是多少？",
        "中国银行和花旗银行哪个好",
        "我想了解中国银行的产品",
        "请介绍一下中国银行"
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
    
    print("\n🎉 银行检测API测试完成！")

if __name__ == "__main__":
    test_bank_detection()
