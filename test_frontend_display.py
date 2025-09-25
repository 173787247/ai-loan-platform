#!/usr/bin/env python3
"""
测试前端页面实际显示效果
"""

import requests
import time
import re

def test_frontend_pages():
    """测试前端页面显示"""
    
    print("🧪 测试前端页面显示效果...")
    
    # 等待前端启动
    print("⏳ 等待前端服务启动...")
    time.sleep(5)
    
    # 测试页面列表
    pages = [
        ("首页", "http://localhost:3000/"),
        ("登录页", "http://localhost:3000/login"),
        ("风险评估", "http://localhost:3000/risk-assessment"),
        ("智能匹配", "http://localhost:3000/auto-matching"),
    ]
    
    for page_name, url in pages:
        print(f"\n📄 测试页面: {page_name}")
        print(f"🔗 URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ 状态码: {response.status_code}")
            
            content = response.text
            print(f"📄 内容长度: {len(content)} 字符")
            
            # 检查关键元素
            checks = [
                ("React根元素", 'id="root"'),
                ("CSS文件", 'static/css'),
                ("JS文件", 'static/js'),
                ("平台标题", "AI助贷招标平台"),
                ("导航栏", "navbar"),
                ("用户信息", "user-info"),
                ("登录按钮", "login"),
            ]
            
            for check_name, pattern in checks:
                if pattern in content:
                    print(f"  ✅ {check_name}: 找到")
                else:
                    print(f"  ❌ {check_name}: 未找到")
            
            # 检查是否有错误
            error_patterns = [
                r'error',
                r'exception',
                r'undefined',
                r'null',
                r'failed',
                r'cannot',
                r'not found'
            ]
            
            errors_found = []
            for pattern in error_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    errors_found.append(pattern)
            
            if errors_found:
                print(f"  ⚠️ 发现错误关键词: {', '.join(errors_found)}")
            else:
                print(f"  ✅ 未发现明显错误")
            
            # 检查HTML结构
            if '<html' in content and '</html>' in content:
                print(f"  ✅ HTML结构完整")
            else:
                print(f"  ❌ HTML结构不完整")
                
            if '<head>' in content and '<body>' in content:
                print(f"  ✅ 基本HTML标签存在")
            else:
                print(f"  ❌ 缺少基本HTML标签")
            
        except requests.exceptions.ConnectionError:
            print(f"  ❌ 连接失败 - 前端服务可能未启动")
        except requests.exceptions.Timeout:
            print(f"  ❌ 请求超时")
        except Exception as e:
            print(f"  ❌ 测试失败: {e}")
    
    print("\n🎯 前端页面测试完成！")

if __name__ == "__main__":
    test_frontend_pages()
