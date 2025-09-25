#!/usr/bin/env python3
"""
AI智能助贷招标平台 - API集成测试

@author AI Loan Platform Team
@version 1.0.0
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List

class APITester:
    """API测试类"""
    
    def __init__(self):
        self.base_urls = {
            "ai_service": "http://localhost:8000",
            "web_app": "http://localhost:3000",
            "admin_app": "http://localhost:3001",
            "gateway": "http://localhost:8080",
            "user_service": "http://localhost:8081",
            "rabbitmq": "http://localhost:15672",
            "elasticsearch": "http://localhost:9200"
        }
        self.test_results = []
    
    def test_ai_service_health(self) -> bool:
        """测试AI服务健康检查"""
        print("🔍 测试AI服务健康检查...")
        try:
            response = requests.get(f"{self.base_urls['ai_service']}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ AI服务健康检查通过: {data}")
                self.test_results.append(("AI服务健康检查", True, data))
                return True
            else:
                print(f"❌ AI服务健康检查失败: {response.status_code}")
                self.test_results.append(("AI服务健康检查", False, f"状态码: {response.status_code}"))
                return False
        except Exception as e:
            print(f"❌ AI服务健康检查异常: {e}")
            self.test_results.append(("AI服务健康检查", False, str(e)))
            return False
    
    def test_ai_service_risk_assessment(self) -> bool:
        """测试AI服务风险评估API"""
        print("🔍 测试AI服务风险评估API...")
        try:
            test_data = {
                "user_id": 1,
                "business_data": {
                    "revenue": 500,
                    "profit": 50,
                    "assets": 1000,
                    "liabilities": 300,
                    "industry": "制造业",
                    "credit_rating": "BBB"
                },
                "market_data": {
                    "gdp_growth": 5.5,
                    "interest_rate": 0.045,
                    "inflation": 0.025
                }
            }
            
            response = requests.post(
                f"{self.base_urls['ai_service']}/api/v1/ai/risk/assess",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 风险评估API测试通过")
                print(f"   风险等级: {data.get('data', {}).get('risk_level', '未知')}")
                self.test_results.append(("风险评估API", True, data))
                return True
            else:
                print(f"❌ 风险评估API测试失败: {response.status_code}")
                print(f"   响应: {response.text}")
                self.test_results.append(("风险评估API", False, f"状态码: {response.status_code}"))
                return False
        except Exception as e:
            print(f"❌ 风险评估API测试异常: {e}")
            self.test_results.append(("风险评估API", False, str(e)))
            return False
    
    def test_ai_service_smart_matching(self) -> bool:
        """测试AI服务智能匹配API"""
        print("🔍 测试AI服务智能匹配API...")
        try:
            test_data = {
                "tender_id": 1,
                "user_requirements": {
                    "loan_amount": 100,
                    "loan_term": 12,
                    "industry": "制造业",
                    "urgency": "normal",
                    "preferred_rate": 0.06
                },
                "available_products": []
            }
            
            response = requests.post(
                f"{self.base_urls['ai_service']}/api/v1/ai/match/proposals",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 智能匹配API测试通过")
                print(f"   匹配产品数: {len(data.get('data', {}).get('recommendations', []))}")
                self.test_results.append(("智能匹配API", True, data))
                return True
            else:
                print(f"❌ 智能匹配API测试失败: {response.status_code}")
                print(f"   响应: {response.text}")
                self.test_results.append(("智能匹配API", False, f"状态码: {response.status_code}"))
                return False
        except Exception as e:
            print(f"❌ 智能匹配API测试异常: {e}")
            self.test_results.append(("智能匹配API", False, str(e)))
            return False
    
    def test_ai_service_recommendation(self) -> bool:
        """测试AI服务推荐引擎API"""
        print("🔍 测试AI服务推荐引擎API...")
        try:
            test_data = {
                "user_id": 1,
                "tender_id": 1,
                "user_preferences": {
                    "loan_amount": 200,
                    "loan_term": 24,
                    "industry": "服务业",
                    "risk_tolerance": "medium",
                    "preferred_features": ["快速审批", "灵活还款"]
                }
            }
            
            response = requests.post(
                f"{self.base_urls['ai_service']}/api/v1/ai/recommend/solutions",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 推荐引擎API测试通过")
                print(f"   推荐数量: {len(data.get('data', {}).get('personalized_recommendations', []))}")
                self.test_results.append(("推荐引擎API", True, data))
                return True
            else:
                print(f"❌ 推荐引擎API测试失败: {response.status_code}")
                print(f"   响应: {response.text}")
                self.test_results.append(("推荐引擎API", False, f"状态码: {response.status_code}"))
                return False
        except Exception as e:
            print(f"❌ 推荐引擎API测试异常: {e}")
            self.test_results.append(("推荐引擎API", False, str(e)))
            return False
    
    def test_web_app_accessibility(self) -> bool:
        """测试Web应用可访问性"""
        print("🔍 测试Web应用可访问性...")
        try:
            response = requests.get(self.base_urls['web_app'], timeout=10)
            if response.status_code == 200:
                print("✅ Web应用可访问")
                self.test_results.append(("Web应用可访问性", True, "状态码: 200"))
                return True
            else:
                print(f"❌ Web应用不可访问: {response.status_code}")
                self.test_results.append(("Web应用可访问性", False, f"状态码: {response.status_code}"))
                return False
        except Exception as e:
            print(f"❌ Web应用访问异常: {e}")
            self.test_results.append(("Web应用可访问性", False, str(e)))
            return False
    
    def test_admin_app_accessibility(self) -> bool:
        """测试管理后台可访问性"""
        print("🔍 测试管理后台可访问性...")
        try:
            response = requests.get(self.base_urls['admin_app'], timeout=10)
            if response.status_code == 200:
                print("✅ 管理后台可访问")
                self.test_results.append(("管理后台可访问性", True, "状态码: 200"))
                return True
            else:
                print(f"❌ 管理后台不可访问: {response.status_code}")
                self.test_results.append(("管理后台可访问性", False, f"状态码: {response.status_code}"))
                return False
        except Exception as e:
            print(f"❌ 管理后台访问异常: {e}")
            self.test_results.append(("管理后台可访问性", False, str(e)))
            return False
    
    def test_database_connectivity(self) -> bool:
        """测试数据库连接"""
        print("🔍 测试数据库连接...")
        try:
            # 测试Elasticsearch
            response = requests.get(f"{self.base_urls['elasticsearch']}/_cluster/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Elasticsearch连接正常: {data.get('status', '未知')}")
                self.test_results.append(("Elasticsearch连接", True, data.get('status', '未知')))
            else:
                print(f"❌ Elasticsearch连接失败: {response.status_code}")
                self.test_results.append(("Elasticsearch连接", False, f"状态码: {response.status_code}"))
                return False
            
            # 测试RabbitMQ
            response = requests.get(f"{self.base_urls['rabbitmq']}/api/overview", timeout=10)
            if response.status_code == 200:
                print("✅ RabbitMQ连接正常")
                self.test_results.append(("RabbitMQ连接", True, "正常"))
            else:
                print(f"❌ RabbitMQ连接失败: {response.status_code}")
                self.test_results.append(("RabbitMQ连接", False, f"状态码: {response.status_code}"))
                return False
            
            return True
        except Exception as e:
            print(f"❌ 数据库连接测试异常: {e}")
            self.test_results.append(("数据库连接", False, str(e)))
            return False
    
    def test_service_performance(self) -> bool:
        """测试服务性能"""
        print("🔍 测试服务性能...")
        try:
            # 测试AI服务响应时间
            start_time = time.time()
            response = requests.get(f"{self.base_urls['ai_service']}/health", timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            if response.status_code == 200 and response_time < 5.0:
                print(f"✅ AI服务响应时间正常: {response_time:.2f}秒")
                self.test_results.append(("AI服务性能", True, f"{response_time:.2f}秒"))
                return True
            else:
                print(f"❌ AI服务响应时间过长: {response_time:.2f}秒")
                self.test_results.append(("AI服务性能", False, f"{response_time:.2f}秒"))
                return False
        except Exception as e:
            print(f"❌ 性能测试异常: {e}")
            self.test_results.append(("服务性能", False, str(e)))
            return False
    
    def run_all_tests(self) -> bool:
        """运行所有测试"""
        print("🚀 AI智能助贷招标平台 - API集成测试")
        print("=" * 60)
        
        tests = [
            self.test_ai_service_health,
            self.test_ai_service_risk_assessment,
            self.test_ai_service_smart_matching,
            self.test_ai_service_recommendation,
            self.test_web_app_accessibility,
            self.test_admin_app_accessibility,
            self.test_database_connectivity,
            self.test_service_performance
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ 测试异常: {e}")
            print()
        
        print("=" * 60)
        print(f"📊 测试结果: {passed}/{total} 通过")
        
        # 打印详细结果
        print("\n📋 详细测试结果:")
        for test_name, success, details in self.test_results:
            status = "✅" if success else "❌"
            print(f"   {status} {test_name}: {details}")
        
        if passed == total:
            print("\n🎉 所有API测试通过！系统运行正常")
            return True
        else:
            print(f"\n⚠️ {total - passed} 个测试失败，请检查相关服务")
            return False

def main():
    """主函数"""
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
