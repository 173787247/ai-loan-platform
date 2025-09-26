#!/usr/bin/env python3
"""
AI贷款智能体系统综合功能测试
验证所有核心功能的正确性和稳定性
"""

import requests
import json
import time
import sys

def test_health_check():
    """测试服务健康状态"""
    print("🔍 1. 测试服务健康状态")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ AI服务健康: {health_data.get('status')}")
            print(f"   版本: {health_data.get('version')}")
            print(f"   GPU可用: {health_data.get('gpu_available')}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_loan_agent_basic():
    """测试贷款智能体基础功能"""
    print("\n🤖 2. 测试贷款智能体基础功能")
    print("-" * 40)
    
    user_id = "test-comprehensive"
    
    # 重置用户档案
    try:
        response = requests.post(f"http://localhost:8000/api/v1/loan-agent/reset/{user_id}")
        if response.status_code == 200:
            print("✅ 用户档案重置成功")
        else:
            print(f"❌ 重置失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 重置异常: {e}")
        return False
    
    # 测试对话流程
    test_messages = [
        "你好，我想申请贷款",
        "我叫测试用户，电话13800138000，我想申请50万元用于经营，期限24个月，在北京申请",
        "我月收入15000元，是经营收入，工作5年了",
        "我有房贷月供4000元，信用卡月还款1000元",
        "我信用评分750分，没有逾期记录，有房产抵押",
        "确认"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"  测试 {i}: {message[:30]}...")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/loan-agent/chat",
                json={
                    "user_id": user_id,
                    "message": message,
                    "session_id": f"session-{user_id}"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    current_state = data.get("current_state", "未知")
                    profile = data.get("profile", {})
                    
                    print(f"    ✅ 状态: {current_state}")
                    
                    # 检查关键信息提取
                    if profile.get("name"):
                        print(f"    ✅ 提取姓名: {profile['name']}")
                    if profile.get("amount"):
                        print(f"    ✅ 提取金额: {profile['amount']}万元")
                    if profile.get("purpose"):
                        print(f"    ✅ 提取用途: {profile['purpose']}")
                    
                    # 检查是否到达报价阶段
                    if current_state == "quotation" or "方案" in data.get("response", ""):
                        print("    🎉 到达报价阶段")
                        break
                else:
                    print(f"    ❌ 对话失败: {result.get('message')}")
            else:
                print(f"    ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"    ❌ 请求异常: {e}")
        
        time.sleep(0.5)
    
    return True

def test_risk_pricing_service():
    """测试风控定价服务"""
    print("\n💰 3. 测试风控定价服务")
    print("-" * 40)
    
    # 测试风控评估
    test_profile = {
        "user_id": "test-risk",
        "name": "测试用户",
        "credit_score": 750,
        "monthly_income": 15000,
        "monthly_debt_payment": 5000,
        "work_years": 5,
        "has_collateral": True,
        "amount": 50,
        "term": 24,
        "purpose": "经营"
    }
    
    try:
        # 通过贷款智能体测试风控定价
        response = requests.post(
            "http://localhost:8000/api/v1/loan-agent/chat",
            json={
                "user_id": "test-risk-pricing",
                "message": "我信用评分750分，月收入15000元，有房贷月供5000元，工作5年，有房产抵押，想申请50万元经营贷款24个月",
                "session_id": "test-session"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                response_text = data.get("response", "")
                
                if "方案" in response_text or "利率" in response_text:
                    print("✅ 风控定价服务正常")
                    print("   检测到报价方案生成")
                    return True
                else:
                    print("⚠️ 风控定价服务可能异常")
                    print(f"   响应内容: {response_text[:100]}...")
                    return False
            else:
                print(f"❌ 风控定价测试失败: {result.get('message')}")
                return False
        else:
            print(f"❌ 风控定价API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 风控定价测试异常: {e}")
        return False

def test_rfq_service():
    """测试助贷招标服务"""
    print("\n🏦 4. 测试助贷招标服务")
    print("-" * 40)
    
    # 测试RFQ创建
    borrower_profile = {
        "user_id": "test-rfq",
        "name": "测试借款人",
        "amount": 50,
        "term": 24,
        "purpose": "经营",
        "credit_score": 750,
        "monthly_income": 15000,
        "debt_ratio": 0.33,
        "has_collateral": True,
        "risk_level": "中低风险"
    }
    
    try:
        # 创建RFQ
        response = requests.post(
            "http://localhost:8000/api/v1/rfq/create",
            json={"borrower_profile": borrower_profile},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                rfq_id = result.get("data", {}).get("rfq_id")
                print(f"✅ RFQ创建成功: {rfq_id}")
                
                # 发布RFQ
                publish_response = requests.post(
                    f"http://localhost:8000/api/v1/rfq/{rfq_id}/publish",
                    json={"deadline_hours": 72},
                    timeout=30
                )
                
                if publish_response.status_code == 200:
                    print("✅ RFQ发布成功")
                    
                    # 模拟投标
                    bid_data = {
                        "lender_id": "bank_001",
                        "bid_data": {
                            "product_name": "闪电贷",
                            "offered_amount": 50,
                            "offered_rate": 5.2,
                            "offered_term": 24,
                            "processing_fee": 500,
                            "conditions": ["需要招商银行代发工资"],
                            "approval_time": 3,
                            "notes": "测试投标"
                        }
                    }
                    
                    bid_response = requests.post(
                        f"http://localhost:8000/api/v1/rfq/{rfq_id}/bid",
                        json=bid_data,
                        timeout=30
                    )
                    
                    if bid_response.status_code == 200:
                        print("✅ 投标提交成功")
                        
                        # 获取投标列表
                        bids_response = requests.get(
                            f"http://localhost:8000/api/v1/rfq/{rfq_id}/bids",
                            timeout=30
                        )
                        
                        if bids_response.status_code == 200:
                            bids_result = bids_response.json()
                            if bids_result.get("success"):
                                bids = bids_result.get("data", {}).get("bids", [])
                                print(f"✅ 获取投标列表成功: {len(bids)} 个投标")
                                return True
                            else:
                                print(f"❌ 获取投标列表失败: {bids_result.get('message')}")
                                return False
                        else:
                            print(f"❌ 获取投标列表API调用失败: {bids_response.status_code}")
                            return False
                    else:
                        print(f"❌ 投标提交失败: {bid_response.status_code}")
                        return False
                else:
                    print(f"❌ RFQ发布失败: {publish_response.status_code}")
                    return False
            else:
                print(f"❌ RFQ创建失败: {result.get('message')}")
                return False
        else:
            print(f"❌ RFQ创建API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 助贷招标测试异常: {e}")
        return False

def test_frontend_access():
    """测试前端访问"""
    print("\n🌐 5. 测试前端访问")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ 前端服务可访问")
            return True
        else:
            print(f"❌ 前端访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端访问异常: {e}")
        return False

def test_rag_service():
    """测试RAG检索服务"""
    print("\n🔍 6. 测试RAG检索服务")
    print("-" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/rag/search",
            json={
                "query": "招商银行个人信用贷款产品",
                "max_results": 3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                results = data.get("results", [])
                print(f"✅ RAG检索成功: 找到 {len(results)} 条结果")
                
                if results:
                    print("   知识库内容正常")
                    return True
                else:
                    print("⚠️ 知识库可能为空")
                    return False
            else:
                print(f"❌ RAG检索失败: {result.get('message')}")
                return False
        else:
            print(f"❌ RAG检索API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ RAG检索测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI贷款智能体系统综合功能测试")
    print("=" * 60)
    
    test_results = []
    
    # 执行所有测试
    test_results.append(("服务健康检查", test_health_check()))
    test_results.append(("贷款智能体基础功能", test_loan_agent_basic()))
    test_results.append(("风控定价服务", test_risk_pricing_service()))
    test_results.append(("助贷招标服务", test_rfq_service()))
    test_results.append(("前端访问", test_frontend_access()))
    test_results.append(("RAG检索服务", test_rag_service()))
    
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
        return True
    else:
        print("⚠️ 部分功能测试失败，需要检查相关服务。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
