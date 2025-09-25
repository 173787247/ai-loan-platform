#!/usr/bin/env python3
"""
调试正则表达式匹配
"""

import re

def debug_regex():
    """调试正则表达式匹配"""
    print("🔍 调试正则表达式匹配...")
    
    test_messages = [
        "花旗银行的产品能在中国销售吗",
        "请介绍一下花旗银行",
        "花旗银行有什么贷款产品？",
        "中国银行和花旗银行哪个好",
        "我想了解中国银行的产品"
    ]
    
    bank_pattern = r'([^，。！？\s]+银行)'
    
    for message in test_messages:
        print(f"\n📝 测试消息: {message}")
        matches = re.findall(bank_pattern, message)
        print(f"🔍 匹配结果: {matches}")
        
        if matches:
            # 过滤掉常见的干扰词
            filtered_matches = []
            for match in matches:
                # 跳过"中国银行"如果句子中还有其他银行名称
                if match == "中国银行" and len(matches) > 1:
                    print(f"❌ 跳过干扰词: {match}")
                    continue
                # 跳过"银行"本身
                if match == "银行":
                    print(f"❌ 跳过干扰词: {match}")
                    continue
                filtered_matches.append(match)
                print(f"✅ 保留匹配: {match}")
            
            if filtered_matches:
                # 优先返回更具体的银行名称（更长的匹配）
                bank_name = max(filtered_matches, key=len)
                print(f"🎯 最终选择: {bank_name}")
            elif matches:
                # 如果没有过滤后的结果，返回第一个匹配
                bank_name = matches[0]
                print(f"🎯 回退选择: {bank_name}")
        else:
            print("❌ 没有匹配到银行")

if __name__ == "__main__":
    debug_regex()
