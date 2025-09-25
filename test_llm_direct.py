#!/usr/bin/env python3
"""
直接测试LLM生成API
"""

import requests
import json
import time

def test_llm_direct():
    """直接测试LLM生成API"""
    print("🤖 直接测试LLM生成API...")
    
    # 等待服务启动
    print("⏳ 等待AI服务启动...")
    time.sleep(20)
    
    # 测试LLM生成
    print("\n1. 测试LLM生成...")
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/llm/generate',
            json={
                'messages': [
                    {'role': 'user', 'content': '请分析以下用户消息，识别其中提到的银行名称。\n\n用户消息: "介绍一下国外有哪些银行在中国有业务？"\n\n请从以下银行列表中选择最匹配的银行名称，如果没有匹配的银行，请返回"未知银行"。\n\n支持的银行列表:\n- 人民银行 (央行、中国人民银行、人行)\n- 招商银行 (招行、CMB)\n- 中国银行 (中行、BOC)\n- 工商银行 (工行、ICBC)\n- 建设银行 (建行、CCB)\n- 农业银行 (农行、ABChina)\n- 光大银行 (光大、CEB)\n- 民生银行 (民生、CMBC)\n- 兴业银行 (兴业、CIB)\n- 浦发银行 (浦发、SPDB)\n- 交通银行 (交行、BOCOM)\n- 中信银行 (中信、CITIC)\n- 华夏银行 (华夏、HXB)\n- 广发银行 (广发、CGB)\n- 平安银行 (平安、PAB)\n- 邮储银行 (邮储、PSBC)\n- 北京银行 (北京、BOB)\n- 上海银行 (上海、BOSC)\n- 江苏银行 (江苏、JSB)\n- 浙商银行 (浙商、CZB)\n- 渤海银行 (渤海、CBHB)\n- 花旗银行 (花旗、Citi)\n- 汇丰银行 (汇丰、HSBC)\n- 渣打银行 (渣打、Standard Chartered)\n- 台湾银行 (台银、Bank of Taiwan)\n- 第一银行 (一银、First Bank)\n- 华南银行 (华银、Hua Nan Bank)\n- 彰化银行 (彰银、Chang Hwa Bank)\n- 土地银行 (土银、Land Bank)\n- 合作金库银行 (合库、Taiwan Cooperative Bank)\n\n注意:\n1. 如果用户询问的是"有哪些银行"、"台湾银行"、"大陆银行"、"国外银行"、"外资银行"等泛指概念，请返回"未知银行"\n2. 如果用户询问的是具体银行的产品或服务，请返回该银行名称\n3. 如果用户询问的是银行比较或选择，请返回"未知银行"\n4. 如果用户询问的是"国外有哪些银行在中国有业务"、"外资银行在中国"等泛指查询，请返回"未知银行"\n5. 如果用户询问的是"花旗银行"、"汇丰银行"等具体银行，请返回该银行名称\n\n请只返回银行名称，不要返回其他内容。'}
                ],
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.1,
                'max_tokens': 50
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ LLM生成成功: {data}")
        else:
            print(f"❌ LLM生成失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ LLM生成异常: {e}")
    
    print("\n🎉 LLM生成API测试完成！")

if __name__ == "__main__":
    test_llm_direct()