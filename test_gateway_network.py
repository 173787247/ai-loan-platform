#!/usr/bin/env python3
"""
测试网关网络连接
"""
import subprocess
import json

def test_gateway_network():
    """测试网关网络连接"""
    print("=== 测试网关网络连接 ===")
    
    # 检查所有容器状态
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                              capture_output=True, text=True, check=True)
        containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
        
        print("运行中的容器:")
        for container in containers:
            print(f"  - {container['Names']}: {container['Status']}")
        
        # 检查网关容器
        gateway_container = next((c for c in containers if 'ai-loan-gateway' in c['Names']), None)
        if gateway_container:
            print(f"\n✅ 网关容器状态: {gateway_container['Status']}")
        else:
            print("❌ 网关容器未找到")
            return
            
        # 检查AI服务容器
        ai_container = next((c for c in containers if 'ai-loan-ai-service' in c['Names']), None)
        if ai_container:
            print(f"✅ AI服务容器状态: {ai_container['Status']}")
        else:
            print("❌ AI服务容器未找到")
            return
            
    except Exception as e:
        print(f"❌ 检查容器状态失败: {e}")
        return
    
    # 测试网关容器内是否能连接到AI服务
    print("\n=== 测试网关容器内网络连接 ===")
    try:
        # 使用wget测试网络连通性
        result = subprocess.run(['docker', 'exec', 'ai-loan-gateway', 'wget', '-q', '--spider', 'http://ai-loan-ai-service:8000/health'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ 网关容器可以连接到AI服务")
        else:
            print(f"❌ 网关容器无法连接到AI服务: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("❌ 网络连接测试超时")
    except Exception as e:
        print(f"❌ 网络连接测试失败: {e}")
    
    # 测试网关容器内是否能解析AI服务名称
    print("\n=== 测试DNS解析 ===")
    try:
        result = subprocess.run(['docker', 'exec', 'ai-loan-gateway', 'nslookup', 'ai-loan-ai-service'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ 网关容器可以解析AI服务名称")
            print(f"   DNS解析结果: {result.stdout}")
        else:
            print(f"❌ 网关容器无法解析AI服务名称: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("❌ DNS解析测试超时")
    except Exception as e:
        print(f"❌ DNS解析测试失败: {e}")

if __name__ == "__main__":
    test_gateway_network()
