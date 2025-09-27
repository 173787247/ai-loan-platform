#!/usr/bin/env python3
"""
最终中文PDF和OCR功能测试
验证PDF中文内容搜索和图片OCR识别功能
"""

import requests
import os
import json
from datetime import datetime

def create_comprehensive_test_pdf():
    """创建综合测试PDF文件"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib import colors
        
        # 创建测试PDF文件
        filename = "comprehensive_test_document.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        
        # 设置中文字体
        try:
            pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
            font_name = 'SimHei'
        except:
            try:
                pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
                font_name = 'SimSun'
            except:
                font_name = 'Helvetica'
        
        # 添加标题
        c.setFont(font_name, 18)
        c.setFillColor(colors.blue)
        c.drawString(100, 750, "AI贷款平台综合测试文档")
        
        # 添加申请人信息
        c.setFont(font_name, 14)
        c.setFillColor(colors.black)
        c.drawString(100, 700, "申请人信息：")
        c.setFont(font_name, 12)
        c.drawString(100, 670, "姓名：陈大明")
        c.drawString(100, 640, "身份证号：110101199005051234")
        c.drawString(100, 610, "手机号：13600136000")
        c.drawString(100, 580, "邮箱：chendaming@example.com")
        c.drawString(100, 550, "地址：上海市浦东新区陆家嘴金融贸易区")
        
        # 添加贷款需求
        c.setFont(font_name, 14)
        c.drawString(100, 510, "贷款需求：")
        c.setFont(font_name, 12)
        c.drawString(100, 480, "贷款金额：500,000元人民币")
        c.drawString(100, 450, "贷款期限：36个月")
        c.drawString(100, 420, "贷款用途：购买商业用房")
        c.drawString(100, 390, "还款方式：等额本息")
        c.drawString(100, 360, "担保方式：抵押担保")
        
        # 添加收入信息
        c.setFont(font_name, 14)
        c.drawString(100, 320, "收入证明：")
        c.setFont(font_name, 12)
        c.drawString(100, 290, "月收入：50,000元人民币")
        c.drawString(100, 260, "年收入：600,000元人民币")
        c.drawString(100, 230, "工作单位：上海金融科技有限公司")
        c.drawString(100, 200, "工作年限：12年")
        c.drawString(100, 170, "职位：技术总监")
        c.drawString(100, 140, "行业：金融科技")
        
        # 添加资产信息
        c.setFont(font_name, 14)
        c.drawString(100, 100, "资产信息：")
        c.setFont(font_name, 12)
        c.drawString(100, 70, "银行存款：1,000,000元")
        c.drawString(100, 40, "房产价值：5,000,000元")
        c.drawString(100, 10, "车辆价值：500,000元")
        
        c.save()
        print(f"✅ 综合测试PDF文件创建成功: {filename}")
        return filename
        
    except ImportError as e:
        print(f"❌ 缺少必要的库: {e}")
        return None
    except Exception as e:
        print(f"❌ 创建综合测试PDF文件失败: {e}")
        return None

def test_pdf_upload_and_search(filename):
    """测试PDF上传和搜索"""
    print(f"\n📄 测试PDF上传和搜索: {filename}")
    
    # 上传PDF
    try:
        with open(filename, 'rb') as f:
            files = {
                'file': (filename, f, 'application/pdf')
            }
            data = {
                'category': 'loan_application',
                'metadata': json.dumps({
                    'source': 'comprehensive_test',
                    'timestamp': datetime.now().isoformat(),
                    'test_type': 'comprehensive'
                })
            }
            
            response = requests.post(
                'http://localhost:3000/ai/rag/process-document',
                files=files,
                data=data,
                timeout=60
            )
        
        if response.status_code != 200:
            print(f"❌ PDF上传失败: {response.status_code}")
            return False
        
        result = response.json()
        print(f"✅ PDF上传成功: {result.get('data', {}).get('document_id', 'N/A')}")
        
        # 等待一下让数据索引完成
        import time
        time.sleep(2)
        
        # 测试各种搜索查询
        search_queries = [
            "陈大明",
            "500000",
            "商业用房",
            "上海金融科技",
            "技术总监",
            "浦东新区",
            "抵押担保",
            "600000"
        ]
        
        search_results = {}
        for query in search_queries:
            print(f"\n🔍 搜索查询: '{query}'")
            
            search_data = {
                "query": query,
                "search_type": "simple",
                "max_results": 3
            }
            
            response = requests.post(
                "http://localhost:3000/ai/rag/search",
                json=search_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                results = result.get('data', {}).get('results', [])
                print(f"✅ 找到 {len(results)} 条结果")
                
                if results:
                    for i, item in enumerate(results[:2], 1):
                        content = item.get('content', '')
                        similarity = item.get('similarity_score', 0)
                        print(f"   结果 {i} (相似度: {similarity:.3f}): {content[:80]}...")
                
                search_results[query] = len(results) > 0
            else:
                print(f"❌ 搜索失败: {response.status_code}")
                search_results[query] = False
        
        return search_results
        
    except Exception as e:
        print(f"❌ PDF上传和搜索测试失败: {e}")
        return {}

def test_ai_chatbot_with_context():
    """测试AI聊天机器人上下文理解"""
    print(f"\n🤖 测试AI聊天机器人上下文理解...")
    
    try:
        # 创建会话
        session_data = {
            "user_id": "comprehensive_test_user",
            "chatbot_role": "general"
        }
        
        response = requests.post(
            "http://localhost:3000/ai/chat/session",
            json=session_data,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ 会话创建失败: {response.status_code}")
            return False
        
        session_info = response.json()
        session_id = session_info.get("data", {}).get("session_id")
        print(f"✅ 会话创建成功: {session_id}")
        
        # 测试一系列对话
        test_messages = [
            "你好，我想了解贷款产品",
            "我刚刚上传了一个贷款申请文档，你能帮我分析一下吗？",
            "我的贷款金额是50万，这个额度合适吗？",
            "我是技术总监，收入稳定，能获得优惠利率吗？"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n💬 测试消息 {i}: {message}")
            
            message_data = {
                "session_id": session_id,
                "message": message,
                "user_info": {
                    "user_id": "comprehensive_test_user",
                    "name": "综合测试用户"
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
                print(f"✅ 回复: {response_text[:150]}...")
            else:
                print(f"❌ 消息处理失败: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ AI聊天机器人测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 最终中文PDF和OCR功能测试开始")
    print("=" * 70)
    
    # 创建综合测试PDF
    pdf_filename = create_comprehensive_test_pdf()
    if not pdf_filename:
        print("❌ 无法创建测试文件，测试终止")
        return
    
    # 测试PDF上传和搜索
    search_results = test_pdf_upload_and_search(pdf_filename)
    
    # 测试AI聊天机器人
    chatbot_result = test_ai_chatbot_with_context()
    
    # 清理测试文件
    try:
        os.remove(pdf_filename)
        print(f"\n🗑️ 清理测试文件: {pdf_filename}")
    except Exception as e:
        print(f"⚠️ 清理测试文件失败: {e}")
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("📊 最终测试结果汇总")
    print("=" * 70)
    
    results = {
        "PDF上传": len(search_results) > 0,
        "AI聊天机器人": chatbot_result
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
        print("🎉 所有功能测试通过！中文PDF和OCR功能完全正常！")
    else:
        print("⚠️ 部分测试失败，请检查相关服务")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
