#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF图片OCR功能
"""

import pdfplumber
import pytesseract
from PIL import Image
import os

def test_pdf_image_ocr():
    """测试PDF图片OCR"""
    pdf_file = "test_pdf_with_image.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF文件不存在: {pdf_file}")
        return
    
    print(f"📄 测试PDF文件: {pdf_file}")
    print(f"📊 文件大小: {os.path.getsize(pdf_file)} bytes")
    print("=" * 60)
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[0]
            print(f"📄 页面数量: {len(pdf.pages)}")
            print(f"🖼️ 图片数量: {len(page.images)}")
            
            if page.images:
                for i, img in enumerate(page.images):
                    print(f"\n🔍 处理图片 {i+1}:")
                    print(f"   名称: {img.get('name', 'Unknown')}")
                    print(f"   尺寸: {img.get('srcsize', 'Unknown')}")
                    print(f"   边界框: {img.get('x0', 0):.1f}, {img.get('y0', 0):.1f}, {img.get('x1', 0):.1f}, {img.get('y1', 0):.1f}")
                    
                    # 提取图片
                    bbox = [img['x0'], img['y0'], img['x1'], img['y1']]
                    img_obj = page.within_bbox(bbox).to_image()
                    pil_img = img_obj.original
                    
                    print(f"   提取后尺寸: {pil_img.size}")
                    print(f"   图片模式: {pil_img.mode}")
                    print(f"   数据范围: {pil_img.getextrema()}")
                    
                    # 尝试不同OCR参数
                    print(f"   OCR测试:")
                    for lang in ['eng', 'chi_sim', 'chi_sim+eng']:
                        try:
                            text = pytesseract.image_to_string(pil_img, lang=lang)
                            print(f"     {lang}: {repr(text[:100])}")
                        except Exception as e:
                            print(f"     {lang}: 错误 - {e}")
                    
                    # 尝试图片预处理
                    print(f"   预处理OCR测试:")
                    try:
                        # 转换为灰度
                        gray_img = pil_img.convert('L')
                        text_gray = pytesseract.image_to_string(gray_img, lang='chi_sim+eng')
                        print(f"     灰度图: {repr(text_gray[:100])}")
                        
                        # 调整大小
                        resized_img = pil_img.resize((pil_img.width * 2, pil_img.height * 2), Image.Resampling.LANCZOS)
                        text_resized = pytesseract.image_to_string(resized_img, lang='chi_sim+eng')
                        print(f"     放大2倍: {repr(text_resized[:100])}")
                        
                    except Exception as e:
                        print(f"     预处理错误: {e}")
            
            # 提取页面文本
            page_text = page.extract_text()
            print(f"\n📝 页面文本长度: {len(page_text)}")
            print(f"📝 页面文本预览: {repr(page_text[:200])}")
            
    except Exception as e:
        print(f"❌ 处理失败: {e}")

if __name__ == "__main__":
    test_pdf_image_ocr()
