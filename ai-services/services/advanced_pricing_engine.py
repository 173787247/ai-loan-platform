"""
高级定价引擎
提供智能利率计算、费用结构和定价优化
"""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid

class PricingStrategy(Enum):
    """定价策略"""
    COMPETITIVE = "competitive"
    PROFIT_OPTIMIZED = "profit_optimized"
    RISK_BASED = "risk_based"
    MARKET_LEADER = "market_leader"

class FeeType(Enum):
    """费用类型"""
    PROCESSING_FEE = "processing_fee"
    LATE_FEE = "late_fee"
    EARLY_REPAYMENT_FEE = "early_repayment_fee"
    INSURANCE_FEE = "insurance_fee"
    NOTARY_FEE = "notary_fee"
    APPRAISAL_FEE = "appraisal_fee"

@dataclass
class PricingResult:
    """定价结果"""
    base_interest_rate: float
    final_interest_rate: float
    monthly_payment: float
    total_interest: float
    total_amount: float
    fees: Dict[FeeType, float]
    total_fees: float
    apr: float  # 年化利率
    pricing_strategy: PricingStrategy
    risk_adjustment: float
    market_adjustment: float
    profit_margin: float
    confidence_score: float
    pricing_timestamp: datetime
    model_version: str

@dataclass
class MarketConditions:
    """市场条件"""
    base_rate: float  # 基准利率
    market_volatility: float  # 市场波动性
    competition_level: float  # 竞争程度
    economic_indicator: float  # 经济指标
    liquidity_condition: float  # 流动性条件

