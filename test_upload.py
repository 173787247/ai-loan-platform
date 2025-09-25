#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档上传测试脚本
"""

import requests
import json

def test_document_upload():
    """测试文档上传功能"""
    
    # AI服务文档上传接口
    ai_url = "http://localhost:8000/api/v1/ai/document/process"
    
    # 测试文档路径
    test_file = "test_document.html"
    
    try:
        print("🚀 开始测试文档上传功能...")
        
        # 准备文件上传
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'text/html')}
            
            print(f"📄 上传文件: {test_file}")
            print(f"🔗 请求URL: {ai_url}")
            
            # 发送POST请求
            response = requests.post(ai_url, files=files)
            
            print(f"📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 文档上传成功！")
                print(f"📋 处理结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
            else:
                print("❌ 文档上传失败！")
                print(f"错误信息: {response.text}")
                
    except FileNotFoundError:
        print(f"❌ 测试文件不存在: {test_file}")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_ai_agent_upload():
    """测试AI智能体文档上传功能"""
    
    agent_url = "http://localhost:8001/api/agent/process-document"
    test_file = "test_document.txt"
    
    try:
        print("\n🤖 开始测试AI智能体文档上传功能...")
        
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'text/html')}
            data = {'user_id': 1}
            
            print(f"📄 上传文件: {test_file}")
            print(f"🔗 请求URL: {agent_url}")
            
            response = requests.post(agent_url, files=files, data=data)
            
            print(f"📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ AI智能体文档处理成功！")
                print(f"📋 处理结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
            else:
                print("❌ AI智能体文档处理失败！")
                print(f"错误信息: {response.text}")
                
    except Exception as e:
        print(f"❌ AI智能体测试失败: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("📄 AI智能助贷招标平台 - 文档上传测试")
    print("=" * 50)
    
    # 测试AI服务文档上传
    test_document_upload()
    
    # 测试AI智能体文档上传
    test_ai_agent_upload()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)
