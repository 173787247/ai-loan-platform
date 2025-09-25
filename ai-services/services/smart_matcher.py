"""
智能匹配服务

@author AI Loan Platform Team
@version 1.0.0
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from loguru import logger
import torch
import torch.nn as nn
from datetime import datetime
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class SmartMatcher:
    """智能匹配服务类"""
    
    def __init__(self):
        self.logger = logger
        self.matching_model = self._create_matching_model()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.product_database = self._load_product_database()
        
    def _create_matching_model(self) -> nn.Module:
        """创建匹配模型"""
        class MatchingModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(20, 128)
                self.fc2 = nn.Linear(128, 64)
                self.fc3 = nn.Linear(64, 32)
                self.fc4 = nn.Linear(32, 1)
                self.dropout = nn.Dropout(0.3)
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
        
        return MatchingModel()
    
    def _load_product_database(self) -> List[Dict[str, Any]]:
        """加载产品数据库"""
        return [
            {
                "id": 1,
                "name": "小微企业流动资金贷款",
                "type": "流动资金贷款",
                "min_amount": 10,
                "max_amount": 500,
                "min_term": 6,
                "max_term": 36,
                "interest_rate_min": 0.045,
                "interest_rate_max": 0.08,
                "requirements": ["营业执照", "财务报表", "银行流水"],
                "target_customers": ["小微企业", "个体工商户"],
                "features": ["快速审批", "灵活还款", "低门槛"],
                "risk_level": "中低"
            },
            {
                "id": 2,
                "name": "企业经营性贷款",
                "type": "经营性贷款",
                "min_amount": 50,
                "max_amount": 2000,
                "min_term": 12,
                "max_term": 60,
                "interest_rate_min": 0.04,
                "interest_rate_max": 0.07,
                "requirements": ["营业执照", "财务报表", "银行流水", "担保"],
                "target_customers": ["中小企业", "制造业"],
                "features": ["长期限", "大额度", "优惠利率"],
                "risk_level": "中等"
            },
            {
                "id": 3,
                "name": "设备购置贷款",
                "type": "设备贷款",
                "min_amount": 100,
                "max_amount": 5000,
                "min_term": 24,
                "max_term": 84,
                "interest_rate_min": 0.035,
                "interest_rate_max": 0.065,
                "requirements": ["营业执照", "设备采购合同", "财务报表"],
                "target_customers": ["制造业", "加工业"],
                "features": ["专项用途", "长期限", "设备抵押"],
                "risk_level": "中低"
            },
            {
                "id": 4,
                "name": "供应链金融贷款",
                "type": "供应链贷款",
                "min_amount": 20,
                "max_amount": 1000,
                "min_term": 3,
                "max_term": 12,
                "interest_rate_min": 0.05,
                "interest_rate_max": 0.09,
                "requirements": ["贸易合同", "发票", "银行流水"],
                "target_customers": ["贸易企业", "供应链企业"],
                "features": ["快速放款", "随借随还", "线上操作"],
                "risk_level": "中低"
            },
            {
                "id": 5,
                "name": "信用贷款",
                "type": "信用贷款",
                "min_amount": 5,
                "max_amount": 100,
                "min_term": 6,
                "max_term": 24,
                "interest_rate_min": 0.08,
                "interest_rate_max": 0.15,
                "requirements": ["身份证", "银行流水", "征信报告"],
                "target_customers": ["个人", "小微企业"],
                "features": ["无担保", "快速审批", "线上申请"],
                "risk_level": "中高"
            }
        ]
    
    def match_proposals(self, tender_id: int, user_requirements: Dict[str, Any], 
                       available_products: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """匹配贷款方案"""
        try:
            self.logger.info(f"开始智能匹配: 招标ID {tender_id}")
            
            if available_products is None:
                available_products = self.product_database
            
            # 提取用户需求特征
            user_features = self._extract_user_features(user_requirements)
            
            # 计算匹配分数
            matching_scores = self._calculate_matching_scores(user_features, available_products)
            
            # 排序和筛选
            ranked_products = self._rank_products(available_products, matching_scores)
            
            # 生成推荐理由
            recommendations = self._generate_recommendations(ranked_products, user_requirements)
            
            # 计算匹配度分析
            matching_analysis = self._analyze_matching_quality(user_features, ranked_products)
            
            result = {
                "tender_id": tender_id,
                "matching_time": datetime.now().isoformat(),
                "total_products": len(available_products),
                "matched_products": len(ranked_products),
                "recommendations": recommendations,
                "matching_analysis": matching_analysis,
                "user_profile": self._create_user_profile(user_requirements),
                "next_steps": self._suggest_next_steps(ranked_products)
            }
            
            self.logger.info(f"智能匹配完成: 招标ID {tender_id}, 匹配产品数: {len(ranked_products)}")
            return result
            
        except Exception as e:
            self.logger.error(f"智能匹配失败: 招标ID {tender_id}, 错误: {str(e)}")
            raise
    
    def _extract_user_features(self, user_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """提取用户需求特征"""
        features = {
            "loan_amount": user_requirements.get('loan_amount', 0),
            "loan_term": user_requirements.get('loan_term', 12),
            "company_type": user_requirements.get('company_type', ''),
            "industry": user_requirements.get('industry', ''),
            "revenue": user_requirements.get('revenue', 0),
            "profit": user_requirements.get('profit', 0),
            "assets": user_requirements.get('assets', 0),
            "liabilities": user_requirements.get('liabilities', 0),
            "credit_rating": user_requirements.get('credit_rating', 'C'),
            "has_collateral": user_requirements.get('has_collateral', False),
            "collateral_value": user_requirements.get('collateral_value', 0),
            "urgency": user_requirements.get('urgency', 'normal'),
            "preferred_rate": user_requirements.get('preferred_rate', 0.08),
            "repayment_capability": user_requirements.get('repayment_capability', 'medium'),
            "business_experience": user_requirements.get('business_experience', 0),
            "employee_count": user_requirements.get('employee_count', 0),
            "loan_purpose": user_requirements.get('loan_purpose', ''),
            "special_requirements": user_requirements.get('special_requirements', []),
            "risk_tolerance": user_requirements.get('risk_tolerance', 'medium'),
            "preferred_features": user_requirements.get('preferred_features', [])
        }
        
        return features
    
    def _calculate_matching_scores(self, user_features: Dict[str, Any], 
                                 available_products: List[Dict[str, Any]]) -> List[float]:
        """计算匹配分数"""
        scores = []
        
        for product in available_products:
            score = 0.0
            
            # 金额匹配度 (30%)
            amount_score = self._calculate_amount_match(user_features['loan_amount'], product)
            score += amount_score * 0.3
            
            # 期限匹配度 (20%)
            term_score = self._calculate_term_match(user_features['loan_term'], product)
            score += term_score * 0.2
            
            # 利率匹配度 (15%)
            rate_score = self._calculate_rate_match(user_features['preferred_rate'], product)
            score += rate_score * 0.15
            
            # 客户类型匹配度 (15%)
            customer_score = self._calculate_customer_match(user_features, product)
            score += customer_score * 0.15
            
            # 担保要求匹配度 (10%)
            collateral_score = self._calculate_collateral_match(user_features, product)
            score += collateral_score * 0.1
            
            # 特殊需求匹配度 (10%)
            special_score = self._calculate_special_match(user_features, product)
            score += special_score * 0.1
            
            scores.append(min(score, 1.0))
        
        return scores
    
    def _calculate_amount_match(self, user_amount: float, product: Dict[str, Any]) -> float:
        """计算金额匹配度"""
        min_amount = product.get('min_amount', 0)
        max_amount = product.get('max_amount', float('inf'))
        
        if min_amount <= user_amount <= max_amount:
            return 1.0
        elif user_amount < min_amount:
            # 用户需求小于最小金额，计算接近度
            return max(0, 1 - (min_amount - user_amount) / min_amount)
        else:
            # 用户需求大于最大金额，计算接近度
            return max(0, 1 - (user_amount - max_amount) / max_amount)
    
    def _calculate_term_match(self, user_term: int, product: Dict[str, Any]) -> float:
        """计算期限匹配度"""
        min_term = product.get('min_term', 0)
        max_term = product.get('max_term', float('inf'))
        
        if min_term <= user_term <= max_term:
            return 1.0
        elif user_term < min_term:
            return max(0, 1 - (min_term - user_term) / min_term)
        else:
            return max(0, 1 - (user_term - max_term) / max_term)
    
    def _calculate_rate_match(self, user_rate: float, product: Dict[str, Any]) -> float:
        """计算利率匹配度"""
        min_rate = product.get('interest_rate_min', 0)
        max_rate = product.get('interest_rate_max', 1)
        
        if min_rate <= user_rate <= max_rate:
            return 1.0
        else:
            # 计算与产品利率范围的接近度
            if user_rate < min_rate:
                return max(0, 1 - (min_rate - user_rate) / min_rate)
            else:
                return max(0, 1 - (user_rate - max_rate) / max_rate)
    
    def _calculate_customer_match(self, user_features: Dict[str, Any], product: Dict[str, Any]) -> float:
        """计算客户类型匹配度"""
        target_customers = product.get('target_customers', [])
        company_type = user_features.get('company_type', '')
        industry = user_features.get('industry', '')
        
        score = 0.0
        
        # 检查公司类型匹配
        for target in target_customers:
            if target in company_type or company_type in target:
                score += 0.5
                break
        
        # 检查行业匹配
        if industry and any(industry in target for target in target_customers):
            score += 0.5
        
        return min(score, 1.0)
    
    def _calculate_collateral_match(self, user_features: Dict[str, Any], product: Dict[str, Any]) -> float:
        """计算担保要求匹配度"""
        has_collateral = user_features.get('has_collateral', False)
        requirements = product.get('requirements', [])
        
        # 检查是否需要担保
        needs_collateral = '担保' in ' '.join(requirements) or '抵押' in ' '.join(requirements)
        
        if needs_collateral and has_collateral:
            return 1.0
        elif not needs_collateral:
            return 1.0
        else:
            return 0.3  # 需要担保但没有提供
    
    def _calculate_special_match(self, user_features: Dict[str, Any], product: Dict[str, Any]) -> float:
        """计算特殊需求匹配度"""
        special_requirements = user_features.get('special_requirements', [])
        preferred_features = user_features.get('preferred_features', [])
        product_features = product.get('features', [])
        
        score = 0.0
        total_checks = len(special_requirements) + len(preferred_features)
        
        if total_checks == 0:
            return 1.0
        
        # 检查特殊需求匹配
        for req in special_requirements:
            if any(req.lower() in feature.lower() for feature in product_features):
                score += 1.0
        
        # 检查偏好特征匹配
        for pref in preferred_features:
            if any(pref.lower() in feature.lower() for feature in product_features):
                score += 1.0
        
        return min(score / total_checks, 1.0)
    
    def _rank_products(self, products: List[Dict[str, Any]], scores: List[float]) -> List[Dict[str, Any]]:
        """排序产品"""
        # 创建产品-分数对
        product_scores = list(zip(products, scores))
        
        # 按分数降序排序
        product_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 只返回分数大于0.3的产品
        ranked_products = []
        for product, score in product_scores:
            if score > 0.3:
                product_copy = product.copy()
                product_copy['matching_score'] = score
                product_copy['matching_percentage'] = f"{score:.1%}"
                ranked_products.append(product_copy)
        
        return ranked_products[:10]  # 返回前10个匹配产品
    
    def _generate_recommendations(self, ranked_products: List[Dict[str, Any]], 
                                user_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成推荐理由"""
        recommendations = []
        
        for i, product in enumerate(ranked_products[:5]):  # 只处理前5个产品
            reasons = []
            
            # 基于匹配分数生成理由
            score = product.get('matching_score', 0)
            if score > 0.8:
                reasons.append("高度匹配您的需求")
            elif score > 0.6:
                reasons.append("较好匹配您的需求")
            else:
                reasons.append("基本匹配您的需求")
            
            # 基于具体特征生成理由
            user_amount = user_requirements.get('loan_amount', 0)
            product_min = product.get('min_amount', 0)
            product_max = product.get('max_amount', float('inf'))
            
            if product_min <= user_amount <= product_max:
                reasons.append(f"贷款金额{user_amount}万在{product_min}-{product_max}万范围内")
            
            user_term = user_requirements.get('loan_term', 0)
            product_min_term = product.get('min_term', 0)
            product_max_term = product.get('max_term', float('inf'))
            
            if product_min_term <= user_term <= product_max_term:
                reasons.append(f"贷款期限{user_term}个月在{product_min_term}-{product_max_term}个月范围内")
            
            # 基于产品特色生成理由
            features = product.get('features', [])
            if features:
                reasons.append(f"产品特色: {', '.join(features[:2])}")
            
            recommendations.append({
                "rank": i + 1,
                "product_id": product.get('id'),
                "product_name": product.get('name'),
                "matching_score": score,
                "reasons": reasons,
                "estimated_rate": f"{product.get('interest_rate_min', 0):.1%}-{product.get('interest_rate_max', 0):.1%}",
                "risk_level": product.get('risk_level', '未知')
            })
        
        return recommendations
    
    def _analyze_matching_quality(self, user_features: Dict[str, Any], 
                                ranked_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析匹配质量"""
        if not ranked_products:
            return {
                "quality": "差",
                "message": "没有找到合适的贷款产品",
                "suggestions": ["调整贷款金额或期限", "考虑提供担保", "联系客服咨询"]
            }
        
        avg_score = sum(p.get('matching_score', 0) for p in ranked_products) / len(ranked_products)
        max_score = max(p.get('matching_score', 0) for p in ranked_products)
        
        if max_score > 0.8:
            quality = "优秀"
            message = "找到了多个高度匹配的贷款产品"
        elif max_score > 0.6:
            quality = "良好"
            message = "找到了合适的贷款产品"
        elif max_score > 0.4:
            quality = "一般"
            message = "找到了一些基本匹配的贷款产品"
        else:
            quality = "较差"
            message = "匹配的贷款产品较少"
        
        return {
            "quality": quality,
            "message": message,
            "average_score": f"{avg_score:.1%}",
            "best_score": f"{max_score:.1%}",
            "total_matches": len(ranked_products)
        }
    
    def _create_user_profile(self, user_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户画像"""
        return {
            "risk_profile": self._assess_risk_profile(user_requirements),
            "preference_profile": self._assess_preference_profile(user_requirements),
            "financial_profile": self._assess_financial_profile(user_requirements),
            "business_profile": self._assess_business_profile(user_requirements)
        }
    
    def _assess_risk_profile(self, user_requirements: Dict[str, Any]) -> str:
        """评估风险画像"""
        revenue = user_requirements.get('revenue', 0)
        profit = user_requirements.get('profit', 0)
        credit_rating = user_requirements.get('credit_rating', 'C')
        has_collateral = user_requirements.get('has_collateral', False)
        
        if credit_rating in ['AAA', 'AA', 'A'] and revenue > 500 and profit > 0 and has_collateral:
            return "低风险客户"
        elif credit_rating in ['BBB', 'BB'] and revenue > 100 and profit >= 0:
            return "中低风险客户"
        elif credit_rating in ['B', 'C'] and revenue > 50:
            return "中等风险客户"
        else:
            return "中高风险客户"
    
    def _assess_preference_profile(self, user_requirements: Dict[str, Any]) -> str:
        """评估偏好画像"""
        urgency = user_requirements.get('urgency', 'normal')
        preferred_features = user_requirements.get('preferred_features', [])
        
        if urgency == 'high' and '快速审批' in preferred_features:
            return "效率优先型"
        elif '优惠利率' in preferred_features:
            return "成本敏感型"
        elif '灵活还款' in preferred_features:
            return "灵活性优先型"
        else:
            return "平衡型"
    
    def _assess_financial_profile(self, user_requirements: Dict[str, Any]) -> str:
        """评估财务画像"""
        revenue = user_requirements.get('revenue', 0)
        loan_amount = user_requirements.get('loan_amount', 0)
        
        if revenue > 1000:
            return "大型企业"
        elif revenue > 500:
            return "中型企业"
        elif revenue > 100:
            return "小型企业"
        else:
            return "微型企业"
    
    def _assess_business_profile(self, user_requirements: Dict[str, Any]) -> str:
        """评估业务画像"""
        industry = user_requirements.get('industry', '')
        business_experience = user_requirements.get('business_experience', 0)
        
        if business_experience > 10:
            return "成熟企业"
        elif business_experience > 5:
            return "成长企业"
        elif business_experience > 2:
            return "初创企业"
        else:
            return "新创企业"
    
    def _suggest_next_steps(self, ranked_products: List[Dict[str, Any]]) -> List[str]:
        """建议下一步行动"""
        steps = []
        
        if ranked_products:
            steps.append("查看详细产品信息")
            steps.append("比较不同产品的优缺点")
            steps.append("准备申请材料")
            steps.append("联系银行或金融机构")
        else:
            steps.append("调整贷款需求")
            steps.append("咨询专业顾问")
            steps.append("考虑其他融资方式")
        
        return steps
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "status": "running",
            "version": "1.0.0",
            "products_loaded": len(self.product_database),
            "model_loaded": self.matching_model is not None
        }