#!/usr/bin/env python3
"""
中文PDF和图片OCR测试脚本
测试PDF中的中文内容搜索和图片OCR识别功能
"""

import requests
import os
import json
from datetime import datetime

def create_chinese_pdf():
    """创建包含中文内容的测试PDF文件"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.utils import ImageReader
        from reportlab.lib import colors
        
        # 创建测试PDF文件
        filename = "chinese_test_document.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        
        # 设置中文字体（使用系统默认字体）
        try:
            # 尝试注册中文字体
            pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
            font_name = 'SimHei'
        except:
            try:
                pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
                font_name = 'SimSun'
            except:
                font_name = 'Helvetica'  # 备用字体
        
        # 添加中文标题
        c.setFont(font_name, 16)
        c.setFillColor(colors.blue)
        c.drawString(100, 750, "AI贷款平台测试文档 - 中文版")
        
        # 添加申请人信息
        c.setFont(font_name, 12)
        c.setFillColor(colors.black)
        c.drawString(100, 700, "申请人信息：")
        c.drawString(100, 670, "姓名：王小明")
        c.drawString(100, 640, "身份证号：110101199003031234")
        c.drawString(100, 610, "手机号：13700137000")
        c.drawString(100, 580, "邮箱：wangxiaoming@example.com")
        
        # 添加贷款需求
        c.drawString(100, 540, "贷款需求：")
        c.drawString(100, 510, "贷款金额：300,000元人民币")
        c.drawString(100, 480, "贷款期限：60个月")
        c.drawString(100, 450, "贷款用途：购买住房")
        c.drawString(100, 420, "还款方式：等额本息")
        
        # 添加收入信息
        c.drawString(100, 380, "收入证明：")
        c.drawString(100, 350, "月收入：35,000元人民币")
        c.drawString(100, 320, "年收入：420,000元人民币")
        c.drawString(100, 290, "工作单位：北京科技有限公司")
        c.drawString(100, 260, "工作年限：10年")
        c.drawString(100, 230, "职位：高级软件工程师")
        
        # 添加资产信息
        c.drawString(100, 190, "资产信息：")
        c.drawString(100, 160, "银行存款：500,000元")
        c.drawString(100, 130, "房产价值：2,000,000元")
        c.drawString(100, 100, "车辆价值：200,000元")
        
        # 添加特殊字符和符号
        c.drawString(100, 70, "特殊字符测试：￥$€£¥@#%&*()[]{}")
        c.drawString(100, 50, "数字测试：1234567890 一二三四五六七八九十")
        
        c.save()
        print(f"✅ 中文测试PDF文件创建成功: {filename}")
        return filename
        
    except ImportError as e:
        print(f"❌ 缺少必要的库: {e}")
        return None
    except Exception as e:
        print(f"❌ 创建中文PDF文件失败: {e}")
        return None

def create_image_pdf():
    """创建包含图片的测试PDF文件"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # 创建测试图片
        img_filename = "test_image.png"
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # 尝试使用中文字体
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # 在图片上绘制中文文字
        draw.text((20, 50), "身份证正面", fill='black', font=font)
        draw.text((20, 80), "姓名：李小红", fill='black', font=font)
        draw.text((20, 110), "身份证号：110101199004041234", fill='black', font=font)
        draw.text((20, 140), "住址：北京市朝阳区某某街道", fill='black', font=font)
        
        # 保存图片
        img.save(img_filename)
        
        # 创建包含图片的PDF
        pdf_filename = "image_test_document.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=A4)
        
        # 添加标题
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.blue)
        c.drawString(100, 750, "Image OCR Test Document")
        
        # 添加图片到PDF
        c.drawImage(img_filename, 100, 500, width=300, height=150)
        
        # 添加说明文字
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(100, 450, "This document contains an image with Chinese text.")
        c.drawString(100, 420, "The image should be processed by OCR to extract text.")
        c.drawString(100, 390, "Text in the image: 身份证正面, 姓名：李小红, etc.")
        
        c.save()
        
        # 清理临时图片文件
        os.remove(img_filename)
        
        print(f"✅ 图片测试PDF文件创建成功: {pdf_filename}")
        return pdf_filename
        
    except ImportError as e:
        print(f"❌ 缺少必要的库: {e}")
        return None
    except Exception as e:
        print(f"❌ 创建图片PDF文件失败: {e}")
        return None

