#!/usr/bin/env python3
"""
调试网关路由问题
"""
import requests
import json
import time

def test_gateway_debug():
    """调试网关路由问题"""
    print("=== 调试网关路由问题 ===")
    
    # 等待网关完全启动
    print("等待网关完全启动...")
    time.sleep(5)
    
    # 测试网关健康检查
    try:
        response = requests.get("http://localhost:8080/actuator/health", timeout=10)
        print(f"✅ 网关健康检查: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   网关状态: {health_data.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ 网关健康检查失败: {e}")
        return
    
    # 测试AI服务直接访问
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"✅ AI服务直接访问: {response.status_code}")
        if response.status_code == 200:
            ai_data = response.json()
            print(f"   AI服务状态: {ai_data.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ AI服务直接访问失败: {e}")
        return
    
    # 测试网关路由到AI服务
    print("\n=== 测试网关路由到AI服务 ===")
    try:
        response = requests.get("http://localhost:8080/api/ai/health", timeout=10)
        print(f"网关路由状态码: {response.status_code}")
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
        print(f"网关路由状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 网关路由成功!")
        else:
            print("❌ 网关路由失败")
            
    except Exception as e:
        print(f"❌ 网关路由测试失败: {e}")

if __name__ == "__main__":
    test_gateway_debug()