class AdvancedPricingEngine:
    """高级定价引擎"""
    
    def __init__(self):
        self.model_version = "v2.1.0"
        self.base_rates = self._initialize_base_rates()
        self.fee_structures = self._initialize_fee_structures()
        self.risk_adjustments = self._initialize_risk_adjustments()
        self.market_conditions = self._get_current_market_conditions()
    
    def _initialize_base_rates(self) -> Dict[str, float]:
        """初始化基础利率"""
        return {
            "personal_loan": 0.08,  # 8%
            "business_loan": 0.10,  # 10%
            "mortgage": 0.06,       # 6%
            "auto_loan": 0.07,      # 7%
            "credit_card": 0.18,    # 18%
            "micro_loan": 0.15      # 15%
        }
    
    def _initialize_fee_structures(self) -> Dict[FeeType, Dict[str, Any]]:
        """初始化费用结构"""
        return {
            FeeType.PROCESSING_FEE: {
                "type": "percentage",
                "rate": 0.01,  # 1%
                "min_amount": 100,
                "max_amount": 5000
            },
            FeeType.LATE_FEE: {
                "type": "fixed",
                "amount": 50,
                "grace_period_days": 5
            },
            FeeType.EARLY_REPAYMENT_FEE: {
                "type": "percentage",
                "rate": 0.02,  # 2%
                "min_months": 12
            },
            FeeType.INSURANCE_FEE: {
                "type": "percentage",
                "rate": 0.005,  # 0.5%
                "required": True
            },
            FeeType.NOTARY_FEE: {
                "type": "fixed",
                "amount": 200
            },
            FeeType.APPRAISAL_FEE: {
                "type": "fixed",
                "amount": 500
            }
        }
    
    def _initialize_risk_adjustments(self) -> Dict[str, float]:
        """初始化风险调整系数"""
        return {
            "low_risk": -0.02,    # -2%
            "medium_risk": 0.0,   # 0%
            "high_risk": 0.03,    # +3%
            "very_high_risk": 0.08  # +8%
        }
    
    def _get_current_market_conditions(self) -> MarketConditions:
        """获取当前市场条件"""
        # 这里应该从外部数据源获取实时市场数据
        # 目前使用模拟数据
        return MarketConditions(
            base_rate=0.035,  # 3.5% 基准利率
            market_volatility=0.3,
            competition_level=0.7,
            economic_indicator=0.6,
            liquidity_condition=0.8
        )
    
    def calculate_pricing(self, loan_request: Dict[str, Any], 
                         risk_assessment: Dict[str, Any],
                         pricing_strategy: PricingStrategy = PricingStrategy.RISK_BASED) -> PricingResult:
        """计算贷款定价"""
        try:
            # 提取贷款信息
            loan_amount = loan_request.get("loan_amount", 0)
            loan_term_months = loan_request.get("loan_term_months", 12)
            loan_type = loan_request.get("loan_type", "personal_loan")
            risk_level = risk_assessment.get("risk_level", "medium")
            
            # 获取基础利率
            base_rate = self.base_rates.get(loan_type, 0.08)
            
            # 计算风险调整
            risk_adjustment = self._calculate_risk_adjustment(risk_level, risk_assessment)
            
            # 计算市场调整
            market_adjustment = self._calculate_market_adjustment(pricing_strategy)
            
            # 计算最终利率
            final_rate = base_rate + risk_adjustment + market_adjustment
            final_rate = max(final_rate, 0.03)  # 最低3%
            
            # 计算月供
            monthly_payment = self._calculate_monthly_payment(loan_amount, final_rate, loan_term_months)
            
            # 计算总利息
            total_interest = monthly_payment * loan_term_months - loan_amount
            
            # 计算费用
            fees = self._calculate_fees(loan_request, loan_amount, loan_term_months)
            total_fees = sum(fees.values())
            
            # 计算APR
            apr = self._calculate_apr(loan_amount, monthly_payment, loan_term_months, total_fees)
            
            # 计算利润空间
            profit_margin = self._calculate_profit_margin(final_rate, loan_amount, total_fees)
            
            # 计算置信度
            confidence_score = self._calculate_pricing_confidence(risk_assessment, loan_request)
            
            return PricingResult(
                base_interest_rate=base_rate,
                final_interest_rate=final_rate,
                monthly_payment=monthly_payment,
                total_interest=total_interest,
                total_amount=loan_amount + total_interest + total_fees,
                fees=fees,
                total_fees=total_fees,
                apr=apr,
                pricing_strategy=pricing_strategy,
                risk_adjustment=risk_adjustment,
                market_adjustment=market_adjustment,
                profit_margin=profit_margin,
                confidence_score=confidence_score,
                pricing_timestamp=datetime.now(),
                model_version=self.model_version
            )
            
        except Exception as e:
            logger.error(f"定价计算失败: {e}")
            return self._create_default_pricing_result(loan_request)
    
    def _calculate_risk_adjustment(self, risk_level: str, risk_assessment: Dict[str, Any]) -> float:
        """计算风险调整"""
        base_adjustment = self.risk_adjustments.get(risk_level, 0.0)
        
        # 基于具体风险因子进行微调
        risk_score = risk_assessment.get("overall_risk_score", 0.5)
        
        # 如果风险得分很高，增加调整
        if risk_score > 0.8:
            base_adjustment += 0.02
        elif risk_score < 0.3:
            base_adjustment -= 0.01
        
        return base_adjustment
    
    def _calculate_market_adjustment(self, strategy: PricingStrategy) -> float:
        """计算市场调整"""
        market = self.market_conditions
        
        if strategy == PricingStrategy.COMPETITIVE:
            # 竞争性定价：降低利率
            adjustment = -0.01 * market.competition_level
        elif strategy == PricingStrategy.PROFIT_OPTIMIZED:
            # 利润优化：提高利率
            adjustment = 0.01 * (1 - market.competition_level)
        elif strategy == PricingStrategy.MARKET_LEADER:
            # 市场领导者：跟随市场
            adjustment = 0.005 * market.market_volatility
        else:  # RISK_BASED
            # 基于风险：根据市场条件调整
            adjustment = 0.01 * market.market_volatility
        
        return adjustment
    
    def _calculate_monthly_payment(self, principal: float, annual_rate: float, months: int) -> float:
        """计算月供"""
        if annual_rate == 0:
            return principal / months
        
        monthly_rate = annual_rate / 12
        return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    def _calculate_fees(self, loan_request: Dict[str, Any], 
                       loan_amount: float, loan_term_months: int) -> Dict[FeeType, float]:
        """计算各种费用"""
        fees = {}
        
        # 手续费
        processing_fee_config = self.fee_structures[FeeType.PROCESSING_FEE]
        if processing_fee_config["type"] == "percentage":
            processing_fee = loan_amount * processing_fee_config["rate"]
            processing_fee = max(processing_fee, processing_fee_config["min_amount"])
            processing_fee = min(processing_fee, processing_fee_config["max_amount"])
        else:
            processing_fee = processing_fee_config["amount"]
        fees[FeeType.PROCESSING_FEE] = processing_fee
        
        # 保险费（如果要求）
        insurance_config = self.fee_structures[FeeType.INSURANCE_FEE]
        if insurance_config["required"]:
            fees[FeeType.INSURANCE_FEE] = loan_amount * insurance_config["rate"]
        else:
            fees[FeeType.INSURANCE_FEE] = 0
        
        # 公证费（大额贷款）
        if loan_amount > 100000:
            fees[FeeType.NOTARY_FEE] = self.fee_structures[FeeType.NOTARY_FEE]["amount"]
        else:
            fees[FeeType.NOTARY_FEE] = 0
        
        # 评估费（抵押贷款）
        if loan_request.get("loan_type") == "mortgage":
            fees[FeeType.APPRAISAL_FEE] = self.fee_structures[FeeType.APPRAISAL_FEE]["amount"]
        else:
            fees[FeeType.APPRAISAL_FEE] = 0
        
        # 提前还款费（如果适用）
        if loan_term_months > 12:
            fees[FeeType.EARLY_REPAYMENT_FEE] = loan_amount * self.fee_structures[FeeType.EARLY_REPAYMENT_FEE]["rate"]
        else:
            fees[FeeType.EARLY_REPAYMENT_FEE] = 0
        
        # 逾期费（预设，实际使用时根据逾期情况计算）
        fees[FeeType.LATE_FEE] = 0
        
        return fees
    
    def _calculate_apr(self, principal: float, monthly_payment: float, 
                      months: int, total_fees: float) -> float:
        """计算年化利率(APR)"""
        if principal == 0:
            return 0
        
        # 使用牛顿法求解APR
        total_payment = monthly_payment * months
        effective_principal = principal - total_fees
        
        if effective_principal <= 0:
            return 0
        
        # 简化的APR计算
        total_interest = total_payment - principal
        apr = (total_interest / effective_principal) * (12 / months)
        
        return min(apr, 1.0)  # 最高100%
    
    def _calculate_profit_margin(self, interest_rate: float, loan_amount: float, 
                               total_fees: float) -> float:
        """计算利润空间"""
        # 简化的利润计算：利率收入 + 费用收入 - 资金成本
        funding_cost = 0.03  # 假设资金成本3%
        interest_income = loan_amount * interest_rate
        fee_income = total_fees
        total_cost = loan_amount * funding_cost
        
        profit = interest_income + fee_income - total_cost
        profit_margin = profit / loan_amount if loan_amount > 0 else 0
        
        return max(profit_margin, 0)
    
    def _calculate_pricing_confidence(self, risk_assessment: Dict[str, Any], 
                                    loan_request: Dict[str, Any]) -> float:
        """计算定价置信度"""
        # 基于风险评估置信度和数据完整性
        risk_confidence = risk_assessment.get("confidence_score", 0.5)
        
        # 检查数据完整性
        required_fields = ["loan_amount", "loan_term_months", "loan_type"]
        data_completeness = sum(1 for field in required_fields if field in loan_request) / len(required_fields)
        
        # 综合置信度
        confidence = (risk_confidence + data_completeness) / 2
        
        return min(confidence, 1.0)
    
    def _create_default_pricing_result(self, loan_request: Dict[str, Any]) -> PricingResult:
        """创建默认定价结果"""
        loan_amount = loan_request.get("loan_amount", 100000)
        loan_term_months = loan_request.get("loan_term_months", 12)
        
        return PricingResult(
            base_interest_rate=0.08,
            final_interest_rate=0.10,
            monthly_payment=self._calculate_monthly_payment(loan_amount, 0.10, loan_term_months),
            total_interest=0,
            total_amount=loan_amount,
            fees={},
            total_fees=0,
            apr=0.10,
            pricing_strategy=PricingStrategy.RISK_BASED,
            risk_adjustment=0.02,
            market_adjustment=0.0,
            profit_margin=0.05,
            confidence_score=0.3,
            pricing_timestamp=datetime.now(),
            model_version=self.model_version
        )
    
    def optimize_pricing(self, loan_request: Dict[str, Any], 
                        risk_assessment: Dict[str, Any],
                        target_profit_margin: float = 0.05) -> List[PricingResult]:
        """优化定价方案"""
        strategies = [
            PricingStrategy.COMPETITIVE,
            PricingStrategy.PROFIT_OPTIMIZED,
            PricingStrategy.RISK_BASED,
            PricingStrategy.MARKET_LEADER
        ]
        
        results = []
        for strategy in strategies:
            pricing = self.calculate_pricing(loan_request, risk_assessment, strategy)
            results.append(pricing)
        
        # 按利润空间排序
        results.sort(key=lambda x: x.profit_margin, reverse=True)
        
        return results
    
    def compare_pricing_scenarios(self, loan_request: Dict[str, Any], 
                                risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """比较不同定价场景"""
        scenarios = {}
        
        # 不同贷款期限
        for term in [12, 24, 36, 60]:
            request = loan_request.copy()
            request["loan_term_months"] = term
            pricing = self.calculate_pricing(request, risk_assessment)
            scenarios[f"{term}个月"] = {
                "monthly_payment": pricing.monthly_payment,
                "total_interest": pricing.total_interest,
                "apr": pricing.apr
            }
        
        # 不同贷款金额
        base_amount = loan_request.get("loan_amount", 100000)
        for amount in [base_amount * 0.5, base_amount, base_amount * 1.5, base_amount * 2]:
            request = loan_request.copy()
            request["loan_amount"] = amount
            pricing = self.calculate_pricing(request, risk_assessment)
            scenarios[f"{amount/10000:.0f}万"] = {
                "monthly_payment": pricing.monthly_payment,
                "total_interest": pricing.total_interest,
                "apr": pricing.apr
            }
        
        return scenarios
    
    def get_pricing_model_info(self) -> Dict[str, Any]:
        """获取定价模型信息"""
        return {
            "model_version": self.model_version,
            "base_rates": self.base_rates,
            "fee_structures": {fee.value: config for fee, config in self.fee_structures.items()},
            "risk_adjustments": self.risk_adjustments,
            "market_conditions": {
                "base_rate": self.market_conditions.base_rate,
                "market_volatility": self.market_conditions.market_volatility,
                "competition_level": self.market_conditions.competition_level,
                "economic_indicator": self.market_conditions.economic_indicator,
                "liquidity_condition": self.market_conditions.liquidity_condition
            }
        }
