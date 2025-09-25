#!/usr/bin/env python3
"""
AI服务测试脚本
测试AI智能贷款平台的所有AI功能

@author AI Loan Platform Team
@version 1.1.0
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

class AIServiceTester:
    """AI服务测试类"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
    
    def test_health_check(self) -> Dict[str, Any]:
        """测试健康检查"""
        print("🔍 测试AI服务健康检查...")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 健康检查成功: {data['status']}")
                print(f"   服务版本: {data['version']}")
                print(f"   GPU可用: {data['gpu_available']}")
                print(f"   GPU数量: {data['gpu_count']}")
                return {"success": True, "data": data}
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            print(f"❌ 健康检查异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_risk_assessment(self) -> Dict[str, Any]:
        """测试风险评估"""
        print("\n🔍 测试风险评估功能...")
        
        test_data = {
            "user_id": 1,
            "business_data": {
                "revenue": 1000000,
                "profit_margin": 0.15,
                "debt_ratio": 0.3,
                "credit_score": 750,
                "business_age": 5,
                "employee_count": 50,
                "industry_risk_score": 0.2,
                "management_experience": 8,
                "audit_quality_score": 0.8,
                "governance_score": 0.7,
                "market_share": 0.05,
                "competitive_position": 0.6,
                "brand_value": 500000,
                "cash_flow_stability": 0.8,
                "working_capital_ratio": 1.2,
                "cash_conversion_cycle": 45,
                "revenue_growth_rate": 0.12,
                "profit_growth_rate": 0.15
            },
            "market_data": {
                "gdp_growth_rate": 0.06,
                "inflation_rate": 0.03,
                "interest_rate": 0.045,
                "unemployment_rate": 0.05,
                "market_volatility": 0.2,
                "sector_volatility": 0.25,
                "currency_volatility": 0.15,
                "sector_growth_rate": 0.08,
                "sector_competition_index": 0.6,
                "regulatory_risk_score": 0.3
            }
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/risk/assess",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 风险评估成功")
                print(f"   用户ID: {data['data']['user_id']}")
                print(f"   评估时间: {data['data']['assessment_time']}")
                print(f"   风险等级: {data['data']['risk_level']}")
                print(f"   综合风险评分: {data['data']['total_risk_score']}")
                print(f"   推荐利率: {data['data']['recommended_rate']}")
                print(f"   最大贷款金额: {data['data']['max_loan_amount']}")
                return {"success": True, "data": data}
            else:
                print(f"❌ 风险评估失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            print(f"❌ 风险评估异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_smart_matching(self) -> Dict[str, Any]:
        """测试智能匹配"""
        print("\n🔍 测试智能匹配功能...")
        
        test_data = {
            "tender_id": 1,
            "user_requirements": {
                "loan_amount": 500000,
                "loan_term": 24,
                "preferred_rate": 0.08,
                "industry": "制造业",
                "company_size": "medium",
                "revenue": 2000000,
                "credit_score": 720,
                "business_age": 3
            },
            "available_products": [
                {
                    "product_id": 1,
                    "product_name": "流动资金贷款",
                    "interest_rate": 0.065,
                    "term_months": 24,
                    "max_amount": 1000000,
                    "min_amount": 100000,
                    "target_industry": ["制造业", "服务业"],
                    "features": ["快速审批", "灵活还款"]
                },
                {
                    "product_id": 2,
                    "product_name": "设备贷款",
                    "interest_rate": 0.055,
                    "term_months": 36,
                    "max_amount": 2000000,
                    "min_amount": 200000,
                    "target_industry": ["制造业", "加工业"],
                    "features": ["专项用途", "长期限"]
                }
            ]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/match/proposals",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 智能匹配成功")
                print(f"   招标ID: {data['data']['tender_id']}")
                print(f"   匹配时间: {data['data']['matching_time']}")
                print(f"   总产品数: {data['data']['total_products']}")
                print(f"   匹配产品数: {data['data']['matched_products']}")
                print(f"   推荐数量: {len(data['data']['recommendations'])}")
                return {"success": True, "data": data}
            else:
                print(f"❌ 智能匹配失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            print(f"❌ 智能匹配异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_recommendation_engine(self) -> Dict[str, Any]:
        """测试推荐引擎"""
        print("\n🔍 测试推荐引擎功能...")
        
        test_data = {
            "tender_id": 1,
            "user_id": 1,
            "user_preferences": {
                "loan_amount": 300000,
                "loan_term": 36,
                "preferred_rate": 0.07,
                "industry": "服务业",
                "company_size": "small",
                "revenue": 800000,
                "credit_score": 680,
                "business_age": 2
            }
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/recommend/solutions",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 推荐引擎成功")
                print(f"   用户ID: {data['data']['user_id']}")
                print(f"   招标ID: {data['data']['tender_id']}")
                print(f"   推荐时间: {data['data']['recommendation_time']}")
                print(f"   个性化推荐数量: {len(data['data']['personalized_recommendations'])}")
                print(f"   热门推荐数量: {len(data['data']['popular_recommendations'])}")
                return {"success": True, "data": data}
            else:
                print(f"❌ 推荐引擎失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            print(f"❌ 推荐引擎异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_document_processing(self) -> Dict[str, Any]:
        """测试文档处理（模拟）"""
        print("\n🔍 测试文档处理功能...")
        print("   注意: 文档处理需要上传实际文件，这里只测试接口可用性")
        
        # 创建一个测试文件
        test_file_path = "test_document.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试文档\n包含一些测试内容\n用于测试OCR和文档处理功能")
        
        try:
            with open(test_file_path, "rb") as f:
                files = {"file": ("test_document.txt", f, "text/plain")}
                response = self.session.post(
                    f"{self.base_url}/api/v1/ai/document/process",
                    files=files
                )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 文档处理成功")
                print(f"   处理结果: {data['message']}")
                return {"success": True, "data": data}
            else:
                print(f"❌ 文档处理失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            print(f"❌ 文档处理异常: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            # 清理测试文件
            import os
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("🚀 开始AI服务综合测试")
        print("=" * 50)
        
        start_time = time.time()
        
        # 运行各项测试
        tests = [
            ("健康检查", self.test_health_check),
            ("风险评估", self.test_risk_assessment),
            ("智能匹配", self.test_smart_matching),
            ("推荐引擎", self.test_recommendation_engine),
            ("文档处理", self.test_document_processing)
        ]
        
        results = {}
        success_count = 0
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
                if result.get("success", False):
                    success_count += 1
            except Exception as e:
                print(f"❌ {test_name}测试异常: {str(e)}")
                results[test_name] = {"success": False, "error": str(e)}
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 输出测试总结
        print("\n" + "=" * 50)
        print("📊 AI服务测试总结")
        print("=" * 50)
        print(f"总测试数: {len(tests)}")
        print(f"成功数: {success_count}")
        print(f"失败数: {len(tests) - success_count}")
        print(f"成功率: {success_count / len(tests) * 100:.1f}%")
        print(f"总耗时: {total_time:.2f}秒")
        
        # 详细结果
        print("\n📋 详细测试结果:")
        for test_name, result in results.items():
            status = "✅ 成功" if result.get("success", False) else "❌ 失败"
            print(f"  {test_name}: {status}")
            if not result.get("success", False) and "error" in result:
                print(f"    错误: {result['error']}")
        
        return {
            "total_tests": len(tests),
            "success_count": success_count,
            "failure_count": len(tests) - success_count,
            "success_rate": success_count / len(tests) * 100,
            "total_time": total_time,
            "results": results
        }

def main():
    """主函数"""
    print("AI智能贷款平台 - AI服务测试工具")
    print("版本: 1.1.0")
    print("作者: AI Loan Platform Team")
    print()
    
    # 创建测试器
    tester = AIServiceTester()
    
    # 运行所有测试
    results = tester.run_all_tests()
    
    # 保存测试结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_service_test_results_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存到: {filename}")
    
    # 返回退出码
    if results["success_rate"] == 100:
        print("\n🎉 所有测试通过！AI服务运行正常！")
        return 0
    else:
        print(f"\n⚠️  有 {results['failure_count']} 个测试失败，请检查相关服务")
        return 1

if __name__ == "__main__":
    exit(main())
