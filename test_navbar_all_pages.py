#!/usr/bin/env python3
"""
测试所有页面的导航栏显示
"""

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_navbar_on_all_pages():
    """测试所有页面的导航栏"""
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        base_url = "http://localhost:3000"
        
        # 测试页面列表
        test_pages = [
            ("首页", "/"),
            ("风险评估", "/risk-assessment"),
            ("智能匹配", "/auto-matching"),
            ("实时监控", "/monitoring"),
            ("通知中心", "/notifications"),
            ("智能仪表板", "/dashboard"),
            ("数据分析", "/analytics"),
            ("报表中心", "/reports"),
            ("AI智能客服", "/ai-chatbot-demo")
        ]
        
        print("🧪 测试所有页面的导航栏显示...")
        
        for page_name, path in test_pages:
            print(f"\n📄 测试页面: {page_name}")
            url = f"{base_url}{path}"
            
            try:
                driver.get(url)
                time.sleep(2)  # 等待页面加载
                
                # 检查导航栏元素
                navbar_elements = {
                    "Logo": "//span[@class='logo-text']",
                    "用户信息": "//div[@class='user-info']",
                    "用户名": "//span[@class='user-name']",
                    "用户类型": "//span[@class='user-type']",
                    "登出按钮": "//button[@class='logout-btn']"
                }
                
                for element_name, xpath in navbar_elements.items():
                    try:
                        element = driver.find_element(By.XPATH, xpath)
                        text = element.text.strip()
                        is_visible = element.is_displayed()
                        print(f"  ✅ {element_name}: '{text}' (可见: {is_visible})")
                        
                        # 检查文字是否被截断
                        if element_name in ["用户类型", "用户名"] and text:
                            if len(text) < 3 or "..." in text:
                                print(f"  ⚠️  {element_name} 可能被截断: '{text}'")
                    except Exception as e:
                        print(f"  ❌ {element_name}: 未找到 - {e}")
                
                # 检查导航链接
                nav_links = driver.find_elements(By.CLASS_NAME, "navbar-link")
                print(f"  📋 导航链接数量: {len(nav_links)}")
                for link in nav_links[:5]:  # 只显示前5个
                    link_text = link.text.strip()
                    if link_text:
                        print(f"    - {link_text}")
                
            except Exception as e:
                print(f"  ❌ 页面加载失败: {e}")
        
        print("\n🎯 导航栏测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    test_navbar_on_all_pages()
