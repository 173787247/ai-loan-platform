#!/usr/bin/env python3
"""
增强银行产品知识库
"""

import asyncio
import asyncpg
import json
from typing import List, Dict, Any

# 数据库配置
DB_CONFIG = {
    'host': 'ai-loan-postgresql',
    'port': 5432,
    'database': 'ai_loan_rag',
    'user': 'ai_loan',
    'password': 'ai_loan123'
}

# 银行产品知识数据
BANK_PRODUCTS = [
    {
        "title": "招商银行个人信用贷款产品",
        "content": "招商银行提供多种个人信用贷款产品：\n\n1. 闪电贷：\n   - 额度：最高30万元\n   - 期限：1-3年\n   - 利率：年化4.5%-6.5%\n   - 特点：纯线上申请，审批快速，无需抵押\n   - 适用人群：有稳定收入的工薪族\n\n2. 个人消费贷款：\n   - 额度：最高50万元\n   - 期限：1-5年\n   - 利率：年化5%-8%\n   - 特点：用途广泛，支持提前还款\n   - 适用人群：有良好信用记录的个人\n\n3. 随薪贷：\n   - 额度：最高30万元\n   - 期限：1-3年\n   - 利率：年化4.8%-6.8%\n   - 特点：面向工资代发客户，审批优先\n   - 适用人群：招商银行工资代发客户",
        "category": "招商银行",
        "tags": ["个人信用贷款", "闪电贷", "消费贷款", "随薪贷", "招商银行"],
        "metadata": {
            "bank": "招商银行",
            "product_type": "个人信用贷款",
            "min_amount": 10000,
            "max_amount": 500000,
            "min_rate": 4.5,
            "max_rate": 8.0,
            "min_term": 12,
            "max_term": 60
        }
    },
    {
        "title": "工商银行个人信用贷款产品",
        "content": "工商银行个人信用贷款产品介绍：\n\n1. 融e借：\n   - 额度：最高80万元\n   - 期限：1-5年\n   - 利率：年化4.35%-6%\n   - 特点：提供多种贷款方式，包括信用贷款\n   - 适用人群：工行优质客户\n\n2. 个人消费贷款：\n   - 额度：最高100万元\n   - 期限：1-5年\n   - 利率：年化4.5%-7%\n   - 特点：用途灵活，支持多种还款方式\n   - 适用人群：有稳定收入来源的个人\n\n3. 工银e贷：\n   - 额度：最高50万元\n   - 期限：1-3年\n   - 利率：年化4.8%-6.5%\n   - 特点：线上申请，快速审批\n   - 适用人群：工行网银用户",
        "category": "工商银行",
        "tags": ["个人信用贷款", "融e借", "消费贷款", "工银e贷", "工商银行"],
        "metadata": {
            "bank": "工商银行",
            "product_type": "个人信用贷款",
            "min_amount": 10000,
            "max_amount": 1000000,
            "min_rate": 4.35,
            "max_rate": 7.0,
            "min_term": 12,
            "max_term": 60
        }
    },
    {
        "title": "建设银行个人信用贷款产品",
        "content": "建设银行个人信用贷款产品：\n\n1. 快贷：\n   - 额度：最高30万元\n   - 期限：1-3年\n   - 利率：年化4.5%-6.5%\n   - 特点：纯线上申请，秒级审批\n   - 适用人群：建行优质客户\n\n2. 个人消费贷款：\n   - 额度：最高50万元\n   - 期限：1-5年\n   - 利率：年化5%-8%\n   - 特点：用途广泛，支持提前还款\n   - 适用人群：有稳定收入的个人\n\n3. 建行e贷：\n   - 额度：最高100万元\n   - 期限：1-5年\n   - 利率：年化4.8%-7.2%\n   - 特点：提供多种担保方式\n   - 适用人群：建行VIP客户",
        "category": "建设银行",
        "tags": ["个人信用贷款", "快贷", "消费贷款", "建行e贷", "建设银行"],
        "metadata": {
            "bank": "建设银行",
            "product_type": "个人信用贷款",
            "min_amount": 10000,
            "max_amount": 1000000,
            "min_rate": 4.5,
            "max_rate": 7.2,
            "min_term": 12,
            "max_term": 60
        }
    },
    {
        "title": "农业银行个人信用贷款产品",
        "content": "农业银行个人信用贷款产品：\n\n1. 随薪贷：\n   - 额度：最高30万元\n   - 期限：1-3年\n   - 利率：年化4.8%-6.8%\n   - 特点：面向工资代发客户，审批优先\n   - 适用人群：农行工资代发客户\n\n2. 个人消费贷款：\n   - 额度：最高50万元\n   - 期限：1-5年\n   - 利率：年化5%-8%\n   - 特点：用途广泛，支持提前还款\n   - 适用人群：有稳定收入的个人\n\n3. 农行e贷：\n   - 额度：最高100万元\n   - 期限：1-5年\n   - 利率：年化4.8%-7.5%\n   - 特点：提供多种担保方式\n   - 适用人群：农行优质客户",
        "category": "农业银行",
        "tags": ["个人信用贷款", "随薪贷", "消费贷款", "农行e贷", "农业银行"],
        "metadata": {
            "bank": "农业银行",
            "product_type": "个人信用贷款",
            "min_amount": 10000,
            "max_amount": 1000000,
            "min_rate": 4.8,
            "max_rate": 7.5,
            "min_term": 12,
            "max_term": 60
        }
    },
    {
        "title": "中国银行个人信用贷款产品",
        "content": "中国银行个人信用贷款产品：\n\n1. 中银e贷：\n   - 额度：最高30万元\n   - 期限：1-3年\n   - 利率：年化4.5%-6.5%\n   - 特点：纯线上申请，快速审批\n   - 适用人群：中行优质客户\n\n2. 个人消费贷款：\n   - 额度：最高50万元\n   - 期限：1-5年\n   - 利率：年化5%-8%\n   - 特点：用途广泛，支持提前还款\n   - 适用人群：有稳定收入的个人\n\n3. 中银快贷：\n   - 额度：最高100万元\n   - 期限：1-5年\n   - 利率：年化4.8%-7.2%\n   - 特点：提供多种担保方式\n   - 适用人群：中行VIP客户",
        "category": "中国银行",
        "tags": ["个人信用贷款", "中银e贷", "消费贷款", "中银快贷", "中国银行"],
        "metadata": {
            "bank": "中国银行",
            "product_type": "个人信用贷款",
            "min_amount": 10000,
            "max_amount": 1000000,
            "min_rate": 4.5,
            "max_rate": 7.2,
            "min_term": 12,
            "max_term": 60
        }
    }
]

