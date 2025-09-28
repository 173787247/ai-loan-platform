#!/usr/bin/env python3
"""
自主机器学习系统
AI能够主动发现知识缺口、制定学习计划、执行学习任务
"""

import asyncio
import json
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
import statistics

class AutonomousLearningSystem:
    """自主机器学习系统"""
    
    def __init__(self, vector_rag_service=None, llm_service=None):
        self.vector_rag_service = vector_rag_service
        self.llm_service = llm_service
        
        # 学习配置
        self.config = {
            "learning_interval": 3600,        # 学习间隔（秒）
            "max_learning_per_cycle": 5,      # 每轮最大学习数量
            "knowledge_gap_threshold": 0.4,   # 知识缺口阈值
            "learning_priority_weights": {    # 学习优先级权重
                "bank_info": 0.4,             # 银行信息
                "product_info": 0.3,          # 产品信息
                "general_knowledge": 0.2,     # 通用知识
                "user_feedback": 0.1          # 用户反馈
            },
            # 停止学习条件
            "stop_conditions": {
                "max_learning_cycles": 100,           # 最大学习轮数
                "min_knowledge_coverage": 0.8,        # 最小知识覆盖度
                "min_quality_score": 0.85,            # 最小质量分数
                "max_gap_ratio": 0.1,                 # 最大知识缺口比例
                "consecutive_no_improvement": 5,      # 连续无改善轮数
                "max_learning_time_hours": 24,        # 最大学习时间（小时）
                "min_learning_interval": 7200         # 最小学习间隔（秒）
            }
        }
        
        # 学习状态
        self.learning_state = {
            "is_learning": False,
            "last_learning_time": None,
            "learning_cycle": 0,
            "total_learned_items": 0,
            "learning_queue": [],
            "learning_history": [],
            "knowledge_gaps": set(),
            "learning_goals": [],
            "start_time": None,
            "consecutive_no_improvement": 0,
            "last_quality_score": 0.0,
            "should_stop": False,
            "stop_reason": None
        }
        
        # 知识领域定义
        self.knowledge_domains = {
            "banks": {
                "chinese_banks": [
                    "招商银行", "工商银行", "建设银行", "农业银行", "中国银行",
                    "光大银行", "民生银行", "兴业银行", "浦发银行", "交通银行",
                    "中信银行", "华夏银行", "广发银行", "平安银行", "邮储银行"
                ],
                "international_banks": [
                    "花旗银行", "汇丰银行", "渣打银行", "摩根大通", "富国银行",
                    "美国银行", "大通银行", "德意志银行", "瑞银", "巴克莱银行",
                    "澳新银行", "加拿大皇家银行", "三菱UFJ银行", "三井住友银行"
                ]
            },
            "products": [
                "个人信用贷款", "信用卡", "房贷", "车贷", "经营贷款",
                "消费贷款", "教育贷款", "装修贷款", "旅游贷款"
            ],
            "topics": [
                "利率计算", "申请条件", "审批流程", "还款方式",
                "风险评估", "征信查询", "贷款比较", "优惠政策"
            ]
        }
        
        # 学习策略
        self.learning_strategies = {
            "exploration": 0.3,    # 探索策略：学习新领域
            "exploitation": 0.4,   # 利用策略：深化已知领域
            "user_driven": 0.3     # 用户驱动：基于用户问题
        }
    
    async def start_autonomous_learning(self):
        """启动自主机器学习"""
        try:
            logger.info("启动自主机器学习系统...")
            
            # 初始化学习状态
            self.learning_state["start_time"] = datetime.now()
            self.learning_state["should_stop"] = False
            self.learning_state["stop_reason"] = None
            
            # 启动学习循环
            asyncio.create_task(self._learning_loop())
            
            # 启动知识缺口检测
            asyncio.create_task(self._gap_detection_loop())
            
            # 启动学习计划制定
            asyncio.create_task(self._planning_loop())
            
            # 启动停止条件监控
            asyncio.create_task(self._stop_condition_monitor())
            
            logger.info("自主机器学习系统已启动")
            
        except Exception as e:
            logger.error(f"启动自主机器学习失败: {e}")
    
    async def _learning_loop(self):
        """学习循环"""
        while True:
            try:
                # 检查是否应该停止学习
                if self.learning_state["should_stop"]:
                    logger.info(f"学习已停止: {self.learning_state['stop_reason']}")
                    break
                
                if not self.learning_state["is_learning"]:
                    await self._execute_learning_cycle()
                
                # 动态调整学习间隔
                interval = self._calculate_learning_interval()
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"学习循环错误: {e}")
                await asyncio.sleep(60)  # 错误时等待1分钟
    
    async def _gap_detection_loop(self):
        """知识缺口检测循环"""
        while True:
            try:
                await self._detect_knowledge_gaps()
                await asyncio.sleep(1800)  # 每30分钟检测一次
                
            except Exception as e:
                logger.error(f"知识缺口检测错误: {e}")
                await asyncio.sleep(300)  # 错误时等待5分钟
    
    async def _planning_loop(self):
        """学习计划制定循环"""
        while True:
            try:
                if not self.learning_state["should_stop"]:
                    await self._create_learning_plan()
                await asyncio.sleep(3600)  # 每小时制定一次计划
                
            except Exception as e:
                logger.error(f"学习计划制定错误: {e}")
                await asyncio.sleep(600)  # 错误时等待10分钟
    
    async def _stop_condition_monitor(self):
        """停止条件监控"""
        while True:
            try:
                if self.learning_state["should_stop"]:
                    break
                
                should_stop, reason = await self._check_stop_conditions()
                if should_stop:
                    self.learning_state["should_stop"] = True
                    self.learning_state["stop_reason"] = reason
                    logger.info(f"触发停止条件: {reason}")
                
                await asyncio.sleep(300)  # 每5分钟检查一次
                
            except Exception as e:
                logger.error(f"停止条件监控错误: {e}")
                await asyncio.sleep(60)
    
    async def _check_stop_conditions(self) -> Tuple[bool, str]:
        """检查停止条件"""
        try:
            stop_conditions = self.config["stop_conditions"]
            current_cycle = self.learning_state["learning_cycle"]
            start_time = self.learning_state["start_time"]
            
            # 1. 检查最大学习轮数
            if current_cycle >= stop_conditions["max_learning_cycles"]:
                return True, f"达到最大学习轮数: {current_cycle}"
            
            # 2. 检查最大学习时间
            if start_time:
                learning_duration = datetime.now() - start_time
                max_hours = stop_conditions["max_learning_time_hours"]
                if learning_duration.total_seconds() >= max_hours * 3600:
                    return True, f"达到最大学习时间: {learning_duration.total_seconds()/3600:.1f}小时"
            
            # 3. 检查知识覆盖度（只有在有知识库内容时才检查）
            coverage_score = await self._calculate_knowledge_coverage()
            if coverage_score > 0 and coverage_score >= stop_conditions["min_knowledge_coverage"]:
                return True, f"知识覆盖度达标: {coverage_score:.2f}"
            
            # 4. 检查质量分数（只有在有学习历史且质量分数大于0时才检查）
            quality_score = await self._calculate_quality_score()
            if quality_score > 0.1 and quality_score >= stop_conditions["min_quality_score"]:
                return True, f"质量分数达标: {quality_score:.2f}"
            
            # 5. 检查知识缺口比例
            gap_ratio = await self._calculate_gap_ratio()
            if gap_ratio <= stop_conditions["max_gap_ratio"]:
                return True, f"知识缺口比例达标: {gap_ratio:.2f}"
            
            # 6. 检查连续无改善
            if self.learning_state["consecutive_no_improvement"] >= stop_conditions["consecutive_no_improvement"]:
                return True, f"连续无改善轮数: {self.learning_state['consecutive_no_improvement']}"
            
            return False, "继续学习"
            
        except Exception as e:
            logger.error(f"检查停止条件失败: {e}")
            return False, f"检查失败: {e}"
    
    async def _calculate_knowledge_coverage(self) -> float:
        """计算知识覆盖度"""
        try:
            if not self.vector_rag_service:
                return 0.0
            
            # 获取知识库统计
            stats = await self.vector_rag_service.get_knowledge_stats()
            total_knowledge = stats.get("total_knowledge", 0)
            
            # 计算覆盖度（基于知识库大小）
            max_expected = 1000  # 预期最大知识条目数
            coverage = min(total_knowledge / max_expected, 1.0)
            
            return coverage
            
        except Exception as e:
            logger.error(f"计算知识覆盖度失败: {e}")
            return 0.0
    
    async def _calculate_quality_score(self) -> float:
        """计算质量分数"""
        try:
            # 基于学习历史计算质量分数
            history = self.learning_state["learning_history"]
            if not history:
                return 0.0
            
            # 计算最近几轮的成功率
            recent_cycles = history[-10:] if len(history) >= 10 else history
            total_goals = sum(cycle["goals_count"] for cycle in recent_cycles)
            successful_goals = sum(cycle["learned_count"] for cycle in recent_cycles)
            
            if total_goals == 0:
                return 0.0
            
            success_rate = successful_goals / total_goals
            
            # 结合知识覆盖度
            coverage = await self._calculate_knowledge_coverage()
            
            # 综合质量分数
            quality_score = (success_rate * 0.6 + coverage * 0.4)
            
            return quality_score
            
        except Exception as e:
            logger.error(f"计算质量分数失败: {e}")
            return 0.0
    
    async def _calculate_gap_ratio(self) -> float:
        """计算知识缺口比例"""
        try:
            gaps = self.learning_state["knowledge_gaps"]
            total_domains = (
                len(self.knowledge_domains["banks"]["chinese_banks"]) +
                len(self.knowledge_domains["banks"]["international_banks"]) +
                len(self.knowledge_domains["products"]) +
                len(self.knowledge_domains["topics"])
            )
            
            if total_domains == 0:
                return 1.0
            
            gap_ratio = len(gaps) / total_domains
            return gap_ratio
            
        except Exception as e:
            logger.error(f"计算知识缺口比例失败: {e}")
            return 1.0
    
    def _calculate_learning_interval(self) -> int:
        """计算学习间隔"""
        try:
            base_interval = self.config["learning_interval"]
            min_interval = self.config["stop_conditions"]["min_learning_interval"]
            
            # 根据学习进度调整间隔
            current_cycle = self.learning_state["learning_cycle"]
            
            # 学习轮数越多，间隔越长
            if current_cycle > 20:
                interval = min_interval
            elif current_cycle > 10:
                interval = base_interval * 1.5
            else:
                interval = base_interval
            
            return int(interval)
            
        except Exception as e:
            logger.error(f"计算学习间隔失败: {e}")
            return self.config["learning_interval"]
    
    async def _detect_knowledge_gaps(self):
        """检测知识缺口"""
        try:
            logger.info("检测知识缺口...")
            
            gaps = set()
            
            # 1. 检测银行信息缺口
            bank_gaps = await self._detect_bank_gaps()
            gaps.update(bank_gaps)
            
            # 2. 检测产品信息缺口
            product_gaps = await self._detect_product_gaps()
            gaps.update(product_gaps)
            
            # 3. 检测通用知识缺口
            topic_gaps = await self._detect_topic_gaps()
            gaps.update(topic_gaps)
            
            # 4. 检测用户问题缺口
            user_gaps = await self._detect_user_gaps()
            gaps.update(user_gaps)
            
            self.learning_state["knowledge_gaps"] = gaps
            logger.info(f"检测到 {len(gaps)} 个知识缺口: {list(gaps)[:5]}...")
            
        except Exception as e:
            logger.error(f"检测知识缺口失败: {e}")
    
    async def _detect_bank_gaps(self) -> set:
        """检测银行信息缺口"""
        gaps = set()
        
        try:
            if not self.vector_rag_service:
                return gaps
            
            # 检查每个银行是否有足够信息
            all_banks = (
                self.knowledge_domains["banks"]["chinese_banks"] +
                self.knowledge_domains["banks"]["international_banks"]
            )
            
            for bank in all_banks:
                # 搜索该银行信息
                results = await self.vector_rag_service.search_knowledge_hybrid(
                    query=bank,
                    max_results=3
                )
                
                if not results:
                    gaps.add(f"银行信息:{bank}")
                    continue
                
                # 检查信息质量
                avg_similarity = statistics.mean([
                    r.get('similarity_score', 0) for r in results
                ]) if results else 0
                
                if avg_similarity < self.config["knowledge_gap_threshold"]:
                    gaps.add(f"银行信息:{bank}")
            
        except Exception as e:
            logger.error(f"检测银行缺口失败: {e}")
        
        return gaps
    
    async def _detect_product_gaps(self) -> set:
        """检测产品信息缺口"""
        gaps = set()
        
        try:
            if not self.vector_rag_service:
                return gaps
            
            for product in self.knowledge_domains["products"]:
                results = await self.vector_rag_service.search_knowledge_hybrid(
                    query=product,
                    max_results=3
                )
                
                if not results:
                    gaps.add(f"产品信息:{product}")
                    continue
                
                avg_similarity = statistics.mean([
                    r.get('similarity_score', 0) for r in results
                ]) if results else 0
                
                if avg_similarity < self.config["knowledge_gap_threshold"]:
                    gaps.add(f"产品信息:{product}")
            
        except Exception as e:
            logger.error(f"检测产品缺口失败: {e}")
        
        return gaps
    
    async def _detect_topic_gaps(self) -> set:
        """检测通用知识缺口"""
        gaps = set()
        
        try:
            if not self.vector_rag_service:
                return gaps
            
            for topic in self.knowledge_domains["topics"]:
                results = await self.vector_rag_service.search_knowledge_hybrid(
                    query=topic,
                    max_results=3
                )
                
                if not results:
                    gaps.add(f"通用知识:{topic}")
                    continue
                
                avg_similarity = statistics.mean([
                    r.get('similarity_score', 0) for r in results
                ]) if results else 0
                
                if avg_similarity < self.config["knowledge_gap_threshold"]:
                    gaps.add(f"通用知识:{topic}")
            
        except Exception as e:
            logger.error(f"检测通用知识缺口失败: {e}")
        
        return gaps
    
    async def _detect_user_gaps(self) -> set:
        """检测用户问题缺口"""
        gaps = set()
        
        try:
            # 这里可以分析用户历史问题，识别高频但回答质量低的问题
            # 目前使用模拟数据
            common_questions = [
                "贷款利率如何计算",
                "申请贷款需要什么条件",
                "哪个银行贷款利率最低",
                "如何提高贷款通过率",
                "提前还款有什么规定"
            ]
            
            for question in common_questions:
                if not self.vector_rag_service:
                    gaps.add(f"用户问题:{question}")
                    continue
                
                results = await self.vector_rag_service.search_knowledge_hybrid(
                    query=question,
                    max_results=3
                )
                
                if not results:
                    gaps.add(f"用户问题:{question}")
                    continue
                
                avg_similarity = statistics.mean([
                    r.get('similarity_score', 0) for r in results
                ]) if results else 0
                
                if avg_similarity < self.config["knowledge_gap_threshold"]:
                    gaps.add(f"用户问题:{question}")
            
        except Exception as e:
            logger.error(f"检测用户问题缺口失败: {e}")
        
        return gaps
    
    async def _create_learning_plan(self):
        """制定学习计划"""
        try:
            logger.info("制定学习计划...")
            
            gaps = self.learning_state["knowledge_gaps"]
            if not gaps:
                logger.info("没有发现知识缺口，无需制定学习计划")
                return
            
            # 按优先级排序学习目标
            learning_goals = []
            
            for gap in gaps:
                priority = self._calculate_learning_priority(gap)
                learning_goals.append({
                    "gap": gap,
                    "priority": priority,
                    "created_at": datetime.now(),
                    "status": "pending"
                })
            
            # 按优先级排序
            learning_goals.sort(key=lambda x: x["priority"], reverse=True)
            
            # 选择前N个目标
            max_goals = self.config["max_learning_per_cycle"]
            selected_goals = learning_goals[:max_goals]
            
            self.learning_state["learning_goals"] = selected_goals
            logger.info(f"制定了 {len(selected_goals)} 个学习目标")
            
        except Exception as e:
            logger.error(f"制定学习计划失败: {e}")
    
    def _calculate_learning_priority(self, gap: str) -> float:
        """计算学习优先级"""
        try:
            base_priority = 0.5
            
            # 根据缺口类型调整优先级
            if gap.startswith("银行信息:"):
                base_priority += self.config["learning_priority_weights"]["bank_info"]
            elif gap.startswith("产品信息:"):
                base_priority += self.config["learning_priority_weights"]["product_info"]
            elif gap.startswith("通用知识:"):
                base_priority += self.config["learning_priority_weights"]["general_knowledge"]
            elif gap.startswith("用户问题:"):
                base_priority += self.config["learning_priority_weights"]["user_feedback"]
            
            # 添加随机性，避免总是学习相同内容
            random_factor = random.uniform(0.8, 1.2)
            
            return min(base_priority * random_factor, 1.0)
            
        except Exception as e:
            logger.error(f"计算学习优先级失败: {e}")
            return 0.5
    
    async def _execute_learning_cycle(self):
        """执行学习周期"""
        try:
            if self.learning_state["is_learning"]:
                return
            
            self.learning_state["is_learning"] = True
            self.learning_state["learning_cycle"] += 1
            
            logger.info(f"开始执行学习周期 {self.learning_state['learning_cycle']}")
            
            goals = self.learning_state["learning_goals"]
            if not goals:
                logger.info("没有学习目标，跳过此周期")
                self.learning_state["is_learning"] = False
                return
            
            # 执行学习任务
            learned_count = 0
            for goal in goals:
                if goal["status"] != "pending":
                    continue
                
                try:
                    success = await self._learn_specific_gap(goal)
                    if success:
                        learned_count += 1
                        goal["status"] = "completed"
                        self.learning_state["total_learned_items"] += 1
                    else:
                        goal["status"] = "failed"
                    
                    # 避免学习过于频繁
                    await asyncio.sleep(5)
                    
                except Exception as e:
                    logger.error(f"学习目标失败 {goal['gap']}: {e}")
                    goal["status"] = "failed"
            
            # 计算当前质量分数
            current_quality = await self._calculate_quality_score()
            
            # 检查是否有改善
            if current_quality > self.learning_state["last_quality_score"]:
                self.learning_state["consecutive_no_improvement"] = 0
                logger.info(f"学习质量提升: {self.learning_state['last_quality_score']:.2f} -> {current_quality:.2f}")
            else:
                self.learning_state["consecutive_no_improvement"] += 1
                logger.info(f"学习质量无改善，连续轮数: {self.learning_state['consecutive_no_improvement']}")
            
            self.learning_state["last_quality_score"] = current_quality
            
            # 记录学习历史
            self.learning_state["learning_history"].append({
                "cycle": self.learning_state["learning_cycle"],
                "timestamp": datetime.now().isoformat(),
                "goals_count": len(goals),
                "learned_count": learned_count,
                "quality_score": current_quality,
                "goals": goals
            })
            
            # 保持历史记录在合理范围内
            if len(self.learning_state["learning_history"]) > 50:
                self.learning_state["learning_history"] = self.learning_state["learning_history"][-25:]
            
            self.learning_state["last_learning_time"] = datetime.now()
            self.learning_state["is_learning"] = False
            
            logger.info(f"学习周期完成，学习了 {learned_count} 个目标，质量分数: {current_quality:.2f}")
            
        except Exception as e:
            logger.error(f"执行学习周期失败: {e}")
            self.learning_state["is_learning"] = False
    
    async def _learn_specific_gap(self, goal: Dict[str, Any]) -> bool:
        """学习特定知识缺口"""
        try:
            gap = goal["gap"]
            logger.info(f"学习知识缺口: {gap}")
            
            # 根据缺口类型选择学习策略
            if gap.startswith("银行信息:"):
                return await self._learn_bank_info(gap)
            elif gap.startswith("产品信息:"):
                return await self._learn_product_info(gap)
            elif gap.startswith("通用知识:"):
                return await self._learn_topic_info(gap)
            elif gap.startswith("用户问题:"):
                return await self._learn_user_question(gap)
            else:
                return False
                
        except Exception as e:
            logger.error(f"学习特定缺口失败 {goal['gap']}: {e}")
            return False
    
    async def _learn_bank_info(self, gap: str) -> bool:
        """学习银行信息"""
        try:
            bank_name = gap.replace("银行信息:", "")
            
            # 生成银行信息内容
            content = await self._generate_bank_content(bank_name)
            
            if content and self.vector_rag_service:
                await self.vector_rag_service.add_knowledge(
                    category="自主学习的银行信息",
                    title=f"{bank_name} 个人信贷产品介绍",
                    content=content,
                    metadata={
                        "learning_source": "autonomous_learning",
                        "learning_time": datetime.now().isoformat(),
                        "bank_name": bank_name,
                        "learning_type": "bank_info"
                    }
                )
                
                logger.info(f"银行信息学习完成: {bank_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"学习银行信息失败 {gap}: {e}")
            return False
    
    async def _learn_product_info(self, gap: str) -> bool:
        """学习产品信息"""
        try:
            product_name = gap.replace("产品信息:", "")
            
            # 生成产品信息内容
            content = await self._generate_product_content(product_name)
            
            if content and self.vector_rag_service:
                await self.vector_rag_service.add_knowledge(
                    category="自主学习的产品信息",
                    title=f"{product_name} 详细介绍",
                    content=content,
                    metadata={
                        "learning_source": "autonomous_learning",
                        "learning_time": datetime.now().isoformat(),
                        "product_name": product_name,
                        "learning_type": "product_info"
                    }
                )
                
                logger.info(f"产品信息学习完成: {product_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"学习产品信息失败 {gap}: {e}")
            return False
    
    async def _learn_topic_info(self, gap: str) -> bool:
        """学习通用知识"""
        try:
            topic_name = gap.replace("通用知识:", "")
            
            # 生成通用知识内容
            content = await self._generate_topic_content(topic_name)
            
            if content and self.vector_rag_service:
                await self.vector_rag_service.add_knowledge(
                    category="自主学习的通用知识",
                    title=f"{topic_name} 详细说明",
                    content=content,
                    metadata={
                        "learning_source": "autonomous_learning",
                        "learning_time": datetime.now().isoformat(),
                        "topic_name": topic_name,
                        "learning_type": "general_knowledge"
                    }
                )
                
                logger.info(f"通用知识学习完成: {topic_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"学习通用知识失败 {gap}: {e}")
            return False
    
    async def _learn_user_question(self, gap: str) -> bool:
        """学习用户问题"""
        try:
            question = gap.replace("用户问题:", "")
            
            # 生成问题解答内容
            content = await self._generate_question_answer(question)
            
            if content and self.vector_rag_service:
                await self.vector_rag_service.add_knowledge(
                    category="自主学习的用户问题",
                    title=f"关于 {question} 的详细解答",
                    content=content,
                    metadata={
                        "learning_source": "autonomous_learning",
                        "learning_time": datetime.now().isoformat(),
                        "question": question,
                        "learning_type": "user_question"
                    }
                )
                
                logger.info(f"用户问题学习完成: {question}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"学习用户问题失败 {gap}: {e}")
            return False
    
    async def _generate_bank_content(self, bank_name: str) -> str:
        """生成银行信息内容"""
        # 这里应该集成真实的银行信息搜索和LLM生成
        # 目前返回模拟内容
        return f"""**{bank_name} 个人信贷产品介绍**

**银行简介**
{bank_name}是知名的金融机构，提供全面的个人银行服务，包括个人贷款、信用卡、投资理财等产品。

**主要个人信贷产品：**

1. {bank_name}个人信用贷款：
   - 额度：根据个人资质确定
   - 利率：年化4.5%-15.6%
   - 期限：12-60个月
   - 特点：无抵押担保，审批快速
   - 适用人群：有稳定收入的个人客户

2. {bank_name}信用卡：
   - 多种信用卡产品
   - 利率：年化12.99%-24.99%
   - 特点：积分奖励，优惠活动
   - 适用人群：不同信用等级的客户

**申请条件：**
- 年龄：18-65周岁
- 收入：有稳定收入来源
- 信用：征信记录良好
- 身份：符合银行要求

**申请方式：**
- 官网申请
- 手机APP申请
- 银行网点申请
- 客服热线咨询

**银行优势：**
- 专业金融服务
- 优质客户服务
- 丰富产品线
- 便捷申请流程"""
    
    async def _generate_product_content(self, product_name: str) -> str:
        """生成产品信息内容"""
        return f"""**{product_name} 详细介绍**

**产品概述**
{product_name}是银行提供的重要金融产品，旨在满足客户的资金需求。

**产品特点：**
- 申请简便
- 审批快速
- 用途灵活
- 还款便利

**申请条件：**
- 年龄要求：18-65周岁
- 收入要求：有稳定收入
- 信用要求：征信良好
- 其他要求：符合银行规定

**申请流程：**
1. 准备申请材料
2. 提交申请
3. 银行审核
4. 审批结果
5. 签署合同
6. 放款到账

**注意事项：**
- 请确保提供真实信息
- 按时还款避免逾期
- 了解产品条款
- 咨询银行客服获取最新信息"""
    
    async def _generate_topic_content(self, topic_name: str) -> str:
        """生成通用知识内容"""
        return f"""**{topic_name} 详细说明**

**基本概念**
{topic_name}是金融领域的重要概念，对理解银行产品和服务具有重要意义。

**主要内容：**
- 定义和含义
- 相关规则和规定
- 实际应用场景
- 注意事项

**实用建议：**
- 了解基本概念
- 掌握相关规则
- 注意实际应用
- 咨询专业人士

**常见问题：**
- 什么是{topic_name}？
- 如何理解{topic_name}？
- {topic_name}有什么作用？
- 如何应用{topic_name}？

**温馨提示：**
- 建议深入学习
- 结合实际应用
- 咨询银行客服
- 获取最新信息"""
    
    async def _generate_question_answer(self, question: str) -> str:
        """生成问题解答内容"""
        return f"""**关于 {question} 的详细解答**

**问题分析**
{question}是用户经常咨询的问题，涉及银行产品和服务的重要方面。

**详细解答：**
1. 基本概念和定义
2. 相关规则和要求
3. 实际操作流程
4. 注意事项和建议

**实用建议：**
- 了解基本要求
- 准备相关材料
- 按照流程操作
- 咨询银行客服

**常见误区：**
- 对概念理解不清
- 忽略重要细节
- 操作流程错误
- 缺乏专业指导

**解决方案：**
- 深入学习相关知识
- 仔细阅读相关规定
- 按照正确流程操作
- 寻求专业帮助

**温馨提示：**
- 建议提前了解
- 准备充分材料
- 按照要求操作
- 及时咨询客服"""
    
    async def get_learning_status(self) -> Dict[str, Any]:
        """获取学习状态"""
        # 计算当前指标
        coverage_score = await self._calculate_knowledge_coverage()
        quality_score = await self._calculate_quality_score()
        gap_ratio = await self._calculate_gap_ratio()
        
        # 计算学习时长
        learning_duration = None
        if self.learning_state["start_time"]:
            duration = datetime.now() - self.learning_state["start_time"]
            learning_duration = {
                "hours": duration.total_seconds() / 3600,
                "minutes": duration.total_seconds() / 60,
                "seconds": duration.total_seconds()
            }
        
        return {
            "learning_state": self.learning_state.copy(),
            "config": self.config.copy(),
            "knowledge_domains": {
                "banks_count": len(self.knowledge_domains["banks"]["chinese_banks"]) + 
                             len(self.knowledge_domains["banks"]["international_banks"]),
                "products_count": len(self.knowledge_domains["products"]),
                "topics_count": len(self.knowledge_domains["topics"])
            },
            "current_metrics": {
                "coverage_score": coverage_score,
                "quality_score": quality_score,
                "gap_ratio": gap_ratio,
                "consecutive_no_improvement": self.learning_state["consecutive_no_improvement"]
            },
            "stop_conditions": {
                "max_cycles": self.config["stop_conditions"]["max_learning_cycles"],
                "min_coverage": self.config["stop_conditions"]["min_knowledge_coverage"],
                "min_quality": self.config["stop_conditions"]["min_quality_score"],
                "max_gap_ratio": self.config["stop_conditions"]["max_gap_ratio"],
                "max_no_improvement": self.config["stop_conditions"]["consecutive_no_improvement"],
                "max_hours": self.config["stop_conditions"]["max_learning_time_hours"]
            },
            "is_learning": self.learning_state["is_learning"],
            "should_stop": self.learning_state["should_stop"],
            "stop_reason": self.learning_state["stop_reason"],
            "learning_duration": learning_duration,
            "next_learning_time": (
                self.learning_state["last_learning_time"] + 
                timedelta(seconds=self._calculate_learning_interval())
            ).isoformat() if self.learning_state["last_learning_time"] else None
        }
    
    async def stop_learning(self):
        """停止自主学习"""
        self.learning_state["is_learning"] = False
        logger.info("自主机器学习已停止")

# 全局实例
autonomous_learning_system = AutonomousLearningSystem()
