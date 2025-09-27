#!/usr/bin/env python3
"""
前端文件上传测试脚本
测试通过nginx代理的文件上传功能
"""

import requests
import os
import json
from datetime import datetime

def create_test_pdf():
    """创建测试PDF文件"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # 创建测试PDF文件
        filename = "frontend_test_document.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # 添加内容
        c.drawString(100, 750, "前端文件上传测试文档")
        c.drawString(100, 700, "申请人信息：")
        c.drawString(100, 650, "姓名：李四")
        c.drawString(100, 600, "身份证号：110101199002021234")
        c.drawString(100, 550, "手机号：13900139000")
        c.drawString(100, 500, "贷款需求：")
        c.drawString(100, 450, "贷款金额：200,000元")
        c.drawString(100, 400, "贷款期限：36个月")
        c.drawString(100, 350, "贷款用途：房屋装修")
        c.drawString(100, 300, "收入证明：")
        c.drawString(100, 250, "月收入：25,000元")
        c.drawString(100, 200, "工作单位：互联网科技公司")
        c.drawString(100, 150, "工作年限：8年")
        
        c.save()
        print(f"✅ 测试PDF文件创建成功: {filename}")
        return filename
        
    except ImportError:
        print("❌ 缺少reportlab库，无法创建PDF文件")
        return None
    except Exception as e:
        print(f"❌ 创建PDF文件失败: {e}")
        return None

def test_frontend_upload(filename):
    """测试前端文件上传（通过nginx代理）"""
    print(f"\n📄 测试前端文件上传: {filename}")
    
    try:
        # 检查文件是否存在
        if not os.path.exists(filename):
            print(f"❌ 文件不存在: {filename}")
            return False
        
        # 准备上传数据
        with open(filename, 'rb') as f:
            files = {
                'file': (filename, f, 'application/pdf')
            }
            data = {
                'category': 'loan_application',
                'metadata': json.dumps({
                    'source': 'frontend_test',
                    'timestamp': datetime.now().isoformat(),
                    'test_type': 'frontend_upload'
                })
            }
            
            # 通过nginx代理上传文件
            response = requests.post(
                'http://localhost:3000/ai/rag/process-document',
                files=files,
                data=data,
                timeout=60
            )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 前端文件上传成功！")
            print(f"📋 文档ID: {result.get('data', {}).get('document_id', 'N/A')}")
            print(f"📁 文件名: {result.get('data', {}).get('filename', 'N/A')}")
            print(f"📂 分类: {result.get('data', {}).get('category', 'N/A')}")
            print(f"📝 创建块数: {result.get('data', {}).get('chunks_created', 'N/A')}")
            print(f"📄 总块数: {result.get('data', {}).get('total_chunks', 'N/A')}")
            print(f"⏱️ 处理时间: {result.get('data', {}).get('processing_time', 'N/A')}秒")
            print(f"📄 文档类型: {result.get('data', {}).get('document_type', 'N/A')}")
            
            # 显示提取的内容（前500字符）
            content = result.get('data', {}).get('content', '')
            if content:
                print(f"📖 提取内容预览: {content[:200]}...")
            else:
                print("⚠️ 未提取到内容")
            
            return True
        else:
            print(f"❌ 前端文件上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查服务状态")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请检查服务是否运行")
        return False
    except Exception as e:
        print(f"❌ 前端文件上传测试失败: {e}")
        return False

def test_frontend_chatbot():
    """测试前端聊天机器人（通过nginx代理）"""
    print("\n🤖 测试前端聊天机器人...")
    
    try:
        # 创建会话
        session_data = {
            "user_id": "frontend_test_user",
            "chatbot_role": "general"
        }
        
        response = requests.post(
            "http://localhost:3000/ai/chat/session",
            json=session_data,
            timeout=10
        )
        
        if response.status_code == 200:
            session_info = response.json()
            session_id = session_info.get("data", {}).get("session_id")
            print(f"✅ 前端会话创建成功: {session_id}")
            
            # 发送消息
            message_data = {
                "session_id": session_id,
                "message": "你好，我想了解贷款产品",
                "user_info": {
                    "user_id": "frontend_test_user",
                    "name": "前端测试用户"
                }
            }
            
            response = requests.post(
                "http://localhost:3000/ai/chat/message",
                json=message_data,
                timeout=30
            )
            
            if response.status_code == 200:
                message_info = response.json()
                response_text = message_info.get('data', {}).get('response', '')
                print(f"✅ 前端消息处理成功: {response_text[:100]}...")
                return True
            else:
                print(f"❌ 前端消息处理失败: {response.status_code}")
                return False
        else:
            print(f"❌ 前端会话创建失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 前端聊天机器人测试失败: {e}")
        return False

def test_frontend_rag_search():
    """测试前端RAG搜索（通过nginx代理）"""
    print("\n🔍 测试前端RAG搜索...")
    
    try:
        search_data = {
            "query": "李四",
            "search_type": "simple",
            "max_results": 5
        }
        
        response = requests.post(
            "http://localhost:3000/ai/rag/search",
            json=search_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            results = result.get('data', {}).get('results', [])
            print(f"✅ 前端RAG搜索成功，找到 {len(results)} 条结果")
            
            for i, item in enumerate(results[:3], 1):
                print(f"📄 结果 {i}:")
                print(f"   标题: {item.get('title', 'N/A')}")
                print(f"   分类: {item.get('category', 'N/A')}")
                print(f"   相似度: {item.get('similarity_score', 'N/A')}")
                print(f"   内容: {item.get('content', '')[:100]}...")
                print()
            
            return True
        else:
            print(f"❌ 前端RAG搜索失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 前端RAG搜索测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 前端文件上传测试开始")
    print("=" * 50)
    
    # 创建测试PDF文件
    pdf_filename = create_test_pdf()
    if not pdf_filename:
        print("❌ 无法创建测试PDF文件，测试终止")
        return
    
    # 测试前端文件上传
    upload_result = test_frontend_upload(pdf_filename)
    
    # 测试前端聊天机器人
    chatbot_result = test_frontend_chatbot()
    
    # 测试前端RAG搜索
    search_result = test_frontend_rag_search()
    
    # 清理测试文件
    try:
        os.remove(pdf_filename)
        print(f"\n🗑️ 清理测试文件: {pdf_filename}")
    except Exception as e:
        print(f"⚠️ 清理测试文件失败: {e}")
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 前端测试结果汇总")
    print("=" * 50)
    
    results = {
        "前端文件上传": upload_result,
        "前端聊天机器人": chatbot_result,
        "前端RAG搜索": search_result
    }
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 总体结果: {total_passed}/{total_tests} 项测试通过")
    
    if total_passed == total_tests:
        print("🎉 所有前端测试通过！文件上传功能正常！")
    else:
        print("⚠️ 部分前端测试失败，请检查相关服务")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
