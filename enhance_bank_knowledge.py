#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强银行知识库 - 添加多银行产品对比信息
"""

import requests
import json

def add_bank_comparison_knowledge():
    """添加银行产品对比知识"""
    base_url = "http://localhost:8000/api/v1"
    
    # 银行产品对比知识
    bank_knowledge = [
        {
            "title": "招商银行个人信用贷款产品",
            "content": """
招商银行个人信用贷款产品详情：

产品名称：招行信用贷
申请条件：
- 年龄：22-55周岁
- 收入：月收入3000元以上
- 信用：征信良好，无逾期记录
- 工作：稳定工作6个月以上

产品特点：
- 利率：4.5%-12%（年化）
- 额度：1-50万元
- 期限：6-36个月
- 审批：最快1个工作日
- 还款：等额本息、等额本金、先息后本

申请材料：
- 身份证原件及复印件
- 收入证明（工资单、银行流水）
- 工作证明（劳动合同、在职证明）
- 征信报告
- 其他资产证明（房产、车产等）
            """,
            "category": "bank_products",
            "metadata": {"bank": "招商银行", "product_type": "个人信用贷款"}
        },
        {
            "title": "工商银行个人信用贷款产品",
            "content": """
工商银行个人信用贷款产品详情：

产品名称：工行融e借
申请条件：
- 年龄：18-65周岁
- 收入：月收入2000元以上
- 信用：征信良好，工行客户优先
- 工作：稳定工作3个月以上

产品特点：
- 利率：3.5%-10.5%（年化）
- 额度：1-80万元
- 期限：6-60个月
- 审批：最快当天放款
- 还款：等额本息、等额本金

申请材料：
- 身份证原件及复印件
- 收入证明（工资单、银行流水）
- 工作证明（劳动合同、在职证明）
- 征信报告
- 工行银行卡或存折
            """,
            "category": "bank_products",
            "metadata": {"bank": "工商银行", "product_type": "个人信用贷款"}
        },
        {
            "title": "建设银行个人信用贷款产品",
            "content": """
建设银行个人信用贷款产品详情：

产品名称：建行快贷
申请条件：
- 年龄：18-65周岁
- 收入：月收入2500元以上
- 信用：征信良好，建行客户优先
- 工作：稳定工作6个月以上

产品特点：
- 利率：4.0%-11.5%（年化）
- 额度：1-100万元
- 期限：6-60个月
- 审批：最快2个工作日
- 还款：等额本息、等额本金、随借随还

申请材料：
- 身份证原件及复印件
- 收入证明（工资单、银行流水）
- 工作证明（劳动合同、在职证明）
- 征信报告
- 建行银行卡或存折
            """,
            "category": "bank_products",
            "metadata": {"bank": "建设银行", "product_type": "个人信用贷款"}
        },
        {
            "title": "银行个人信用贷款对比分析",
            "content": """
个人信用贷款银行对比分析：

🏦 利率对比：
- 工商银行：3.5%-10.5%（最低）
- 建设银行：4.0%-11.5%
- 招商银行：4.5%-12%

💰 额度对比：
- 建设银行：1-100万（最高）
- 工商银行：1-80万
- 招商银行：1-50万

⏰ 审批速度：
- 工商银行：最快当天放款
- 招商银行：最快1个工作日
- 建设银行：最快2个工作日

📋 申请条件：
- 工商银行：要求最低（月收入2000元，工作3个月）
- 建设银行：要求中等（月收入2500元，工作6个月）
- 招商银行：要求较高（月收入3000元，工作6个月）

💡 选择建议：
- 追求低利率：选择工商银行
- 需要高额度：选择建设银行
- 追求快速审批：选择工商银行
- 需要灵活还款：选择建设银行
            """,
            "category": "bank_comparison",
            "metadata": {"type": "产品对比", "banks": ["工商银行", "建设银行", "招商银行"]}
        },
        {
            "title": "贷款申请材料清单",
            "content": """
个人信用贷款申请材料清单：

📋 必备材料：
1. 身份证原件及复印件
2. 收入证明（以下任选其一）：
   - 工资单（最近3个月）
   - 银行流水（最近6个月）
   - 个人所得税完税证明
3. 工作证明：
   - 劳动合同
   - 在职证明
   - 工作证
4. 征信报告（个人版）

📋 补充材料（有助于提高额度）：
1. 资产证明：
   - 房产证复印件
   - 车辆行驶证
   - 存款证明
2. 学历证明：
   - 毕业证书
   - 学位证书
3. 其他证明：
   - 结婚证（已婚）
   - 子女出生证明（有子女）
   - 保险单

⚠️ 注意事项：
- 所有复印件需清晰可读
- 收入证明需加盖单位公章
- 征信报告需在有效期内
- 材料准备越充分，审批通过率越高
            """,
            "category": "application_guide",
            "metadata": {"type": "申请指南", "product": "个人信用贷款"}
        },
        {
            "title": "贷款审核流程和标准",
            "content": """
个人信用贷款审核流程和标准：

🔍 审核流程：
1. 材料初审（1-2个工作日）
   - 检查材料完整性
   - 验证材料真实性
   - 初步信用评估

2. 征信查询（1个工作日）
   - 查询央行征信报告
   - 分析信用记录
   - 评估信用风险

3. 收入核实（1-2个工作日）
   - 核实收入证明
   - 分析银行流水
   - 评估还款能力

4. 综合评估（1-2个工作日）
   - 综合评分
   - 确定贷款额度
   - 制定还款方案

5. 审批决定（1个工作日）
   - 审批通过/拒绝
   - 确定最终利率
   - 签署贷款合同

📊 审核标准：
- 征信评分：600分以上
- 收入稳定性：连续6个月有收入
- 负债率：不超过月收入的50%
- 逾期记录：近2年无严重逾期
- 工作稳定性：当前工作满6个月

🎯 提高通过率的方法：
1. 保持良好的征信记录
2. 提供充分的收入证明
3. 降低个人负债率
4. 选择适合的贷款产品
5. 准备完整的申请材料
            """,
            "category": "audit_guide",
            "metadata": {"type": "审核指南", "product": "个人信用贷款"}
        }
    ]
    
    print("🚀 开始添加银行产品对比知识...")
    print("=" * 60)
    
    success_count = 0
    for i, knowledge in enumerate(bank_knowledge, 1):
        print(f"\n📚 添加知识 {i}: {knowledge['title']}")
        
        try:
            response = requests.post(
                f"{base_url}/rag/knowledge",
                json=knowledge,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ 添加成功: {result.get('message')}")
                    success_count += 1
                else:
                    print(f"❌ 添加失败: {result.get('message')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ 添加异常: {e}")
    
    print(f"\n🎉 知识添加完成！成功添加 {success_count}/{len(bank_knowledge)} 条知识")
    
    # 测试知识库搜索
    print("\n🔍 测试知识库搜索...")
    test_queries = [
        "招商银行 个人信用贷款",
        "工商银行 建设银行 对比",
        "贷款申请材料",
        "贷款审核流程"
    ]
    
    for query in test_queries:
        print(f"\n📚 搜索: {query}")
        try:
            response = requests.post(
                f"{base_url}/rag/search",
                json={'query': query, 'limit': 3},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()['data']['results']
                print(f"找到 {len(results)} 条结果:")
                for j, result in enumerate(results[:3], 1):
                    title = result.get('title', '未知标题')
                    content = result.get('content', '')[:100]
                    print(f"  {j}. {title}: {content}...")
            else:
                print(f"❌ 搜索失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 搜索异常: {e}")

if __name__ == "__main__":
    add_bank_comparison_knowledge()
