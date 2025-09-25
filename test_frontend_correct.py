#!/usr/bin/env python3
"""
正确测试前端页面
"""

import requests
import re
from bs4 import BeautifulSoup

def test_frontend_correct():
    """正确测试前端页面"""
    
    print("🧪 正确测试前端页面...")
    
    try:
        # 测试首页
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ 首页状态码: {response.status_code}")
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 检查CSS文件
        css_links = soup.find_all('link', rel='stylesheet')
        print(f"📄 CSS文件数量: {len(css_links)}")
        for link in css_links:
            href = link.get('href', '')
            print(f"  - {href}")
        
        # 检查JS文件
        js_scripts = soup.find_all('script', src=True)
        print(f"📄 JS文件数量: {len(js_scripts)}")
        for script in js_scripts:
            src = script.get('src', '')
            print(f"  - {src}")
        
        # 检查React根元素
        root_div = soup.find('div', id='root')
        if root_div:
            print("✅ React根元素存在")
            print(f"📄 根元素内容长度: {len(root_div.get_text())}")
        else:
            print("❌ React根元素不存在")
        
        # 检查页面标题
        title = soup.find('title')
        if title:
            print(f"📄 页面标题: {title.get_text()}")
        
        # 检查是否有错误信息
        error_elements = soup.find_all(text=re.compile(r'error|Error|ERROR', re.I))
        if error_elements:
            print(f"⚠️ 发现错误信息: {len(error_elements)} 处")
            for error in error_elements[:3]:  # 只显示前3个
                print(f"  - {error.strip()}")
        else:
            print("✅ 未发现错误信息")
        
        # 检查页面内容
        body_text = soup.get_text()
        if "AI助贷招标平台" in body_text:
            print("✅ 找到平台标题")
        else:
            print("❌ 未找到平台标题")
            
        if "智能金融科技解决方案" in body_text:
            print("✅ 找到副标题")
        else:
            print("❌ 未找到副标题")
        
        print(f"📄 页面总文本长度: {len(body_text)} 字符")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_frontend_correct()
