#!/usr/bin/env python3
"""
使用LLM搜索银行贷款FAQ并构建专业知识库
"""

import requests
import json
import asyncio
import asyncpg
from typing import List, Dict, Any

# 数据库配置
DB_CONFIG = {
    'host': 'ai-loan-postgresql',
    'port': 5432,
    'database': 'ai_loan_rag',
    'user': 'ai_loan',
    'password': 'ai_loan123'
}

# 银行贷款FAQ搜索提示词
FAQ_SEARCH_PROMPTS = [
    {
        "category": "招商银行",
        "prompts": [
            "请提供招商银行个人信用贷款的详细FAQ，包括产品特点、申请条件、利率、额度、审批流程、常见问题等",
            "招商银行闪电贷的具体申请条件和审批流程是什么？有什么注意事项？",
            "招商银行个人消费贷款的利率计算方式和还款方式有哪些？",
            "招商银行随薪贷的客户群体和优惠政策是什么？"
        ]
    },
    {
        "category": "工商银行",
        "prompts": [
            "请提供工商银行个人信用贷款的详细FAQ，包括融e借、个人消费贷款等产品的具体信息",
            "工商银行融e借的申请条件、利率、额度和审批时间是什么？",
            "工商银行个人消费贷款的用途限制和还款方式有哪些？",
            "工商银行工银e贷的客户准入条件和优惠政策是什么？"
        ]
    },
    {
        "category": "建设银行",
        "prompts": [
            "请提供建设银行个人信用贷款的详细FAQ，包括快贷、个人消费贷款等产品信息",
            "建设银行快贷的申请条件、利率、额度和审批流程是什么？",
            "建设银行个人消费贷款的用途和还款方式有哪些？",
            "建设银行建行e贷的客户群体和特色服务是什么？"
        ]
    },
    {
        "category": "农业银行",
        "prompts": [
            "请提供农业银行个人信用贷款的详细FAQ，包括随薪贷、个人消费贷款等产品信息",
            "农业银行随薪贷的申请条件、利率、额度和审批时间是什么？",
            "农业银行个人消费贷款的用途和还款方式有哪些？",
            "农业银行农行e贷的客户准入条件和优惠政策是什么？"
        ]
    },
    {
        "category": "中国银行",
        "prompts": [
            "请提供中国银行个人信用贷款的详细FAQ，包括中银e贷、个人消费贷款等产品信息",
            "中国银行中银e贷的申请条件、利率、额度和审批流程是什么？",
            "中国银行个人消费贷款的用途和还款方式有哪些？",
            "中国银行中银快贷的客户群体和特色服务是什么？"
        ]
    },
    {
        "category": "通用贷款知识",
        "prompts": [
            "请提供个人信用贷款的通用FAQ，包括申请条件、利率计算、还款方式、注意事项等",
            "个人信用贷款的利率是如何计算的？有哪些影响因素？",
            "个人信用贷款的还款方式有哪些？提前还款有什么规定？",
            "个人信用贷款申请被拒绝的常见原因有哪些？如何提高通过率？",
            "个人信用贷款和抵押贷款有什么区别？各有什么优缺点？"
        ]
    }
]

