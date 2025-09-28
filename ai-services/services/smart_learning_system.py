#!/usr/bin/env python3
"""
智能学习系统 - 自动扩展RAG知识库
包括学习进度判断、知识质量评估、自动学习触发等
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
import statistics

class SmartLearningSystem:
    """智能学习系统"""
    
    def __init__(self, vector_rag_service=None, llm_service=None):
        self.vector_rag_service = vector_rag_service
        self.llm_service = llm_service
        
        # 学习配置
        self.learning_config = {
            "min_knowledge_threshold": 0.3,  # 最小知识覆盖阈值
            "max_learning_attempts": 3,      # 最大学习尝试次数
            "learning_cooldown": 3600,       # 学习冷却时间（秒）
            "quality_threshold": 0.7,        # 知识质量阈值
            "diversity_threshold": 0.5,      # 知识多样性阈值
        }
        
        # 学习状态跟踪
        self.learning_stats = {
            "total_queries": 0,
            "successful_answers": 0,
            "failed_queries": 0,
            "learning_attempts": 0,
            "knowledge_gaps": set(),
            "last_learning_time": None,
            "learning_history": []
        }
        
        # 知识库质量指标
        self.knowledge_metrics = {
            "coverage_score": 0.0,      # 知识覆盖度
            "quality_score": 0.0,       # 知识质量
            "diversity_score": 0.0,     # 知识多样性
            "freshness_score": 0.0,     # 知识新鲜度
            "completeness_score": 0.0   # 知识完整性
        }
    
    async def should_learn_more(self, user_query: str, current_response: str) -> Tuple[bool, str]:
        """判断是否需要学习更多知识"""
        try:
            # 1. 检查响应质量
            response_quality = await self._assess_response_quality(user_query, current_response)
            
            # 2. 检查知识覆盖度
            coverage_score = await self._assess_knowledge_coverage(user_query)
            
            # 3. 检查学习频率限制
            if not self._can_learn_now():
                return False, "学习频率限制"
            
            # 4. 综合判断
            should_learn = (
                response_quality < self.learning_config["quality_threshold"] or
                coverage_score < self.learning_config["min_knowledge_threshold"]
            )
            
            reason = ""
            if response_quality < self.learning_config["quality_threshold"]:
                reason += f"响应质量低({response_quality:.2f}) "
            if coverage_score < self.learning_config["min_knowledge_threshold"]:
                reason += f"知识覆盖不足({coverage_score:.2f}) "
            
            return should_learn, reason.strip()
            
        except Exception as e:
            logger.error(f"判断学习需求失败: {e}")
            return False, f"判断失败: {e}"
    
    async def _assess_response_quality(self, query: str, response: str) -> float:
        """评估响应质量"""
        try:
            quality_indicators = {
                "length_score": min(len(response) / 500, 1.0),  # 长度适中
                "structure_score": self._check_response_structure(response),  # 结构完整
                "relevance_score": await self._check_relevance(query, response),  # 相关性
                "completeness_score": self._check_completeness(response),  # 完整性
                "accuracy_score": self._check_accuracy(response)  # 准确性
            }
            
            # 加权平均
            weights = {
                "length_score": 0.1,
                "structure_score": 0.2,
                "relevance_score": 0.3,
                "completeness_score": 0.2,
                "accuracy_score": 0.2
            }
            
            quality_score = sum(
                quality_indicators[key] * weights[key] 
                for key in weights
            )
            
            logger.info(f"响应质量评估: {quality_indicators}, 总分: {quality_score:.2f}")
            return quality_score
            
        except Exception as e:
            logger.error(f"评估响应质量失败: {e}")
            return 0.5  # 默认中等质量
    
    def _check_response_structure(self, response: str) -> float:
        """检查响应结构"""
        structure_indicators = [
            "**" in response,  # 有标题
            "**" in response and response.count("**") >= 4,  # 多个标题
            "- " in response,  # 有列表
            "：" in response or ":" in response,  # 有说明
            len(response.split("\n")) >= 5  # 有段落
        ]
        return sum(structure_indicators) / len(structure_indicators)
    
    async def _check_relevance(self, query: str, response: str) -> float:
        """检查响应相关性"""
        try:
            # 简单的关键词匹配
            query_keywords = set(re.findall(r'[\u4e00-\u9fff\w]+', query.lower()))
            response_keywords = set(re.findall(r'[\u4e00-\u9fff\w]+', response.lower()))
            
            if not query_keywords:
                return 0.5
            
            overlap = len(query_keywords.intersection(response_keywords))
            relevance = overlap / len(query_keywords)
            
            return min(relevance * 2, 1.0)  # 放大相关性分数
            
        except Exception as e:
            logger.error(f"检查相关性失败: {e}")
            return 0.5
    
    def _check_completeness(self, response: str) -> float:
        """检查响应完整性"""
        completeness_indicators = [
            "银行" in response or "Bank" in response,
            "贷款" in response or "Loan" in response,
            "利率" in response or "Rate" in response,
            "额度" in response or "Amount" in response,
            "申请" in response or "Apply" in response,
            "条件" in response or "Condition" in response
        ]
        return sum(completeness_indicators) / len(completeness_indicators)
    
    def _check_accuracy(self, response: str) -> float:
        """检查响应准确性"""
        accuracy_indicators = [
            "抱歉" not in response,  # 没有道歉
            "无法" not in response,  # 没有无法处理
            "暂时" not in response,  # 没有暂时无法
            "稍后" not in response,  # 没有稍后再试
            "具体" in response or "详细" in response  # 有具体信息
        ]
        return sum(accuracy_indicators) / len(accuracy_indicators)
    
    async def _assess_knowledge_coverage(self, query: str) -> float:
        """评估知识覆盖度"""
        try:
            if not self.vector_rag_service:
                return 0.0
            
            # 搜索相关知识
            results = await self.vector_rag_service.search_knowledge_hybrid(
                query=query,
                max_results=5
            )
            
            if not results:
                return 0.0
            
            # 计算平均相似度
            similarities = [r.get('similarity_score', 0) for r in results]
            avg_similarity = statistics.mean(similarities) if similarities else 0.0
            
            # 计算覆盖度
            coverage = min(avg_similarity * 1.5, 1.0)  # 放大相似度
            
            logger.info(f"知识覆盖度: {coverage:.2f} (平均相似度: {avg_similarity:.2f})")
            return coverage
            
        except Exception as e:
            logger.error(f"评估知识覆盖度失败: {e}")
            return 0.0
    
    def _can_learn_now(self) -> bool:
        """检查是否可以现在学习"""
        if not self.learning_stats["last_learning_time"]:
            return True
        
        time_since_last_learning = (
            datetime.now() - self.learning_stats["last_learning_time"]
        ).total_seconds()
        
        return time_since_last_learning >= self.learning_config["learning_cooldown"]
    
    async def trigger_learning(self, query: str, failed_response: str = None) -> Dict[str, Any]:
        """触发学习过程"""
        try:
            logger.info(f"触发学习过程: {query}")
            
            # 1. 分析查询意图
            learning_targets = await self._analyze_learning_targets(query)
            
            # 2. 执行学习
            learning_results = []
            for target in learning_targets:
                result = await self._learn_about_target(target)
                if result:
                    learning_results.append(result)
            
            # 3. 更新学习统计
            self._update_learning_stats(query, learning_results)
            
            # 4. 重新评估知识库质量
            await self._update_knowledge_metrics()
            
            return {
                "success": len(learning_results) > 0,
                "learned_targets": learning_targets,
                "learning_results": learning_results,
                "knowledge_metrics": self.knowledge_metrics.copy()
            }
            
        except Exception as e:
            logger.error(f"触发学习失败: {e}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_learning_targets(self, query: str) -> List[str]:
        """分析学习目标"""
        try:
            # 提取银行名称
            bank_keywords = [
                "银行", "Bank", "花旗", "Citi", "汇丰", "HSBC", "渣打", "Standard",
                "摩根", "JPMorgan", "富国", "Wells", "美国银行", "BOA", "大通", "Chase",
                "德意志", "Deutsche", "瑞银", "UBS", "巴克莱", "Barclays"
            ]
            
            targets = []
            for keyword in bank_keywords:
                if keyword.lower() in query.lower():
                    # 找到对应的完整银行名称
                    bank_name = self._map_keyword_to_bank_name(keyword)
                    if bank_name and bank_name not in targets:
                        targets.append(bank_name)
            
            # 如果没有找到具体银行，分析查询类型
            if not targets:
                if any(word in query for word in ["贷款", "利率", "申请", "条件"]):
                    targets.append("个人贷款通用知识")
                elif any(word in query for word in ["信用卡", "积分", "优惠"]):
                    targets.append("信用卡通用知识")
                elif any(word in query for word in ["房贷", "购房", "房屋"]):
                    targets.append("房贷通用知识")
            
            logger.info(f"学习目标: {targets}")
            return targets
            
        except Exception as e:
            logger.error(f"分析学习目标失败: {e}")
            return []
    
    def _map_keyword_to_bank_name(self, keyword: str) -> str:
        """将关键词映射到完整银行名称"""
        mapping = {
            "花旗": "花旗银行", "Citi": "花旗银行",
            "汇丰": "汇丰银行", "HSBC": "汇丰银行",
            "渣打": "渣打银行", "Standard": "渣打银行",
            "摩根": "摩根大通", "JPMorgan": "摩根大通",
            "富国": "富国银行", "Wells": "富国银行",
            "美国银行": "美国银行", "BOA": "美国银行",
            "大通": "大通银行", "Chase": "大通银行",
            "德意志": "德意志银行", "Deutsche": "德意志银行",
            "瑞银": "瑞银", "UBS": "瑞银",
            "巴克莱": "巴克莱银行", "Barclays": "巴克莱银行"
        }
        return mapping.get(keyword, "")
    
    async def _learn_about_target(self, target: str) -> Dict[str, Any]:
        """学习特定目标的知识"""
        try:
            logger.info(f"开始学习: {target}")
            
            # 这里可以集成真实的网络搜索和学习逻辑
            # 目前返回模拟的学习结果
            if "银行" in target:
                learned_content = await self._learn_bank_info(target)
            else:
                learned_content = await self._learn_general_knowledge(target)
            
            if learned_content and self.vector_rag_service:
                # 保存到知识库
                await self.vector_rag_service.add_knowledge(
                    category="自主学习",
                    title=f"{target} - 自主学习",
                    content=learned_content,
                    metadata={
                        "learning_source": "auto_learning",
                        "learning_time": datetime.now().isoformat(),
                        "target": target
                    }
                )
                
                logger.info(f"学习完成并保存: {target}")
                return {
                    "target": target,
                    "content_length": len(learned_content),
                    "success": True
                }
            
            return {"target": target, "success": False}
            
        except Exception as e:
            logger.error(f"学习目标失败 {target}: {e}")
            return {"target": target, "success": False, "error": str(e)}
    
    async def _learn_bank_info(self, bank_name: str) -> str:
        """学习银行信息"""
        # 这里应该集成真实的银行信息搜索
        # 目前返回模拟数据
        if "花旗" in bank_name:
            return f"""**{bank_name} 个人信贷产品介绍**

