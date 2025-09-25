#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF文本提取
"""

import PyPDF2
import os

def test_pdf_extraction():
    """测试PDF文本提取"""
    pdf_file = "test_document.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF文件不存在: {pdf_file}")
        return
    
    try:
        print(f"📄 测试PDF文件: {pdf_file}")
        print(f"📊 文件大小: {os.path.getsize(pdf_file)} bytes")
        
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"📄 页数: {len(pdf_reader.pages)}")
            
            if len(pdf_reader.pages) > 0:
                text = pdf_reader.pages[0].extract_text()
                print(f"📝 第一页内容长度: {len(text)}")
                print(f"📄 内容预览: {text[:200]}")
                
                if len(text) > 0:
                    print("✅ PDF文本提取成功")
                else:
                    print("❌ PDF文本提取失败 - 内容为空")
            else:
                print("❌ PDF文件没有页面")
                
    except Exception as e:
        print(f"❌ PDF提取异常: {e}")

if __name__ == "__main__":
    test_pdf_extraction()