def test_pdf_upload(filename, test_name):
    """测试PDF文档上传"""
    print(f"\n📄 测试{test_name}PDF上传: {filename}")
    
    try:
        if not os.path.exists(filename):
            print(f"❌ 文件不存在: {filename}")
            return False
        
        with open(filename, 'rb') as f:
            files = {
                'file': (filename, f, 'application/pdf')
            }
            data = {
                'category': 'loan_application',
                'metadata': json.dumps({
                    'source': 'chinese_test',
                    'timestamp': datetime.now().isoformat(),
                    'test_type': test_name
                })
            }
            
            response = requests.post(
                'http://localhost:3000/ai/rag/process-document',
                files=files,
                data=data,
                timeout=60
            )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {test_name}PDF上传成功！")
            print(f"📋 文档ID: {result.get('data', {}).get('document_id', 'N/A')}")
            print(f"📁 文件名: {result.get('data', {}).get('filename', 'N/A')}")
            print(f"📂 分类: {result.get('data', {}).get('category', 'N/A')}")
            print(f"📝 创建块数: {result.get('data', {}).get('chunks_created', 'N/A')}")
            print(f"📄 总块数: {result.get('data', {}).get('total_chunks', 'N/A')}")
            print(f"⏱️ 处理时间: {result.get('data', {}).get('processing_time', 'N/A')}秒")
            print(f"📄 文档类型: {result.get('data', {}).get('document_type', 'N/A')}")
            
            # 显示提取的内容
            content = result.get('data', {}).get('content', '')
            if content:
                print(f"📖 提取内容预览: {content[:300]}...")
                return content
            else:
                print("⚠️ 未提取到内容")
                return None
        else:
            print(f"❌ {test_name}PDF上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ {test_name}PDF上传测试失败: {e}")
        return None

def test_chinese_search(queries):
    """测试中文内容搜索"""
    print(f"\n🔍 测试中文内容搜索...")
    
    results = {}
    for query in queries:
        print(f"\n🔍 搜索查询: '{query}'")
        
        try:
            search_data = {
                "query": query,
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
                search_results = result.get('data', {}).get('results', [])
                print(f"✅ 搜索成功，找到 {len(search_results)} 条结果")
                
                if search_results:
                    for i, item in enumerate(search_results[:2], 1):
                        print(f"📄 结果 {i}:")
                        print(f"   标题: {item.get('title', 'N/A')}")
                        print(f"   分类: {item.get('category', 'N/A')}")
                        print(f"   相似度: {item.get('similarity_score', 'N/A')}")
                        content = item.get('content', '')
                        print(f"   内容: {content[:100]}...")
                        print()
                else:
                    print("❌ 未找到匹配结果")
                
                results[query] = len(search_results) > 0
            else:
                print(f"❌ 搜索失败: {response.status_code}")
                results[query] = False
                
        except Exception as e:
            print(f"❌ 搜索测试失败: {e}")
            results[query] = False
    
    return results

def test_ai_chatbot_chinese():
    """测试AI聊天机器人中文对话"""
    print(f"\n🤖 测试AI聊天机器人中文对话...")
    
    try:
        # 创建会话
        session_data = {
            "user_id": "chinese_test_user",
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
            print(f"✅ 会话创建成功: {session_id}")
            
            # 发送中文消息
            message_data = {
                "session_id": session_id,
                "message": "你好，我想了解贷款产品，特别是住房贷款的相关信息",
                "user_info": {
                    "user_id": "chinese_test_user",
                    "name": "中文测试用户"
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
                print(f"✅ 中文消息处理成功: {response_text[:200]}...")
                return True
            else:
                print(f"❌ 中文消息处理失败: {response.status_code}")
                return False
        else:
            print(f"❌ 会话创建失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 中文聊天机器人测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 中文PDF和图片OCR测试开始")
    print("=" * 60)
    
    # 创建测试文件
    chinese_pdf = create_chinese_pdf()
    image_pdf = create_image_pdf()
    
    if not chinese_pdf and not image_pdf:
        print("❌ 无法创建测试文件，测试终止")
        return
    
    # 测试中文PDF上传
    chinese_content = None
    if chinese_pdf:
        chinese_content = test_pdf_upload(chinese_pdf, "中文")
    
    # 测试图片PDF上传
    image_content = None
    if image_pdf:
        image_content = test_pdf_upload(image_pdf, "图片")
    
    # 测试中文搜索
    search_queries = [
        "王小明",
        "300000",
        "住房",
        "北京科技",
        "身份证",
        "李小红",
        "朝阳区"
    ]
    
    search_results = test_chinese_search(search_queries)
    
    # 测试中文聊天
    chatbot_result = test_ai_chatbot_chinese()
    
    # 清理测试文件
    for filename in [chinese_pdf, image_pdf]:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"\n🗑️ 清理测试文件: {filename}")
            except Exception as e:
                print(f"⚠️ 清理测试文件失败: {e}")
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 中文PDF和OCR测试结果汇总")
    print("=" * 60)
    
    results = {
        "中文PDF上传": chinese_content is not None,
        "图片PDF上传": image_content is not None,
        "中文聊天机器人": chatbot_result
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
        print("🎉 所有中文和OCR测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查相关服务")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
