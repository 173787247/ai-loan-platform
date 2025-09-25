#!/usr/bin/env python3
"""
测试Docker容器间网络连接
"""
import requests
import json

def test_network_connectivity():
    """测试网络连接"""
    print("=== 测试Docker容器间网络连接 ===")
    
    # 测试AI服务直接访问
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ AI服务直接访问: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"❌ AI服务直接访问失败: {e}")
    
    # 测试网关健康检查
    try:
        response = requests.get("http://localhost:8080/actuator/health", timeout=5)
        print(f"✅ 网关健康检查: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"❌ 网关健康检查失败: {e}")
    
    # 测试网关路由到AI服务
    try:
        response = requests.get("http://localhost:8080/api/ai/health", timeout=5)
        print(f"✅ 网关路由到AI服务: {response.status_code}")
        print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 网关路由到AI服务失败: {e}")
    
    # 测试网关路由到用户服务
    try:
        response = requests.get("http://localhost:8080/api/users/health", timeout=5)
        print(f"✅ 网关路由到用户服务: {response.status_code}")
        print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 网关路由到用户服务失败: {e}")

if __name__ == "__main__":
    test_network_connectivity()
