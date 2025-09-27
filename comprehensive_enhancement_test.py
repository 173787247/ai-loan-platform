#!/usr/bin/env python3
"""
综合增强功能测试脚本
测试OCR优化、性能增强、监控系统等新功能
"""

import requests
import os
import json
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image():
    """创建测试图片"""
    try:
        # 创建图片
        img = Image.new('RGB', (600, 400), color='white')
        draw = ImageDraw.Draw(img)
        
        # 尝试使用中文字体
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # 绘制中文文字
        texts = [
            "AI贷款平台测试文档",
            "申请人：张三",
            "身份证号：110101199001011234",
            "手机号：13800138000",
            "贷款金额：500,000元",
            "贷款期限：36个月",
            "工作单位：北京科技有限公司",
            "职位：高级工程师",
            "月收入：25,000元"
        ]
        
        y_position = 50
        for text in texts:
            draw.text((50, y_position), text, fill='black', font=font)
            y_position += 40
        
        # 保存图片
        filename = "test_ocr_image.png"
        img.save(filename)
        print(f"✅ 测试图片创建成功: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ 创建测试图片失败: {e}")
        return None

def test_performance_apis():
    """测试性能监控API"""
    print("\n📊 测试性能监控API...")
    
    try:
        # 测试性能摘要
        response = requests.get("http://localhost:3000/ai/api/v1/performance/summary", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ 性能摘要获取成功")
            data = result.get('data', {})
            print(f"   CPU使用率: {data.get('current', {}).get('cpu_percent', 'N/A')}%")
            print(f"   内存使用率: {data.get('current', {}).get('memory_percent', 'N/A')}%")
            print(f"   活跃连接数: {data.get('current', {}).get('active_connections', 'N/A')}")
            print(f"   平均响应时间: {data.get('current', {}).get('response_time_avg', 'N/A')}秒")
        else:
            print(f"❌ 性能摘要获取失败: {response.status_code}")
            return False
        
        # 测试缓存统计
        response = requests.get("http://localhost:3000/ai/api/v1/performance/cache/stats", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ 缓存统计获取成功")
            data = result.get('data', {})
            print(f"   缓存大小: {data.get('size', 'N/A')}")
            print(f"   最大缓存: {data.get('max_size', 'N/A')}")
            print(f"   命中率: {data.get('hit_rate', 'N/A'):.2%}")
        else:
            print(f"❌ 缓存统计获取失败: {response.status_code}")
            return False
        
        # 测试性能优化
        response = requests.post("http://localhost:3000/ai/api/v1/performance/optimize", timeout=30)
        if response.status_code == 200:
            print("✅ 性能优化执行成功")
        else:
            print(f"❌ 性能优化执行失败: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 性能监控API测试失败: {e}")
        return False

def test_advanced_ocr(image_path):
    """测试高级OCR功能"""
    print(f"\n🔍 测试高级OCR功能: {image_path}")
    
    try:
        if not os.path.exists(image_path):
            print(f"❌ 图片文件不存在: {image_path}")
            return False
        
        # 测试OCR识别
        ocr_data = {
            "image_path": os.path.abspath(image_path),
            "engines": ["paddleocr", "tesseract"],
            "language": "chi_sim+eng"
        }
        
        response = requests.post(
            "http://localhost:3000/ai/api/v1/ocr/recognize",
            json=ocr_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OCR识别成功")
            data = result.get('data', {})
            print(f"   识别文本: {data.get('text', '')[:100]}...")
            print(f"   置信度: {data.get('confidence', 0):.3f}")
            print(f"   使用引擎: {data.get('engine', 'N/A')}")
            print(f"   处理时间: {data.get('processing_time', 0):.3f}秒")
            
            # 显示所有结果
            all_results = data.get('all_results', [])
            if all_results:
                print(f"   所有引擎结果:")
                for i, result in enumerate(all_results, 1):
                    print(f"     引擎 {i} ({result.get('engine', 'N/A')}): 置信度 {result.get('confidence', 0):.3f}")
            
            return True
        else:
            print(f"❌ OCR识别失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OCR功能测试失败: {e}")
        return False

def test_enhanced_document_upload(image_path):
    """测试增强的文档上传功能"""
    print(f"\n📄 测试增强的文档上传: {image_path}")
    
    try:
        if not os.path.exists(image_path):
            print(f"❌ 图片文件不存在: {image_path}")
            return False
        
        # 上传图片文档
        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path, f, 'image/png')
            }
            data = {
                'category': 'test_ocr',
                'metadata': json.dumps({
                    'source': 'enhancement_test',
                    'timestamp': datetime.now().isoformat(),
                    'test_type': 'ocr_enhancement'
                })
            }
            
            response = requests.post(
                'http://localhost:3000/ai/api/v1/rag/process-document',
                files=files,
                data=data,
                timeout=120
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 增强文档上传成功")
            data = result.get('data', {})
            print(f"   文档ID: {data.get('document_id', 'N/A')}")
            print(f"   文件名: {data.get('filename', 'N/A')}")
            print(f"   处理时间: {data.get('processing_time', 'N/A')}秒")
            print(f"   文档类型: {data.get('document_type', 'N/A')}")
            
            # 显示提取的内容
            content = data.get('content', '')
            if content:
                print(f"   提取内容: {content[:200]}...")
                return True
            else:
                print("⚠️ 未提取到内容")
                return False
        else:
            print(f"❌ 增强文档上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 增强文档上传测试失败: {e}")
        return False

def test_enhanced_search():
    """测试增强的搜索功能"""
    print(f"\n🔍 测试增强的搜索功能...")
    
    search_queries = [
        "张三",
        "500000",
        "北京科技",
        "高级工程师",
        "25000"
    ]
    
    results = {}
    for query in search_queries:
        print(f"\n🔍 搜索查询: '{query}'")
        
        try:
            search_data = {
                "query": query,
                "search_type": "simple",
                "max_results": 3
            }
            
            response = requests.post(
                "http://localhost:3000/ai/api/v1/rag/search",
                json=search_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                search_results = result.get('data', {}).get('results', [])
                print(f"✅ 找到 {len(search_results)} 条结果")
                
                if search_results:
                    for i, item in enumerate(search_results[:2], 1):
                        content = item.get('content', '')
                        similarity = item.get('similarity_score', 0)
                        print(f"   结果 {i} (相似度: {similarity:.3f}): {content[:80]}...")
                
                results[query] = len(search_results) > 0
            else:
                print(f"❌ 搜索失败: {response.status_code}")
                results[query] = False
                
        except Exception as e:
            print(f"❌ 搜索测试失败: {e}")
            results[query] = False
    
    return results

def test_ai_chatbot_enhanced():
    """测试增强的AI聊天机器人"""
    print(f"\n🤖 测试增强的AI聊天机器人...")
    
    try:
        # 创建会话
        session_data = {
            "user_id": "enhancement_test_user",
            "chatbot_role": "general"
        }
        
        response = requests.post(
            "http://localhost:3000/ai/api/v1/chat/session",
            json=session_data,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ 会话创建失败: {response.status_code}")
            return False
        
        session_info = response.json()
        session_id = session_info.get("data", {}).get("session_id")
        print(f"✅ 会话创建成功: {session_id}")
        
        # 测试增强对话
        test_messages = [
            "你好，我想了解最新的贷款产品",
            "我刚刚上传了一个包含身份证信息的图片，你能帮我分析一下吗？",
            "我的月收入是25000元，能申请多少额度的贷款？",
            "请帮我分析一下我的贷款风险等级"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n💬 测试消息 {i}: {message}")
            
            message_data = {
                "session_id": session_id,
                "message": message,
                "user_info": {
                    "user_id": "enhancement_test_user",
                    "name": "增强测试用户"
                }
            }
            
            response = requests.post(
                "http://localhost:3000/ai/api/v1/chat/message",
                json=message_data,
                timeout=30
            )
            
            if response.status_code == 200:
                message_info = response.json()
                response_text = message_info.get('data', {}).get('response', '')
                print(f"✅ 回复: {response_text[:150]}...")
            else:
                print(f"❌ 消息处理失败: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 增强AI聊天机器人测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 综合增强功能测试开始")
    print("=" * 70)
    
    # 创建测试图片
    image_filename = create_test_image()
    if not image_filename:
        print("❌ 无法创建测试图片，测试终止")
        return
    
    # 测试性能监控API
    performance_result = test_performance_apis()
    
    # 测试高级OCR
    ocr_result = test_advanced_ocr(image_filename)
    
    # 测试增强文档上传
    upload_result = test_enhanced_document_upload(image_filename)
    
    # 等待一下让数据索引完成
    print("\n⏳ 等待数据索引完成...")
    time.sleep(3)
    
    # 测试增强搜索
    search_results = test_enhanced_search()
    
    # 测试增强AI聊天机器人
    chatbot_result = test_ai_chatbot_enhanced()
    
    # 清理测试文件
    try:
        os.remove(image_filename)
        print(f"\n🗑️ 清理测试文件: {image_filename}")
    except Exception as e:
        print(f"⚠️ 清理测试文件失败: {e}")
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("📊 综合增强功能测试结果汇总")
    print("=" * 70)
    
    results = {
        "性能监控API": performance_result,
        "高级OCR功能": ocr_result,
        "增强文档上传": upload_result,
        "增强AI聊天机器人": chatbot_result
    }
    
    # 添加搜索结果
    for query, found in search_results.items():
        results[f"搜索'{query}'"] = found
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 总体结果: {total_passed}/{total_tests} 项测试通过")
    
    if total_passed == total_tests:
        print("🎉 所有增强功能测试通过！系统优化完成！")
    else:
        print("⚠️ 部分测试失败，请检查相关服务")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