# 贷款申请条件知识
LOAN_CONDITIONS = [
    {
        "title": "个人信用贷款申请条件",
        "content": "个人信用贷款申请条件：\n\n1. 基本条件：\n   - 年龄：18-65周岁\n   - 身份：中国公民，具有完全民事行为能力\n   - 居住：在申请银行所在城市有固定住所\n   - 收入：有稳定的收入来源\n\n2. 收入要求：\n   - 月收入：一般要求月收入3000元以上\n   - 收入证明：提供工资单、银行流水等收入证明\n   - 收入稳定性：连续工作6个月以上\n\n3. 信用要求：\n   - 信用记录：无不良信用记录\n   - 信用评分：一般要求信用评分600分以上\n   - 负债比率：月负债不超过月收入的50%\n\n4. 其他要求：\n   - 用途明确：贷款用途合法合规\n   - 还款能力：有足够的还款能力\n   - 担保人：部分产品可能需要担保人",
        "category": "申请条件",
        "tags": ["申请条件", "收入要求", "信用要求", "年龄要求", "个人信用贷款"],
        "metadata": {
            "min_age": 18,
            "max_age": 65,
            "min_income": 3000,
            "min_credit_score": 600,
            "max_debt_ratio": 0.5,
            "min_work_months": 6
        }
    }
]

