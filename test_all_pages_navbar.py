#!/usr/bin/env python3
"""
全面测试所有页面的导航栏显示问题
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_all_pages():
    """测试所有页面的导航栏"""
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        base_url = "http://localhost:3000"
        
        # 等待前端启动
        print("⏳ 等待前端服务启动...")
        time.sleep(10)
        
        # 测试页面列表
        test_pages = [
            ("首页", "/"),
            ("登录页", "/login"),
            ("风险评估", "/risk-assessment"),
            ("智能匹配", "/auto-matching"),
            ("实时监控", "/monitoring"),
            ("通知中心", "/notifications"),
            ("智能仪表板", "/dashboard"),
            ("数据分析", "/analytics"),
            ("报表中心", "/reports"),
            ("AI智能客服", "/ai-chatbot-demo")
        ]
        
        print("🧪 开始全面测试所有页面的导航栏...")
        
        for page_name, path in test_pages:
            print(f"\n📄 测试页面: {page_name} ({path})")
            url = f"{base_url}{path}"
            
            try:
                driver.get(url)
                time.sleep(3)  # 等待页面完全加载
                
                # 检查页面是否正常加载
                page_title = driver.title
                print(f"  📋 页面标题: {page_title}")
                
                # 检查导航栏关键元素
                navbar_issues = []
                
                # 1. 检查Logo
                try:
                    logo = driver.find_element(By.CLASS_NAME, "navbar-logo")
                    logo_text = logo.text.strip()
                    print(f"  ✅ Logo: '{logo_text}'")
                except:
                    navbar_issues.append("Logo未找到")
                
                # 2. 检查用户信息区域
                try:
                    user_info = driver.find_element(By.CLASS_NAME, "user-info")
                    user_text = user_info.text.strip()
                    print(f"  👤 用户信息: '{user_text}'")
                    
                    # 检查是否有换行问题
                    if '\n' in user_text or len(user_text.split()) > 3:
                        navbar_issues.append(f"用户信息换行: '{user_text}'")
                    
                except:
                    navbar_issues.append("用户信息未找到")
                
                # 3. 检查用户名
                try:
                    username = driver.find_element(By.CLASS_NAME, "user-name")
                    username_text = username.text.strip()
                    print(f"  👤 用户名: '{username_text}'")
                except:
                    pass
                
                # 4. 检查用户类型
                try:
                    user_type = driver.find_element(By.CLASS_NAME, "user-type")
                    user_type_text = user_type.text.strip()
                    print(f"  🏷️ 用户类型: '{user_type_text}'")
                    
                    # 检查是否被截断
                    if len(user_type_text) < 2 or user_type_text in ['统', '管', '理', '员']:
                        navbar_issues.append(f"用户类型被截断: '{user_type_text}'")
                        
                except:
                    pass
                
                # 5. 检查导航链接数量
                try:
                    nav_links = driver.find_elements(By.CLASS_NAME, "navbar-link")
                    print(f"  🔗 导航链接数量: {len(nav_links)}")
                    
                    # 检查前几个链接的文本
                    for i, link in enumerate(nav_links[:5]):
                        link_text = link.text.strip()
                        if link_text:
                            print(f"    - {link_text}")
                            
                except:
                    navbar_issues.append("导航链接未找到")
                
                # 6. 检查登出按钮
                try:
                    logout_btn = driver.find_element(By.CLASS_NAME, "logout-btn")
                    logout_text = logout_btn.text.strip()
                    print(f"  🚪 登出按钮: '{logout_text}'")
                except:
                    pass
                
                # 汇总问题
                if navbar_issues:
                    print(f"  ❌ 发现问题: {', '.join(navbar_issues)}")
                else:
                    print(f"  ✅ 页面正常")
                
            except Exception as e:
                print(f"  ❌ 页面加载失败: {e}")
        
        print("\n🎯 全面测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    test_all_pages()
