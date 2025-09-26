#!/usr/bin/env python3
"""
风控和定价服务
提供真实的风控评估和定价计算功能
"""

import asyncio
import json
import random
import math
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RiskAssessmentService:
    """风控评估服务"""
    
    def __init__(self):
        self.risk_factors = {
            "credit_score": {"weight": 0.3, "thresholds": [600, 700, 750, 800]},
            "debt_ratio": {"weight": 0.25, "thresholds": [0.3, 0.5, 0.7, 0.8]},
            "income_stability": {"weight": 0.2, "thresholds": [5000, 10000, 15000, 20000]},
            "work_experience": {"weight": 0.15, "thresholds": [1, 3, 5, 8]},
            "collateral": {"weight": 0.1, "thresholds": [False, True]}
        }
    
    async def assess_risk(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """评估用户风险"""
        try:
            # 提取关键信息
            credit_score = profile.get("credit_score", 0)
            monthly_income = profile.get("monthly_income", 0)
            monthly_debt = profile.get("monthly_debt_payment", 0)
            work_years = profile.get("work_years", 0)
            has_collateral = profile.get("has_collateral", False)
            
            # 计算负债比率
            debt_ratio = monthly_debt / monthly_income if monthly_income > 0 else 1.0
            
            # 计算各项风险分数
            risk_scores = {}
            
            # 信用评分风险
            credit_risk = self._calculate_credit_risk(credit_score)
            risk_scores["credit_score"] = credit_risk
            
            # 负债比率风险
            debt_risk = self._calculate_debt_risk(debt_ratio)
            risk_scores["debt_ratio"] = debt_risk
            
            # 收入稳定性风险
            income_risk = self._calculate_income_risk(monthly_income)
            risk_scores["income_stability"] = income_risk
            
            # 工作经验风险
            work_risk = self._calculate_work_risk(work_years)
            risk_scores["work_experience"] = work_risk
            
            # 抵押物风险
            collateral_risk = self._calculate_collateral_risk(has_collateral)
            risk_scores["collateral"] = collateral_risk
            
            # 计算综合风险分数
            total_risk_score = sum(
                risk_scores[factor] * self.risk_factors[factor]["weight"]
                for factor in risk_scores
            )
            
            # 确定风险等级
            risk_level = self._determine_risk_level(total_risk_score)
            
            # 生成风险报告
            risk_report = self._generate_risk_report(risk_scores, total_risk_score, risk_level)
            
            # 决定是否批准
            approved = risk_level in ["低风险", "中低风险"]
            
            return {
                "approved": approved,
                "risk_level": risk_level,
                "risk_score": total_risk_score,
                "risk_factors": risk_scores,
                "risk_report": risk_report,
                "recommendations": self._generate_recommendations(risk_scores, approved)
            }
            
        except Exception as e:
            logger.error(f"风控评估失败: {e}")
            return {
                "approved": False,
                "risk_level": "高风险",
                "risk_score": 1.0,
                "error": str(e)
            }
    
    def _calculate_credit_risk(self, credit_score: int) -> float:
        """计算信用评分风险"""
        if credit_score >= 800:
            return 0.1
        elif credit_score >= 750:
            return 0.3
        elif credit_score >= 700:
            return 0.5
        elif credit_score >= 600:
            return 0.7
        else:
            return 1.0
    
    def _calculate_debt_risk(self, debt_ratio: float) -> float:
        """计算负债比率风险"""
        if debt_ratio <= 0.3:
            return 0.1
        elif debt_ratio <= 0.5:
            return 0.3
        elif debt_ratio <= 0.7:
            return 0.6
        elif debt_ratio <= 0.8:
            return 0.8
        else:
            return 1.0
    
    def _calculate_income_risk(self, monthly_income: float) -> float:
        """计算收入稳定性风险"""
        if monthly_income >= 20000:
            return 0.1
        elif monthly_income >= 15000:
            return 0.2
        elif monthly_income >= 10000:
            return 0.4
        elif monthly_income >= 5000:
            return 0.6
        else:
            return 0.9
    
    def _calculate_work_risk(self, work_years: float) -> float:
        """计算工作经验风险"""
        if work_years >= 8:
            return 0.1
        elif work_years >= 5:
            return 0.2
        elif work_years >= 3:
            return 0.4
        elif work_years >= 1:
            return 0.6
        else:
            return 0.8
    
    def _calculate_collateral_risk(self, has_collateral: bool) -> float:
        """计算抵押物风险"""
        return 0.2 if has_collateral else 0.8
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """确定风险等级"""
        if risk_score <= 0.3:
            return "低风险"
        elif risk_score <= 0.5:
            return "中低风险"
        elif risk_score <= 0.7:
            return "中风险"
        elif risk_score <= 0.8:
            return "中高风险"
        else:
            return "高风险"
    
    def _generate_risk_report(self, risk_scores: Dict, total_score: float, risk_level: str) -> str:
        """生成风险报告"""
        report = f"风险等级：{risk_level}\n"
        report += f"综合风险分数：{total_score:.2f}\n\n"
        report += "各维度风险分析：\n"
        
        for factor, score in risk_scores.items():
            factor_name = {
                "credit_score": "信用评分",
                "debt_ratio": "负债比率",
                "income_stability": "收入稳定性",
                "work_experience": "工作经验",
                "collateral": "抵押物"
            }.get(factor, factor)
            
            level = "优秀" if score <= 0.3 else "良好" if score <= 0.5 else "一般" if score <= 0.7 else "较差"
            report += f"- {factor_name}：{level} (分数: {score:.2f})\n"
        
        return report
    
    def _generate_recommendations(self, risk_scores: Dict, approved: bool) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if not approved:
            if risk_scores.get("credit_score", 0) > 0.7:
                recommendations.append("建议提升信用评分，按时还款，减少信用卡使用")
            
            if risk_scores.get("debt_ratio", 0) > 0.7:
                recommendations.append("建议减少现有负债，提高可支配收入比例")
            
            if risk_scores.get("income_stability", 0) > 0.7:
                recommendations.append("建议提供更多收入证明，或考虑增加收入来源")
            
            if risk_scores.get("work_experience", 0) > 0.7:
                recommendations.append("建议在现单位工作更长时间，或提供更稳定的工作证明")
            
            if risk_scores.get("collateral", 0) > 0.7:
                recommendations.append("建议提供抵押物或担保人，降低贷款风险")
        else:
            recommendations.append("您的申请条件良好，建议选择利率较低的产品")
            recommendations.append("建议按时还款，保持良好的信用记录")
        
        return recommendations

class PricingService:
    """定价服务"""
    
    def __init__(self):
        self.base_rates = {
            "招商银行": {"base_rate": 4.5, "risk_adjustment": 0.1},
            "工商银行": {"base_rate": 4.2, "risk_adjustment": 0.12},
            "建设银行": {"base_rate": 4.3, "risk_adjustment": 0.11},
            "农业银行": {"base_rate": 4.4, "risk_adjustment": 0.13},
            "中国银行": {"base_rate": 4.1, "risk_adjustment": 0.14}
        }
        
        self.risk_adjustments = {
            "低风险": 0.0,
            "中低风险": 0.5,
            "中风险": 1.0,
            "中高风险": 1.5,
            "高风险": 2.0
        }
    
    async def calculate_pricing(self, profile: Dict[str, Any], risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """计算定价方案"""
        try:
            amount = profile.get("amount", 0)
            term = profile.get("term", 12)
            risk_level = risk_assessment.get("risk_level", "中风险")
            
            if not risk_assessment.get("approved", False):
                return []
            
            quotations = []
            
            for bank_name, bank_config in self.base_rates.items():
                # 计算基础利率
                base_rate = bank_config["base_rate"]
                risk_adjustment = self.risk_adjustments.get(risk_level, 1.0)
                final_rate = base_rate + risk_adjustment
                
                # 计算月还款额
                monthly_payment = self._calculate_monthly_payment(amount * 10000, final_rate, term)
                
                # 计算总利息和总还款额
                total_interest = monthly_payment * term - amount * 10000
                total_amount = monthly_payment * term
                
                # 计算手续费
                processing_fee = self._calculate_processing_fee(amount, bank_name)
                
                # 计算批准概率
                approval_probability = self._calculate_approval_probability(risk_level, bank_name)
                
                # 生成条件
                conditions = self._generate_conditions(bank_name, profile, risk_level)
                
                # 生成原因
                reasons = self._generate_reasons(risk_level, bank_name, profile)
                
                quotation = {
                    "bank_name": bank_name,
                    "product_name": self._get_product_name(bank_name),
                    "approved_amount": amount,
                    "interest_rate": final_rate,
                    "term_months": term,
                    "monthly_payment": monthly_payment,
                    "total_interest": total_interest,
                    "total_amount": total_amount,
                    "processing_fee": processing_fee,
                    "conditions": conditions,
                    "risk_level": risk_level,
                    "approval_probability": approval_probability,
                    "reasons": reasons
                }
                
                quotations.append(quotation)
            
            # 按利率排序
            quotations.sort(key=lambda x: x["interest_rate"])
            
            return quotations
            
        except Exception as e:
            logger.error(f"定价计算失败: {e}")
            return []
    
    def _calculate_monthly_payment(self, principal: float, annual_rate: float, months: int) -> float:
        """计算月还款额（等额本息）"""
        if annual_rate == 0:
            return principal / months
        
        monthly_rate = annual_rate / 100 / 12
        return principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    
    def _calculate_processing_fee(self, amount: float, bank_name: str) -> float:
        """计算手续费"""
        base_fee = min(amount * 0.01, 1000)  # 1%或最高1000元
        bank_multiplier = {
            "招商银行": 1.0,
            "工商银行": 0.8,
            "建设银行": 0.9,
            "农业银行": 1.1,
            "中国银行": 0.7
        }.get(bank_name, 1.0)
        
        return base_fee * bank_multiplier
    
    def _calculate_approval_probability(self, risk_level: str, bank_name: str) -> float:
        """计算批准概率"""
        base_probability = {
            "低风险": 0.95,
            "中低风险": 0.85,
            "中风险": 0.70,
            "中高风险": 0.50,
            "高风险": 0.20
        }.get(risk_level, 0.50)
        
        bank_adjustment = {
            "招商银行": 0.05,
            "工商银行": 0.10,
            "建设银行": 0.08,
            "农业银行": 0.03,
            "中国银行": 0.12
        }.get(bank_name, 0.0)
        
        return min(max(base_probability + bank_adjustment, 0.0), 1.0) * 100
    
    def _generate_conditions(self, bank_name: str, profile: Dict, risk_level: str) -> List[str]:
        """生成附加条件"""
        conditions = []
        
        if bank_name == "招商银行":
            conditions.append("需要招商银行代发工资或信用卡客户")
        elif bank_name == "工商银行":
            conditions.append("需要工商银行客户或代发工资")
        elif bank_name == "建设银行":
            conditions.append("需要建设银行VIP客户")
        elif bank_name == "农业银行":
            conditions.append("需要农业银行代发工资客户")
        elif bank_name == "中国银行":
            conditions.append("需要中国银行优质客户")
        
        if risk_level in ["中高风险", "高风险"]:
            conditions.append("需要提供担保人")
        
        if profile.get("amount", 0) > 30:
            conditions.append("需要提供收入证明和银行流水")
        
        return conditions
    
    def _generate_reasons(self, risk_level: str, bank_name: str, profile: Dict) -> List[str]:
        """生成批准原因"""
        reasons = []
        
        if risk_level == "低风险":
            reasons.append("信用评分优秀")
            reasons.append("收入稳定可靠")
        elif risk_level == "中低风险":
            reasons.append("信用记录良好")
            reasons.append("负债比率合理")
        
        if profile.get("has_collateral", False):
            reasons.append("有抵押物保障")
        
        if profile.get("work_years", 0) >= 3:
            reasons.append("工作稳定")
        
        if profile.get("monthly_income", 0) >= 10000:
            reasons.append("收入水平较高")
        
        return reasons
    
    def _get_product_name(self, bank_name: str) -> str:
        """获取产品名称"""
        products = {
            "招商银行": "闪电贷",
            "工商银行": "融e借",
            "建设银行": "快贷",
            "农业银行": "随薪贷",
            "中国银行": "中银e贷"
        }
        return products.get(bank_name, "个人信用贷款")

class RiskPricingService:
    """风控定价综合服务"""
    
    def __init__(self):
        self.risk_service = RiskAssessmentService()
        self.pricing_service = PricingService()
    
    async def process_application(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """处理贷款申请"""
        try:
            # 风控评估
            risk_assessment = await self.risk_service.assess_risk(profile)
            
            # 定价计算
            quotations = await self.pricing_service.calculate_pricing(profile, risk_assessment)
            
            return {
                "success": True,
                "risk_assessment": risk_assessment,
                "quotations": quotations,
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"申请处理失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
