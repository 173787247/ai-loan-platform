#!/usr/bin/env python3
"""
创建OCR测试图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_images():
    """创建OCR测试图片"""
    print("🖼️ 创建OCR测试图片...")
    
    # 创建测试目录
    test_dir = "demo_test_images"
    os.makedirs(test_dir, exist_ok=True)
    
    # 创建测试图片1: 贷款产品信息
    img1 = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img1)
    
    # 尝试使用系统字体，如果失败则使用默认字体
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    draw.text((50, 50), "AI智能助贷平台 - 产品介绍", fill='black', font=font_large)
    
    # 绘制产品信息
    y_pos = 100
    products = [
        "个人信用贷款: 1-50万元, 年利率4.5%-12%",
        "企业流动资金贷款: 10-500万元, 年利率3.8%-8.5%",
        "抵押贷款: 房产评估价70%, 年利率3.2%-6.8%",
        "消费贷款: 5-30万元, 年利率5.5%-15%"
    ]
    
    for product in products:
        draw.text((50, y_pos), product, fill='black', font=font_medium)
        y_pos += 40
    
    # 绘制申请条件
    draw.text((50, y_pos + 20), "申请条件:", fill='black', font=font_medium)
    conditions = [
        "• 年满18周岁，具有完全民事行为能力",
        "• 有稳定的收入来源和还款能力",
        "• 个人信用记录良好",
        "• 提供真实有效的身份证明和收入证明"
    ]
    
    for condition in conditions:
        y_pos += 30
        draw.text((70, y_pos), condition, fill='black', font=font_small)
    
    # 保存图片
    img1.save(f"{test_dir}/loan_products_info.png")
    print(f"✅ 创建图片1: {test_dir}/loan_products_info.png")
    
    # 创建测试图片2: 申请流程
    img2 = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img2)
    
    # 绘制标题
    draw.text((50, 50), "贷款申请流程", fill='black', font=font_large)
    
    # 绘制流程步骤
    y_pos = 100
    steps = [
        "第一步: 在线申请",
        "  - 访问AI智能助贷平台",
        "  - 填写基本信息",
        "  - 上传必要材料",
        "",
        "第二步: 智能评估",
        "  - AI风险评估系统分析",
        "  - 信用评分计算",
        "  - 风险等级确定",
        "",
        "第三步: 产品匹配",
        "  - 智能匹配最优产品",
        "  - 多维度对比分析",
        "  - 个性化推荐",
        "",
        "第四步: 审核放款",
        "  - 人工审核确认",
        "  - 合同签署",
        "  - 资金到账"
    ]
    
    for step in steps:
        if step.startswith("第"):
            draw.text((50, y_pos), step, fill='black', font=font_medium)
        elif step.startswith("  -"):
            draw.text((70, y_pos), step, fill='black', font=font_small)
        else:
            draw.text((50, y_pos), step, fill='black', font=font_small)
        y_pos += 25
    
    # 保存图片
    img2.save(f"{test_dir}/application_process.png")
    print(f"✅ 创建图片2: {test_dir}/application_process.png")
    
    # 创建测试图片3: 利率表
    img3 = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img3)
    
    # 绘制标题
    draw.text((50, 50), "贷款利率表", fill='black', font=font_large)
    
    # 绘制表格
    y_pos = 100
    table_data = [
        "产品类型          最低利率    最高利率    贷款期限",
        "个人信用贷款      4.5%       12%        6-36个月",
        "企业流贷          3.8%       8.5%       3-24个月",
        "抵押贷款          3.2%       6.8%       1-20年",
        "消费贷款          5.5%       15%        6-60个月"
    ]
    
    for row in table_data:
        draw.text((50, y_pos), row, fill='black', font=font_medium)
        y_pos += 35
    
    # 添加说明
    y_pos += 20
    draw.text((50, y_pos), "注: 实际利率根据个人信用状况和风险评估结果确定", 
              fill='red', font=font_small)
    
    # 保存图片
    img3.save(f"{test_dir}/interest_rates.png")
    print(f"✅ 创建图片3: {test_dir}/interest_rates.png")
    
    print(f"🎉 所有测试图片创建完成: {test_dir}/")
    return test_dir

if __name__ == "__main__":
    create_test_images()
