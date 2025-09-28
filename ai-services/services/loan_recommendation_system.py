#!/usr/bin/env python3
"""
智能贷款推荐系统
基于用户画像和银行产品数据进行深度分析和智能推荐
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
import math

class LoanRecommendationSystem:
    """智能贷款推荐系统"""
    
    def __init__(self, vector_rag_service=None, llm_service=None):
        self.vector_rag_service = vector_rag_service
        self.llm_service = llm_service
        
        # 银行产品数据库（结构化数据）
        self.bank_products_db = {
            # 国有大型银行
            "工商银行": {
                "融e借": {
                    "min_amount": 10000,
                    "max_amount": 300000,
                    "min_rate": 0.035,
                    "max_rate": 0.105,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 5000,
                    "age_range": [22, 60],
                    "special_features": ["工行客户优先", "利率较低", "审批快速"],
                    "risk_level": "低",
                    "popularity_score": 9.2
                }
            },
            "建设银行": {
                "快贷": {
                    "min_amount": 10000,
                    "max_amount": 100000,
                    "min_rate": 0.040,
                    "max_rate": 0.115,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["建行客户优先", "审批极快", "随借随还"],
                    "risk_level": "低",
                    "popularity_score": 8.8
                }
            },
            "农业银行": {
                "网捷贷": {
                    "min_amount": 10000,
                    "max_amount": 300000,
                    "min_rate": 0.045,
                    "max_rate": 0.120,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["农村覆盖广", "利率优惠", "审批快速"],
                    "risk_level": "低",
                    "popularity_score": 8.5
                }
            },
            "中国银行": {
                "中银E贷": {
                    "min_amount": 10000,
                    "max_amount": 300000,
                    "min_rate": 0.045,
                    "max_rate": 0.110,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 5000,
                    "age_range": [22, 60],
                    "special_features": ["国际化程度高", "利率较低", "审批快速"],
                    "risk_level": "低",
                    "popularity_score": 8.7
                }
            },
            "交通银行": {
                "好享贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.050,
                    "max_rate": 0.125,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["消费分期", "额度循环", "使用便捷"],
                    "risk_level": "低",
                    "popularity_score": 8.3
                }
            },
            
            # 股份制银行
            "招商银行": {
                "闪电贷": {
                    "min_amount": 10000,
                    "max_amount": 300000,
                    "min_rate": 0.050,
                    "max_rate": 0.150,
                    "min_term": 12,
                    "max_term": 60,
                    "approval_time": "秒级",
                    "credit_requirements": "征信良好",
                    "income_requirements": 3000,
                    "age_range": [22, 55],
                    "special_features": ["纯线上申请", "秒级放款", "随借随还"],
                    "risk_level": "中",
                    "popularity_score": 9.0
                },
                "招行信用贷": {
                    "min_amount": 10000,
                    "max_amount": 500000,
                    "min_rate": 0.045,
                    "max_rate": 0.120,
                    "min_term": 12,
                    "max_term": 60,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 5000,
                    "age_range": [22, 55],
                    "special_features": ["产品丰富", "服务优质", "审批快速"],
                    "risk_level": "中",
                    "popularity_score": 8.9
                }
            },
            "浦发银行": {
                "浦银点贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.050,
                    "max_rate": 0.130,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["线上申请", "快速审批", "利率优惠"],
                    "risk_level": "中",
                    "popularity_score": 8.1
                }
            },
            "民生银行": {
                "民生易贷": {
                    "min_amount": 10000,
                    "max_amount": 300000,
                    "min_rate": 0.055,
                    "max_rate": 0.140,
                    "min_term": 12,
                    "max_term": 48,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["申请简便", "审批快速", "额度灵活"],
                    "risk_level": "中",
                    "popularity_score": 8.0
                }
            },
            "兴业银行": {
                "兴闪贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.055,
                    "max_rate": 0.135,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["线上申请", "快速审批", "随借随还"],
                    "risk_level": "中",
                    "popularity_score": 7.9
                }
            },
            "光大银行": {
                "光速贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.060,
                    "max_rate": 0.140,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["纯线上操作", "审批快速", "使用便捷"],
                    "risk_level": "中",
                    "popularity_score": 7.8
                }
            },
            "华夏银行": {
                "华夏易贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.060,
                    "max_rate": 0.145,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["申请简便", "审批快速", "额度灵活"],
                    "risk_level": "中",
                    "popularity_score": 7.7
                }
            },
            "中信银行": {
                "信秒贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.055,
                    "max_rate": 0.140,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["线上申请", "快速审批", "利率优惠"],
                    "risk_level": "中",
                    "popularity_score": 7.8
                }
            },
            "广发银行": {
                "广发E秒贷": {
                    "min_amount": 10000,
                    "max_amount": 200000,
                    "min_rate": 0.060,
                    "max_rate": 0.150,
                    "min_term": 12,
                    "max_term": 36,
                    "approval_time": "1-2天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 4000,
                    "age_range": [22, 60],
                    "special_features": ["纯线上操作", "秒级审批", "随借随还"],
                    "risk_level": "中",
                    "popularity_score": 7.6
                }
            },
            "平安银行": {
                "新一贷": {
                    "min_amount": 10000,
                    "max_amount": 500000,
                    "min_rate": 0.065,
                    "max_rate": 0.180,
                    "min_term": 12,
                    "max_term": 60,
                    "approval_time": "1-3天",
                    "credit_requirements": "征信良好",
                    "income_requirements": 5000,
                    "age_range": [22, 55],
                    "special_features": ["产品特色鲜明", "审批快速", "额度灵活"],
                    "risk_level": "中高",
                    "popularity_score": 8.2
                }
            },
            
            # 民营银行
            "微众银行": {
                "微粒贷": {
                    "min_amount": 500,
                    "max_amount": 300000,
                    "min_rate": 0.070,
                    "max_rate": 0.200,
                    "min_term": 1,
                    "max_term": 24,
                    "approval_time": "秒级",
                    "credit_requirements": "征信良好",
                    "income_requirements": 2000,
                    "age_range": [18, 55],
                    "special_features": ["纯线上", "秒级放款", "随借随还", "门槛低"],
                    "risk_level": "中高",
                    "popularity_score": 9.1
                }
            },
            "网商银行": {
                "网商贷": {
                    "min_amount": 1000,
                    "max_amount": 1000000,
                    "min_rate": 0.080,
                    "max_rate": 0.240,
                    "min_term": 1,
                    "max_term": 24,
                    "approval_time": "秒级",
                    "credit_requirements": "征信良好",
                    "income_requirements": 3000,
                    "age_range": [18, 55],
                    "special_features": ["纯线上", "秒级放款", "额度高", "小微企业"],
                    "risk_level": "中高",
                    "popularity_score": 8.8
                }
            }
        }
        
        # 用户画像权重配置
        self.user_profile_weights = {
            "income_level": 0.25,      # 收入水平权重
            "credit_score": 0.20,      # 信用评分权重
            "loan_amount": 0.20,       # 贷款金额权重
            "loan_term": 0.15,         # 贷款期限权重
            "urgency": 0.10,           # 紧急程度权重
            "risk_tolerance": 0.10     # 风险承受能力权重
        }
        
        # 产品评分权重配置
        self.product_score_weights = {
            "interest_rate": 0.30,     # 利率权重
            "approval_speed": 0.20,    # 审批速度权重
            "loan_amount": 0.15,       # 贷款额度权重
            "flexibility": 0.15,       # 灵活性权重
            "reputation": 0.10,        # 银行声誉权重
            "special_features": 0.10   # 特殊功能权重
        }
    
    async def analyze_user_profile(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析用户画像"""
        try:
            profile = {
                "income_level": self._categorize_income(user_info.get("monthly_income", 0)),
                "credit_score": self._categorize_credit_score(user_info.get("credit_score", 600)),
                "loan_amount": user_info.get("loan_amount", 100000),
                "loan_term": user_info.get("loan_term", 24),
                "urgency": user_info.get("urgency", "normal"),
                "risk_tolerance": user_info.get("risk_tolerance", "medium"),
                "age": user_info.get("age", 30),
                "employment_type": user_info.get("employment_type", "employee"),
                "existing_loans": user_info.get("existing_loans", 0)
            }
            
            # 计算用户风险等级
            profile["risk_level"] = self._calculate_user_risk_level(profile)
            
            # 计算用户偏好
            profile["preferences"] = self._calculate_user_preferences(profile)
            
            logger.info(f"用户画像分析完成: {profile}")
            return profile
            
        except Exception as e:
            logger.error(f"用户画像分析失败: {e}")
            return {}
    
    def _categorize_income(self, monthly_income: int) -> str:
        """收入水平分类"""
        if monthly_income >= 20000:
            return "high"
        elif monthly_income >= 10000:
            return "medium_high"
        elif monthly_income >= 5000:
            return "medium"
        elif monthly_income >= 3000:
            return "low_medium"
        else:
            return "low"
    
    def _categorize_credit_score(self, credit_score: int) -> str:
        """信用评分分类"""
        if credit_score >= 750:
            return "excellent"
        elif credit_score >= 700:
            return "good"
        elif credit_score >= 650:
            return "fair"
        elif credit_score >= 600:
            return "poor"
        else:
            return "very_poor"
    
    def _calculate_user_risk_level(self, profile: Dict[str, Any]) -> str:
        """计算用户风险等级"""
        risk_score = 0
        
        # 收入水平风险
        income_risk = {
            "high": 0, "medium_high": 1, "medium": 2, 
            "low_medium": 3, "low": 4
        }
        risk_score += income_risk.get(profile["income_level"], 2)
        
        # 信用评分风险
        credit_risk = {
            "excellent": 0, "good": 1, "fair": 2, 
            "poor": 3, "very_poor": 4
        }
        risk_score += credit_risk.get(profile["credit_score"], 2)
        
        # 年龄风险
        age = profile["age"]
        if age < 25 or age > 55:
            risk_score += 1
        
        # 现有贷款风险
        if profile["existing_loans"] > 2:
            risk_score += 1
        
        if risk_score <= 2:
            return "low"
        elif risk_score <= 4:
            return "medium"
        else:
            return "high"
    
    def _calculate_user_preferences(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """计算用户偏好"""
        preferences = {
            "prefers_low_rate": False,
            "prefers_fast_approval": False,
            "prefers_high_amount": False,
            "prefers_flexible_terms": False,
            "prefers_online_only": False
        }
        
        # 基于收入水平判断偏好
        if profile["income_level"] in ["high", "medium_high"]:
            preferences["prefers_low_rate"] = True
            preferences["prefers_high_amount"] = True
        
        # 基于紧急程度判断偏好
        if profile["urgency"] == "urgent":
            preferences["prefers_fast_approval"] = True
        
        # 基于风险承受能力判断偏好
        if profile["risk_tolerance"] == "high":
            preferences["prefers_flexible_terms"] = True
            preferences["prefers_online_only"] = True
        
        return preferences
    
    async def calculate_product_scores(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """计算产品评分"""
        try:
            scored_products = []
            
            for bank_name, products in self.bank_products_db.items():
                for product_name, product_info in products.items():
                    score = await self._calculate_single_product_score(
                        user_profile, bank_name, product_name, product_info
                    )
                    
                    scored_products.append({
                        "bank_name": bank_name,
                        "product_name": product_name,
                        "product_info": product_info,
                        "score": score,
                        "match_reasons": self._get_match_reasons(user_profile, product_info),
                        "suitability": self._calculate_suitability(user_profile, product_info)
                    })
            
            # 按评分排序
            scored_products.sort(key=lambda x: x["score"], reverse=True)
            
            logger.info(f"产品评分计算完成，共 {len(scored_products)} 个产品")
            return scored_products
            
        except Exception as e:
            logger.error(f"产品评分计算失败: {e}")
            return []
    
    async def _calculate_single_product_score(self, user_profile: Dict[str, Any], 
                                            bank_name: str, product_name: str, 
                                            product_info: Dict[str, Any]) -> float:
        """计算单个产品评分"""
        try:
            total_score = 0.0
            
            # 1. 利率评分 (30%)
            rate_score = self._calculate_rate_score(user_profile, product_info)
            total_score += rate_score * self.product_score_weights["interest_rate"]
            
            # 2. 审批速度评分 (20%)
            speed_score = self._calculate_speed_score(user_profile, product_info)
            total_score += speed_score * self.product_score_weights["approval_speed"]
            
            # 3. 贷款额度评分 (15%)
            amount_score = self._calculate_amount_score(user_profile, product_info)
            total_score += amount_score * self.product_score_weights["loan_amount"]
            
            # 4. 灵活性评分 (15%)
            flexibility_score = self._calculate_flexibility_score(user_profile, product_info)
            total_score += flexibility_score * self.product_score_weights["flexibility"]
            
            # 5. 银行声誉评分 (10%)
            reputation_score = self._calculate_reputation_score(bank_name)
            total_score += reputation_score * self.product_score_weights["reputation"]
            
            # 6. 特殊功能评分 (10%)
            features_score = self._calculate_features_score(user_profile, product_info)
            total_score += features_score * self.product_score_weights["special_features"]
            
            # 7. 用户匹配度评分
            match_score = self._calculate_match_score(user_profile, product_info)
            total_score += match_score * 0.5  # 额外匹配度权重
            
            return min(total_score, 10.0)  # 最高10分
            
        except Exception as e:
            logger.error(f"产品评分计算失败 {bank_name}-{product_name}: {e}")
            return 0.0
    
    def _calculate_rate_score(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """计算利率评分"""
        try:
            user_amount = user_profile["loan_amount"]
            user_term = user_profile["loan_term"]
            
            # 根据用户条件估算实际利率
            estimated_rate = self._estimate_actual_rate(user_profile, product_info)
            
            # 利率越低评分越高
            if estimated_rate <= 0.05:
                return 10.0
            elif estimated_rate <= 0.08:
                return 8.0
            elif estimated_rate <= 0.12:
                return 6.0
            elif estimated_rate <= 0.15:
                return 4.0
            else:
                return 2.0
                
        except Exception as e:
            logger.error(f"利率评分计算失败: {e}")
            return 5.0
    
    def _calculate_speed_score(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """计算审批速度评分"""
        try:
            urgency = user_profile["urgency"]
            approval_time = product_info["approval_time"]
            
            if approval_time == "秒级":
                return 10.0
            elif approval_time == "1-2天":
                return 8.0
            elif approval_time == "1-3天":
                return 6.0
            else:
                return 4.0
                
        except Exception as e:
            logger.error(f"审批速度评分计算失败: {e}")
            return 5.0
    
    def _calculate_amount_score(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """计算贷款额度评分"""
        try:
            user_amount = user_profile["loan_amount"]
            min_amount = product_info["min_amount"]
            max_amount = product_info["max_amount"]
            
            if user_amount < min_amount:
                return 0.0  # 不满足最低额度要求
            elif user_amount > max_amount:
                return 5.0  # 超过最高额度，但可能可以申请
            else:
                # 在范围内，根据额度利用率评分
                utilization = (user_amount - min_amount) / (max_amount - min_amount)
                return 5.0 + utilization * 5.0
                
        except Exception as e:
            logger.error(f"贷款额度评分计算失败: {e}")
            return 5.0
    
    def _calculate_flexibility_score(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """计算灵活性评分"""
        try:
            score = 5.0
            
            # 期限灵活性
            user_term = user_profile["loan_term"]
            min_term = product_info["min_term"]
            max_term = product_info["max_term"]
            
            if min_term <= user_term <= max_term:
                term_range = max_term - min_term
                if term_range >= 24:
                    score += 2.0
                elif term_range >= 12:
                    score += 1.0
            
            # 特殊功能加分
            features = product_info.get("special_features", [])
            if "随借随还" in features:
                score += 1.0
            if "纯线上" in features:
                score += 1.0
            if "额度循环" in features:
                score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"灵活性评分计算失败: {e}")
            return 5.0
    
    def _calculate_reputation_score(self, bank_name: str) -> float:
        """计算银行声誉评分"""
        try:
            reputation_scores = {
                "工商银行": 9.5, "建设银行": 9.5, "农业银行": 9.5, 
                "中国银行": 9.5, "交通银行": 9.0,
                "招商银行": 9.2, "浦发银行": 8.8, "民生银行": 8.5,
                "兴业银行": 8.5, "光大银行": 8.3, "华夏银行": 8.0,
                "中信银行": 8.5, "广发银行": 8.0, "平安银行": 8.2,
                "微众银行": 8.8, "网商银行": 8.5
            }
            return reputation_scores.get(bank_name, 7.0)
            
        except Exception as e:
            logger.error(f"银行声誉评分计算失败: {e}")
            return 7.0
    
    def _calculate_features_score(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """计算特殊功能评分"""
        try:
            score = 5.0
            features = product_info.get("special_features", [])
            preferences = user_profile.get("preferences", {})
            
            # 根据用户偏好匹配特殊功能
            if preferences.get("prefers_fast_approval") and "秒级" in str(features):
                score += 2.0
            if preferences.get("prefers_online_only") and "纯线上" in str(features):
                score += 2.0
            if preferences.get("prefers_flexible_terms") and "随借随还" in str(features):
                score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"特殊功能评分计算失败: {e}")
            return 5.0
    
    def _calculate_match_score(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """计算用户匹配度评分"""
        try:
            score = 5.0
            
            # 年龄匹配
            user_age = user_profile["age"]
            age_range = product_info.get("age_range", [18, 60])
            if age_range[0] <= user_age <= age_range[1]:
                score += 1.0
            
            # 收入匹配
            user_income = user_profile.get("monthly_income", 0)
            income_req = product_info.get("income_requirements", 0)
            if user_income >= income_req:
                score += 1.0
            
            # 风险等级匹配
            user_risk = user_profile["risk_level"]
            product_risk = product_info.get("risk_level", "medium")
            if user_risk == product_risk:
                score += 1.0
            elif abs(self._risk_level_to_number(user_risk) - self._risk_level_to_number(product_risk)) == 1:
                score += 0.5
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"用户匹配度评分计算失败: {e}")
            return 5.0
    
    def _risk_level_to_number(self, risk_level: str) -> int:
        """风险等级转数字"""
        risk_map = {"low": 1, "medium": 2, "high": 3, "中高": 3}
        return risk_map.get(risk_level, 2)
    
    def _estimate_actual_rate(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """估算实际利率"""
        try:
            min_rate = product_info["min_rate"]
            max_rate = product_info["max_rate"]
            
            # 基于用户条件调整利率
            base_rate = (min_rate + max_rate) / 2
            
            # 信用评分调整
            credit_score = user_profile["credit_score"]
            if credit_score >= 750:
                rate_adjustment = -0.01
            elif credit_score >= 700:
                rate_adjustment = -0.005
            elif credit_score >= 650:
                rate_adjustment = 0.0
            elif credit_score >= 600:
                rate_adjustment = 0.01
            else:
                rate_adjustment = 0.02
            
            # 收入水平调整
            income_level = user_profile["income_level"]
            if income_level in ["high", "medium_high"]:
                rate_adjustment -= 0.005
            elif income_level in ["low", "low_medium"]:
                rate_adjustment += 0.01
            
            estimated_rate = base_rate + rate_adjustment
            return max(min(estimated_rate, max_rate), min_rate)
            
        except Exception as e:
            logger.error(f"实际利率估算失败: {e}")
            return product_info.get("min_rate", 0.08)
    
    def _get_match_reasons(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> List[str]:
        """获取匹配原因"""
        reasons = []
        
        # 利率匹配
        estimated_rate = self._estimate_actual_rate(user_profile, product_info)
        if estimated_rate <= 0.08:
            reasons.append("利率较低")
        
        # 审批速度匹配
        if product_info["approval_time"] == "秒级":
            reasons.append("审批极快")
        elif product_info["approval_time"] == "1-2天":
            reasons.append("审批快速")
        
        # 额度匹配
        user_amount = user_profile["loan_amount"]
        if product_info["max_amount"] >= user_amount:
            reasons.append("额度充足")
        
        # 特殊功能匹配
        features = product_info.get("special_features", [])
        if "随借随还" in features:
            reasons.append("支持随借随还")
        if "纯线上" in features:
            reasons.append("纯线上操作")
        
        return reasons
    
    def _calculate_suitability(self, user_profile: Dict[str, Any], product_info: Dict[str, Any]) -> str:
        """计算适合度"""
        try:
            score = 0
            
            # 基本条件检查
            user_amount = user_profile["loan_amount"]
            if product_info["min_amount"] <= user_amount <= product_info["max_amount"]:
                score += 2
            
            user_age = user_profile["age"]
            age_range = product_info.get("age_range", [18, 60])
            if age_range[0] <= user_age <= age_range[1]:
                score += 1
            
            user_income = user_profile.get("monthly_income", 0)
            if user_income >= product_info.get("income_requirements", 0):
                score += 1
            
            # 风险匹配
            user_risk = user_profile["risk_level"]
            product_risk = product_info.get("risk_level", "medium")
            if user_risk == product_risk:
                score += 2
            elif abs(self._risk_level_to_number(user_risk) - self._risk_level_to_number(product_risk)) == 1:
                score += 1
            
            if score >= 5:
                return "非常适合"
            elif score >= 3:
                return "比较适合"
            elif score >= 1:
                return "一般适合"
            else:
                return "不太适合"
                
        except Exception as e:
            logger.error(f"适合度计算失败: {e}")
            return "一般适合"
    
    async def generate_recommendation_report(self, user_profile: Dict[str, Any], 
                                           scored_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成推荐报告"""
        try:
            # 获取前5个推荐产品
            top_products = scored_products[:5]
            
            # 生成详细分析
            analysis = {
                "user_profile_summary": self._generate_profile_summary(user_profile),
                "recommendation_reasoning": self._generate_recommendation_reasoning(user_profile, top_products),
                "top_recommendations": self._format_top_recommendations(top_products),
                "comparison_table": self._generate_comparison_table(top_products),
                "risk_analysis": self._generate_risk_analysis(user_profile, top_products),
                "cost_analysis": self._generate_cost_analysis(user_profile, top_products),
                "next_steps": self._generate_next_steps(top_products)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"推荐报告生成失败: {e}")
            return {}
    
    def _generate_profile_summary(self, user_profile: Dict[str, Any]) -> str:
        """生成用户画像摘要"""
        income_level = user_profile["income_level"]
        credit_score = user_profile["credit_score"]
        risk_level = user_profile["risk_level"]
        
        return f"基于您的收入水平({income_level})、信用评分({credit_score})和风险等级({risk_level})，为您推荐最适合的贷款产品。"
    
    def _generate_recommendation_reasoning(self, user_profile: Dict[str, Any], 
                                         top_products: List[Dict[str, Any]]) -> str:
        """生成推荐理由"""
        reasoning = "推荐理由：\n"
        
        for i, product in enumerate(top_products[:3], 1):
            bank_name = product["bank_name"]
            product_name = product["product_name"]
            score = product["score"]
            reasons = product["match_reasons"]
            
            reasoning += f"\n{i}. {bank_name}-{product_name} (评分: {score:.1f}/10)\n"
            reasoning += f"   匹配原因: {', '.join(reasons)}\n"
        
        return reasoning
    
    def _format_top_recommendations(self, top_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """格式化顶级推荐"""
        formatted = []
        
        for i, product in enumerate(top_products, 1):
            formatted.append({
                "rank": i,
                "bank_name": product["bank_name"],
                "product_name": product["product_name"],
                "score": round(product["score"], 1),
                "suitability": product["suitability"],
                "estimated_rate": f"{self._estimate_actual_rate({}, product['product_info']):.1%}",
                "max_amount": f"{product['product_info']['max_amount']:,}元",
                "approval_time": product["product_info"]["approval_time"],
                "special_features": product["product_info"]["special_features"]
            })
        
        return formatted
    
    def _generate_comparison_table(self, top_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成对比表格"""
        comparison = []
        
        for product in top_products:
            info = product["product_info"]
            comparison.append({
                "银行": product["bank_name"],
                "产品": product["product_name"],
                "利率范围": f"{info['min_rate']:.1%}-{info['max_rate']:.1%}",
                "额度范围": f"{info['min_amount']:,}-{info['max_amount']:,}元",
                "期限范围": f"{info['min_term']}-{info['max_term']}个月",
                "审批时间": info["approval_time"],
                "评分": f"{product['score']:.1f}/10"
            })
        
        return comparison
    
    def _generate_risk_analysis(self, user_profile: Dict[str, Any], 
                               top_products: List[Dict[str, Any]]) -> str:
        """生成风险分析"""
        user_risk = user_profile["risk_level"]
        
        analysis = f"风险分析：\n"
        analysis += f"您的风险等级: {user_risk}\n\n"
        
        for product in top_products[:3]:
            bank_name = product["bank_name"]
            product_name = product["product_name"]
            product_risk = product["product_info"]["risk_level"]
            
            analysis += f"{bank_name}-{product_name}:\n"
            analysis += f"  产品风险等级: {product_risk}\n"
            
            if user_risk == product_risk:
                analysis += "  风险匹配度: 完全匹配 ✓\n"
            elif abs(self._risk_level_to_number(user_risk) - self._risk_level_to_number(product_risk)) == 1:
                analysis += "  风险匹配度: 基本匹配 △\n"
            else:
                analysis += "  风险匹配度: 需要谨慎 ⚠\n"
            analysis += "\n"
        
        return analysis
    
    def _generate_cost_analysis(self, user_profile: Dict[str, Any], 
                               top_products: List[Dict[str, Any]]) -> str:
        """生成成本分析"""
        user_amount = user_profile["loan_amount"]
        user_term = user_profile["loan_term"]
        
        analysis = f"成本分析 (贷款金额: {user_amount:,}元, 期限: {user_term}个月):\n\n"
        
        for product in top_products[:3]:
            bank_name = product["bank_name"]
            product_name = product["product_name"]
            
            # 计算月供和总利息
            estimated_rate = self._estimate_actual_rate(user_profile, product["product_info"])
            monthly_rate = estimated_rate / 12
            monthly_payment = user_amount * monthly_rate * (1 + monthly_rate)**user_term / ((1 + monthly_rate)**user_term - 1)
            total_interest = monthly_payment * user_term - user_amount
            
            analysis += f"{bank_name}-{product_name}:\n"
            analysis += f"  预估利率: {estimated_rate:.1%}\n"
            analysis += f"  月供: {monthly_payment:,.0f}元\n"
            analysis += f"  总利息: {total_interest:,.0f}元\n"
            analysis += f"  总还款: {monthly_payment * user_term:,.0f}元\n\n"
        
        return analysis
    
    def _generate_next_steps(self, top_products: List[Dict[str, Any]]) -> List[str]:
        """生成下一步建议"""
        steps = [
            "1. 仔细阅读推荐产品的详细条款和条件",
            "2. 准备相关申请材料（身份证、收入证明、征信报告等）",
            "3. 联系银行客服或访问银行官网了解最新政策",
            "4. 可以同时申请2-3家银行的产品进行对比",
            "5. 注意申请时间间隔，避免短期内多次查询征信"
        ]
        
        if top_products:
            best_product = top_products[0]
            steps.append(f"6. 优先考虑 {best_product['bank_name']}-{best_product['product_name']}，评分最高")
        
        return steps

# 全局实例
loan_recommendation_system = LoanRecommendationSystem()
