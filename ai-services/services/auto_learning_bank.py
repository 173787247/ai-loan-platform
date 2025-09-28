#!/usr/bin/env python3
"""
银行信息自主学习服务
当用户询问未知银行时，自动搜索并学习银行信息
"""

import asyncio
import aiohttp
import json
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from loguru import logger
from datetime import datetime
import time

class AutoLearningBankService:
    """银行信息自主学习服务"""
    
    def __init__(self, vector_rag_service=None):
        self.vector_rag_service = vector_rag_service
        self.learned_banks = set()  # 已学习的银行
        self.session = None
        
        # 银行搜索关键词映射
        self.bank_search_keywords = {
            "花旗银行": ["花旗银行", "Citibank", "花旗", "Citi"],
            "汇丰银行": ["汇丰银行", "HSBC", "汇丰"],
            "渣打银行": ["渣打银行", "Standard Chartered", "渣打"],
            "摩根大通": ["摩根大通", "JPMorgan Chase", "JPM", "摩根"],
            "富国银行": ["富国银行", "Wells Fargo", "富国"],
            "美国银行": ["美国银行", "Bank of America", "BOA"],
            "大通银行": ["大通银行", "Chase Bank", "Chase"],
            "德意志银行": ["德意志银行", "Deutsche Bank", "德银"],
            "瑞银": ["瑞银", "UBS", "瑞士银行"],
            "巴克莱银行": ["巴克莱银行", "Barclays", "巴克莱"],
            "劳埃德银行": ["劳埃德银行", "Lloyds Bank", "劳埃德"],
            "苏格兰皇家银行": ["苏格兰皇家银行", "RBS", "苏皇"],
            "澳新银行": ["澳新银行", "ANZ", "澳新"],
            "西太平洋银行": ["西太平洋银行", "Westpac", "西太"],
            "加拿大皇家银行": ["加拿大皇家银行", "RBC", "加皇"],
            "多伦多道明银行": ["多伦多道明银行", "TD Bank", "道明"],
            "蒙特利尔银行": ["蒙特利尔银行", "BMO", "蒙银"],
            "三菱UFJ银行": ["三菱UFJ银行", "MUFG", "三菱"],
            "三井住友银行": ["三井住友银行", "SMBC", "三井住友"],
            "瑞穗银行": ["瑞穗银行", "Mizuho", "瑞穗"]
        }
    
    async def detect_unknown_bank(self, user_message: str) -> Optional[str]:
        """检测用户询问的未知银行"""
        try:
            # 检查是否包含银行关键词
            for bank_name, keywords in self.bank_search_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in user_message.lower():
                        # 检查知识库中是否已有该银行信息
                        if await self._check_bank_in_knowledge_base(bank_name):
                            logger.info(f"银行 {bank_name} 已在知识库中")
                            return None
                        else:
                            logger.info(f"发现未知银行: {bank_name}")
                            return bank_name
            return None
        except Exception as e:
            logger.error(f"检测未知银行失败: {e}")
            return None
    
    async def _check_bank_in_knowledge_base(self, bank_name: str) -> bool:
        """检查银行是否已在知识库中"""
        try:
            if not self.vector_rag_service:
                return False
            
            # 搜索知识库
            results = await self.vector_rag_service.search_knowledge_hybrid(
                query=bank_name,
                max_results=3
            )
            
            # 检查是否有相关结果
            for result in results:
                title = result.get('title', '')
                content = result.get('content', '')
                if bank_name in title or bank_name in content:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"检查银行知识库失败: {e}")
            return False
    
    async def learn_bank_info(self, bank_name: str) -> Dict[str, Any]:
        """自主学习银行信息"""
        try:
            logger.info(f"开始学习银行信息: {bank_name}")
            
            # 1. 搜索银行官网信息
            bank_info = await self._search_bank_website(bank_name)
            
            # 2. 搜索银行产品信息
            products_info = await self._search_bank_products(bank_name)
            
            # 3. 使用LLM整理信息
            organized_info = await self._organize_bank_info_with_llm(bank_name, bank_info, products_info)
            
            # 4. 保存到知识库
            if organized_info and self.vector_rag_service:
                await self._save_bank_info_to_knowledge_base(organized_info)
                self.learned_banks.add(bank_name)
                logger.info(f"银行 {bank_name} 信息学习完成")
            
            return organized_info
            
        except Exception as e:
            logger.error(f"学习银行信息失败: {e}")
            return {}
    
    async def _search_bank_website(self, bank_name: str) -> Dict[str, Any]:
        """搜索银行官网信息"""
        try:
            # 构建搜索URL
            search_queries = [
                f"{bank_name} 官网 个人贷款",
                f"{bank_name} 信用卡 产品",
                f"{bank_name} 银行 服务",
                f"{bank_name} 利率 条件"
            ]
            
            bank_info = {
                "name": bank_name,
                "website": "",
                "products": [],
                "contact": "",
                "description": ""
            }
            
            # 这里可以集成真实的网络搜索API
            # 目前返回模拟数据
            if "花旗" in bank_name or "Citi" in bank_name:
                bank_info = {
                    "name": "花旗银行",
                    "website": "https://www.citibank.com.cn",
                    "products": ["个人贷款", "信用卡", "房贷", "车贷"],
                    "contact": "400-821-1880",
                    "description": "花旗银行是美国最大的银行之一，在中国提供全面的个人银行服务。"
                }
            elif "汇丰" in bank_name or "HSBC" in bank_name:
                bank_info = {
                    "name": "汇丰银行",
                    "website": "https://www.hsbc.com.cn",
                    "products": ["个人贷款", "信用卡", "投资理财"],
                    "contact": "400-820-3090",
                    "description": "汇丰银行是全球领先的金融服务公司，在中国有超过150年的历史。"
                }
            
            return bank_info
            
        except Exception as e:
            logger.error(f"搜索银行官网失败: {e}")
            return {}
    
    async def _search_bank_products(self, bank_name: str) -> List[Dict[str, Any]]:
        """搜索银行产品信息"""
        try:
            # 这里可以集成真实的银行产品搜索
            # 目前返回模拟数据
            products = []
            
            if "花旗" in bank_name or "Citi" in bank_name:
                products = [
                    {
                        "name": "花旗个人信用贷款",
                        "amount": "10万-100万元",
                        "rate": "4.5%-15.6%",
                        "term": "12-60个月",
                        "features": "无抵押担保，审批快速"
                    },
                    {
                        "name": "花旗信用卡",
                        "amount": "根据信用等级",
                        "rate": "12.99%-24.99%",
                        "term": "循环信用",
                        "features": "积分奖励，全球通用"
                    }
                ]
            elif "汇丰" in bank_name or "HSBC" in bank_name:
                products = [
                    {
                        "name": "汇丰个人贷款",
                        "amount": "5万-200万元",
                        "rate": "4.2%-16.8%",
                        "term": "12-84个月",
                        "features": "灵活还款，专业服务"
                    }
                ]
            
            return products
            
        except Exception as e:
            logger.error(f"搜索银行产品失败: {e}")
            return []
    
    async def _organize_bank_info_with_llm(self, bank_name: str, bank_info: Dict[str, Any], products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """使用LLM整理银行信息"""
        try:
            # 构建提示词
            prompt = f"""
请整理以下银行信息，生成结构化的银行产品介绍：

银行名称: {bank_name}
银行信息: {json.dumps(bank_info, ensure_ascii=False, indent=2)}
产品信息: {json.dumps(products, ensure_ascii=False, indent=2)}

请生成以下格式的银行介绍：

**{bank_name} 个人信贷产品介绍**

**银行简介**
[银行的基本介绍，包括历史、规模、特色等]

**主要个人信贷产品：**

1. [产品名称]：
   - 额度：[额度范围]
   - 利率：[利率范围]
   - 期限：[期限范围]
   - 特点：[产品特点]
   - 适用人群：[适用人群]

2. [产品名称]：
   - 额度：[额度范围]
   - 利率：[利率范围]
   - 期限：[期限范围]
   - 特点：[产品特点]
   - 适用人群：[适用人群]

**申请条件：**
- 年龄：[年龄要求]
- 收入：[收入要求]
- 信用：[信用要求]
- 身份：[身份要求]

**申请方式：**
- 官网：[官网地址]
- 手机APP：[APP名称]
- 银行网点：[网点信息]
- 客服热线：[客服电话]

**银行优势：**
- [优势1]
- [优势2]
- [优势3]

请用中文回答，保持专业和友好的语调。
"""
            
            # 这里应该调用LLM服务
            # 目前返回模拟的整理结果
            organized_content = f"""**{bank_name} 个人信贷产品介绍**

**银行简介**
{bank_info.get('description', '')}

**主要个人信贷产品：**

"""
            
            for i, product in enumerate(products, 1):
                organized_content += f"""
{i}. {product.get('name', '')}：
   - 额度：{product.get('amount', '')}
   - 利率：{product.get('rate', '')}
   - 期限：{product.get('term', '')}
   - 特点：{product.get('features', '')}
   - 适用人群：有稳定收入的个人客户

"""
            
            organized_content += f"""
**申请条件：**
- 年龄：18-65周岁
- 收入：月收入5000元以上
- 信用：征信记录良好
- 身份：中国大陆居民

**申请方式：**
- 官网：{bank_info.get('website', '')}
- 手机APP：{bank_name}手机银行
- 银行网点：全国主要城市
- 客服热线：{bank_info.get('contact', '')}

**银行优势：**
- 国际知名银行品牌
- 专业的客户服务
- 丰富的金融产品
- 先进的数字银行平台
"""
            
            return {
                "title": f"{bank_name} 个人信贷产品介绍",
                "content": organized_content,
                "category": "国际银行",
                "tags": [bank_name, "个人贷款", "信用卡", "国际银行"],
                "metadata": {
                    "bank": bank_name,
                    "bank_type": "国际银行",
                    "learned_at": datetime.now().isoformat(),
                    "source": "auto_learning"
                }
            }
            
        except Exception as e:
            logger.error(f"LLM整理银行信息失败: {e}")
            return {}
    
    async def _save_bank_info_to_knowledge_base(self, bank_info: Dict[str, Any]):
        """保存银行信息到知识库"""
        try:
            if not self.vector_rag_service:
                logger.warning("向量RAG服务不可用，无法保存银行信息")
                return
            
            # 添加到知识库
            await self.vector_rag_service.add_knowledge(
                category=bank_info.get("category", "国际银行"),
                title=bank_info.get("title", ""),
                content=bank_info.get("content", ""),
                metadata=bank_info.get("metadata", {})
            )
            
            logger.info(f"银行信息已保存到知识库: {bank_info.get('title', '')}")
            
        except Exception as e:
            logger.error(f"保存银行信息到知识库失败: {e}")
    
    async def auto_learn_and_respond(self, user_message: str) -> str:
        """自动学习并回复银行信息"""
        try:
            # 1. 检测未知银行
            unknown_bank = await self.detect_unknown_bank(user_message)
            
            if not unknown_bank:
                return None  # 没有检测到未知银行
            
            # 2. 学习银行信息
            bank_info = await self.learn_bank_info(unknown_bank)
            
            if bank_info:
                return bank_info.get("content", "")
            else:
                return f"抱歉，我暂时无法获取 {unknown_bank} 的详细信息，请稍后再试。"
                
        except Exception as e:
            logger.error(f"自动学习银行信息失败: {e}")
            return None

# 全局实例
auto_learning_bank_service = AutoLearningBankService()
