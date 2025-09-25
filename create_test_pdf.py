#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试PDF文档
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

def create_test_pdf():
    """创建测试PDF文档"""
    
    # 创建PDF文件
    filename = "test_document.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # 设置字体
    c.setFont("Helvetica-Bold", 16)
    
    # 标题
    c.drawString(100, height - 100, "AI智能助贷招标平台 - 测试文档")
    
    # 公司信息
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    company_info = [
        "公司名称：北京科技有限公司",
        "统一社会信用代码：91110000123456789X",
        "法定代表人：张三",
        "注册资本：1000万元人民币",
        "成立日期：2020年1月1日",
        "经营范围：技术开发、技术咨询、技术服务",
        "",
        "财务状况：",
        "• 年营业收入：500万元",
        "• 净利润：50万元", 
        "• 总资产：2000万元",
        "• 负债总额：800万元",
        "",
        "贷款需求：",
        "• 申请金额：200万元",
        "• 贷款期限：12个月",
        "• 贷款用途：流动资金周转",
        "• 还款方式：等额本息",
        "",
        "联系方式：",
        "联系人：李四",
        "联系电话：13800138000",
        "邮箱：lisi@example.com"
    ]
    
    for line in company_info:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    # 保存PDF
    c.save()
    
    print(f"✅ 测试PDF文档已创建: {filename}")
    print(f"📁 文件大小: {os.path.getsize(filename)} bytes")
    
    return filename

if __name__ == "__main__":
    create_test_pdf()
