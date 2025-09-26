#!/usr/bin/env python3
"""
系统状态检查脚本
检查所有服务是否正常运行
"""

import requests
import json

def check_system_status():
    """检查系统状态"""
    print("🔍 AI贷款智能体系统状态检查")
    print("=" * 50)
    
    # 1. 检查AI服务
    print("1. 检查AI服务...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ AI服务正常 - 版本: {health_data.get('version')}")
            print(f"   GPU可用: {health_data.get('gpu_available')}")
        else:
            print(f"   ❌ AI服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ AI服务无法访问: {e}")
        return False
    
    # 2. 检查前端服务
    print("2. 检查前端服务...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("   ✅ 前端服务正常")
        else:
            print(f"   ❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 前端服务无法访问: {e}")
        return False
    
    # 3. 检查数据库连接
    print("3. 检查数据库连接...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/rag/search",
            json={
                "query": "测试",
                "search_type": "text",
                "max_results": 1
            },
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ 数据库连接正常")
        else:
            print(f"   ❌ 数据库连接异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
        return False
    
    print("\n🎉 系统状态检查完成！所有服务正常运行")
    return True

if __name__ == "__main__":
    check_system_status()
