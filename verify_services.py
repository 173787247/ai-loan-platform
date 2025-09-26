#!/usr/bin/env python3
"""
专项验证：助贷招标服务和RAG检索服务
"""

import requests
import json
import time

def test_rfq_service():
    """测试助贷招标服务"""
    print("🏦 测试助贷招标服务")
    print("-" * 40)
    
    # 创建借款人档案
    borrower_profile = {
        "user_id": "verify-rfq",
        "name": "验证用户",
        "amount": 30,
        "term": 36,
        "purpose": "经营",
        "credit_score": 780,
        "monthly_income": 20000,
        "debt_ratio": 0.25,
        "has_collateral": True,
        "risk_level": "低风险"
    }
    
    try:
        # 1. 创建RFQ
        print("1. 创建RFQ...")
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
            else:
                print(f"   ❌ RFQ创建失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ RFQ创建API调用失败: {response.status_code}")
            return False
        
        # 2. 发布RFQ
        print("2. 发布RFQ...")
        response = requests.post(
            f"http://localhost:8000/api/v1/rfq/{rfq_id}/publish",
            json={"deadline_hours": 48},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ RFQ发布成功")
            else:
                print(f"   ❌ RFQ发布失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ RFQ发布API调用失败: {response.status_code}")
            return False
        
        # 3. 提交投标
        print("3. 提交投标...")
        bid_data = {
            "lender_id": "bank_verify_001",
            "bid_data": {
                "product_name": "验证测试贷",
                "offered_amount": 30,
                "offered_rate": 4.8,
                "offered_term": 36,
                "processing_fee": 300,
                "conditions": ["需要验证银行代发工资"],
                "approval_time": 2,
                "notes": "验证测试投标"
            }
        }
        
        response = requests.post(
            f"http://localhost:8000/api/v1/rfq/{rfq_id}/bid",
            json=bid_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ 投标提交成功")
            else:
                print(f"   ❌ 投标提交失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ 投标提交API调用失败: {response.status_code}")
            return False
        
        # 4. 获取投标列表
        print("4. 获取投标列表...")
        response = requests.get(
            f"http://localhost:8000/api/v1/rfq/{rfq_id}/bids",
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                bids = data.get("bids", [])
                total_bids = data.get("total_bids", 0)
                print(f"   ✅ 获取投标列表成功: {total_bids} 个投标")
                
                if bids:
                    print("   投标详情:")
                    for i, bid in enumerate(bids[:2], 1):  # 只显示前2个
                        print(f"     {i}. {bid.get('product_name', 'N/A')} - 利率: {bid.get('offered_rate', 'N/A')}%")
                
                return True
            else:
                print(f"   ❌ 获取投标列表失败: {result.get('message')}")
                return False
        else:
            print(f"   ❌ 获取投标列表API调用失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 助贷招标服务测试异常: {e}")
        return False

def test_rag_service():
    """测试RAG检索服务"""
    print("\n🔍 测试RAG检索服务")
    print("-" * 40)
    
    # 测试查询
    test_queries = [
        "招商银行个人信用贷款产品",
        "工商银行经营贷款利率",
        "建设银行房贷政策"
    ]
    
    success_count = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. 测试查询: {query}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/rag/search",
                json={
                    "query": query,
                    "max_results": 3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    results = data.get("results", [])
                    print(f"   ✅ 找到 {len(results)} 条结果")
                    
                    if results:
                        success_count += 1
                        print("   结果示例:")
                        for j, result_item in enumerate(results[:2], 1):  # 只显示前2个
                            content = result_item.get("content", "")[:100]
                            print(f"     {j}. {content}...")
                    else:
                        print("   ⚠️ 未找到相关结果")
                else:
                    print(f"   ❌ RAG检索失败: {result.get('message')}")
            else:
                print(f"   ❌ RAG检索API调用失败: {response.status_code}")
                print(f"   响应内容: {response.text}")
        except Exception as e:
            print(f"   ❌ RAG检索测试异常: {e}")
    
    print(f"\nRAG检索成功率: {success_count}/{len(test_queries)}")
    return success_count > 0

def main():
    """主验证函数"""
    print("🚀 专项服务验证")
    print("=" * 50)
    
    # 验证助贷招标服务
    rfq_success = test_rfq_service()
    
    # 验证RAG检索服务
    rag_success = test_rag_service()
    
    # 输出结果
    print("\n📊 验证结果")
    print("=" * 50)
    print(f"助贷招标服务: {'✅ 通过' if rfq_success else '❌ 失败'}")
    print(f"RAG检索服务: {'✅ 通过' if rag_success else '❌ 失败'}")
    
    if rfq_success and rag_success:
        print("\n🎉 所有服务验证通过！")
        return True
    else:
        print("\n⚠️ 部分服务需要进一步优化")
        return False

if __name__ == "__main__":
    main()
