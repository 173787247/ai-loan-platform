#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件上传功能
"""

import requests
import json
import os
from pathlib import Path

def test_file_upload():
    """测试文件上传API"""
    base_url = "http://localhost:8000"
    
    print("🧪 测试文件上传功能")
    print("=" * 50)
    
    # 测试PDF文件上传
    test_files = [
        {
            "name": "test_document.pdf",
            "path": "test_document.pdf",
            "type": "application/pdf"
        },
        {
            "name": "test_text_image.jpg", 
            "path": "test_text_image.jpg",
            "type": "image/jpeg"
        }
    ]
    
    for file_info in test_files:
        print(f"\n📄 测试上传文件: {file_info['name']}")
        
        # 检查文件是否存在
        if not os.path.exists(file_info['path']):
            print(f"❌ 文件不存在: {file_info['path']}")
            continue
            
        try:
            # 准备文件上传
            with open(file_info['path'], 'rb') as f:
                files = {
                    'file': (file_info['name'], f, file_info['type'])
                }
                
                data = {
                    'category': 'loan_application',
                    'metadata': json.dumps({
                        'uploadTime': '2024-01-01T00:00:00Z',
                        'fileType': file_info['type'],
                        'fileSize': os.path.getsize(file_info['path'])
                    })
                }
                
                # 发送请求
                response = requests.post(
                    f"{base_url}/api/v1/rag/process-document",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                print(f"📊 响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 上传成功: {result.get('message', '未知')}")
                    if 'data' in result:
                        data = result['data']
                        print(f"📋 文档ID: {data.get('document_id', '未知')}")
                        print(f"📄 文件名: {data.get('filename', '未知')}")
                        print(f"📊 文档类型: {data.get('document_type', '未知')}")
                        print(f"📝 提取内容长度: {data.get('content_length', 0)}")
                        print(f"🔢 分块数量: {data.get('chunks_created', 0)}/{data.get('total_chunks', 0)}")
                        if data.get('content'):
                            print(f"📄 内容预览: {data['content'][:100]}...")
                else:
                    print(f"❌ 上传失败: {response.text}")
                    
        except Exception as e:
            print(f"❌ 上传异常: {e}")
    
    # 测试文档搜索
    print(f"\n🔍 测试文档搜索")
    try:
        search_data = {
            "query": "贷款申请",
            "limit": 5
        }
        
        response = requests.post(
            f"{base_url}/api/v1/rag/search",
            json=search_data,
            timeout=10
        )
        
        print(f"📊 搜索响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', {})
            results = data.get('results', [])
            total_results = data.get('total_results', 0)
            print(f"✅ 搜索成功: 找到 {total_results} 个结果")
            for i, doc in enumerate(results[:3], 1):
                title = doc.get('title', '未知标题')
                score = doc.get('similarity_score', 0)
                print(f"  {i}. {title} - {score:.3f}")
        else:
            print(f"❌ 搜索失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 搜索异常: {e}")

def test_ai_chat_with_files():
    """测试AI聊天中的文件处理"""
    base_url = "http://localhost:8000"
    
    print(f"\n🤖 测试AI聊天文件处理")
    print("=" * 50)
    
    try:
        # 创建聊天会话
        session_data = {
            "user_id": "test_user_123",
            "role": "borrower"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/chat/session",
            json=session_data,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ 创建会话失败: {response.text}")
            return
            
        session_result = response.json()
        session_id = session_result['data']['session_id']
        print(f"✅ 创建会话成功: {session_id}")
        
        # 发送包含文件信息的消息
        message_data = {
            "message": "📎 我已上传了以下文件：test_document.pdf, test_text_image.jpg\n\n请帮我分析这些贷款申请材料。",
            "user_id": "test_user_123",
            "metadata": {
                "has_files": True,
                "file_count": 2,
                "file_types": ["pdf", "image"]
            }
        }
        
        response = requests.post(
            f"{base_url}/api/v1/chat/message",
            json={
                "session_id": session_id,
                "message": message_data["message"],
                "user_id": message_data["user_id"],
                "metadata": message_data["metadata"]
            },
            timeout=30
        )
        
        print(f"📊 消息响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 消息发送成功")
            print(f"🤖 AI回复: {result['data']['response'][:200]}...")
        else:
            print(f"❌ 消息发送失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 聊天测试异常: {e}")

if __name__ == "__main__":
    print("🚀 开始文件上传功能测试")
    print("=" * 60)
    
    # 检查AI服务状态
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI服务运行正常")
        else:
            print("❌ AI服务异常")
            exit(1)
    except Exception as e:
        print(f"❌ 无法连接到AI服务: {e}")
        exit(1)
    
    # 运行测试
    test_file_upload()
    test_ai_chat_with_files()
    
    print("\n🎉 文件上传功能测试完成")
