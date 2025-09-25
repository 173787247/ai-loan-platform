#!/usr/bin/env python3
"""
测试首页具体问题
"""

import requests
import time

def test_homepage():
    """测试首页问题"""
    
    print("🧪 测试首页问题...")
    
    try:
        # 测试首页
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ 首页状态码: {response.status_code}")
        
        # 检查响应内容
        content = response.text
        print(f"📄 响应长度: {len(content)} 字符")
        
        # 检查关键元素是否存在
        if "AI助贷招标平台" in content:
            print("✅ 找到平台标题")
        else:
            print("❌ 未找到平台标题")
            
        if "智能金融科技解决方案" in content:
            print("✅ 找到副标题")
        else:
            print("❌ 未找到副标题")
            
        if "home-header" in content:
            print("✅ 找到首页头部")
        else:
            print("❌ 未找到首页头部")
            
        if "features" in content:
            print("✅ 找到功能区域")
        else:
            print("❌ 未找到功能区域")
            
        # 检查是否有错误信息
        if "error" in content.lower():
            print("⚠️ 发现错误信息")
            
        if "exception" in content.lower():
            print("⚠️ 发现异常信息")
            
        # 检查CSS和JS是否正确加载
        if "static/css" in content:
            print("✅ CSS文件正常加载")
        else:
            print("❌ CSS文件可能有问题")
            
        if "static/js" in content:
            print("✅ JS文件正常加载")
        else:
            print("❌ JS文件可能有问题")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_homepage()
