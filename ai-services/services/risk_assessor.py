"""
风险评估服务

@author AI Loan Platform Team
@version 1.0.0
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from loguru import logger
import torch
import torch.nn as nn
from datetime import datetime, timedelta
import json

class RiskAssessor:
    """风险评估服务类"""
    
    def __init__(self):
        self.logger = logger
        self.risk_models = self._load_risk_models()
        
    def _load_risk_models(self) -> Dict[str, Any]:
        """加载风险评估模型"""
        return {
            "credit_model": self._create_credit_model(),
            "market_model": self._create_market_model(),
            "liquidity_model": self._create_liquidity_model()
        }
    
    def _create_credit_model(self) -> nn.Module:
        """创建信用风险模型"""
        class CreditRiskModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(10, 64)
                self.fc2 = nn.Linear(64, 32)
                self.fc3 = nn.Linear(32, 16)
                self.fc4 = nn.Linear(16, 1)
                self.dropout = nn.Dropout(0.2)
                self.relu = nn.ReLU()
                self.sigmoid = nn.Sigmoid()
                
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.dropout(x)
                x = self.relu(self.fc2(x))
                x = self.dropout(x)
                x = self.relu(self.fc3(x))
                x = self.sigmoid(self.fc4(x))
                return x
        
        return CreditRiskModel()
    
    def _create_market_model(self) -> nn.Module:
        """创建市场风险模型"""
        class MarketRiskModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(8, 32)
                self.fc2 = nn.Linear(32, 16)
                self.fc3 = nn.Linear(16, 1)
                self.relu = nn.ReLU()
                self.sigmoid = nn.Sigmoid()
                
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.relu(self.fc2(x))
                x = self.sigmoid(self.fc3(x))
                return x
        
        return MarketRiskModel()
    
    def _create_liquidity_model(self) -> nn.Module:
        """创建流动性风险模型"""
        class LiquidityRiskModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(6, 24)
                self.fc2 = nn.Linear(24, 12)
                self.fc3 = nn.Linear(12, 1)
                self.relu = nn.ReLU()
                self.sigmoid = nn.Sigmoid()
                
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.relu(self.fc2(x))
                x = self.sigmoid(self.fc3(x))
                return x
        
        return LiquidityRiskModel()
    
    def assess_risk(self, user_id: int, business_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估风险"""
        try:
            self.logger.info(f"开始风险评估: 用户ID {user_id}")
            
            # 计算基础风险分数
            base_score = self._calculate_base_risk_score(business_data)
            
            # 计算市场风险分数
            market_score = self._calculate_market_risk_score(market_data)
            
            # 计算信用风险分数
            credit_score = self._calculate_credit_risk_score(business_data)
            
            # 计算流动性风险分数
            liquidity_score = self._calculate_liquidity_risk_score(business_data)
            
            # 计算操作风险分数
            operational_score = self._calculate_operational_risk_score(business_data)
            
            # 计算综合风险分数
            total_score = self._calculate_total_risk_score(
                base_score, market_score, credit_score, liquidity_score, operational_score
            )
            
            # 确定风险等级
            risk_level = self._determine_risk_level(total_score)
            
            # 计算风险概率
            risk_probability = self._calculate_risk_probability(total_score, business_data)
            
            # 生成风险报告
            risk_report = self._generate_risk_report(
                base_score, market_score, credit_score, liquidity_score, operational_score,
                total_score, risk_level, risk_probability, business_data
            )
            
            # 识别风险因素
            risk_factors = self._identify_risk_factors(business_data, market_data)
            
            # 建议缓解策略
            mitigation_strategies = self._suggest_mitigation_strategies(risk_level, business_data)
            
            # 生成推荐
            recommendations = self._generate_recommendations(risk_level, business_data)
            
            result = {
                "user_id": user_id,
                "assessment_time": datetime.now().isoformat(),
                "risk_scores": {
                    "base_risk_score": base_score,
                    "market_risk_score": market_score,
                    "credit_risk_score": credit_score,
                    "liquidity_risk_score": liquidity_score,
                    "operational_risk_score": operational_score,
                    "total_risk_score": total_score
                },
                "risk_level": risk_level,
                "risk_probability": risk_probability,
                "risk_report": risk_report,
                "risk_factors": risk_factors,
                "mitigation_strategies": mitigation_strategies,
                "recommendations": recommendations,
                "confidence_level": self._calculate_confidence_level(business_data)
            }
            
            self.logger.info(f"风险评估完成: 用户ID {user_id}, 风险等级: {risk_level}")
            return result
            
        except Exception as e:
            self.logger.error(f"风险评估失败: 用户ID {user_id}, 错误: {str(e)}")
            raise
    
    def _calculate_base_risk_score(self, business_data: Dict[str, Any]) -> float:
        """计算基础风险分数"""
        score = 0.0
        
        # 企业规模风险
        revenue = business_data.get('revenue', 0)
        if revenue < 100:
            score += 0.3
        elif revenue < 500:
            score += 0.2
        elif revenue < 1000:
            score += 0.1
        
        # 盈利能力风险
        profit = business_data.get('profit', 0)
        if profit < 0:
            score += 0.4
        elif profit < revenue * 0.05:
            score += 0.2
        elif profit < revenue * 0.1:
            score += 0.1
        
        # 资产负债率风险
        assets = business_data.get('assets', 1)
        liabilities = business_data.get('liabilities', 0)
        debt_ratio = liabilities / assets if assets > 0 else 1
        
        if debt_ratio > 0.8:
            score += 0.3
        elif debt_ratio > 0.6:
            score += 0.2
        elif debt_ratio > 0.4:
            score += 0.1
        
        # 行业风险
        industry = business_data.get('industry', '')
        high_risk_industries = ['房地产', '建筑', '贸易', '餐饮']
        if any(risk_industry in industry for risk_industry in high_risk_industries):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_market_risk_score(self, market_data: Dict[str, Any]) -> float:
        """计算市场风险分数"""
        score = 0.0
        
        # 宏观经济指标
        gdp_growth = market_data.get('gdp_growth', 0)
        if gdp_growth < 3:
            score += 0.3
        elif gdp_growth < 5:
            score += 0.2
        elif gdp_growth < 7:
            score += 0.1
        
        # 利率风险
        interest_rate = market_data.get('interest_rate', 0)
        if interest_rate > 0.06:
            score += 0.2
        elif interest_rate > 0.04:
            score += 0.1
        
        # 通胀风险
        inflation = market_data.get('inflation', 0)
        if inflation > 0.05:
            score += 0.2
        elif inflation > 0.03:
            score += 0.1
        
        # 汇率风险
        exchange_rate_volatility = market_data.get('exchange_rate_volatility', 0)
        if exchange_rate_volatility > 0.1:
            score += 0.2
        elif exchange_rate_volatility > 0.05:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_credit_risk_score(self, business_data: Dict[str, Any]) -> float:
        """计算信用风险分数"""
        score = 0.0
        
        # 信用历史
        credit_history = business_data.get('credit_history', {})
        if credit_history.get('default_count', 0) > 0:
            score += 0.4
        elif credit_history.get('late_payment_count', 0) > 3:
            score += 0.2
        elif credit_history.get('late_payment_count', 0) > 1:
            score += 0.1
        
        # 信用评级
        credit_rating = business_data.get('credit_rating', 'C')
        rating_scores = {'AAA': 0.0, 'AA': 0.1, 'A': 0.2, 'BBB': 0.3, 'BB': 0.4, 'B': 0.5, 'C': 0.6, 'D': 0.8}
        score += rating_scores.get(credit_rating, 0.6)
        
        # 担保情况
        collateral = business_data.get('collateral', {})
        if not collateral.get('has_collateral', False):
            score += 0.2
        elif collateral.get('collateral_value', 0) < business_data.get('loan_amount', 0) * 0.8:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_liquidity_risk_score(self, business_data: Dict[str, Any]) -> float:
        """计算流动性风险分数"""
        score = 0.0
        
        # 现金流
        cash_flow = business_data.get('cash_flow', 0)
        monthly_expenses = business_data.get('monthly_expenses', 1)
        if cash_flow < monthly_expenses * 3:
            score += 0.4
        elif cash_flow < monthly_expenses * 6:
            score += 0.2
        elif cash_flow < monthly_expenses * 12:
            score += 0.1
        
        # 流动资产比率
        current_assets = business_data.get('current_assets', 0)
        current_liabilities = business_data.get('current_liabilities', 1)
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
        
        if current_ratio < 1:
            score += 0.3
        elif current_ratio < 1.5:
            score += 0.2
        elif current_ratio < 2:
            score += 0.1
        
        # 应收账款周转率
        accounts_receivable = business_data.get('accounts_receivable', 0)
        revenue = business_data.get('revenue', 1)
        if accounts_receivable > revenue * 0.3:
            score += 0.2
        elif accounts_receivable > revenue * 0.2:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_operational_risk_score(self, business_data: Dict[str, Any]) -> float:
        """计算操作风险分数"""
        score = 0.0
        
        # 管理经验
        management_experience = business_data.get('management_experience', 0)
        if management_experience < 2:
            score += 0.3
        elif management_experience < 5:
            score += 0.2
        elif management_experience < 10:
            score += 0.1
        
        # 员工数量
        employee_count = business_data.get('employee_count', 0)
        if employee_count < 5:
            score += 0.2
        elif employee_count < 20:
            score += 0.1
        
        # 业务复杂度
        business_complexity = business_data.get('business_complexity', 'low')
        complexity_scores = {'low': 0.0, 'medium': 0.1, 'high': 0.2, 'very_high': 0.3}
        score += complexity_scores.get(business_complexity, 0.1)
        
        # 合规记录
        compliance_record = business_data.get('compliance_record', {})
        if compliance_record.get('violation_count', 0) > 0:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_total_risk_score(self, base_score: float, market_score: float, 
                                  credit_score: float, liquidity_score: float, 
                                  operational_score: float) -> float:
        """计算综合风险分数"""
        weights = {
            'base': 0.25,
            'market': 0.15,
            'credit': 0.30,
            'liquidity': 0.20,
            'operational': 0.10
        }
        
        total_score = (
            base_score * weights['base'] +
            market_score * weights['market'] +
            credit_score * weights['credit'] +
            liquidity_score * weights['liquidity'] +
            operational_score * weights['operational']
        )
        
        return min(total_score, 1.0)
    
    def _determine_risk_level(self, total_score: float) -> str:
        """确定风险等级"""
        if total_score <= 0.2:
            return "低风险"
        elif total_score <= 0.4:
            return "中低风险"
        elif total_score <= 0.6:
            return "中等风险"
        elif total_score <= 0.8:
            return "中高风险"
        else:
            return "高风险"
    
    def _calculate_risk_probability(self, total_score: float, business_data: Dict[str, Any]) -> float:
        """计算风险概率"""
        base_probability = total_score
        
        # 根据企业规模调整
        revenue = business_data.get('revenue', 0)
        if revenue > 1000:
            base_probability *= 0.8
        elif revenue > 500:
            base_probability *= 0.9
        
        # 根据行业调整
        industry = business_data.get('industry', '')
        stable_industries = ['制造业', '服务业', '科技']
        if any(stable_industry in industry for stable_industry in stable_industries):
            base_probability *= 0.9
        
        return min(base_probability, 1.0)
    
    def _generate_risk_report(self, base_score: float, market_score: float, 
                            credit_score: float, liquidity_score: float, 
                            operational_score: float, total_score: float, 
                            risk_level: str, risk_probability: float, 
                            business_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成风险报告"""
        return {
            "summary": f"综合风险等级: {risk_level}",
            "risk_probability": f"{risk_probability:.2%}",
            "key_risks": self._identify_key_risks(base_score, market_score, credit_score, liquidity_score, operational_score),
            "risk_trend": self._analyze_risk_trend(business_data),
            "recommended_actions": self._get_recommended_actions(risk_level),
            "monitoring_frequency": self._get_monitoring_frequency(risk_level)
        }
    
    def _identify_key_risks(self, base_score: float, market_score: float, 
                          credit_score: float, liquidity_score: float, 
                          operational_score: float) -> List[str]:
        """识别关键风险"""
        risks = []
        risk_threshold = 0.6
        
        if base_score > risk_threshold:
            risks.append("基础经营风险较高")
        if market_score > risk_threshold:
            risks.append("市场环境风险较高")
        if credit_score > risk_threshold:
            risks.append("信用风险较高")
        if liquidity_score > risk_threshold:
            risks.append("流动性风险较高")
        if operational_score > risk_threshold:
            risks.append("操作风险较高")
        
        return risks if risks else ["风险水平正常"]
    
    def _analyze_risk_trend(self, business_data: Dict[str, Any]) -> str:
        """分析风险趋势"""
        # 这里可以基于历史数据进行分析
        # 简化实现
        return "风险趋势稳定"
    
    def _get_recommended_actions(self, risk_level: str) -> List[str]:
        """获取推荐行动"""
        actions = {
            "低风险": ["定期监控", "维持现状"],
            "中低风险": ["加强监控", "优化流程"],
            "中等风险": ["密切监控", "制定应对计划", "加强内控"],
            "中高风险": ["重点监控", "制定应急预案", "加强风险管理"],
            "高风险": ["实时监控", "立即制定应对措施", "加强风险管控"]
        }
        return actions.get(risk_level, ["需要进一步评估"])
    
    def _get_monitoring_frequency(self, risk_level: str) -> str:
        """获取监控频率"""
        frequencies = {
            "低风险": "季度监控",
            "中低风险": "月度监控",
            "中等风险": "双周监控",
            "中高风险": "周度监控",
            "高风险": "每日监控"
        }
        return frequencies.get(risk_level, "月度监控")
    
    def _identify_risk_factors(self, business_data: Dict[str, Any], market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """识别风险因素"""
        factors = []
        
        # 财务风险因素
        if business_data.get('debt_ratio', 0) > 0.6:
            factors.append({
                "type": "财务风险",
                "factor": "资产负债率过高",
                "impact": "高",
                "description": "企业负债率超过60%，财务风险较高"
            })
        
        # 市场风险因素
        if market_data.get('gdp_growth', 0) < 3:
            factors.append({
                "type": "市场风险",
                "factor": "经济增长放缓",
                "impact": "中",
                "description": "GDP增长率低于3%，市场环境不利"
            })
        
        # 信用风险因素
        if business_data.get('credit_rating', 'C') in ['C', 'D']:
            factors.append({
                "type": "信用风险",
                "factor": "信用评级较低",
                "impact": "高",
                "description": "企业信用评级为C或D级，信用风险较高"
            })
        
        return factors
    
    def _suggest_mitigation_strategies(self, risk_level: str, business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """建议缓解策略"""
        strategies = []
        
        if risk_level in ["中高风险", "高风险"]:
            strategies.append({
                "strategy": "增加担保",
                "description": "要求企业提供更多担保物或第三方担保",
                "priority": "高"
            })
            
            strategies.append({
                "strategy": "缩短贷款期限",
                "description": "将贷款期限缩短，降低风险敞口",
                "priority": "中"
            })
            
            strategies.append({
                "strategy": "提高利率",
                "description": "适当提高贷款利率，补偿风险",
                "priority": "中"
            })
        
        if business_data.get('liquidity_score', 0) > 0.6:
            strategies.append({
                "strategy": "加强现金流监控",
                "description": "密切监控企业现金流状况",
                "priority": "高"
            })
        
        return strategies
    
    def _generate_recommendations(self, risk_level: str, business_data: Dict[str, Any]) -> List[str]:
        """生成推荐"""
        recommendations = []
        
        if risk_level == "低风险":
            recommendations.append("建议批准贷款申请")
            recommendations.append("可以给予优惠利率")
        elif risk_level == "中低风险":
            recommendations.append("建议批准贷款申请，但需要加强监控")
            recommendations.append("可以考虑给予标准利率")
        elif risk_level == "中等风险":
            recommendations.append("建议谨慎批准，需要额外担保")
            recommendations.append("建议提高利率")
        elif risk_level == "中高风险":
            recommendations.append("建议拒绝或要求大幅增加担保")
            recommendations.append("如果批准，需要严格监控")
        else:  # 高风险
            recommendations.append("建议拒绝贷款申请")
            recommendations.append("建议企业先改善财务状况")
        
        return recommendations
    
    def _calculate_confidence_level(self, business_data: Dict[str, Any]) -> float:
        """计算置信度"""
        # 基于数据完整性和质量计算置信度
        required_fields = ['revenue', 'profit', 'assets', 'liabilities']
        available_fields = sum(1 for field in required_fields if field in business_data and business_data[field] is not None)
        
        completeness = available_fields / len(required_fields)
        
        # 基于数据质量调整
        quality_score = 1.0
        if business_data.get('data_quality', 'unknown') == 'low':
            quality_score = 0.7
        elif business_data.get('data_quality', 'unknown') == 'medium':
            quality_score = 0.85
        
        return completeness * quality_score
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "status": "running",
            "version": "1.0.0",
            "models_loaded": len(self.risk_models),
            "gpu_available": torch.cuda.is_available()
        }