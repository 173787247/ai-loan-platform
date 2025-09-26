"""
集成优化测试脚本
测试第三方服务集成、数据同步、API稳定性和监控系统
"""

import requests
import json
import time
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_third_party_integration():
    """测试第三方服务集成"""
    print("🔗 测试第三方服务集成")
    print("=" * 50)
    
    # 测试征信报告获取
    print("1. 测试征信报告获取...")
    try:
        response = requests.post(
            f"{BASE_URL}/third-party/credit-report",
            json={
                "user_id": "test_user_001",
                "id_number": "110101199001011234"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 征信报告获取成功")
                print(f"   服务名称: {data['service_name']}")
                print(f"   响应时间: {data['response_time']:.3f}秒")
                print(f"   请求ID: {data['request_id']}")
            else:
                print(f"   ❌ 征信报告获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print()
    
    # 测试身份验证
    print("2. 测试身份验证...")
    try:
        response = requests.post(
            f"{BASE_URL}/third-party/verify-identity",
            json={
                "id_number": "110101199001011234",
                "name": "张三",
                "phone": "13800138000"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 身份验证成功")
                print(f"   服务名称: {data['service_name']}")
                print(f"   响应时间: {data['response_time']:.3f}秒")
                print(f"   请求ID: {data['request_id']}")
            else:
                print(f"   ❌ 身份验证失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print()
    
    # 测试服务状态
    print("3. 测试服务状态...")
    try:
        response = requests.get(f"{BASE_URL}/third-party/service-status", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 服务状态获取成功")
                print(f"   服务数量: {len(data)}")
                for service_name, status in data.items():
                    print(f"   - {service_name}: {status['status']} ({status['circuit_breaker_state']})")
            else:
                print(f"   ❌ 服务状态获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")

def test_data_sync():
    """测试数据同步"""
    print("\n🔄 测试数据同步")
    print("=" * 50)
    
    # 测试添加同步任务
    print("1. 测试添加同步任务...")
    try:
        response = requests.post(
            f"{BASE_URL}/sync/add-task",
            json={
                "source": "database",
                "target": "cache",
                "sync_type": "real_time",
                "data_key": "test_sync_key",
                "data": {"test": "data", "timestamp": datetime.now().isoformat()},
                "priority": 1
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                task_id = result["data"]["task_id"]
                print(f"   ✅ 同步任务添加成功")
                print(f"   任务ID: {task_id}")
                
                # 测试获取任务详情
                time.sleep(1)
                test_task_details(task_id)
            else:
                print(f"   ❌ 同步任务添加失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print()
    
    # 测试同步状态
    print("2. 测试同步状态...")
    try:
        response = requests.get(f"{BASE_URL}/sync/status", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 同步状态获取成功")
                print(f"   总任务数: {data['total_tasks']}")
                print(f"   待处理: {data['pending_tasks']}")
                print(f"   进行中: {data['in_progress_tasks']}")
                print(f"   已完成: {data['completed_tasks']}")
                print(f"   失败: {data['failed_tasks']}")
                print(f"   队列大小: {data['queue_size']}")
            else:
                print(f"   ❌ 同步状态获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")

def test_task_details(task_id):
    """测试任务详情"""
    try:
        response = requests.get(f"{BASE_URL}/sync/task/{task_id}", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 任务详情获取成功")
                print(f"   任务ID: {data['task_id']}")
                print(f"   状态: {data['status']}")
                print(f"   源: {data['source']}")
                print(f"   目标: {data['target']}")
                print(f"   同步类型: {data['sync_type']}")
            else:
                print(f"   ❌ 任务详情获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")

def test_api_stability():
    """测试API稳定性"""
    print("\n🛡️ 测试API稳定性")
    print("=" * 50)
    
    # 测试稳定性指标
    print("1. 测试稳定性指标...")
    try:
        response = requests.get(f"{BASE_URL}/stability/metrics", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 稳定性指标获取成功")
                print(f"   总API数: {data['total_apis']}")
                print(f"   熔断器数量: {data['total_circuit_breakers']}")
                print(f"   限流器数量: {data['total_rate_limiters']}")
                
                # 显示API指标
                if data['api_metrics']:
                    print("   API指标:")
                    for api_name, metrics in data['api_metrics'].items():
                        print(f"   - {api_name}: 成功率 {metrics['success_rate']:.1%}, 平均响应时间 {metrics['average_response_time']:.3f}s")
            else:
                print(f"   ❌ 稳定性指标获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print()
    
    # 测试稳定性健康检查
    print("2. 测试稳定性健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/stability/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 稳定性健康检查成功")
                print(f"   状态: {data['status']}")
                print(f"   熔断器: {data['circuit_breakers']['healthy']}/{data['circuit_breakers']['total']} 健康")
                print(f"   限流器: {data['rate_limiters']['healthy']}/{data['rate_limiters']['total']} 健康")
            else:
                print(f"   ❌ 稳定性健康检查失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")

def test_monitoring_system():
    """测试监控系统"""
    print("\n📊 测试监控系统")
    print("=" * 50)
    
    # 测试系统状态
    print("1. 测试系统状态...")
    try:
        response = requests.get(f"{BASE_URL}/monitoring/system-status", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 系统状态获取成功")
                print(f"   监控状态: {'运行中' if data['is_monitoring'] else '已停止'}")
                print(f"   CPU使用率: {data['cpu_percent']:.1f}%")
                print(f"   内存使用率: {data['memory_percent']:.1f}%")
                print(f"   磁盘使用率: {data['disk_percent']:.1f}%")
                print(f"   进程数量: {data['process_count']}")
                print(f"   负载平均值: {data['load_avg_1min']:.2f}")
                print(f"   活跃告警: {data['active_alerts']}")
            else:
                print(f"   ❌ 系统状态获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print()
    
    # 测试监控指标
    print("2. 测试监控指标...")
    try:
        response = requests.get(f"{BASE_URL}/monitoring/metrics", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 监控指标获取成功")
                print(f"   指标数量: {len(data)}")
                
                # 显示关键指标
                key_metrics = ["system.cpu_percent", "system.memory_percent", "system.disk_percent"]
                for metric_name in key_metrics:
                    if metric_name in data:
                        metric = data[metric_name]
                        print(f"   - {metric_name}: 当前 {metric['current']:.1f}, 平均 {metric['avg']:.1f}, 最大 {metric['max']:.1f}")
            else:
                print(f"   ❌ 监控指标获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    print()
    
    # 测试监控告警
    print("3. 测试监控告警...")
    try:
        response = requests.get(f"{BASE_URL}/monitoring/alerts", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"   ✅ 监控告警获取成功")
                print(f"   活跃告警: {data['active_alerts']}")
                print(f"   24小时总告警: {data['total_alerts_24h']}")
                
                # 显示告警级别分布
                if data['alerts_by_level']:
                    print("   告警级别分布:")
                    for level, count in data['alerts_by_level'].items():
                        if count > 0:
                            print(f"   - {level}: {count}")
                
                # 显示最近告警
                if data['recent_alerts']:
                    print("   最近告警:")
                    for alert in data['recent_alerts'][:3]:  # 显示最近3个
                        print(f"   - {alert['name']}: {alert['level']} - {alert['message']}")
            else:
                print(f"   ❌ 监控告警获取失败: {result.get('message')}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")

def test_integration_performance():
    """测试集成性能"""
    print("\n⚡ 测试集成性能")
    print("=" * 50)
    
    # 并发测试
    print("1. 并发API调用测试...")
    import concurrent.futures
    
    def make_request():
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/monitoring/system-status", timeout=5)
            end_time = time.time()
            return {
                "success": response.status_code == 200,
                "response_time": end_time - start_time,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "response_time": 0,
                "error": str(e)
            }
    
    # 并发10个请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    
    if successful_requests:
        avg_response_time = sum(r["response_time"] for r in successful_requests) / len(successful_requests)
        print(f"   ✅ 并发测试完成")
        print(f"   成功请求: {len(successful_requests)}/10")
        print(f"   失败请求: {len(failed_requests)}/10")
        print(f"   平均响应时间: {avg_response_time:.3f}秒")
    else:
        print(f"   ❌ 所有请求都失败了")

def main():
    """主测试函数"""
    print("🚀 集成优化测试开始")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试目标: {BASE_URL}")
    print("=" * 60)
    
    # 检查服务健康状态
    try:
        health_response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 服务健康检查通过")
        else:
            print("❌ 服务健康检查失败")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        return
    
    print()
    
    # 执行各项测试
    test_third_party_integration()
    test_data_sync()
    test_api_stability()
    test_monitoring_system()
    test_integration_performance()
    
    print("\n" + "=" * 60)
    print("🎉 集成优化测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
