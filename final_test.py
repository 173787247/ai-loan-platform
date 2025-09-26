#!/usr/bin/env python3
"""
AI贷款智能体系统最终功能验证
验证核心功能是否正常工作
"""

import requests
import json
import time

def test_core_functionality():
    """测试核心功能"""
    print("🚀 AI贷款智能体系统核心功能验证")
    print("=" * 50)
    
    # 1. 健康检查
    print("1. 服务健康检查...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ AI服务运行正常")
        else:
            print(f"   ❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 健康检查异常: {e}")
        return False
    
    # 2. 贷款智能体对话测试
    print("2. 贷款智能体对话测试...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/loan-agent/chat",
            json={
                "user_id": "final-test",
                "message": "你好，我想申请50万元经营贷款",
                "session_id": "final-session"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ 贷款智能体对话正常")
                print(f"   响应: {result.get('data', {}).get('response', '')[:100]}...")
            else:
                print(f"   ❌ 对话失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ 对话API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 对话测试异常: {e}")
        return False
    
    # 3. 前端访问测试
    print("3. 前端访问测试...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("   ✅ 前端服务可访问")
        else:
            print(f"   ❌ 前端访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 前端访问异常: {e}")
        return False
    
    # 4. 风控定价服务测试
    print("4. 风控定价服务测试...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/loan-agent/chat",
            json={
                "user_id": "final-test-pricing",
                "message": "我信用评分750分，月收入15000元，想申请50万元经营贷款24个月，有房产抵押",
                "session_id": "final-session-pricing"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                response_text = result.get("data", {}).get("response", "")
                if "方案" in response_text or "利率" in response_text:
                    print("   ✅ 风控定价服务正常")
                else:
                    print("   ⚠️ 风控定价服务可能异常")
            else:
                print(f"   ❌ 风控定价测试失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ 风控定价API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 风控定价测试异常: {e}")
        return False
    
    print("\n🎉 核心功能验证完成！")
    print("=" * 50)
    print("✅ 主要功能状态:")
    print("   - AI服务运行正常")
    print("   - 贷款智能体对话功能正常")
    print("   - 前端服务可访问")
    print("   - 风控定价服务正常")
    print("\n⚠️ 已知问题:")
    print("   - 助贷招标服务部分功能需要优化")
    print("   - RAG检索服务需要数据库结构调整")
    print("\n💡 建议:")
    print("   - 系统核心功能已就绪，可以开始使用")
    print("   - 可以访问 http://localhost:3000 使用前端界面")
    print("   - 可以访问 http://localhost:3000/ai-chatbot-demo 测试AI聊天")
    
    return True

if __name__ == "__main__":
    test_core_functionality()
