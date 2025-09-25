#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的前端显示测试脚本
检查页面是否正确加载和显示
"""

import requests
import time

def test_page_display():
    """测试页面显示"""
    base_url = "http://localhost:3000"
    
    print("🔍 检查前端页面显示...")
    
    try:
        # 测试首页
        print("\n📄 测试首页...")
        response = requests.get(base_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ 首页状态码: {response.status_code}")
            print(f"📄 页面大小: {len(response.text)} 字符")
            
            # 检查关键元素
            content = response.text
            
            # 检查CSS文件
            has_css = 'main.' in content and '.css' in content
            print(f"  {'✅' if has_css else '❌'} CSS文件: {'已加载' if has_css else '未加载'}")
            
            # 检查JS文件
            has_js = 'main.' in content and '.js' in content
            print(f"  {'✅' if has_js else '❌'} JS文件: {'已加载' if has_js else '未加载'}")
            
            # 检查平台标题
            has_title = 'AI助贷招标平台' in content
            print(f"  {'✅' if has_title else '❌'} 平台标题: {'找到' if has_title else '未找到'}")
            
            # 检查React根元素
            has_react_root = 'id="root"' in content
            print(f"  {'✅' if has_react_root else '❌'} React根元素: {'找到' if has_react_root else '未找到'}")
            
            # 检查是否有错误信息
            has_error = 'error' in content.lower() and 'react' in content.lower()
            print(f"  {'❌' if has_error else '✅'} 错误检查: {'发现错误' if has_error else '无错误'}")
            
            # 检查HTML结构
            has_html_structure = '<html' in content and '<body>' in content and '</body>' in content
            print(f"  {'✅' if has_html_structure else '❌'} HTML结构: {'完整' if has_html_structure else '不完整'}")
            
            # 检查是否使用生产构建
            is_production = 'main.' in content and 'static' in content
            print(f"  {'✅' if is_production else '❌'} 构建模式: {'生产构建' if is_production else '开发模式'}")
            
        else:
            print(f"❌ 首页访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端服务，请检查容器是否运行")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_css_files():
    """测试CSS文件是否可访问"""
    print("\n🎨 测试CSS文件...")
    
    try:
        # 测试CSS文件
        css_response = requests.get("http://localhost:3000/static/css/main.66c8c144.css", timeout=5)
        if css_response.status_code == 200:
            print(f"✅ CSS文件可访问: {len(css_response.text)} 字符")
            
            # 检查关键样式
            css_content = css_response.text
            has_navbar_styles = '.navbar' in css_content or '.user-navbar' in css_content
            has_home_styles = '.home-header' in css_content or '.home' in css_content
            has_responsive_styles = '@media' in css_content
            
            print(f"  {'✅' if has_navbar_styles else '❌'} 导航栏样式: {'找到' if has_navbar_styles else '未找到'}")
            print(f"  {'✅' if has_home_styles else '❌'} 首页样式: {'找到' if has_home_styles else '未找到'}")
            print(f"  {'✅' if has_responsive_styles else '❌'} 响应式样式: {'找到' if has_responsive_styles else '未找到'}")
            
        else:
            print(f"❌ CSS文件访问失败: {css_response.status_code}")
            
    except Exception as e:
        print(f"❌ CSS文件测试失败: {e}")

def main():
    """主函数"""
    print("🧪 前端显示测试开始...")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 测试页面显示
    test_page_display()
    
    # 测试CSS文件
    test_css_files()
    
    print("\n" + "=" * 50)
    print("🎯 测试完成！")
    print("\n💡 如果发现问题，请检查：")
    print("1. 前端容器是否正常运行")
    print("2. 是否使用生产构建")
    print("3. CSS文件是否正确加载")

if __name__ == "__main__":
    main()
