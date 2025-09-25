#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建包含图片的PDF文档用于测试OCR功能
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont
import os

def create_pdf_with_image():
    """创建包含图片的PDF文档"""
    # 1. 先创建一个包含文字的图片
    img_width, img_height = 400, 200
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 添加文字到图片
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text_lines = [
        "AI助贷招标平台",
        "PDF图片OCR测试",
        "Test PDF Image OCR",
        "2025-09-23"
    ]
    
    y_pos = 30
    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (img_width - text_width) // 2
        draw.text((x_pos, y_pos), line, fill='black', font=font)
        y_pos += 40
    
    # 保存图片
    img_path = "temp_image_for_pdf.jpg"
    img.save(img_path, "JPEG", quality=95)
    print(f"✅ 创建测试图片: {img_path}")
    
    # 2. 创建PDF并添加图片
    pdf_path = "test_pdf_with_image.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    # 添加文字内容
    c.setFont("Helvetica", 16)
    c.drawString(50, height - 50, "AI助贷招标平台 - PDF图片OCR测试文档")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "此PDF包含以下内容：")
    c.drawString(50, height - 100, "1. 纯文本内容")
    c.drawString(50, height - 120, "2. 嵌入的图片（需要OCR处理）")
    c.drawString(50, height - 140, "3. 混合内容")
    
    # 添加图片
    try:
        c.drawImage(img_path, 50, height - 350, width=300, height=150)
        c.drawString(50, height - 370, "上图包含文字，需要OCR识别：")
    except Exception as e:
        print(f"⚠️ 添加图片失败: {e}")
        c.drawString(50, height - 350, "图片添加失败，但PDF已创建")
    
    # 添加更多文字
    c.drawString(50, height - 400, "文档编号: PDF-OCR-TEST-001")
    c.drawString(50, height - 420, "创建日期: 2025-09-23")
    c.drawString(50, height - 440, "测试目的: 验证PDF图片OCR功能")
    
    c.save()
    
    # 清理临时文件
    if os.path.exists(img_path):
        os.remove(img_path)
    
    print(f"✅ 创建PDF文档: {pdf_path}")
    print(f"📊 PDF大小: {os.path.getsize(pdf_path)} bytes")
    
    return pdf_path

if __name__ == "__main__":
    create_pdf_with_image()