**银行简介**
{bank_name}是美国最大的银行之一，也是全球领先的金融服务公司。在中国，{bank_name}提供全面的个人银行服务，包括个人贷款、信用卡、投资理财等产品。

**主要个人信贷产品：**

1. {bank_name}个人信用贷款：
   - 额度：人民币10万-100万元
   - 利率：年化4.5%-15.6%
   - 期限：12-60个月
   - 特点：无抵押担保，审批快速
   - 适用人群：有稳定收入的个人客户

2. {bank_name}信用卡：
   - 多种信用卡产品
   - 利率：年化12.99%-24.99%
   - 特点：积分奖励，全球通用
   - 适用人群：不同信用等级的客户

**申请条件：**
- 年龄：18-65周岁
- 收入：月收入5000元以上
- 信用：征信记录良好
- 身份：中国大陆居民

**申请方式：**
- 官网：{bank_name}官网
- 手机APP：{bank_name}手机银行
- 银行网点：全国主要城市
- 客服热线：400-xxx-xxxx

**银行优势：**
- 国际知名银行品牌
- 专业的客户服务
- 丰富的金融产品
- 先进的数字银行平台"""
        
        return f"关于{bank_name}的详细信息正在学习中..."
    
    async def _learn_general_knowledge(self, topic: str) -> str:
        """学习通用知识"""
        if "个人贷款" in topic:
            return """**个人贷款通用知识**

