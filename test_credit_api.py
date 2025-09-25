#!/usr/bin/env python3
"""
测试征信API功能
"""

import requests
import json
import time

def test_credit_api():
    """测试征信API"""
    base_url = "http://localhost:8000"
    
    print("🧪 测试征信API功能...")
    
    # 1. 测试健康检查
    try:
        response = requests.get(f"{base_url}/api/v1/credit/health", timeout=10)
        if response.status_code == 200:
            print("✅ 征信API健康检查通过")
        else:
            print(f"❌ 征信API健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 征信API健康检查错误: {e}")
    
    # 2. 测试获取提供商列表
    try:
        response = requests.get(f"{base_url}/api/v1/credit/providers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ 获取提供商列表成功")
            print(f"   提供商数量: {len(data.get('data', {}).get('providers', []))}")
            for provider in data.get('data', {}).get('providers', []):
                print(f"   - {provider['name']}: {provider['remaining']}/{provider['free_quota']} 剩余")
        else:
            print(f"❌ 获取提供商列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取提供商列表错误: {e}")
    
    # 3. 测试征信查询
    test_companies = [
        "大洋晶典商业集团有限公司",
        "腾讯科技有限公司", 
        "阿里巴巴集团控股有限公司",
        "百度在线网络技术有限公司"
    ]
    
    for company in test_companies:
        print(f"\n🔍 测试查询企业: {company}")
        try:
            response = requests.post(
                f"{base_url}/api/v1/credit/query",
                json={
                    "company_name": company,
                    "provider": "jingdong"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    credit_data = data.get('data', {})
                    print(f"   ✅ 查询成功")
                    print(f"   信用评分: {credit_data.get('credit_score')}")
                    print(f"   信用等级: {credit_data.get('credit_level')}")
                    print(f"   数据来源: {credit_data.get('credit_source')}")
                    print(f"   是否模拟: {'是' if credit_data.get('is_mock') else '否'}")
                else:
                    print(f"   ❌ 查询失败: {data.get('message')}")
            else:
                print(f"   ❌ 查询失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 查询错误: {e}")
        
        time.sleep(1)  # 避免请求过快
    
    # 4. 测试使用统计
    try:
        response = requests.get(f"{base_url}/api/v1/credit/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("\n📊 使用统计:")
            stats = data.get('data', {})
            for provider, stat in stats.items():
                print(f"   {stat['name']}: {stat['used']}/{stat['quota']} 已使用")
        else:
            print(f"❌ 获取使用统计失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取使用统计错误: {e}")
    
    print("\n🎯 征信API测试完成！")

if __name__ == "__main__":
    test_credit_api()
