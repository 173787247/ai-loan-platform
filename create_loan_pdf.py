#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_loan_pdf():
    """创建银行贷款产品介绍PDF"""
    filename = "银行贷款产品介绍.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # 标题
    title = Paragraph("银行贷款产品介绍", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # 内容
    content = """
    <h2>个人信用贷款产品</h2>
    
    <h3>工商银行 - 工行融e借</h3>
    <p>产品特点：</p>
    <ul>
    <li>利率范围：3.5%-10.5%（年化）</li>
    <li>贷款额度：1-80万元</li>
    <li>贷款期限：6-60个月</li>
    <li>审批速度：最快当天放款</li>
    <li>申请条件：月收入2000元以上，稳定工作3个月以上</li>
    </ul>
    
    <h3>建设银行 - 建行快贷</h3>
    <p>产品特点：</p>
    <ul>
    <li>利率范围：4.0%-11.5%（年化）</li>
    <li>贷款额度：1-100万元</li>
    <li>贷款期限：6-60个月</li>
    <li>审批速度：最快2个工作日</li>
    <li>申请条件：月收入2500元以上，稳定工作6个月以上</li>
    </ul>
    
    <h3>招商银行 - 招行信用贷</h3>
    <p>产品特点：</p>
    <ul>
    <li>利率范围：4.5%-12%（年化）</li>
    <li>贷款额度：1-50万元</li>
    <li>贷款期限：6-60个月</li>
    <li>审批速度：最快1个工作日</li>
    <li>申请条件：月收入3000元以上，稳定工作6个月以上</li>
    </ul>
    
    <h2>申请材料清单</h2>
    <p>必备材料：</p>
    <ul>
    <li>身份证原件及复印件</li>
    <li>收入证明（工资单或银行流水）</li>
    <li>工作证明（劳动合同或在职证明）</li>
    <li>征信报告（个人版）</li>
    </ul>
    
    <h2>申请流程</h2>
    <ol>
    <li>在线申请或到银行网点申请</li>
    <li>提交相关材料</li>
    <li>银行审核</li>
    <li>审批通过后放款</li>
    </ol>
    """
    
    content_para = Paragraph(content, styles['Normal'])
    story.append(content_para)
    
    # 生成PDF
    doc.build(story)
    print(f"PDF文件已创建: {filename}")
    return filename

if __name__ == "__main__":
    create_loan_pdf()
