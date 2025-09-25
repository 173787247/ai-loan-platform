#!/usr/bin/env python3
"""
AI助贷招标平台 - 生产环境API测试脚本

@author AI Loan Platform Team
@version 1.0.0
"""

import requests
import json
import time
import numpy as np
from datetime import datetime
import sys

# 生产环境API配置
PROD_CONFIG = {
    'gateway_url': 'http://localhost:8080/api',
    'ai_service_url': 'http://localhost:8000/api/v1',
    'web_app_url': 'http://localhost:3000',
    'admin_app_url': 'http://localhost:3001',
    'nginx_url': 'http://localhost:80'
}

class ProductionAPITester:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m", 
            "WARNING": "\033[93m",
            "ERROR": "\033[91m"
        }
        color = colors.get(level, "\033[0m")
        print(f"{color}[{timestamp}] {level}: {message}\033[0m")
        
    def test_endpoint(self, name, url, method="GET", data=None, headers=None):
        """测试单个端点"""
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            if response.status_code == 200:
                self.log(f"{name} - 响应时间: {response_time:.2f}ms", "SUCCESS")
                self.results.append({
                    'name': name,
                    'status': 'PASS',
                    'response_time': response_time,
                    'status_code': response.status_code
                })
                return True
            else:
                self.log(f"{name} - HTTP {response.status_code}", "ERROR")
                self.results.append({
                    'name': name,
                    'status': 'FAIL',
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'error': response.text
                })
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"{name} - 连接失败: {str(e)}", "ERROR")
            self.results.append({
                'name': name,
                'status': 'FAIL',
                'response_time': 0,
                'status_code': 0,
                'error': str(e)
            })
            return False
    
    def test_gateway_health(self):
        """测试网关健康检查"""
        self.log("测试网关健康检查...")
        return self.test_endpoint(
            "网关健康检查",
            f"{PROD_CONFIG['gateway_url']}/health"
        )
    
    def test_ai_service_health(self):
        """测试AI服务健康检查"""
        self.log("测试AI服务健康检查...")
        return self.test_endpoint(
            "AI服务健康检查",
            f"{PROD_CONFIG['ai_service_url']}/health"
        )
    
    def test_ai_model_status(self):
        """测试AI模型状态"""
        self.log("测试AI模型状态...")
        return self.test_endpoint(
            "AI模型状态",
            f"{PROD_CONFIG['ai_service_url']}/model/status"
        )
    
    def test_ai_model_training(self):
        """测试AI模型训练"""
        self.log("测试AI模型训练...")
        
        # 生成模拟训练数据
        training_data = {
            "model_name": "risk_prediction",
            "training_data": {
                "X_train": np.random.rand(50, 20).tolist(),
                "y_train": np.random.randint(0, 5, 50).tolist(),
                "X_val": np.random.rand(10, 20).tolist(),
                "y_val": np.random.randint(0, 5, 10).tolist()
            }
        }
        
        return self.test_endpoint(
            "AI模型训练",
            f"{PROD_CONFIG['ai_service_url']}/model/train",
            method="POST",
            data=training_data
        )
    
    def test_ai_model_prediction(self):
        """测试AI模型预测"""
        self.log("测试AI模型预测...")
        
        prediction_data = {
            "model_name": "risk_prediction",
            "input_data": np.random.rand(20).tolist()
        }
        
        return self.test_endpoint(
            "AI模型预测",
            f"{PROD_CONFIG['ai_service_url']}/model/predict",
            method="POST",
            data=prediction_data
        )
    
    def test_risk_assessment(self):
        """测试风险评估"""
        self.log("测试风险评估...")
        
        risk_data = {
            "user_id": 1,
            "business_data": {
                "revenue": 1000,
                "profit": 100,
                "assets": 2000,
                "liabilities": 800,
                "industry": "制造业",
                "credit_rating": "A"
            },
            "market_data": {
                "gdp_growth": 5.5,
                "interest_rate": 0.035,
                "inflation": 0.025
            }
        }
        
        return self.test_endpoint(
            "风险评估",
            f"{PROD_CONFIG['ai_service_url']}/risk/assess",
            method="POST",
            data=risk_data
        )
    
    def test_web_app(self):
        """测试前端应用"""
        self.log("测试前端应用...")
        return self.test_endpoint(
            "前端应用",
            PROD_CONFIG['web_app_url']
        )
    
    def test_admin_app(self):
        """测试管理后台"""
        self.log("测试管理后台...")
        return self.test_endpoint(
            "管理后台",
            PROD_CONFIG['admin_app_url']
        )
    
    def test_nginx_load_balancer(self):
        """测试Nginx负载均衡器"""
        self.log("测试Nginx负载均衡器...")
        return self.test_endpoint(
            "Nginx负载均衡器",
            PROD_CONFIG['nginx_url']
        )
    
    def test_api_through_gateway(self):
        """测试通过网关的API调用"""
        self.log("测试通过网关的API调用...")
        return self.test_endpoint(
            "网关API路由",
            f"{PROD_CONFIG['gateway_url']}/ai/status"
        )
    
    def run_performance_test(self, endpoint_name, url, iterations=10):
        """运行性能测试"""
        self.log(f"运行性能测试: {endpoint_name} ({iterations}次)")
        
        response_times = []
        success_count = 0
        
        for i in range(iterations):
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)
                
                if response.status_code == 200:
                    success_count += 1
                    
            except requests.exceptions.RequestException:
                response_times.append(0)
        
        if response_times:
            avg_time = np.mean(response_times)
            min_time = np.min(response_times)
            max_time = np.max(response_times)
            success_rate = (success_count / iterations) * 100
            
            self.log(f"性能测试结果 - 平均: {avg_time:.2f}ms, 最小: {min_time:.2f}ms, 最大: {max_time:.2f}ms, 成功率: {success_rate:.1f}%", "SUCCESS")
            
            return {
                'endpoint': endpoint_name,
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'success_rate': success_rate
            }
        
        return None
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("开始生产环境API测试...")
        self.log("=" * 50)
        
        # 基础健康检查
        self.test_gateway_health()
        self.test_ai_service_health()
        self.test_web_app()
        self.test_admin_app()
        self.test_nginx_load_balancer()
        
        # AI服务测试
        self.test_ai_model_status()
        self.test_ai_model_training()
        self.test_ai_model_prediction()
        self.test_risk_assessment()
        
        # 网关路由测试
        self.test_api_through_gateway()
        
        # 性能测试
        self.log("=" * 50)
        self.log("开始性能测试...")
        
        performance_results = []
        performance_results.append(self.run_performance_test("AI服务健康检查", f"{PROD_CONFIG['ai_service_url']}/health"))
        performance_results.append(self.run_performance_test("网关健康检查", f"{PROD_CONFIG['gateway_url']}/health"))
        performance_results.append(self.run_performance_test("前端应用", PROD_CONFIG['web_app_url']))
        
        # 生成测试报告
        self.generate_report(performance_results)
    
    def generate_report(self, performance_results):
        """生成测试报告"""
        self.log("=" * 50)
        self.log("生成测试报告...")
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
                'duration_seconds': duration
            },
            'test_results': self.results,
            'performance_results': [r for r in performance_results if r is not None],
            'timestamp': end_time.isoformat()
        }
        
        # 保存报告
        report_file = f"prod-test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 显示摘要
        self.log("=" * 50)
        self.log("测试结果摘要:")
        self.log(f"总测试数: {total_tests}")
        self.log(f"通过测试: {passed_tests}")
        self.log(f"失败测试: {failed_tests}")
        self.log(f"成功率: {(passed_tests / total_tests) * 100:.1f}%")
        self.log(f"测试时长: {duration:.2f}秒")
        self.log(f"详细报告: {report_file}")
        
        if failed_tests > 0:
            self.log("失败的测试:", "ERROR")
            for result in self.results:
                if result['status'] == 'FAIL':
                    self.log(f"  - {result['name']}: {result.get('error', 'Unknown error')}", "ERROR")
        
        return report

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("AI助贷招标平台 - 生产环境API测试脚本")
        print("用法: python test-prod-api.py")
        print("功能: 测试生产环境的所有API端点和性能")
        return
    
    tester = ProductionAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
