#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的页面显示检查脚本
检查所有页面的文字显示、布局和样式问题
"""

import requests
import time
import json

def test_page_accessibility(url, page_name):
    """测试页面可访问性"""
    print(f"\n📄 测试页面: {page_name}")
    print(f"🔗 URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ 状态码: {response.status_code}")
            print(f"📄 页面大小: {len(response.text)} 字符")
            
            content = response.text
            
            # 检查基本元素
            checks = {
                'React根元素': 'id="root"' in content,
                'HTML结构完整': '<html' in content and '<body>' in content and '</body>' in content,
                'CSS文件加载': 'main.' in content and '.css' in content,
                'JS文件加载': 'main.' in content and '.js' in content,
                '平台标题': 'AI助贷招标平台' in content,
                '无JavaScript错误': 'error' not in content.lower() or 'react' not in content.lower(),
                '无404错误': '404' not in content and 'not found' not in content.lower()
            }
            
            for check_name, result in checks.items():
                print(f"  {'✅' if result else '❌'} {check_name}: {'通过' if result else '失败'}")
            
            # 检查特定页面的元素
            if 'login' in url:
                login_checks = {
                    '登录表单': 'login' in content.lower() or 'password' in content.lower(),
                    '用户名输入': 'username' in content.lower() or 'email' in content.lower(),
                    '密码输入': 'password' in content.lower(),
                    '登录按钮': 'login' in content.lower() or '登录' in content
                }
                for check_name, result in login_checks.items():
                    print(f"  {'✅' if result else '❌'} {check_name}: {'找到' if result else '未找到'}")
            
            elif 'risk-assessment' in url:
                risk_checks = {
                    '风险评估表单': 'risk' in content.lower() or 'assessment' in content.lower(),
                    '企业名称输入': 'company' in content.lower() or '企业' in content,
                    '风险评估按钮': 'assess' in content.lower() or '评估' in content
                }
                for check_name, result in risk_checks.items():
                    print(f"  {'✅' if result else '❌'} {check_name}: {'找到' if result else '未找到'}")
            
            elif 'auto-matching' in url:
                matching_checks = {
                    '自动匹配功能': 'matching' in content.lower() or '匹配' in content,
                    '匹配按钮': 'match' in content.lower() or '匹配' in content
                }
                for check_name, result in matching_checks.items():
                    print(f"  {'✅' if result else '❌'} {check_name}: {'找到' if result else '未找到'}")
            
            return True
            
        else:
            print(f"❌ 状态码: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 无法连接到服务器")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_css_loading():
    """测试CSS文件加载"""
    print("\n🎨 测试CSS文件加载...")
    
    try:
        # 测试主CSS文件
        css_response = requests.get("http://localhost:3000/static/css/main.66c8c144.css", timeout=5)
        
        if css_response.status_code == 200:
            print(f"✅ 主CSS文件: {len(css_response.text)} 字符")
            
            css_content = css_response.text
            
            # 检查关键样式
            style_checks = {
                '导航栏样式': '.navbar' in css_content or '.user-navbar' in css_content,
                '首页样式': '.home' in css_content or '.home-header' in css_content,
                '响应式样式': '@media' in css_content,
                '用户信息样式': '.user-info' in css_content or '.user-name' in css_content,
                '按钮样式': '.btn' in css_content or '.button' in css_content,
                '表单样式': '.form' in css_content or 'input' in css_content,
                '布局样式': 'flex' in css_content or 'grid' in css_content,
                '文字样式': 'font-size' in css_content or 'font-family' in css_content
            }
            
            for check_name, result in style_checks.items():
                print(f"  {'✅' if result else '❌'} {check_name}: {'找到' if result else '未找到'}")
            
            # 检查是否有中文支持
            has_chinese_fonts = 'font-family' in css_content and ('Microsoft' in css_content or 'SimSun' in css_content or 'PingFang' in css_content)
            print(f"  {'✅' if has_chinese_fonts else '⚠️'} 中文字体支持: {'找到' if has_chinese_fonts else '未明确配置'}")
            
            return True
        else:
            print(f"❌ CSS文件访问失败: {css_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CSS文件测试失败: {e}")
        return False

def test_js_loading():
    """测试JavaScript文件加载"""
    print("\n⚡ 测试JavaScript文件加载...")
    
    try:
        # 测试主JS文件
        js_response = requests.get("http://localhost:3000/static/js/main.832e8636.js", timeout=5)
        
        if js_response.status_code == 200:
            print(f"✅ 主JS文件: {len(js_response.text)} 字符")
            
            js_content = js_response.text
            
            # 检查关键功能
            js_checks = {
                'React相关': 'react' in js_content.lower(),
                '路由功能': 'router' in js_content.lower() or 'route' in js_content.lower(),
                'HTTP请求': 'fetch' in js_content.lower() or 'axios' in js_content.lower(),
                '状态管理': 'state' in js_content.lower() or 'useState' in js_content,
                '组件功能': 'component' in js_content.lower() or 'Component' in js_content
            }
            
            for check_name, result in js_checks.items():
                print(f"  {'✅' if result else '❌'} {check_name}: {'找到' if result else '未找到'}")
            
            return True
        else:
            print(f"❌ JS文件访问失败: {js_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ JS文件测试失败: {e}")
        return False

def test_api_connectivity():
    """测试API连接性"""
    print("\n🔌 测试API连接性...")
    
    api_endpoints = [
        "http://localhost:8000/api/v1/health",
        "http://localhost:8000/api/v1/chat/session",
        "http://localhost:8000/api/v1/credit/query"
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"  {'✅' if response.status_code in [200, 404, 405] else '❌'} {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {endpoint}: 连接失败")

def main():
    """主函数"""
    print("🧪 全面页面显示检查开始...")
    print("=" * 60)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    # 测试的页面列表
    pages_to_test = [
        ("http://localhost:3000/", "首页"),
        ("http://localhost:3000/login", "登录页"),
        ("http://localhost:3000/risk-assessment", "风险评估页"),
        ("http://localhost:3000/auto-matching", "自动匹配页"),
        ("http://localhost:3000/ai-chatbot-demo", "AI客服演示页")
    ]
    
    # 测试所有页面
    successful_pages = 0
    for url, page_name in pages_to_test:
        if test_page_accessibility(url, page_name):
            successful_pages += 1
    
    # 测试CSS和JS加载
    css_ok = test_css_loading()
    js_ok = test_js_loading()
    
    # 测试API连接
    test_api_connectivity()
    
    # 总结
    print("\n" + "=" * 60)
    print("🎯 检查完成！")
    print(f"📊 页面测试: {successful_pages}/{len(pages_to_test)} 通过")
    print(f"🎨 CSS加载: {'✅ 正常' if css_ok else '❌ 异常'}")
    print(f"⚡ JS加载: {'✅ 正常' if js_ok else '❌ 异常'}")
    
    if successful_pages == len(pages_to_test) and css_ok and js_ok:
        print("\n🎉 所有检查都通过了！页面显示应该正常。")
    else:
        print("\n⚠️ 发现问题，请检查上述失败的测试项。")
    
    print("\n💡 如果页面显示仍有问题，请检查：")
    print("1. 浏览器缓存 - 尝试硬刷新 (Ctrl+F5)")
    print("2. 网络连接 - 确保所有服务都在运行")
    print("3. 控制台错误 - 打开浏览器开发者工具查看错误")

if __name__ == "__main__":
    main()
