#!/usr/bin/env python3
"""
测试简单格式化
"""

def test_simple_format():
    """测试简单格式化"""
    print("🧪 测试简单格式化")
    print("=" * 50)
    
    # 模拟格式化内容
    formatted_lines = []
    formatted_lines.append("💰 **100万个人信用贷款银行推荐**")
    formatted_lines.append("=" * 50)
    formatted_lines.append("")
    formatted_lines.append("🎯 **100万贷款推荐分析**")
    formatted_lines.append("-" * 35)
    formatted_lines.append("")
    formatted_lines.append("🏆 **首选推荐：建设银行**")
    formatted_lines.append("-" * 30)
    formatted_lines.append("✅ 额度支持：1-100万（最高）")
    formatted_lines.append("✅ 利率范围：4.0%-11.5%")
    formatted_lines.append("✅ 审批速度：最快2个工作日")
    formatted_lines.append("✅ 申请条件：月收入2500元，工作6个月")
    formatted_lines.append("")
    
    result = '\n'.join(formatted_lines)
    
    print("📊 格式化结果:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    
    print("\n📊 原始字符串 (repr):")
    print("=" * 60)
    print(repr(result))
    print("=" * 60)
    
    print(f"\n📈 统计:")
    print(f"  • 总字符数: {len(result)}")
    print(f"  • 换行符数量: {result.count('\\n')}")
    print(f"  • 行数: {len(result.split('\\n'))}")

if __name__ == "__main__":
    test_simple_format()
