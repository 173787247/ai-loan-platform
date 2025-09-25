#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不同PDF处理库的效果
"""

import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
import os

def test_pdf_libraries():
    """测试不同PDF处理库"""
    pdf_file = "test_document.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF文件不存在: {pdf_file}")
        return
    
    print(f"📄 测试PDF文件: {pdf_file}")
    print(f"📊 文件大小: {os.path.getsize(pdf_file)} bytes")
    print("=" * 60)
    
    # 1. 测试PyPDF2
    print("\n🔍 测试 PyPDF2:")
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"   页数: {len(reader.pages)}")
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()
                print(f"   内容长度: {len(text)}")
                print(f"   内容预览: {repr(text[:100])}")
                if len(text) > 0:
                    print("   ✅ PyPDF2 提取成功")
                else:
                    print("   ❌ PyPDF2 提取失败 - 内容为空")
    except Exception as e:
        print(f"   ❌ PyPDF2 异常: {e}")
    
    # 2. 测试pdfplumber
    print("\n🔍 测试 pdfplumber:")
    try:
        with pdfplumber.open(pdf_file) as pdf:
            print(f"   页数: {len(pdf.pages)}")
            if len(pdf.pages) > 0:
                text = pdf.pages[0].extract_text()
                print(f"   内容长度: {len(text) if text else 0}")
                print(f"   内容预览: {repr(text[:100]) if text else 'None'}")
                if text and len(text) > 0:
                    print("   ✅ pdfplumber 提取成功")
                else:
                    print("   ❌ pdfplumber 提取失败 - 内容为空")
    except Exception as e:
        print(f"   ❌ pdfplumber 异常: {e}")
    
    # 3. 测试PyMuPDF (fitz)
    print("\n🔍 测试 PyMuPDF (fitz):")
    try:
        doc = fitz.open(pdf_file)
        print(f"   页数: {len(doc)}")
        if len(doc) > 0:
            page = doc[0]
            text = page.get_text()
            print(f"   内容长度: {len(text)}")
            print(f"   内容预览: {repr(text[:100])}")
            if len(text) > 0:
                print("   ✅ PyMuPDF 提取成功")
            else:
                print("   ❌ PyMuPDF 提取失败 - 内容为空")
        doc.close()
    except Exception as e:
        print(f"   ❌ PyMuPDF 异常: {e}")
    
    # 4. 测试pdfplumber的表格提取
    print("\n🔍 测试 pdfplumber 表格提取:")
    try:
        with pdfplumber.open(pdf_file) as pdf:
            if len(pdf.pages) > 0:
                page = pdf.pages[0]
                tables = page.extract_tables()
                print(f"   表格数量: {len(tables) if tables else 0}")
                if tables:
                    for i, table in enumerate(tables):
                        print(f"   表格 {i+1} 行数: {len(table)}")
                        if table and len(table) > 0:
                            print(f"   表格 {i+1} 列数: {len(table[0])}")
                            print(f"   表格 {i+1} 预览: {table[0][:3] if len(table[0]) > 0 else 'Empty'}")
    except Exception as e:
        print(f"   ❌ pdfplumber 表格提取异常: {e}")

if __name__ == "__main__":
    test_pdf_libraries()
