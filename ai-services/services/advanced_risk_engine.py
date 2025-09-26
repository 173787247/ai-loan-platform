"""
高级风控引擎
提供智能风险评估、决策逻辑和风险监控
"""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid

class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class RiskFactor(Enum):
    """风险因子"""
    CREDIT_SCORE = "credit_score"
    INCOME_STABILITY = "income_stability"
    DEBT_RATIO = "debt_ratio"
    EMPLOYMENT_HISTORY = "employment_history"
    COLLATERAL = "collateral"
    LOAN_HISTORY = "loan_history"
    AGE = "age"
    MARITAL_STATUS = "marital_status"
    EDUCATION = "education"
    INDUSTRY_RISK = "industry_risk"

@dataclass
class RiskAssessment:
    """风险评估结果"""
    overall_risk_score: float
    risk_level: RiskLevel
    approval_recommendation: str
    risk_factors: Dict[RiskFactor, float]
    risk_explanations: Dict[RiskFactor, str]
    mitigation_suggestions: List[str]
    confidence_score: float
    assessment_timestamp: datetime
    model_version: str

@dataclass
class CreditProfile:
    """信用档案"""
    credit_score: int
    credit_history_years: float
    payment_delinquencies: int
    credit_utilization: float
    recent_inquiries: int
    public_records: int
    credit_mix: str
    account_age: float

@dataclass
class IncomeProfile:
    """收入档案"""
    annual_income: float
    income_stability: float
    employment_years: float
    job_title: str
    industry: str
    income_growth_rate: float
    additional_income: float
    income_verification: str

