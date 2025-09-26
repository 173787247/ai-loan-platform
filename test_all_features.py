#!/usr/bin/env python3
"""
AI贷款智能体系统完整功能测试
测试所有已完成的功能模块
"""

import requests
import json
import time

def test_ai_chatbot():
    """测试AI聊天机器人"""
    print("🤖 测试AI聊天机器人")
    print("-" * 40)
    
    try:
        # 测试创建会话
        response = requests.post(
            "http://localhost:8000/api/v1/ai-chatbot/create-session",
            json={"user_id": "test_user"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                session_id = result.get("data", {}).get("session_id")
                print(f"   ✅ 会话创建成功: {session_id}")
                
                # 测试发送消息
                response = requests.post(
                    "http://localhost:8000/api/v1/ai-chatbot/process-message",
                    json={
                        "user_id": "test_user",
                        "message": "你好，我想了解贷款产品",
                        "session_id": session_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        response_text = result.get("data", {}).get("response", "")
                        print(f"   ✅ 消息处理成功")
                        print(f"   AI回复: {response_text[:100]}...")
                        return True
                    else:
                        print(f"   ❌ 消息处理失败: {result.get('message')}")
                        return False
                else:
                    print(f"   ❌ 消息发送失败: {response.status_code}")
                    return False
            else:
                print(f"   ❌ 会话创建失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ 会话创建API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ AI聊天机器人测试异常: {e}")
        return False

def test_loan_agent():
    """测试贷款智能体"""
    print("\n🏦 测试贷款智能体")
    print("-" * 40)
    
    try:
        # 重置用户档案
        response = requests.post(
            "http://localhost:8000/api/v1/loan-agent/reset/test_loan_agent",
            timeout=30
        )
        
        if response.status_code == 200:
            print("   ✅ 用户档案重置成功")
        else:
            print(f"   ❌ 用户档案重置失败: {response.status_code}")
            return False
        
        # 测试对话流程
        test_messages = [
            "你好，我想申请贷款",
            "我叫张三，电话13800138000，想申请50万元经营贷款",
            "我月收入20000元，工作3年了"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"   {i}. 测试消息: {message[:30]}...")
            
            response = requests.post(
                "http://localhost:8000/api/v1/loan-agent/chat",
                json={
                    "user_id": "test_loan_agent",
                    "message": message,
                    "session_id": "test_session"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    current_state = data.get("current_state", "未知")
                    print(f"      ✅ 状态: {current_state}")
                else:
                    print(f"      ❌ 对话失败: {result.get('message')}")
                    return False
            else:
                print(f"      ❌ 对话API调用失败: {response.status_code}")
                return False
        
        print("   ✅ 贷款智能体测试完成")
        return True
        
    except Exception as e:
        print(f"   ❌ 贷款智能体测试异常: {e}")
        return False

def test_rag_service():
    """测试RAG检索服务"""
    print("\n🔍 测试RAG检索服务")
    print("-" * 40)
    
    test_queries = [
        "招商银行个人信用贷款",
        "贷款利率",
        "个人信用贷款"
    ]
    
    success_count = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"   {i}. 测试查询: {query}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/rag/search",
                json={
                    "query": query,
                    "search_type": "text",
                    "max_results": 3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    results = data.get("results", [])
                    total_found = data.get("total_results", 0)
                    
                    if total_found > 0:
                        success_count += 1
                        print(f"      ✅ 找到 {total_found} 条结果")
                    else:
                        print(f"      ⚠️ 未找到结果")
                else:
                    print(f"      ❌ 搜索失败: {result.get('message')}")
            else:
                print(f"      ❌ 搜索API调用失败: {response.status_code}")
        except Exception as e:
            print(f"      ❌ 搜索异常: {e}")
    
    print(f"   RAG检索成功率: {success_count}/{len(test_queries)}")
    return success_count > 0

def test_rfq_service():
    """测试助贷招标服务"""
    print("\n🏦 测试助贷招标服务")
    print("-" * 40)
    
    try:
        # 创建RFQ
        borrower_profile = {
            "user_id": "test_rfq",
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
        
        response = requests.post(
            "http://localhost:8000/api/v1/rfq/create",
            json={"borrower_profile": borrower_profile},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                rfq_id = result.get("data", {}).get("rfq_id")
                print(f"   ✅ RFQ创建成功: {rfq_id}")
                
                # 发布RFQ
                response = requests.post(
                    f"http://localhost:8000/api/v1/rfq/{rfq_id}/publish",
                    json={"deadline_hours": 72},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("   ✅ RFQ发布成功")
                    
                    # 提交投标
                    bid_data = {
                        "lender_id": "test_bank_001",
                        "bid_data": {
                            "product_name": "测试贷款产品",
                            "offered_amount": 30,
                            "offered_rate": 5.5,
                            "offered_term": 24,
                            "processing_fee": 500,
                            "conditions": ["需要银行代发工资"],
                            "approval_time": 3,
                            "notes": "测试投标"
                        }
                    }
                    
                    response = requests.post(
                        f"http://localhost:8000/api/v1/rfq/{rfq_id}/bid",
                        json=bid_data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        print("   ✅ 投标提交成功")
                        
                        # 获取投标列表
                        response = requests.get(
                            f"http://localhost:8000/api/v1/rfq/{rfq_id}/bids",
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("success"):
                                data = result.get("data", {})
                                total_bids = data.get("total_bids", 0)
                                print(f"   ✅ 获取投标列表成功: {total_bids} 个投标")
                                return True
                            else:
                                print(f"   ❌ 获取投标列表失败: {result.get('message')}")
                                return False
                        else:
                            print(f"   ❌ 获取投标列表API调用失败: {response.status_code}")
                            return False
                    else:
                        print(f"   ❌ 投标提交失败: {response.status_code}")
                        return False
                else:
                    print(f"   ❌ RFQ发布失败: {response.status_code}")
                    return False
            else:
                print(f"   ❌ RFQ创建失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ RFQ创建API调用失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 助贷招标服务测试异常: {e}")
        return False

def test_frontend_access():
    """测试前端访问"""
    print("\n🌐 测试前端访问")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("   ✅ 前端主页可访问")
            
            # 测试聊天页面
            response = requests.get("http://localhost:3000/ai-chatbot-demo", timeout=10)
            if response.status_code == 200:
                print("   ✅ AI聊天页面可访问")
                return True
            else:
                print(f"   ❌ AI聊天页面访问失败: {response.status_code}")
                return False
        else:
            print(f"   ❌ 前端主页访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 前端访问异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI贷款智能体系统完整功能测试")
    print("=" * 60)
    
    # 执行所有测试
    test_results = []
    
    test_results.append(("AI聊天机器人", test_ai_chatbot()))
    test_results.append(("贷款智能体", test_loan_agent()))
    test_results.append(("RAG检索服务", test_rag_service()))
    test_results.append(("助贷招标服务", test_rfq_service()))
    test_results.append(("前端访问", test_frontend_access()))
    
    # 输出测试结果
    print("\n📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有功能测试通过！系统运行正常。")
    else:
        print("⚠️ 部分功能测试失败，需要检查相关服务。")
    
    print("\n💡 使用建议:")
    print("1. 访问 http://localhost:3000 使用主界面")
    print("2. 访问 http://localhost:3000/ai-chatbot-demo 测试AI聊天")
    print("3. 使用API进行高级功能测试")

if __name__ == "__main__":
    main()
