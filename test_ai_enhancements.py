#!/usr/bin/env python3
"""
测试AI增强功能
"""

import requests
import json
import time

def test_ai_enhancements():
    """测试AI增强功能"""
    print("🧠 AI增强功能测试")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    test_user_id = "test_user_123"
    test_session_id = "test_session_456"
    
    # 1. 测试增强AI聊天
    print("1. 测试增强AI聊天...")
    try:
        response = requests.post(f"{base_url}/ai/enhanced-chat", json={
            "user_id": test_user_id,
            "message": "你好，我想了解个人信用贷款",
            "session_id": test_session_id
        }, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                print(f"   ✅ 增强聊天成功")
                print(f"   💬 回复: {data.get('response', '')[:100]}...")
                print(f"   🎯 置信度: {data.get('confidence', 0):.2f}")
                print(f"   🔄 下一状态: {data.get('next_state', '')}")
                print(f"   ❓ 建议问题: {len(data.get('suggested_questions', []))} 个")
            else:
                print(f"   ❌ 增强聊天失败: {result.get('message')}")
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    # 2. 测试个性化推荐
    print("\n2. 测试个性化推荐...")
    try:
        response = requests.get(f"{base_url}/ai/personalized-recommendations/{test_user_id}?max_recommendations=3", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                recommendations = data.get("recommendations", [])
                print(f"   ✅ 个性化推荐成功")
                print(f"   📊 推荐数量: {len(recommendations)}")
                for i, rec in enumerate(recommendations[:2], 1):
                    print(f"   {i}. {rec.get('title', '')} (相关性: {rec.get('relevance_score', 0):.2f})")
            else:
                print(f"   ❌ 个性化推荐失败: {result.get('message')}")
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    # 3. 测试增强知识库搜索
    print("\n3. 测试增强知识库搜索...")
    try:
        response = requests.get(f"{base_url}/ai/enhanced-knowledge/search?query=个人信用贷款&max_results=3", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                results = data.get("results", [])
                print(f"   ✅ 增强知识库搜索成功")
                print(f"   📚 搜索结果: {len(results)} 条")
                for i, result in enumerate(results[:2], 1):
                    print(f"   {i}. {result.get('title', '')} (相关性: {result.get('relevance_score', 0):.2f})")
            else:
                print(f"   ❌ 增强知识库搜索失败: {result.get('message')}")
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    # 4. 测试对话摘要
    print("\n4. 测试对话摘要...")
    try:
        response = requests.get(f"{base_url}/ai/dialog-summary/{test_session_id}", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                print(f"   ✅ 对话摘要成功")
                print(f"   💬 对话轮数: {data.get('turn_count', 0)}")
                print(f"   🎯 当前状态: {data.get('current_state', '')}")
                print(f"   📝 当前话题: {data.get('current_topic', '')}")
            else:
                print(f"   ❌ 对话摘要失败: {result.get('message')}")
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    # 5. 测试用户画像
    print("\n5. 测试用户画像...")
    try:
        response = requests.get(f"{base_url}/ai/user-profile/{test_user_id}", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                print(f"   ✅ 用户画像成功")
                print(f"   👤 用户类型: {data.get('profile_type', '')}")
                print(f"   💰 收入范围: {data.get('income_range', '')}")
                print(f"   🎯 兴趣: {', '.join(data.get('interests', []))}")
                print(f"   📊 交互次数: {data.get('interaction_count', 0)}")
            else:
                print(f"   ❌ 用户画像失败: {result.get('message')}")
        elif response.status_code == 404:
            print(f"   ℹ️ 用户画像不存在（新用户）")
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print(f"\n🎉 AI增强功能测试完成！")

def test_multi_turn_conversation():
    """测试多轮对话"""
    print(f"\n🔄 多轮对话测试")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    test_user_id = "multi_turn_user"
    test_session_id = "multi_turn_session"
    
    conversation_messages = [
        "你好，我想了解贷款产品",
        "个人信用贷款需要什么条件？",
        "利率是多少？",
        "如何申请？",
        "谢谢，我明白了"
    ]
    
    for i, message in enumerate(conversation_messages, 1):
        print(f"{i}. 用户: {message}")
        
        try:
            response = requests.post(f"{base_url}/ai/enhanced-chat", json={
                "user_id": test_user_id,
                "message": message,
                "session_id": test_session_id
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    print(f"   AI: {data.get('response', '')[:100]}...")
                    print(f"   状态: {data.get('next_state', '')} | 置信度: {data.get('confidence', 0):.2f}")
                    
                    if data.get('suggested_questions'):
                        print(f"   建议问题: {data.get('suggested_questions')[0]}")
                else:
                    print(f"   ❌ 响应失败: {result.get('message')}")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
        
        print()

if __name__ == "__main__":
    test_ai_enhancements()
    test_multi_turn_conversation()