class AdvancedRiskEngine:
    """高级风控引擎"""
    
    def __init__(self):
        self.model_version = "v2.1.0"
        self.risk_weights = self._initialize_risk_weights()
        self.industry_risk_scores = self._initialize_industry_risks()
        self.risk_thresholds = self._initialize_risk_thresholds()
    
    def _initialize_risk_weights(self) -> Dict[RiskFactor, float]:
        """初始化风险权重"""
        return {
            RiskFactor.CREDIT_SCORE: 0.25,
            RiskFactor.INCOME_STABILITY: 0.20,
            RiskFactor.DEBT_RATIO: 0.15,
            RiskFactor.EMPLOYMENT_HISTORY: 0.10,
            RiskFactor.LOAN_HISTORY: 0.10,
            RiskFactor.AGE: 0.05,
            RiskFactor.MARITAL_STATUS: 0.05,
            RiskFactor.EDUCATION: 0.05,
            RiskFactor.INDUSTRY_RISK: 0.05
        }
    
    def _initialize_industry_risks(self) -> Dict[str, float]:
        """初始化行业风险评分"""
        return {
            "金融": 0.3,
            "科技": 0.2,
            "医疗": 0.2,
            "教育": 0.1,
            "政府": 0.1,
            "制造业": 0.4,
            "零售": 0.5,
            "餐饮": 0.6,
            "建筑": 0.7,
            "娱乐": 0.8,
            "其他": 0.5
        }
    
    def _initialize_risk_thresholds(self) -> Dict[str, float]:
        """初始化风险阈值"""
        return {
            "low_risk_max": 0.3,
            "medium_risk_max": 0.6,
            "high_risk_max": 0.8,
            "approval_threshold": 0.7
        }
    
    def assess_risk(self, applicant_data: Dict[str, Any]) -> RiskAssessment:
        """综合风险评估"""
        try:
            # 提取关键信息
            credit_profile = self._extract_credit_profile(applicant_data)
            income_profile = self._extract_income_profile(applicant_data)
            
            # 计算各风险因子得分
            risk_factors = {}
            risk_explanations = {}
            
            # 信用评分风险
            credit_risk = self._calculate_credit_risk(credit_profile)
            risk_factors[RiskFactor.CREDIT_SCORE] = credit_risk["score"]
            risk_explanations[RiskFactor.CREDIT_SCORE] = credit_risk["explanation"]
            
            # 收入稳定性风险
            income_risk = self._calculate_income_risk(income_profile)
            risk_factors[RiskFactor.INCOME_STABILITY] = income_risk["score"]
            risk_explanations[RiskFactor.INCOME_STABILITY] = income_risk["explanation"]
            
            # 负债比率风险
            debt_risk = self._calculate_debt_risk(applicant_data)
            risk_factors[RiskFactor.DEBT_RATIO] = debt_risk["score"]
            risk_explanations[RiskFactor.DEBT_RATIO] = debt_risk["explanation"]
            
            # 就业历史风险
            employment_risk = self._calculate_employment_risk(income_profile)
            risk_factors[RiskFactor.EMPLOYMENT_HISTORY] = employment_risk["score"]
            risk_explanations[RiskFactor.EMPLOYMENT_HISTORY] = employment_risk["explanation"]
            
            # 贷款历史风险
            loan_history_risk = self._calculate_loan_history_risk(applicant_data)
            risk_factors[RiskFactor.LOAN_HISTORY] = loan_history_risk["score"]
            risk_explanations[RiskFactor.LOAN_HISTORY] = loan_history_risk["explanation"]
            
            # 年龄风险
            age_risk = self._calculate_age_risk(applicant_data)
            risk_factors[RiskFactor.AGE] = age_risk["score"]
            risk_explanations[RiskFactor.AGE] = age_risk["explanation"]
            
            # 婚姻状况风险
            marital_risk = self._calculate_marital_risk(applicant_data)
            risk_factors[RiskFactor.MARITAL_STATUS] = marital_risk["score"]
            risk_explanations[RiskFactor.MARITAL_STATUS] = marital_risk["explanation"]
            
            # 教育背景风险
            education_risk = self._calculate_education_risk(applicant_data)
            risk_factors[RiskFactor.EDUCATION] = education_risk["score"]
            risk_explanations[RiskFactor.EDUCATION] = education_risk["explanation"]
            
            # 行业风险
            industry_risk = self._calculate_industry_risk(income_profile)
            risk_factors[RiskFactor.INDUSTRY_RISK] = industry_risk["score"]
            risk_explanations[RiskFactor.INDUSTRY_RISK] = industry_risk["explanation"]
            
            # 计算综合风险得分
            overall_risk_score = self._calculate_overall_risk_score(risk_factors)
            
            # 确定风险等级
            risk_level = self._determine_risk_level(overall_risk_score)
            
            # 生成审批建议
            approval_recommendation = self._generate_approval_recommendation(
                overall_risk_score, risk_factors, applicant_data
            )
            
            # 生成风险缓解建议
            mitigation_suggestions = self._generate_mitigation_suggestions(
                risk_factors, overall_risk_score
            )
            
            # 计算置信度
            confidence_score = self._calculate_confidence_score(risk_factors, applicant_data)
            
            return RiskAssessment(
                overall_risk_score=overall_risk_score,
                risk_level=risk_level,
                approval_recommendation=approval_recommendation,
                risk_factors=risk_factors,
                risk_explanations=risk_explanations,
                mitigation_suggestions=mitigation_suggestions,
                confidence_score=confidence_score,
                assessment_timestamp=datetime.now(),
                model_version=self.model_version
            )
            
        except Exception as e:
            logger.error(f"风险评估失败: {e}")
            return self._create_default_risk_assessment()
    
    def _extract_credit_profile(self, data: Dict[str, Any]) -> CreditProfile:
        """提取信用档案"""
        return CreditProfile(
            credit_score=data.get("credit_score", 600),
            credit_history_years=data.get("credit_history_years", 0),
            payment_delinquencies=data.get("payment_delinquencies", 0),
            credit_utilization=data.get("credit_utilization", 0.3),
            recent_inquiries=data.get("recent_inquiries", 0),
            public_records=data.get("public_records", 0),
            credit_mix=data.get("credit_mix", "basic"),
            account_age=data.get("account_age", 0)
        )
    
    def _extract_income_profile(self, data: Dict[str, Any]) -> IncomeProfile:
        """提取收入档案"""
        return IncomeProfile(
            annual_income=data.get("annual_income", 0),
            income_stability=data.get("income_stability", 0.5),
            employment_years=data.get("employment_years", 0),
            job_title=data.get("job_title", ""),
            industry=data.get("industry", "其他"),
            income_growth_rate=data.get("income_growth_rate", 0),
            additional_income=data.get("additional_income", 0),
            income_verification=data.get("income_verification", "unverified")
        )
    
    def _calculate_credit_risk(self, credit_profile: CreditProfile) -> Dict[str, Any]:
        """计算信用风险"""
        score = credit_profile.credit_score
        
        if score >= 750:
            risk_score = 0.1
            explanation = "信用评分优秀，风险极低"
        elif score >= 700:
            risk_score = 0.2
            explanation = "信用评分良好，风险较低"
        elif score >= 650:
            risk_score = 0.4
            explanation = "信用评分一般，风险中等"
        elif score >= 600:
            risk_score = 0.6
            explanation = "信用评分偏低，风险较高"
        else:
            risk_score = 0.9
            explanation = "信用评分较差，风险很高"
        
        # 考虑其他信用因素
        if credit_profile.payment_delinquencies > 3:
            risk_score += 0.2
            explanation += "，存在多次逾期记录"
        
        if credit_profile.credit_utilization > 0.8:
            risk_score += 0.1
            explanation += "，信用卡使用率过高"
        
        return {"score": min(risk_score, 1.0), "explanation": explanation}
    
    def _calculate_income_risk(self, income_profile: IncomeProfile) -> Dict[str, Any]:
        """计算收入风险"""
        if income_profile.annual_income < 50000:
            base_risk = 0.7
            explanation = "年收入较低，还款能力有限"
        elif income_profile.annual_income < 100000:
            base_risk = 0.4
            explanation = "年收入中等，还款能力一般"
        elif income_profile.annual_income < 200000:
            base_risk = 0.2
            explanation = "年收入较高，还款能力较强"
        else:
            base_risk = 0.1
            explanation = "年收入很高，还款能力很强"
        
        # 考虑收入稳定性
        if income_profile.income_stability < 0.3:
            base_risk += 0.3
            explanation += "，收入不稳定"
        elif income_profile.income_stability < 0.6:
            base_risk += 0.1
            explanation += "，收入相对稳定"
        
        # 考虑就业年限
        if income_profile.employment_years < 1:
            base_risk += 0.2
            explanation += "，就业时间较短"
        
        return {"score": min(base_risk, 1.0), "explanation": explanation}
    
    def _calculate_debt_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算负债风险"""
        monthly_income = data.get("monthly_income", 0)
        monthly_debt = data.get("monthly_debt", 0)
        
        if monthly_income == 0:
            return {"score": 1.0, "explanation": "无法计算负债比率"}
        
        debt_ratio = monthly_debt / monthly_income
        
        if debt_ratio > 0.5:
            risk_score = 0.9
            explanation = f"负债比率过高({debt_ratio:.1%})，还款压力大"
        elif debt_ratio > 0.4:
            risk_score = 0.6
            explanation = f"负债比率较高({debt_ratio:.1%})，需关注还款能力"
        elif debt_ratio > 0.3:
            risk_score = 0.3
            explanation = f"负债比率适中({debt_ratio:.1%})，还款能力良好"
        else:
            risk_score = 0.1
            explanation = f"负债比率较低({debt_ratio:.1%})，还款能力强"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_employment_risk(self, income_profile: IncomeProfile) -> Dict[str, Any]:
        """计算就业风险"""
        employment_years = income_profile.employment_years
        
        if employment_years < 0.5:
            risk_score = 0.8
            explanation = "就业时间过短，工作稳定性差"
        elif employment_years < 2:
            risk_score = 0.5
            explanation = "就业时间较短，工作稳定性一般"
        elif employment_years < 5:
            risk_score = 0.2
            explanation = "就业时间适中，工作稳定性良好"
        else:
            risk_score = 0.1
            explanation = "就业时间较长，工作稳定性很好"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_loan_history_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算贷款历史风险"""
        loan_count = data.get("loan_count", 0)
        default_count = data.get("default_count", 0)
        
        if default_count > 0:
            risk_score = 0.9
            explanation = f"存在{default_count}次违约记录，信用风险很高"
        elif loan_count == 0:
            risk_score = 0.6
            explanation = "无贷款历史，无法评估还款能力"
        elif loan_count < 3:
            risk_score = 0.3
            explanation = "贷款历史较少，还款能力待验证"
        else:
            risk_score = 0.1
            explanation = "贷款历史丰富，还款能力已验证"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_age_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算年龄风险"""
        age = data.get("age", 30)
        
        if age < 22:
            risk_score = 0.7
            explanation = "年龄过小，收入稳定性不足"
        elif age < 25:
            risk_score = 0.4
            explanation = "年龄较小，收入增长潜力大但稳定性一般"
        elif age < 35:
            risk_score = 0.1
            explanation = "年龄适中，收入稳定且增长潜力大"
        elif age < 50:
            risk_score = 0.2
            explanation = "年龄成熟，收入稳定"
        elif age < 60:
            risk_score = 0.3
            explanation = "年龄较大，收入可能下降"
        else:
            risk_score = 0.6
            explanation = "年龄过大，收入下降风险高"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_marital_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算婚姻状况风险"""
        marital_status = data.get("marital_status", "single")
        
        if marital_status == "married":
            risk_score = 0.1
            explanation = "已婚，家庭稳定性好，还款能力强"
        elif marital_status == "divorced":
            risk_score = 0.4
            explanation = "离异，家庭稳定性一般"
        else:
            risk_score = 0.3
            explanation = "未婚，家庭稳定性待评估"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_education_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算教育背景风险"""
        education = data.get("education", "high_school")
        
        education_scores = {
            "phd": 0.1,
            "master": 0.15,
            "bachelor": 0.2,
            "associate": 0.3,
            "high_school": 0.4,
            "below_high_school": 0.6
        }
        
        risk_score = education_scores.get(education, 0.4)
        education_names = {
            "phd": "博士",
            "master": "硕士",
            "bachelor": "本科",
            "associate": "专科",
            "high_school": "高中",
            "below_high_school": "高中以下"
        }
        
        explanation = f"教育背景为{education_names.get(education, '未知')}，收入稳定性{'较高' if risk_score < 0.3 else '一般'}"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_industry_risk(self, income_profile: IncomeProfile) -> Dict[str, Any]:
        """计算行业风险"""
        industry = income_profile.industry
        risk_score = self.industry_risk_scores.get(industry, 0.5)
        
        if risk_score < 0.3:
            explanation = f"{industry}行业风险较低，收入稳定性好"
        elif risk_score < 0.5:
            explanation = f"{industry}行业风险中等，收入相对稳定"
        else:
            explanation = f"{industry}行业风险较高，收入稳定性待观察"
        
        return {"score": risk_score, "explanation": explanation}
    
    def _calculate_overall_risk_score(self, risk_factors: Dict[RiskFactor, float]) -> float:
        """计算综合风险得分"""
        weighted_score = 0.0
        
        for factor, score in risk_factors.items():
            weight = self.risk_weights.get(factor, 0.1)
            weighted_score += score * weight
        
        return min(weighted_score, 1.0)
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """确定风险等级"""
        if risk_score <= self.risk_thresholds["low_risk_max"]:
            return RiskLevel.LOW
        elif risk_score <= self.risk_thresholds["medium_risk_max"]:
            return RiskLevel.MEDIUM
        elif risk_score <= self.risk_thresholds["high_risk_max"]:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH
    
    def _generate_approval_recommendation(self, risk_score: float, 
                                        risk_factors: Dict[RiskFactor, float],
                                        applicant_data: Dict[str, Any]) -> str:
        """生成审批建议"""
        if risk_score <= self.risk_thresholds["approval_threshold"]:
            return "建议批准"
        elif risk_score <= 0.8:
            return "建议有条件批准"
        else:
            return "建议拒绝"
    
    def _generate_mitigation_suggestions(self, risk_factors: Dict[RiskFactor, float], 
                                       overall_score: float) -> List[str]:
        """生成风险缓解建议"""
        suggestions = []
        
        # 基于各风险因子生成建议
        for factor, score in risk_factors.items():
            if score > 0.6:  # 高风险因子
                if factor == RiskFactor.CREDIT_SCORE:
                    suggestions.append("建议提供担保人或抵押物")
                elif factor == RiskFactor.INCOME_STABILITY:
                    suggestions.append("建议提供更详细的收入证明")
                elif factor == RiskFactor.DEBT_RATIO:
                    suggestions.append("建议降低贷款金额或延长还款期限")
                elif factor == RiskFactor.EMPLOYMENT_HISTORY:
                    suggestions.append("建议提供工作稳定性证明")
        
        if overall_score > 0.7:
            suggestions.append("建议增加首付比例")
            suggestions.append("建议提供额外担保")
        
        return suggestions
    
    def _calculate_confidence_score(self, risk_factors: Dict[RiskFactor, float], 
                                  applicant_data: Dict[str, Any]) -> float:
        """计算置信度得分"""
        # 基于数据完整性和一致性计算置信度
        data_completeness = self._calculate_data_completeness(applicant_data)
        factor_consistency = self._calculate_factor_consistency(risk_factors)
        
        confidence = (data_completeness + factor_consistency) / 2
        return min(confidence, 1.0)
    
    def _calculate_data_completeness(self, data: Dict[str, Any]) -> float:
        """计算数据完整性"""
        required_fields = ["credit_score", "annual_income", "age", "employment_years"]
        provided_fields = sum(1 for field in required_fields if field in data and data[field] is not None)
        return provided_fields / len(required_fields)
    
    def _calculate_factor_consistency(self, risk_factors: Dict[RiskFactor, float]) -> float:
        """计算因子一致性"""
        scores = list(risk_factors.values())
        if not scores:
            return 0.5
        
        # 计算方差，方差越小一致性越高
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        consistency = 1.0 - min(variance, 1.0)
        
        return consistency
    
    def _create_default_risk_assessment(self) -> RiskAssessment:
        """创建默认风险评估"""
        return RiskAssessment(
            overall_risk_score=0.5,
            risk_level=RiskLevel.MEDIUM,
            approval_recommendation="需要更多信息进行评估",
            risk_factors={},
            risk_explanations={},
            mitigation_suggestions=["建议提供更详细的申请材料"],
            confidence_score=0.3,
            assessment_timestamp=datetime.now(),
            model_version=self.model_version
        )
    
    def get_risk_model_info(self) -> Dict[str, Any]:
        """获取风控模型信息"""
        return {
            "model_version": self.model_version,
            "risk_weights": {factor.value: weight for factor, weight in self.risk_weights.items()},
            "risk_thresholds": self.risk_thresholds,
            "industry_risks": self.industry_risk_scores,
            "supported_factors": [factor.value for factor in RiskFactor]
        }