**什么是个人贷款？**
个人贷款是银行向个人客户提供的无抵押信用贷款，用于个人消费、教育、医疗等用途。

**个人贷款特点：**
- 无需抵押担保
- 申请手续简便
- 放款速度快
- 用途灵活多样

**申请条件：**
- 年龄：18-65周岁
- 收入：有稳定收入来源
- 信用：征信记录良好
- 工作：稳定工作3个月以上

**利率影响因素：**
- 个人征信记录
- 收入水平
- 工作稳定性
- 银行客户等级
- 贷款期限和金额

**申请建议：**
1. 保持良好的征信记录
2. 提供稳定的收入证明
3. 选择适合的银行产品
4. 多家银行对比后选择最优方案"""
        
        return f"关于{topic}的详细信息正在学习中..."
    
    def _update_learning_stats(self, query: str, results: List[Dict[str, Any]]):
        """更新学习统计"""
        self.learning_stats["total_queries"] += 1
        self.learning_stats["learning_attempts"] += 1
        self.learning_stats["last_learning_time"] = datetime.now()
        
        successful_learnings = [r for r in results if r.get("success", False)]
        self.learning_stats["successful_answers"] += len(successful_learnings)
        
        # 记录学习历史
        self.learning_stats["learning_history"].append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results": results
        })
        
        # 保持历史记录在合理范围内
        if len(self.learning_stats["learning_history"]) > 100:
            self.learning_stats["learning_history"] = self.learning_stats["learning_history"][-50:]
    
    async def _update_knowledge_metrics(self):
        """更新知识库质量指标"""
        try:
            if not self.vector_rag_service:
                return
            
            # 获取知识库统计
            stats = await self.vector_rag_service.get_knowledge_stats()
            
            # 计算各项指标
            total_knowledge = stats.get("total_knowledge", 0)
            categories = stats.get("categories", {})
            
            # 覆盖度：基于知识库大小
            self.knowledge_metrics["coverage_score"] = min(total_knowledge / 100, 1.0)
            
            # 多样性：基于类别数量
            self.knowledge_metrics["diversity_score"] = min(len(categories) / 10, 1.0)
            
            # 新鲜度：基于最近学习时间
            if self.learning_stats["last_learning_time"]:
                hours_since_learning = (
                    datetime.now() - self.learning_stats["last_learning_time"]
                ).total_seconds() / 3600
                self.knowledge_metrics["freshness_score"] = max(0, 1 - hours_since_learning / 24)
            else:
                self.knowledge_metrics["freshness_score"] = 0.0
            
            # 完整性：基于学习成功率
            if self.learning_stats["learning_attempts"] > 0:
                success_rate = self.learning_stats["successful_answers"] / self.learning_stats["learning_attempts"]
                self.knowledge_metrics["completeness_score"] = success_rate
            else:
                self.knowledge_metrics["completeness_score"] = 0.0
            
            # 质量：综合指标
            self.knowledge_metrics["quality_score"] = (
                self.knowledge_metrics["coverage_score"] * 0.3 +
                self.knowledge_metrics["diversity_score"] * 0.2 +
                self.knowledge_metrics["freshness_score"] * 0.2 +
                self.knowledge_metrics["completeness_score"] * 0.3
            )
            
            logger.info(f"知识库质量指标更新: {self.knowledge_metrics}")
            
        except Exception as e:
            logger.error(f"更新知识库质量指标失败: {e}")
    
    async def get_learning_status(self) -> Dict[str, Any]:
        """获取学习状态"""
        return {
            "learning_stats": self.learning_stats.copy(),
            "knowledge_metrics": self.knowledge_metrics.copy(),
            "learning_config": self.learning_config.copy(),
            "is_learning_needed": await self._is_learning_needed()
        }
    
    async def _is_learning_needed(self) -> bool:
        """判断是否需要继续学习"""
        # 基于多个指标判断
        quality_score = self.knowledge_metrics["quality_score"]
        coverage_score = self.knowledge_metrics["coverage_score"]
        freshness_score = self.knowledge_metrics["freshness_score"]
        
        # 如果质量、覆盖度或新鲜度不足，需要学习
        needs_learning = (
            quality_score < 0.7 or
            coverage_score < 0.5 or
            freshness_score < 0.3
        )
        
        return needs_learning

# 全局实例
smart_learning_system = SmartLearningSystem()
