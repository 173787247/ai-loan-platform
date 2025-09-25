#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_loan_pdf():
    """创建真实的银行贷款产品介绍PDF"""
    filename = "real_loan_guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # 标题
    title = Paragraph("中国工商银行个人信用贷款产品介绍", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # 产品概述
    overview = Paragraph("""
    <b>产品概述：</b><br/>
    工行融e借是工商银行推出的个人信用贷款产品，具有额度高、利率低、审批快的特点。
    """, styles['Normal'])
    story.append(overview)
    story.append(Spacer(1, 12))
    
    # 产品特点
    features = Paragraph("""
    <b>产品特点：</b><br/>
    • 贷款额度：1-80万元<br/>
    • 贷款利率：3.5%-10.5%（年化）<br/>
    • 贷款期限：6-60个月<br/>
    • 审批速度：最快当天放款<br/>
    • 还款方式：等额本息、等额本金
    """, styles['Normal'])
    story.append(features)
    story.append(Spacer(1, 12))
    
    # 申请条件
    conditions = Paragraph("""
    <b>申请条件：</b><br/>
    • 年龄：18-65周岁<br/>
    • 收入：月收入2000元以上<br/>
    • 信用：征信良好，工行客户优先<br/>
    • 工作：稳定工作3个月以上
    """, styles['Normal'])
    story.append(conditions)
    story.append(Spacer(1, 12))
    
    # 申请材料
    materials = Paragraph("""
    <b>申请材料：</b><br/>
    • 身份证原件及复印件<br/>
    • 收入证明（工资单、银行流水）<br/>
    • 工作证明（劳动合同、在职证明）<br/>
    • 征信报告<br/>
    • 工行银行卡或存折
    """, styles['Normal'])
    story.append(materials)
    story.append(Spacer(1, 12))
    
    # 申请流程
    process = Paragraph("""
    <b>申请流程：</b><br/>
    1. 在线申请：登录工行手机银行或网银<br/>
    2. 提交材料：上传相关证明文件<br/>
    3. 系统审核：自动评估信用状况<br/>
    4. 人工审批：银行工作人员审核<br/>
    5. 放款：审批通过后立即放款
    """, styles['Normal'])
    story.append(process)
    story.append(Spacer(1, 12))
    
    # 注意事项
    notes = Paragraph("""
    <b>注意事项：</b><br/>
    • 请确保提供真实有效的材料<br/>
    • 保持良好的信用记录<br/>
    • 按时还款，避免逾期<br/>
    • 如有疑问，请联系客服热线：95588
    """, styles['Normal'])
    story.append(notes)
    
    # 生成PDF
    doc.build(story)
    print(f"已创建PDF文件: {filename}")
    return filename

if __name__ == "__main__":
    create_loan_pdf()
