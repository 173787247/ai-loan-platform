"""
知识库增强服务
扩展知识库内容，提高检索精度和相关性
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from loguru import logger
from dataclasses import dataclass
from enum import Enum

class KnowledgeCategory(Enum):
    """知识库分类"""
    LOAN_PRODUCTS = "loan_products"
    INTEREST_RATES = "interest_rates"
    APPLICATION_PROCESS = "application_process"
    REQUIREMENTS = "requirements"
    FAQ = "faq"
    BANK_INFO = "bank_info"
    POLICIES = "policies"
    NEWS = "news"

@dataclass
class EnhancedKnowledge:
    """增强的知识条目"""
    id: str
    title: str
    content: str
    category: KnowledgeCategory
    keywords: List[str]
    entities: Dict[str, Any]
    relevance_score: float
    confidence: float
    source: str
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    related_topics: List[str]

class KnowledgeEnhancer:
    """知识库增强器"""
    
    def __init__(self, vector_rag_service=None):
        self.vector_rag_service = vector_rag_service
        self.enhanced_knowledge: Dict[str, EnhancedKnowledge] = {}
        
        # 银行产品知识库
        self.bank_products = {
            "招商银行": {
                "个人信用贷款": {
                    "利率": "4.35%-15.6%",
                    "额度": "1-50万",
                    "期限": "1-5年",
                    "条件": "年收入10万以上，征信良好"
                },
                "经营贷款": {
                    "利率": "4.5%-12%",
                    "额度": "10-500万",
                    "期限": "1-10年",
                    "条件": "营业执照满1年，年营业额100万以上"
                }
            },
            "工商银行": {
                "个人信用贷款": {
                    "利率": "4.2%-16%",
                    "额度": "1-30万",
                    "期限": "1-3年",
                    "条件": "年收入8万以上，征信良好"
                }
            }
        }
    
    def enhance_knowledge_base(self) -> Dict[str, Any]:
        """增强知识库"""
        try:
            enhanced_count = 0
            
            # 增强银行产品知识
            for bank, products in self.bank_products.items():
                for product, details in products.items():
                    knowledge = self._create_enhanced_knowledge(
                        title=f"{bank}{product}",
                        content=self._format_product_info(bank, product, details),
                        category=KnowledgeCategory.LOAN_PRODUCTS,
                        keywords=[bank, product, "贷款", "利率", "申请"],
                        entities={"bank": bank, "product": product, "type": "loan"}
                    )
                    self.enhanced_knowledge[knowledge.id] = knowledge
                    enhanced_count += 1
            
            # 增强FAQ知识
            faq_knowledge = self._create_faq_knowledge()
            for faq in faq_knowledge:
                self.enhanced_knowledge[faq.id] = faq
                enhanced_count += 1
            
            logger.info(f"知识库增强完成，新增 {enhanced_count} 条知识")
            return {
                "success": True,
                "enhanced_count": enhanced_count,
                "categories": [cat.value for cat in KnowledgeCategory]
            }
            
        except Exception as e:
            logger.error(f"知识库增强失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_enhanced_knowledge(self, title: str, content: str, category: KnowledgeCategory, 
                                 keywords: List[str], entities: Dict[str, Any]) -> EnhancedKnowledge:
        """创建增强知识条目"""
        knowledge_id = f"enhanced_{len(self.enhanced_knowledge) + 1}"
        
        return EnhancedKnowledge(
            id=knowledge_id,
            title=title,
            content=content,
            category=category,
            keywords=keywords,
            entities=entities,
            relevance_score=1.0,
            confidence=0.9,
            source="enhanced_knowledge_base",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tags=self._extract_tags(content),
            related_topics=self._find_related_topics(title, content)
        )
    
    def _format_product_info(self, bank: str, product: str, details: Dict[str, Any]) -> str:
        """格式化产品信息"""
        content = f"# {bank}{product}\n\n"
        content += f"**银行**: {bank}\n"
        content += f"**产品**: {product}\n\n"
        
        for key, value in details.items():
            content += f"**{key}**: {value}\n"
        
        content += f"\n**申请条件**: 具体条件请咨询银行客服\n"
        content += f"**申请流程**: 1. 准备材料 2. 提交申请 3. 银行审核 4. 放款\n"
        
        return content
    
    def _create_faq_knowledge(self) -> List[EnhancedKnowledge]:
        """创建FAQ知识"""
        faqs = [
            {
                "question": "个人信用贷款需要什么条件？",
                "answer": "个人信用贷款一般需要：1. 年收入8-10万以上 2. 征信记录良好 3. 有稳定工作 4. 年龄18-65岁",
                "keywords": ["个人信用贷款", "条件", "要求", "申请"]
            },
            {
                "question": "贷款利率是如何计算的？",
                "answer": "贷款利率通常采用年化利率，计算方式为：利息 = 本金 × 年利率 × 期限。不同银行和产品利率不同。",
                "keywords": ["利率", "计算", "利息", "年化"]
            },
            {
                "question": "贷款申请需要准备哪些材料？",
                "answer": "一般需要：1. 身份证 2. 收入证明 3. 银行流水 4. 征信报告 5. 工作证明等。具体材料以银行要求为准。",
                "keywords": ["材料", "申请", "准备", "证件"]
            }
        ]
        
        faq_knowledge = []
        for i, faq in enumerate(faqs):
            knowledge = self._create_enhanced_knowledge(
                title=faq["question"],
                content=f"**问题**: {faq['question']}\n\n**答案**: {faq['answer']}",
                category=KnowledgeCategory.FAQ,
                keywords=faq["keywords"],
                entities={"type": "faq", "question": faq["question"]}
            )
            faq_knowledge.append(knowledge)
        
        return faq_knowledge
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        tags = []
        
        # 银行标签
        banks = ["招商银行", "工商银行", "建设银行", "农业银行", "中国银行"]
        for bank in banks:
            if bank in content:
                tags.append(bank)
        
        # 产品标签
        products = ["个人信用贷款", "经营贷款", "房贷", "车贷", "消费贷款"]
        for product in products:
            if product in content:
                tags.append(product)
        
        # 类型标签
        if "利率" in content:
            tags.append("利率")
        if "申请" in content:
            tags.append("申请")
        if "条件" in content:
            tags.append("条件")
        
        return list(set(tags))
    
    def _find_related_topics(self, title: str, content: str) -> List[str]:
        """查找相关话题"""
        topics = []
        
        # 基于标题和内容提取相关话题
        if "贷款" in title or "贷款" in content:
            topics.extend(["利率", "申请", "条件", "流程"])
        
        if "银行" in title or "银行" in content:
            topics.extend(["产品", "服务", "政策"])
        
        if "利率" in content:
            topics.extend(["计算", "比较", "优惠"])
        
        return list(set(topics))
    
    def search_enhanced_knowledge(self, query: str, category: str = None, 
                                max_results: int = 5) -> List[Dict[str, Any]]:
        """搜索增强知识库"""
        try:
            results = []
            query_lower = query.lower()
            
            for knowledge in self.enhanced_knowledge.values():
                # 分类过滤
                if category and knowledge.category.value != category:
                    continue
                
                # 计算相关性得分
                relevance_score = self._calculate_relevance(query, knowledge)
                
                if relevance_score > 0.1:  # 相关性阈值
                    results.append({
                        "id": knowledge.id,
                        "title": knowledge.title,
                        "content": knowledge.content,
                        "category": knowledge.category.value,
                        "relevance_score": relevance_score,
                        "confidence": knowledge.confidence,
                        "keywords": knowledge.keywords,
                        "entities": knowledge.entities,
                        "tags": knowledge.tags,
                        "related_topics": knowledge.related_topics,
                        "source": knowledge.source
                    })
            
            # 按相关性排序
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"增强知识库搜索失败: {e}")
            return []
    
    def _calculate_relevance(self, query: str, knowledge: EnhancedKnowledge) -> float:
        """计算相关性得分"""
        score = 0.0
        query_lower = query.lower()
        
        # 标题匹配
        if any(keyword.lower() in query_lower for keyword in knowledge.keywords):
            score += 0.5
        
        # 内容匹配
        content_lower = knowledge.content.lower()
        query_words = query_lower.split()
        matched_words = sum(1 for word in query_words if word in content_lower)
        score += (matched_words / len(query_words)) * 0.3
        
        # 实体匹配
        for entity_type, entity_value in knowledge.entities.items():
            if entity_value.lower() in query_lower:
                score += 0.2
        
        return min(score, 1.0)
    
    def get_knowledge_statistics(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        try:
            category_counts = {}
            for knowledge in self.enhanced_knowledge.values():
                category = knowledge.category.value
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return {
                "total_knowledge": len(self.enhanced_knowledge),
                "category_distribution": category_counts,
                "average_confidence": sum(k.confidence for k in self.enhanced_knowledge.values()) / len(self.enhanced_knowledge),
                "last_updated": max(k.updated_at for k in self.enhanced_knowledge.values()).isoformat()
            }
        except Exception as e:
            logger.error(f"获取知识库统计失败: {e}")
            return {}
