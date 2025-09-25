#!/usr/bin/env python3
"""
简单测试网关路由
"""
import requests
import json

def test_gateway_simple():
    """简单测试网关路由"""
    print("=== 简单测试网关路由 ===")
    
    # 测试网关健康检查
    try:
        response = requests.get("http://localhost:8080/actuator/health", timeout=5)
        print(f"✅ 网关健康检查: {response.status_code}")
        if response.status_code == 200:
            print("   网关服务正常运行")
    except Exception as e:
        print(f"❌ 网关健康检查失败: {e}")
        return
    
    # 测试网关路由到AI服务
    print("\n=== 测试网关路由到AI服务 ===")
    try:
        response = requests.get("http://localhost:8080/api/ai/health", timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 网关路由成功!")
        else:
            print("❌ 网关路由失败")
            
    except Exception as e:
        print(f"❌ 网关路由测试失败: {e}")
    
    # 测试网关路由到用户服务
    print("\n=== 测试网关路由到用户服务 ===")
    try:
        response = requests.get("http://localhost:8080/api/users/health", timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 网关路由成功!")
        else:
            print("❌ 网关路由失败")
            
    except Exception as e:
        print(f"❌ 网关路由测试失败: {e}")

if __name__ == "__main__":
    test_gateway_simple()