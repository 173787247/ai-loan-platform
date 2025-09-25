#!/usr/bin/env python3
"""
AI智能助贷招标平台 - Docker服务测试

@author AI Loan Platform Team
@version 1.0.0
"""

import subprocess
import json
import sys
import time
from typing import List, Dict, Any

class DockerServiceTester:
    """Docker服务测试类"""
    
    def __init__(self):
        self.expected_services = [
            "ai-loan-ai-service",
            "ai-loan-web-app", 
            "ai-loan-admin-app",
            "ai-loan-gateway",
            "ai-loan-user-service",
            "ai-loan-mysql",
            "ai-loan-redis",
            "ai-loan-mongodb",
            "ai-loan-elasticsearch",
            "ai-loan-rabbitmq"
        ]
        self.test_results = []
    
    def run_docker_command(self, command: List[str]) -> tuple:
        """运行Docker命令"""
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "命令超时"
        except Exception as e:
            return False, "", str(e)
    
    def test_docker_ps(self) -> bool:
        """测试Docker容器运行状态"""
        print("🔍 检查Docker容器运行状态...")
        try:
            success, stdout, stderr = self.run_docker_command(["docker", "ps", "--format", "json"])
            if not success:
                print(f"❌ Docker ps命令失败: {stderr}")
                self.test_results.append(("Docker ps命令", False, stderr))
                return False
            
            running_containers = []
            for line in stdout.strip().split('\n'):
                if line:
                    try:
                        container = json.loads(line)
                        running_containers.append(container['Names'])
                    except json.JSONDecodeError:
                        continue
            
            print(f"✅ 发现 {len(running_containers)} 个运行中的容器")
            
            # 检查期望的服务
            missing_services = []
            for service in self.expected_services:
                if not any(service in container for container in running_containers):
                    missing_services.append(service)
            
            if missing_services:
                print(f"❌ 缺少服务: {missing_services}")
                self.test_results.append(("Docker服务检查", False, f"缺少: {missing_services}"))
                return False
            else:
                print("✅ 所有期望的服务都在运行")
                self.test_results.append(("Docker服务检查", True, f"{len(running_containers)}个容器运行中"))
                return True
                
        except Exception as e:
            print(f"❌ Docker ps检查异常: {e}")
            self.test_results.append(("Docker ps检查", False, str(e)))
            return False
    
    def test_container_health(self) -> bool:
        """测试容器健康状态"""
        print("🔍 检查容器健康状态...")
        try:
            success, stdout, stderr = self.run_docker_command([
                "docker", "ps", "--filter", "status=running", "--format", "table {{.Names}}\t{{.Status}}"
            ])
            
            if not success:
                print(f"❌ 获取容器状态失败: {stderr}")
                self.test_results.append(("容器健康检查", False, stderr))
                return False
            
            print("📋 容器状态:")
            print(stdout)
            
            # 检查是否有异常退出的容器
            success, stdout, stderr = self.run_docker_command([
                "docker", "ps", "-a", "--filter", "status=exited", "--format", "{{.Names}}"
            ])
            
            if success and stdout.strip():
                exited_containers = stdout.strip().split('\n')
                print(f"⚠️ 发现退出的容器: {exited_containers}")
                self.test_results.append(("容器健康检查", False, f"退出的容器: {exited_containers}"))
                return False
            else:
                print("✅ 没有异常退出的容器")
                self.test_results.append(("容器健康检查", True, "所有容器运行正常"))
                return True
                
        except Exception as e:
            print(f"❌ 容器健康检查异常: {e}")
            self.test_results.append(("容器健康检查", False, str(e)))
            return False
    
    def test_docker_compose_status(self) -> bool:
        """测试Docker Compose状态"""
        print("🔍 检查Docker Compose状态...")
        try:
            success, stdout, stderr = self.run_docker_command([
                "docker-compose", "-f", "docker-compose.gpu.yml", "ps"
            ])
            
            if not success:
                print(f"❌ Docker Compose状态检查失败: {stderr}")
                self.test_results.append(("Docker Compose状态", False, stderr))
                return False
            
            print("📋 Docker Compose服务状态:")
            print(stdout)
            
            # 检查服务状态
            if "Up" in stdout and "ai-loan-ai-service" in stdout:
                print("✅ Docker Compose服务运行正常")
                self.test_results.append(("Docker Compose状态", True, "服务运行正常"))
                return True
            else:
                print("❌ Docker Compose服务状态异常")
                self.test_results.append(("Docker Compose状态", False, "服务状态异常"))
                return False
                
        except Exception as e:
            print(f"❌ Docker Compose状态检查异常: {e}")
            self.test_results.append(("Docker Compose状态", False, str(e)))
            return False
    
    def test_docker_logs(self) -> bool:
        """测试Docker日志"""
        print("🔍 检查Docker日志...")
        try:
            # 检查AI服务日志
            success, stdout, stderr = self.run_docker_command([
                "docker", "logs", "--tail", "10", "ai-loan-ai-service"
            ])
            
            if not success:
                print(f"❌ 获取AI服务日志失败: {stderr}")
                self.test_results.append(("Docker日志检查", False, stderr))
                return False
            
            print("📋 AI服务最新日志:")
            print(stdout)
            
            # 检查是否有错误日志
            if "ERROR" in stdout or "Exception" in stdout:
                print("⚠️ 发现错误日志")
                self.test_results.append(("Docker日志检查", False, "发现错误日志"))
                return False
            else:
                print("✅ AI服务日志正常")
                self.test_results.append(("Docker日志检查", True, "日志正常"))
                return True
                
        except Exception as e:
            print(f"❌ Docker日志检查异常: {e}")
            self.test_results.append(("Docker日志检查", False, str(e)))
            return False
    
    def test_docker_resources(self) -> bool:
        """测试Docker资源使用"""
        print("🔍 检查Docker资源使用...")
        try:
            success, stdout, stderr = self.run_docker_command([
                "docker", "stats", "--no-stream", "--format", "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
            ])
            
            if not success:
                print(f"❌ 获取Docker资源使用失败: {stderr}")
                self.test_results.append(("Docker资源检查", False, stderr))
                return False
            
            print("📋 Docker资源使用情况:")
            print(stdout)
            
            # 检查CPU和内存使用
            lines = stdout.strip().split('\n')[1:]  # 跳过标题行
            high_usage_containers = []
            
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        container = parts[0]
                        cpu_perc = parts[1].replace('%', '')
                        mem_usage = parts[2]
                        
                        try:
                            cpu_float = float(cpu_perc)
                            if cpu_float > 80:
                                high_usage_containers.append(f"{container}: {cpu_perc}%")
                        except ValueError:
                            continue
            
            if high_usage_containers:
                print(f"⚠️ 发现高CPU使用容器: {high_usage_containers}")
                self.test_results.append(("Docker资源检查", False, f"高CPU使用: {high_usage_containers}"))
                return False
            else:
                print("✅ Docker资源使用正常")
                self.test_results.append(("Docker资源检查", True, "资源使用正常"))
                return True
                
        except Exception as e:
            print(f"❌ Docker资源检查异常: {e}")
            self.test_results.append(("Docker资源检查", False, str(e)))
            return False
    
    def test_docker_networks(self) -> bool:
        """测试Docker网络"""
        print("🔍 检查Docker网络...")
        try:
            success, stdout, stderr = self.run_docker_command([
                "docker", "network", "ls"
            ])
            
            if not success:
                print(f"❌ 获取Docker网络失败: {stderr}")
                self.test_results.append(("Docker网络检查", False, stderr))
                return False
            
            print("📋 Docker网络列表:")
            print(stdout)
            
            # 检查项目网络
            if "ai-loan-platform" in stdout:
                print("✅ 项目网络存在")
                self.test_results.append(("Docker网络检查", True, "项目网络正常"))
                return True
            else:
                print("❌ 项目网络不存在")
                self.test_results.append(("Docker网络检查", False, "项目网络不存在"))
                return False
                
        except Exception as e:
            print(f"❌ Docker网络检查异常: {e}")
            self.test_results.append(("Docker网络检查", False, str(e)))
            return False
    
    def run_all_tests(self) -> bool:
        """运行所有测试"""
        print("🚀 AI智能助贷招标平台 - Docker服务测试")
        print("=" * 60)
        
        tests = [
            self.test_docker_ps,
            self.test_container_health,
            self.test_docker_compose_status,
            self.test_docker_logs,
            self.test_docker_resources,
            self.test_docker_networks
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
            print("\n🎉 所有Docker测试通过！容器运行正常")
            return True
        else:
            print(f"\n⚠️ {total - passed} 个测试失败，请检查Docker服务")
            return False

def main():
    """主函数"""
    tester = DockerServiceTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
