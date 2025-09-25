#!/usr/bin/env python3
"""
测试网关连接
"""
import requests
import json

def test_gateway_connection():
    """测试网关连接"""
    print("=== 测试网关连接 ===")
    
    # 测试网关健康检查
    try:
        response = requests.get("http://localhost:8080/actuator/health", timeout=5)
        print(f"✅ 网关健康检查: {response.status_code}")
        if response.status_code == 200:
            print("   网关服务正常运行")
    except Exception as e:
        print(f"❌ 网关健康检查失败: {e}")
        return
    
    # 测试AI服务直接访问
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ AI服务直接访问: {response.status_code}")
        if response.status_code == 200:
            print("   AI服务正常运行")
    except Exception as e:
        print(f"❌ AI服务直接访问失败: {e}")
        return
    
    # 测试网关路由到AI服务 - 使用不同的路径
    test_paths = [
        "/api/ai/health",
        "/api/ai/",
        "/api/ai",
        "/health"
    ]
    
    for path in test_paths:
        try:
            print(f"\n测试路径: {path}")
            response = requests.get(f"http://localhost:8080{path}", timeout=10)
            print(f"   状态码: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")
            if response.status_code == 200:
                print(f"   响应内容: {response.text[:200]}...")
                print("   ✅ 成功!")
                break
            else:
                print(f"   错误响应: {response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")

if __name__ == "__main__":
    test_gateway_connection()
