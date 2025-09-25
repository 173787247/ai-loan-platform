#!/usr/bin/env python3
"""
调试关键词匹配
"""

def debug_keywords():
    """调试关键词匹配"""
    print("🔍 调试关键词匹配...")
    
    # 模拟银行关键词映射
    bank_keywords = {
        "人民银行": ["人民银行", "央行", "pboc", "中国人民银行", "央行", "人民银行", "人行"],
        "招商银行": ["招商银行", "招行", "cmb", "招商"],
        "中国银行": ["中国银行", "中行", "boc", "中国"],
        "工商银行": ["工商银行", "工行", "icbc", "工商"],
        "建设银行": ["建设银行", "建行", "ccb", "建设"],
        "农业银行": ["农业银行", "农行", "abchina", "农业"],
        "光大银行": ["光大银行", "光大", "cebbank", "光大"],
        "民生银行": ["民生银行", "民生", "cmbc", "民生"],
        "兴业银行": ["兴业银行", "兴业", "cib", "兴业"],
        "浦发银行": ["浦发银行", "浦发", "spdb", "浦发"],
        "交通银行": ["交通银行", "交行", "bocom", "交通"],
        "中信银行": ["中信银行", "中信", "citic", "中信"],
        "华夏银行": ["华夏银行", "华夏", "hxb", "华夏"],
        "广发银行": ["广发银行", "广发", "cgb", "广发"],
        "平安银行": ["平安银行", "平安", "pab", "平安"],
        "邮储银行": ["邮储银行", "邮储", "psbc", "邮储"],
        "北京银行": ["北京银行", "北京", "bob", "北京"],
        "上海银行": ["上海银行", "上海", "bosc", "上海"],
        "江苏银行": ["江苏银行", "江苏", "jsb", "江苏"],
        "浙商银行": ["浙商银行", "浙商", "czb", "浙商"],
        "渤海银行": ["渤海银行", "渤海", "cbhb", "渤海"]
    }
    
    test_message = "花旗银行的产品能在中国销售吗"
    user_message_lower = test_message.lower()
    
    print(f"📝 测试消息: {test_message}")
    print(f"📝 小写消息: {user_message_lower}")
    
    # 直接关键词匹配 - 优先匹配完整的银行名称
    for bank_name, keywords in bank_keywords.items():
        # 优先匹配完整的银行名称
        if bank_name in test_message:
            print(f"✅ 完整银行名称匹配: {bank_name}")
            return bank_name
        # 然后匹配其他关键词
        for keyword in keywords:
            if keyword == bank_name:  # 跳过银行名称本身，避免重复匹配
                continue
            if keyword in user_message_lower:
                print(f"✅ 关键词匹配: {bank_name} -> {keyword}")
                return bank_name
    
    print("❌ 没有匹配到预设银行")
    return None

if __name__ == "__main__":
    result = debug_keywords()
    print(f"🎯 最终结果: {result}")
