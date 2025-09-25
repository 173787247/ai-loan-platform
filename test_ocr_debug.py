#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR调试测试脚本
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os

def test_ocr():
    """测试OCR功能"""
    image_file = "test_image.jpg"
    
    if not os.path.exists(image_file):
        print(f"❌ 图片文件不存在: {image_file}")
        return
    
    print(f"📸 测试图片: {image_file}")
    print(f"📊 文件大小: {os.path.getsize(image_file)} bytes")
    print("=" * 60)
    
    # 1. 测试OpenCV读取
    print("\n🔍 测试OpenCV读取:")
    try:
        image = cv2.imread(image_file)
        if image is not None:
            print(f"   ✅ OpenCV读取成功: {image.shape}")
        else:
            print("   ❌ OpenCV读取失败")
            return
    except Exception as e:
        print(f"   ❌ OpenCV异常: {e}")
        return
    
    # 2. 测试PIL读取
    print("\n🔍 测试PIL读取:")
    try:
        pil_image = Image.open(image_file)
        print(f"   ✅ PIL读取成功: {pil_image.size}, {pil_image.mode}")
    except Exception as e:
        print(f"   ❌ PIL异常: {e}")
    
    # 3. 测试直接OCR
    print("\n🔍 测试直接OCR:")
    try:
        # 使用PIL
        text = pytesseract.image_to_string(pil_image, lang='chi_sim+eng')
        print(f"   PIL OCR结果长度: {len(text)}")
        print(f"   PIL OCR内容: {repr(text[:100])}")
        
        # 使用OpenCV
        text_cv = pytesseract.image_to_string(image, lang='chi_sim+eng')
        print(f"   OpenCV OCR结果长度: {len(text_cv)}")
        print(f"   OpenCV OCR内容: {repr(text_cv[:100])}")
        
        if text.strip() or text_cv.strip():
            print("   ✅ OCR提取成功")
        else:
            print("   ❌ OCR提取失败 - 内容为空")
    except Exception as e:
        print(f"   ❌ OCR异常: {e}")
    
    # 4. 测试图片预处理
    print("\n🔍 测试图片预处理:")
    try:
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(f"   ✅ 灰度转换成功: {gray.shape}")
        
        # 去噪
        denoised = cv2.medianBlur(gray, 3)
        print(f"   ✅ 去噪成功: {denoised.shape}")
        
        # 二值化
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"   ✅ 二值化成功: {binary.shape}")
        
        # 对预处理后的图片进行OCR
        text_processed = pytesseract.image_to_string(binary, lang='chi_sim+eng')
        print(f"   预处理后OCR结果长度: {len(text_processed)}")
        print(f"   预处理后OCR内容: {repr(text_processed[:100])}")
        
        if text_processed.strip():
            print("   ✅ 预处理后OCR提取成功")
        else:
            print("   ❌ 预处理后OCR提取失败 - 内容为空")
    except Exception as e:
        print(f"   ❌ 预处理异常: {e}")
    
    # 5. 测试不同语言模式
    print("\n🔍 测试不同语言模式:")
    try:
        for lang in ['eng', 'chi_sim', 'chi_sim+eng']:
            text_lang = pytesseract.image_to_string(image, lang=lang)
            print(f"   {lang}: 长度={len(text_lang)}, 内容={repr(text_lang[:50])}")
    except Exception as e:
        print(f"   ❌ 语言模式测试异常: {e}")

if __name__ == "__main__":
    test_ocr()
