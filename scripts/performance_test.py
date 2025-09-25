#!/usr/bin/env python3
"""
AI智能贷款平台性能测试脚本
"""

import asyncio
import aiohttp
import time
import json
import statistics
from datetime import datetime
from typing import List, Dict, Any

class PerformanceTest:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.results = []
        
    async def make_request(self, session: aiohttp.ClientSession, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        """发送单个请求并记录性能数据"""
        start_time = time.time()
        try:
            if method == "GET":
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    await response.text()
                    status_code = response.status
            elif method == "POST":
                async with session.post(f"{self.base_url}{endpoint}", json=data) as response:
                    await response.text()
                    status_code = response.status
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "response_time": response_time,
                "success": 200 <= status_code < 300,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            end_time = time.time()
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "response_time": end_time - start_time,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def make_request_with_url(self, session: aiohttp.ClientSession, base_url: str, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        """发送单个请求并记录性能数据（指定URL）"""
        start_time = time.time()
        try:
            if method == "GET":
                async with session.get(f"{base_url}{endpoint}") as response:
                    await response.text()
                    status_code = response.status
            elif method == "POST":
                async with session.post(f"{base_url}{endpoint}", json=data) as response:
                    await response.text()
                    status_code = response.status
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "response_time": response_time,
                "success": 200 <= status_code < 300,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            end_time = time.time()
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "response_time": end_time - start_time,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def test_health_endpoints(self, session: aiohttp.ClientSession, concurrent_users: int = 10):
        """测试健康检查端点"""
        print(f"测试健康检查端点 - 并发用户: {concurrent_users}")
        
        endpoints = [
            "/actuator/health",
            "/api/loans/health",
            "/api/risk/health",
            "/api/matching/health",
            "/api/admin/health"
        ]
        
        tasks = []
        for _ in range(concurrent_users):
            for endpoint in endpoints:
                tasks.append(self.make_request(session, endpoint))
        
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
        
        # 统计结果
        self.print_statistics("健康检查端点", results)
    
    async def test_loan_application(self, session: aiohttp.ClientSession, concurrent_users: int = 10):
        """测试贷款申请接口"""
        print(f"测试贷款申请接口 - 并发用户: {concurrent_users}")
        
        loan_data = {
            "userId": 1,
            "loanAmount": 100000,
            "loanTermMonths": 12,
            "loanPurpose": "经营周转",
            "monthlyIncome": 50000,
            "creditScore": 750
        }
        
        tasks = []
        for _ in range(concurrent_users):
            tasks.append(self.make_request(session, "/api/loans/apply", "POST", loan_data))
        
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
        
        # 统计结果
        self.print_statistics("贷款申请接口", results)
    
    async def test_risk_assessment(self, session: aiohttp.ClientSession, concurrent_users: int = 10):
        """测试风险评估接口"""
        print(f"测试风险评估接口 - 并发用户: {concurrent_users}")
        
        risk_data = {
            "userId": 1,
            "loanAmount": 100000,
            "monthlyIncome": 50000,
            "creditScore": 750,
            "loanTermMonths": 12,
            "occupation": "企业主",
            "workExperience": "3年",
            "hasExistingLoans": False,
            "hasOverdueHistory": False,
            "loanPurpose": "经营周转"
        }
        
        tasks = []
        for _ in range(concurrent_users):
            tasks.append(self.make_request(session, "/api/risk/assess", "POST", risk_data))
        
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
        
        # 统计结果
        self.print_statistics("风险评估接口", results)
    
    async def test_matching_service(self, session: aiohttp.ClientSession, concurrent_users: int = 10):
        """测试智能匹配接口"""
        print(f"测试智能匹配接口 - 并发用户: {concurrent_users}")
        
        matching_data = {
            "userId": 1,
            "loanAmount": 100000,
            "loanTermMonths": 12,
            "loanPurpose": "经营周转",
            "monthlyIncome": 50000,
            "creditScore": 750,
            "riskLevel": "LOW",
            "occupation": "企业主",
            "workExperience": "3年",
            "hasExistingLoans": False
        }
        
        tasks = []
        for _ in range(concurrent_users):
            tasks.append(self.make_request(session, "/api/matching/match", "POST", matching_data))
        
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
        
        # 统计结果
        self.print_statistics("智能匹配接口", results)
    
    async def test_admin_dashboard(self, session: aiohttp.ClientSession, concurrent_users: int = 10):
        """测试管理后台接口"""
        print(f"测试管理后台接口 - 并发用户: {concurrent_users}")
        
        # 管理后台服务使用不同的端口
        admin_base_url = "http://localhost:8081"
        
        endpoints = [
            "/api/admin/dashboard/stats",
            "/api/admin/users?page=0&size=10",
            "/api/admin/loans?page=0&size=10",
            "/api/admin/system/stats"
        ]
        
        tasks = []
        for _ in range(concurrent_users):
            for endpoint in endpoints:
                # 使用管理后台的专用端口
                tasks.append(self.make_request_with_url(session, admin_base_url, endpoint))
        
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
        
        # 统计结果
        self.print_statistics("管理后台接口", results)
    
    def print_statistics(self, test_name: str, results: List[Dict[str, Any]]):
        """打印测试统计信息"""
        if not results:
            return
            
        response_times = [r["response_time"] for r in results]
        success_count = sum(1 for r in results if r["success"])
        total_count = len(results)
        success_rate = (success_count / total_count) * 100
        
        print(f"\n{test_name} 测试结果:")
        print(f"  总请求数: {total_count}")
        print(f"  成功请求数: {success_count}")
        print(f"  成功率: {success_rate:.2f}%")
        print(f"  平均响应时间: {statistics.mean(response_times):.3f}s")
        print(f"  最小响应时间: {min(response_times):.3f}s")
        print(f"  最大响应时间: {max(response_times):.3f}s")
        print(f"  中位数响应时间: {statistics.median(response_times):.3f}s")
        
        if len(response_times) > 1:
            print(f"  标准差: {statistics.stdev(response_times):.3f}s")
        
        # 响应时间分布
        p95 = sorted(response_times)[int(len(response_times) * 0.95)]
        p99 = sorted(response_times)[int(len(response_times) * 0.99)]
        print(f"  95%响应时间: {p95:.3f}s")
        print(f"  99%响应时间: {p99:.3f}s")
    
    async def run_comprehensive_test(self):
        """运行综合性能测试"""
        print("开始AI智能贷款平台综合性能测试")
        print("=" * 50)
        
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # 测试不同并发级别
            concurrent_levels = [1, 5, 10, 20, 50]
            
            for concurrent_users in concurrent_levels:
                print(f"\n{'='*20} 并发用户数: {concurrent_users} {'='*20}")
                
                # 健康检查测试
                await self.test_health_endpoints(session, concurrent_users)
                await asyncio.sleep(1)
                
                # 业务接口测试
                await self.test_loan_application(session, concurrent_users)
                await asyncio.sleep(1)
                
                await self.test_risk_assessment(session, concurrent_users)
                await asyncio.sleep(1)
                
                await self.test_matching_service(session, concurrent_users)
                await asyncio.sleep(1)
                
                await self.test_admin_dashboard(session, concurrent_users)
                await asyncio.sleep(2)
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成性能测试报告"""
        if not self.results:
            print("没有测试结果可生成报告")
            return
        
        # 按端点分组统计
        endpoint_stats = {}
        for result in self.results:
            endpoint = result["endpoint"]
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = []
            endpoint_stats[endpoint].append(result)
        
        print("\n" + "="*60)
        print("性能测试报告")
        print("="*60)
        
        for endpoint, results in endpoint_stats.items():
            response_times = [r["response_time"] for r in results]
            success_count = sum(1 for r in results if r["success"])
            total_count = len(results)
            success_rate = (success_count / total_count) * 100
            
            print(f"\n端点: {endpoint}")
            print(f"  请求总数: {total_count}")
            print(f"  成功率: {success_rate:.2f}%")
            print(f"  平均响应时间: {statistics.mean(response_times):.3f}s")
            print(f"  95%响应时间: {sorted(response_times)[int(len(response_times) * 0.95)]:.3f}s")
            print(f"  99%响应时间: {sorted(response_times)[int(len(response_times) * 0.99)]:.3f}s")
        
        # 保存详细结果到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细测试结果已保存到: {filename}")

async def main():
    """主函数"""
    test = PerformanceTest()
    await test.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