def call_llm_for_faq(prompt: str, category: str) -> str:
    """调用LLM获取FAQ信息"""
    try:
        # 创建会话
        session_response = requests.post(
            "http://localhost:8000/api/v1/chat/session",
            json={
                "user_id": "faq-search",
                "chatbot_role": "general"
            },
            timeout=10
        )
        
        if session_response.status_code != 200:
            print(f"❌ 创建会话失败: {session_response.status_code}")
            return ""
        
        session_data = session_response.json()
        session_id = session_data.get('data', {}).get('session_id')
        
        # 发送FAQ搜索请求
        response = requests.post(
            "http://localhost:8000/api/v1/chat/message",
            json={
                "session_id": session_id,
                "message": prompt,
                "user_id": "faq-search"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return result.get('data', {}).get('response', '')
            else:
                print(f"❌ LLM调用失败: {result.get('message', '未知错误')}")
                return ""
        else:
            print(f"❌ API调用失败: {response.status_code}")
            return ""
            
    except Exception as e:
        print(f"❌ 调用LLM失败: {str(e)}")
        return ""

def parse_faq_content(content: str, category: str) -> List[Dict[str, Any]]:
    """解析FAQ内容并提取结构化信息"""
    faq_items = []
    
    # 按段落分割内容
    paragraphs = content.split('\n\n')
    
    current_title = ""
    current_content = ""
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # 检查是否是标题（通常以数字、符号或特定格式开头）
        if (paragraph.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
            paragraph.startswith(('###', '##', '#')) or
            paragraph.startswith(('Q:', 'A:', '问题:', '答案:')) or
            paragraph.startswith(('产品名称:', '产品特点:', '申请条件:', '利率:', '额度:', '期限:')) or
            len(paragraph) < 100 and '：' in paragraph):
            
            # 保存上一个FAQ项目
            if current_title and current_content:
                faq_items.append({
                    "title": current_title,
                    "content": current_content,
                    "category": category
                })
            
            # 开始新的FAQ项目
            current_title = paragraph.replace('#', '').strip()
            current_content = ""
        else:
            # 添加到当前内容
            if current_content:
                current_content += "\n\n" + paragraph
            else:
                current_content = paragraph
    
    # 保存最后一个FAQ项目
    if current_title and current_content:
        faq_items.append({
            "title": current_title,
            "content": current_content,
            "category": category
        })
    
    return faq_items

async def search_and_store_faqs():
    """搜索并存储FAQ信息"""
    try:
        # 连接数据库
        conn = await asyncpg.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        
        # 清空现有数据
        await conn.execute("DELETE FROM knowledge_base")
        print("✅ 清空现有数据")
        
        total_faqs = 0
        
        for category_info in FAQ_SEARCH_PROMPTS:
            category = category_info["category"]
            prompts = category_info["prompts"]
            
            print(f"\n🔍 搜索 {category} FAQ...")
            
            for i, prompt in enumerate(prompts, 1):
                print(f"  提示词 {i}: {prompt[:50]}...")
                
                # 调用LLM获取FAQ
                faq_content = call_llm_for_faq(prompt, category)
                
                if faq_content:
                    print(f"  ✅ 获取到 {len(faq_content)} 字符的FAQ内容")
                    
                    # 解析FAQ内容
                    faq_items = parse_faq_content(faq_content, category)
                    print(f"  📝 解析出 {len(faq_items)} 个FAQ项目")
                    
                    # 存储到数据库
                    for faq_item in faq_items:
                        # 生成标签
                        tags = [category, "FAQ", "银行贷款"]
                        if "申请条件" in faq_item["title"]:
                            tags.append("申请条件")
                        if "利率" in faq_item["title"]:
                            tags.append("利率")
                        if "额度" in faq_item["title"]:
                            tags.append("额度")
                        if "审批" in faq_item["title"]:
                            tags.append("审批流程")
                        if "还款" in faq_item["title"]:
                            tags.append("还款方式")
                        
                        # 生成元数据
                        metadata = {
                            "category": category,
                            "type": "FAQ",
                            "source": "LLM搜索",
                            "content_length": len(faq_item["content"]),
                            "tags": tags
                        }
                        
                        await conn.execute("""
                            INSERT INTO knowledge_base (title, content, category, tags, metadata, created_at, updated_at)
                            VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
                        """, 
                        faq_item["title"], 
                        faq_item["content"], 
                        faq_item["category"], 
                        tags, 
                        json.dumps(metadata)
                        )
                        
                        total_faqs += 1
                else:
                    print(f"  ❌ 获取FAQ内容失败")
                
                # 避免请求过于频繁
                await asyncio.sleep(2)
        
        print(f"\n✅ 总共存储了 {total_faqs} 个FAQ项目")
        
        # 查询存储的数据
        result = await conn.fetch("SELECT COUNT(*) as count FROM knowledge_base")
        print(f"✅ 知识库中共有 {result[0]['count']} 条记录")
        
        await conn.close()
        print("✅ 数据库连接关闭")
        
    except Exception as e:
        print(f"❌ 搜索和存储FAQ失败: {e}")

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
    print("开始使用LLM搜索银行贷款FAQ...")
    
    # 搜索并存储FAQ
    await search_and_store_faqs()
    
    # 生成嵌入向量
    await generate_embeddings()
    
    print("FAQ知识库构建完成！")

if __name__ == "__main__":
    asyncio.run(main())
