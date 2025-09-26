#!/usr/bin/env python3
"""
快速测试脚本
快速验证核心功能是否正常
"""

import requests
import json

def quick_test():
    """快速测试核心功能"""
    print("⚡ AI贷款智能体系统快速测试")
    print("=" * 40)
    
    # 1. 检查服务状态
    print("1. 检查服务状态...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ AI服务正常")
        else:
            print("   ❌ AI服务异常")
            return False
    except:
        print("   ❌ AI服务无法访问")
        return False
    
    # 2. 测试AI聊天
    print("2. 测试AI聊天...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/chat/session",
            json={"user_id": "quick_test", "chatbot_role": "general"},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                session_id = result.get("data", {}).get("session_id")
                
                response = requests.post(
                    "http://localhost:8000/api/v1/chat/message",
                    json={
                        "session_id": session_id,
                        "message": "你好",
                        "user_info": {"user_id": "quick_test"}
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    print("   ✅ AI聊天正常")
                else:
                    print("   ❌ AI聊天异常")
                    return False
            else:
                print("   ❌ 会话创建失败")
                return False
        else:
            print("   ❌ 会话创建API异常")
            return False
    except:
        print("   ❌ AI聊天测试异常")
        return False
    
    # 3. 测试RAG检索
    print("3. 测试RAG检索...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/rag/search",
            json={
                "query": "个人信用贷款",
                "search_type": "text",
                "max_results": 1
            },
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                results = data.get("results", [])
                if results:
                    print("   ✅ RAG检索正常")
                else:
                    print("   ⚠️ RAG检索无结果")
            else:
                print("   ❌ RAG检索失败")
                return False
        else:
            print("   ❌ RAG检索API异常")
            return False
    except:
        print("   ❌ RAG检索测试异常")
        return False
    
    # 4. 测试前端访问
    print("4. 测试前端访问...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("   ✅ 前端访问正常")
        else:
            print("   ❌ 前端访问异常")
            return False
    except:
        print("   ❌ 前端访问失败")
        return False
    
    print("\n🎉 快速测试完成！核心功能正常")
    print("\n💡 接下来您可以:")
    print("1. 运行 python test_all_features.py 进行完整测试")
    print("2. 访问 http://localhost:3000 使用前端界面")
    print("3. 访问 http://localhost:3000/ai-chatbot-demo 测试AI聊天")
    
    return True

if __name__ == "__main__":
    quick_test()
