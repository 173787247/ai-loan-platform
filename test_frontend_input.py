#!/usr/bin/env python3
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_frontend_input():
    """测试前端输入框功能"""
    print("🧪 测试前端输入框功能...")
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    try:
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:3000")
        
        print("✅ 页面加载成功")
        
        # 等待页面加载
        time.sleep(3)
        
        # 查找输入框
        try:
            input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            print("✅ 找到输入框")
            
            # 检查输入框是否可用
            is_enabled = input_element.is_enabled()
            print(f"输入框是否启用: {is_enabled}")
            
            # 尝试输入文字
            input_element.clear()
            input_element.send_keys("测试消息")
            
            # 检查输入是否成功
            input_value = input_element.get_attribute('value')
            print(f"输入框内容: '{input_value}'")
            
            if input_value == "测试消息":
                print("✅ 输入框可以正常输入")
            else:
                print("❌ 输入框无法输入")
                
        except Exception as e:
            print(f"❌ 找不到输入框: {e}")
            
        # 查找发送按钮
        try:
            send_button = driver.find_element(By.XPATH, "//button[contains(text(), '发送')]")
            print("✅ 找到发送按钮")
            
            # 检查按钮是否可用
            is_button_enabled = send_button.is_enabled()
            print(f"发送按钮是否启用: {is_button_enabled}")
            
        except Exception as e:
            print(f"❌ 找不到发送按钮: {e}")
            
        driver.quit()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_frontend_input()
