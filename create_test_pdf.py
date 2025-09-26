#!/usr/bin/env python3
"""
创建测试PDF文件
在桌面生成一个简单的PDF用于测试
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os

def create_test_pdf():
    """创建测试PDF文件"""
    desktop_path = Path.home() / "Desktop"
    pdf_path = desktop_path / "test_document.pdf"
    
    try:
        # 创建PDF
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        width, height = letter
        
        # 添加标题
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "AI智能助贷招标平台 - 测试文档")
        
        # 添加内容
        c.setFont("Helvetica", 12)
        y_position = height - 150
        
        content = [
            "这是一个用于测试PDF上传功能的文档。",
            "",
            "文档内容：",
            "1. 测试文档上传功能",
            "2. 验证OCR识别能力", 
            "3. 检查文档处理流程",
            "",
            "技术信息：",
            "- 文档类型：PDF",
            "- 创建时间：2025年9月25日",
            "- 用途：系统测试",
            "",
            "如果您看到这个文档，说明PDF上传功能正常工作！",
            "",
            "AI智能助贷招标平台",
            "智能金融科技解决方案"
        ]
        
        for line in content:
            c.drawString(100, y_position, line)
            y_position -= 20
        
        # 保存PDF
        c.save()
        
        print(f"✅ 测试PDF文件已创建: {pdf_path}")
        print(f"文件大小: {pdf_path.stat().st_size / 1024:.2f} KB")
        return pdf_path
        
    except ImportError:
        print("❌ 缺少reportlab库，正在安装...")
        os.system("pip install reportlab")
        print("请重新运行此脚本")
        return None
    except Exception as e:
        print(f"❌ 创建PDF失败: {str(e)}")
        return None

if __name__ == "__main__":
    create_test_pdf()