# 利率计算知识
RATE_CALCULATION = [
    {
        "title": "个人信用贷款利率计算",
        "content": "个人信用贷款利率计算：\n\n1. 利率类型：\n   - 年化利率：按年计算的利率\n   - 月利率：按月计算的利率\n   - 日利率：按日计算的利率\n\n2. 利率计算方式：\n   - 等额本息：每月还款金额相同\n   - 等额本金：每月还款本金相同，利息递减\n   - 先息后本：前期只还利息，到期还本金\n\n3. 利率影响因素：\n   - 信用评分：信用评分越高，利率越低\n   - 收入水平：收入越高，利率越低\n   - 贷款期限：期限越长，利率越高\n   - 贷款金额：金额越大，利率越低\n   - 银行政策：不同银行利率政策不同\n\n4. 利率计算公式：\n   - 等额本息：月还款额 = 贷款本金 × [月利率 × (1+月利率)^还款月数] / [(1+月利率)^还款月数 - 1]\n   - 等额本金：月还款额 = 贷款本金 / 还款月数 + (贷款本金 - 已还本金) × 月利率",
        "category": "利率计算",
        "tags": ["利率计算", "等额本息", "等额本金", "年化利率", "月利率"],
        "metadata": {
            "calculation_methods": ["等额本息", "等额本金", "先息后本"],
            "rate_factors": ["信用评分", "收入水平", "贷款期限", "贷款金额", "银行政策"]
        }
    }
]

async def insert_knowledge_data():
    """插入知识数据到数据库"""
    try:
        # 连接数据库
        conn = await asyncpg.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        
        # 清空现有数据
        await conn.execute("DELETE FROM knowledge_base")
        print("✅ 清空现有数据")
        
        # 插入银行产品数据
        for product in BANK_PRODUCTS:
            await conn.execute("""
                INSERT INTO knowledge_base (title, content, category, tags, metadata, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
            """, 
            product["title"], 
            product["content"], 
            product["category"], 
            product["tags"], 
            json.dumps(product["metadata"])
            )
        
        # 插入申请条件数据
        for condition in LOAN_CONDITIONS:
            await conn.execute("""
                INSERT INTO knowledge_base (title, content, category, tags, metadata, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
            """, 
            condition["title"], 
            condition["content"], 
            condition["category"], 
            condition["tags"], 
            json.dumps(condition["metadata"])
            )
        
        # 插入利率计算数据
        for rate in RATE_CALCULATION:
            await conn.execute("""
                INSERT INTO knowledge_base (title, content, category, tags, metadata, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
            """, 
            rate["title"], 
            rate["content"], 
            rate["category"], 
            rate["tags"], 
            json.dumps(rate["metadata"])
            )
        
        print("✅ 知识数据插入成功")
        
        # 查询插入的数据
        result = await conn.fetch("SELECT COUNT(*) as count FROM knowledge_base")
        print(f"✅ 知识库中共有 {result[0]['count']} 条记录")
        
        await conn.close()
        print("✅ 数据库连接关闭")
        
    except Exception as e:
        print(f"❌ 插入知识数据失败: {e}")

async def generate_embeddings():
    """生成向量嵌入"""
    try:
        from sentence_transformers import SentenceTransformer
        
        # 加载嵌入模型
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ 嵌入模型加载成功")
        
        # 连接数据库
        conn = await asyncpg.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        
        # 获取所有知识数据
        records = await conn.fetch("SELECT id, title, content FROM knowledge_base WHERE embedding IS NULL")
        print(f"✅ 找到 {len(records)} 条需要生成嵌入的记录")
        
        # 生成嵌入
        for record in records:
            # 组合标题和内容
            text = f"{record['title']} {record['content']}"
            
            # 生成嵌入向量
            embedding = model.encode(text)
            
            # 更新数据库 - 将向量转换为字符串格式
            embedding_str = '[' + ','.join(map(str, embedding.tolist())) + ']'
            await conn.execute("""
                UPDATE knowledge_base 
                SET embedding = $1::vector, updated_at = NOW()
                WHERE id = $2
            """, embedding_str, record['id'])
            
            print(f"✅ 已生成记录 {record['id']} 的嵌入向量")
        
        print("✅ 所有嵌入向量生成完成")
        await conn.close()
        
    except Exception as e:
        print(f"❌ 生成嵌入向量失败: {e}")

async def main():
    """主函数"""
    print("开始增强银行产品知识库...")
    
    # 插入知识数据
    await insert_knowledge_data()
    
    # 生成嵌入向量
    await generate_embeddings()
    
    print("知识库增强完成！")

if __name__ == "__main__":
    asyncio.run(main())