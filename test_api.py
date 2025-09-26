#!/usr/bin/env python3
"""
API接口测试脚本
测试所有API端点的功能
"""

import requests
import json

def test_api_endpoints():
    """测试API端点"""
    print("🔌 API接口测试")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # 1. 健康检查
    print("1. 健康检查 API")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ GET /health - 正常")
        else:
            print(f"   ❌ GET /health - 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ GET /health - 异常: {e}")
    
    # 2. AI聊天机器人API
    print("\n2. AI聊天机器人 API")
    try:
        # 创建会话
        response = requests.post(f"{base_url}/api/v1/ai-chatbot/create-session", 
                               json={"user_id": "api_test"})
        if response.status_code == 200:
            print("   ✅ POST /api/v1/ai-chatbot/create-session - 正常")
            session_id = response.json().get("data", {}).get("session_id")
            
            # 发送消息
            response = requests.post(f"{base_url}/api/v1/ai-chatbot/process-message",
                                   json={
                                       "user_id": "api_test",
                                       "message": "测试消息",
                                       "session_id": session_id
                                   })
            if response.status_code == 200:
                print("   ✅ POST /api/v1/ai-chatbot/process-message - 正常")
            else:
                print(f"   ❌ POST /api/v1/ai-chatbot/process-message - 失败: {response.status_code}")
        else:
            print(f"   ❌ POST /api/v1/ai-chatbot/create-session - 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ AI聊天机器人API - 异常: {e}")
    
    # 3. 贷款智能体API
    print("\n3. 贷款智能体 API")
    try:
        # 重置档案
        response = requests.post(f"{base_url}/api/v1/loan-agent/reset/api_test")
        if response.status_code == 200:
            print("   ✅ POST /api/v1/loan-agent/reset/{user_id} - 正常")
        else:
            print(f"   ❌ POST /api/v1/loan-agent/reset/{user_id} - 失败: {response.status_code}")
        
        # 对话
        response = requests.post(f"{base_url}/api/v1/loan-agent/chat",
                               json={
                                   "user_id": "api_test",
                                   "message": "我想申请贷款",
                                   "session_id": "test_session"
                               })
        if response.status_code == 200:
            print("   ✅ POST /api/v1/loan-agent/chat - 正常")
        else:
            print(f"   ❌ POST /api/v1/loan-agent/chat - 失败: {response.status_code}")
        
        # 获取档案
        response = requests.get(f"{base_url}/api/v1/loan-agent/profile/api_test")
        if response.status_code == 200:
            print("   ✅ GET /api/v1/loan-agent/profile/{user_id} - 正常")
        else:
            print(f"   ❌ GET /api/v1/loan-agent/profile/{user_id} - 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 贷款智能体API - 异常: {e}")
    
    # 4. RAG检索API
    print("\n4. RAG检索 API")
    try:
        # 文本搜索
        response = requests.post(f"{base_url}/api/v1/rag/search",
                               json={
                                   "query": "个人信用贷款",
                                   "search_type": "text",
                                   "max_results": 3
                               })
        if response.status_code == 200:
            print("   ✅ POST /api/v1/rag/search (text) - 正常")
        else:
            print(f"   ❌ POST /api/v1/rag/search (text) - 失败: {response.status_code}")
        
        # 向量搜索
        response = requests.post(f"{base_url}/api/v1/rag/search",
                               json={
                                   "query": "个人信用贷款",
                                   "search_type": "vector",
                                   "max_results": 3
                               })
        if response.status_code == 200:
            print("   ✅ POST /api/v1/rag/search (vector) - 正常")
        else:
            print(f"   ❌ POST /api/v1/rag/search (vector) - 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ RAG检索API - 异常: {e}")
    
    # 5. 助贷招标API
    print("\n5. 助贷招标 API")
    try:
        # 创建RFQ
        response = requests.post(f"{base_url}/api/v1/rfq/create",
                               json={
                                   "borrower_profile": {
                                       "user_id": "api_test_rfq",
                                       "name": "测试借款人",
                                       "amount": 30,
                                       "term": 24,
                                       "purpose": "经营",
                                       "credit_score": 750,
                                       "monthly_income": 15000,
                                       "debt_ratio": 0.3,
                                       "has_collateral": True,
                                       "risk_level": "中风险"
                                   }
                               })
        if response.status_code == 200:
            print("   ✅ POST /api/v1/rfq/create - 正常")
            rfq_id = response.json().get("data", {}).get("rfq_id")
            
            # 发布RFQ
            response = requests.post(f"{base_url}/api/v1/rfq/{rfq_id}/publish",
                                   json={"deadline_hours": 72})
            if response.status_code == 200:
                print("   ✅ POST /api/v1/rfq/{rfq_id}/publish - 正常")
            else:
                print(f"   ❌ POST /api/v1/rfq/{rfq_id}/publish - 失败: {response.status_code}")
        else:
            print(f"   ❌ POST /api/v1/rfq/create - 失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 助贷招标API - 异常: {e}")
    
    print("\n🎉 API接口测试完成！")

if __name__ == "__main__":
    test_api_endpoints()
