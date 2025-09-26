#!/usr/bin/env python3
"""
PDF上传测试程序
测试AI服务的文档上传功能
"""

import requests
import os
import json
from pathlib import Path

def find_pdf_files_on_desktop():
    """在桌面查找PDF文件"""
    desktop_path = Path.home() / "Desktop"
    pdf_files = list(desktop_path.glob("*.pdf"))
    return pdf_files

def test_pdf_upload(pdf_path):
    """测试PDF上传"""
    url = "http://localhost:8000/api/v1/rag/process-document"
    
    print(f"正在测试上传: {pdf_path}")
    print(f"文件大小: {pdf_path.stat().st_size / 1024:.2f} KB")
    
    try:
        # 准备文件上传
        with open(pdf_path, 'rb') as f:
            files = {
                'file': (pdf_path.name, f, 'application/pdf')
            }
            data = {
                'category': 'test',
                'metadata': '{"test": true, "source": "desktop_test"}'
            }
            
            print("发送请求到AI服务...")
            response = requests.post(url, files=files, data=data, timeout=30)
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 上传成功!")
                print(f"文档ID: {result.get('data', {}).get('document_id', 'N/A')}")
                print(f"文件名: {result.get('data', {}).get('filename', 'N/A')}")
                print(f"处理时间: {result.get('data', {}).get('processing_time', 'N/A')}ms")
                print(f"创建块数: {result.get('data', {}).get('chunks_created', 'N/A')}")
                print(f"文档类型: {result.get('data', {}).get('document_type', 'N/A')}")
                return True
            else:
                print(f"❌ 上传失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 无法连接到AI服务 (localhost:8000)")
        print("请确保AI服务正在运行")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时: 上传时间过长")
        return False
    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return False

def test_ai_service_health():
    """测试AI服务健康状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ AI服务健康检查通过")
            print(f"服务状态: {health_data.get('status', 'unknown')}")
            print(f"服务版本: {health_data.get('version', 'unknown')}")
            print(f"GPU可用: {health_data.get('gpu_available', False)}")
            return True
        else:
            print(f"❌ AI服务健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到AI服务: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("PDF上传测试程序")
    print("=" * 60)
    
    # 1. 检查AI服务健康状态
    print("\n1. 检查AI服务健康状态...")
    if not test_ai_service_health():
        print("请先启动AI服务: docker-compose -f docker-compose.gpu.yml up -d ai-service")
        return
    
    # 2. 查找桌面PDF文件
    print("\n2. 查找桌面PDF文件...")
    pdf_files = find_pdf_files_on_desktop()
    
    if not pdf_files:
        print("❌ 桌面没有找到PDF文件")
        print("请将PDF文件放到桌面，然后重新运行测试")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name} ({pdf_file.stat().st_size / 1024:.2f} KB)")
    
    # 3. 测试上传
    print("\n3. 开始测试上传...")
    success_count = 0
    
    for pdf_file in pdf_files:
        print(f"\n{'='*40}")
        if test_pdf_upload(pdf_file):
            success_count += 1
        print(f"{'='*40}")
    
    # 4. 测试结果
    print(f"\n测试完成!")
    print(f"成功上传: {success_count}/{len(pdf_files)} 个文件")
    
    if success_count == len(pdf_files):
        print("🎉 所有PDF文件上传成功!")
    elif success_count > 0:
        print("⚠️  部分PDF文件上传成功")
    else:
        print("❌ 所有PDF文件上传失败")

if __name__ == "__main__":
    main()
