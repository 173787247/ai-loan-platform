#!/usr/bin/env python3
"""
AI贷款平台服务测试脚本
测试所有主要功能是否正常工作
"""

import requests
import json
import time
from datetime import datetime

def test_service_health():
    """测试服务健康状态"""
    print("🔍 测试服务健康状态...")
    
    services = {
        "前端服务": "http://localhost:3000/",
        "AI服务": "http://localhost:8000/health",
        "网关服务": "http://localhost:8080/health"
    }
    
    results = {}
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: 正常 (状态码: {response.status_code})")
                results[name] = True
            else:
                print(f"❌ {name}: 异常 (状态码: {response.status_code})")
                results[name] = False
        except Exception as e:
            print(f"❌ {name}: 连接失败 - {e}")
            results[name] = False
    
    return results

def test_ai_chatbot():
    """测试AI聊天机器人"""
    print("\n🤖 测试AI聊天机器人...")
    
    try:
        # 测试创建会话
        session_data = {
            "user_id": "test_user_001",
            "role": "customer"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/ai-chatbot/create-session",
            json=session_data,
            timeout=10
        )
        
        if response.status_code == 200:
            session_info = response.json()
            session_id = session_info.get("data", {}).get("session_id")
            print(f"✅ 会话创建成功: {session_id}")
            
            # 测试发送消息
            message_data = {
                "session_id": session_id,
                "message": "你好，我想了解贷款产品"
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/ai-chatbot/process-message",
                json=message_data,
                timeout=30
            )
            
            if response.status_code == 200:
                message_info = response.json()
                print(f"✅ 消息处理成功: {message_info.get('data', {}).get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ 消息处理失败: {response.status_code}")
                return False
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI聊天机器人测试失败: {e}")
        return False

def test_risk_assessment():
    """测试风险评估"""
    print("\n🛡️ 测试风险评估...")
    
    try:
        risk_data = {
            "credit_score": 750,
            "annual_income": 200000,
            "monthly_income": 16667,
            "monthly_debt": 5000,
            "employment_years": 5,
            "age": 35,
            "marital_status": "married",
            "education": "bachelor",
            "industry": "科技"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/risk/advanced-assessment",
            json=risk_data,
            timeout=30
        )
        
        if response.status_code == 200:
            risk_info = response.json()
            print(f"✅ 风险评估成功: 风险等级 {risk_info.get('data', {}).get('risk_level', 'N/A')}")
            return True
        else:
            print(f"❌ 风险评估失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 风险评估测试失败: {e}")
        return False

def test_pricing_calculation():
    """测试定价计算"""
    print("\n💰 测试定价计算...")
    
    try:
        pricing_data = {
            "loan_request": {
                "loan_amount": 100000,
                "loan_term_months": 24,
                "loan_type": "personal_loan"
            },
            "risk_assessment": {
                "overall_risk_score": 0.3,
                "risk_level": "low"
            },
            "pricing_strategy": "risk_based"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/pricing/calculate",
            json=pricing_data,
            timeout=30
        )
        
        if response.status_code == 200:
            pricing_info = response.json()
            print(f"✅ 定价计算成功: 利率 {pricing_info.get('data', {}).get('final_interest_rate', 'N/A')}%")
            return True
        else:
            print(f"❌ 定价计算失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 定价计算测试失败: {e}")
        return False

def test_rag_search():
    """测试RAG搜索"""
    print("\n🔍 测试RAG搜索...")
    
    try:
        search_data = {
            "query": "招商银行",
            "search_type": "simple",
            "max_results": 5
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/rag/search",
            json=search_data,
            timeout=30
        )
        
        if response.status_code == 200:
            search_info = response.json()
            results_count = len(search_info.get('data', {}).get('results', []))
            print(f"✅ RAG搜索成功: 找到 {results_count} 条结果")
            return True
        else:
            print(f"❌ RAG搜索失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ RAG搜索测试失败: {e}")
        return False

def test_frontend_pages():
    """测试前端页面"""
    print("\n🌐 测试前端页面...")
    
    pages = [
        "http://localhost:3000/",
        "http://localhost:3000/ai-chatbot-demo",
        "http://localhost:3000/loan-application"
    ]
    
    results = []
    for page in pages:
        try:
            response = requests.get(page, timeout=10)
            if response.status_code == 200:
                print(f"✅ 页面访问成功: {page}")
                results.append(True)
            else:
                print(f"❌ 页面访问失败: {page} (状态码: {response.status_code})")
                results.append(False)
        except Exception as e:
            print(f"❌ 页面访问失败: {page} - {e}")
            results.append(False)
    
    return all(results)

def main():
    """主测试函数"""
    print("🚀 AI贷款平台服务测试开始")
    print("=" * 50)
    
    # 测试服务健康状态
    health_results = test_service_health()
    
    # 测试AI聊天机器人
    chatbot_result = test_ai_chatbot()
    
    # 测试风险评估
    risk_result = test_risk_assessment()
    
    # 测试定价计算
    pricing_result = test_pricing_calculation()
    
    # 测试RAG搜索
    rag_result = test_rag_search()
    
    # 测试前端页面
    frontend_result = test_frontend_pages()
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    all_results = {
        "服务健康状态": all(health_results.values()),
        "AI聊天机器人": chatbot_result,
        "风险评估": risk_result,
        "定价计算": pricing_result,
        "RAG搜索": rag_result,
        "前端页面": frontend_result
    }
    
    for test_name, result in all_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    total_passed = sum(all_results.values())
    total_tests = len(all_results)
    
    print(f"\n🎯 总体结果: {total_passed}/{total_tests} 项测试通过")
    
    if total_passed == total_tests:
        print("🎉 所有测试通过！系统运行正常！")
    else:
        print("⚠️ 部分测试失败，请检查相关服务")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
