#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建包含文字的测试图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_text_image():
    """创建包含文字的测试图片"""
    # 创建白色背景图片
    width, height = 400, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # 尝试使用系统字体
    try:
        # Windows系统字体
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            # 备用字体
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
    
    # 绘制文字
    text_lines = [
        "AI助贷招标平台",
        "测试文档OCR功能",
        "Test Document OCR",
        "2025-09-23"
    ]
    
    y_position = 20
    for line in text_lines:
        # 计算文字位置（居中）
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) // 2
        
        # 绘制黑色文字
        draw.text((x_position, y_position), line, fill='black', font=font)
        y_position += 40
    
    # 保存图片
    output_file = "test_text_image.jpg"
    image.save(output_file, "JPEG", quality=95)
    print(f"✅ 创建测试图片: {output_file}")
    print(f"📊 图片大小: {image.size}")
    print(f"📝 包含文字: {len(text_lines)}行")
    
    return output_file

if __name__ == "__main__":
    create_text_image()
