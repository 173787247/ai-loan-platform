"""
推荐引擎服务

@author AI Loan Platform Team
@version 1.0.0
"""

import numpy as np
from typing import Dict, Any, List
from loguru import logger
from datetime import datetime
from collections import defaultdict

class RecommendationEngine:
    """推荐引擎服务类"""
    
    def __init__(self):
        self.logger = logger
        self.user_behavior_data = defaultdict(list)
        self.product_features = self._load_product_features()
        self.user_profiles = {}
        
    def _load_product_features(self) -> Dict[int, Dict[str, Any]]:
        """加载产品特征"""
        return {
            1: {
                "category": "流动资金贷款",
                "amount_range": (10, 500),
                "term_range": (6, 36),
                "rate_range": (0.045, 0.08),
                "risk_level": "中低",
                "target_industry": ["制造业", "服务业", "贸易"],
                "features": ["快速审批", "灵活还款", "低门槛"],
                "popularity_score": 0.8
            },
            2: {
                "category": "经营性贷款",
                "amount_range": (50, 2000),
                "term_range": (12, 60),
                "rate_range": (0.04, 0.07),
                "risk_level": "中等",
                "target_industry": ["制造业", "建筑业", "科技"],
                "features": ["长期限", "大额度", "优惠利率"],
                "popularity_score": 0.7
            },
            3: {
                "category": "设备贷款",
                "amount_range": (100, 5000),
                "term_range": (24, 84),
                "rate_range": (0.035, 0.065),
                "risk_level": "中低",
                "target_industry": ["制造业", "加工业", "农业"],
                "features": ["专项用途", "长期限", "设备抵押"],
                "popularity_score": 0.6
            },
            4: {
                "category": "供应链贷款",
                "amount_range": (20, 1000),
                "term_range": (3, 12),
                "rate_range": (0.05, 0.09),
                "risk_level": "中低",
                "target_industry": ["贸易", "物流", "零售"],
                "features": ["快速放款", "随借随还", "线上操作"],
                "popularity_score": 0.75
            },
            5: {
                "category": "信用贷款",
                "amount_range": (5, 100),
                "term_range": (6, 24),
                "rate_range": (0.08, 0.15),
                "risk_level": "中高",
                "target_industry": ["服务业", "科技", "文化"],
                "features": ["无担保", "快速审批", "线上申请"],
                "popularity_score": 0.9
            }
        }
    
    def recommend_solutions(self, user_id: int, tender_id: int, 
                          user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """推荐解决方案"""
        try:
            self.logger.info(f"开始推荐解决方案: 用户ID {user_id}, 招标ID {tender_id}")
            
            # 更新用户画像
            self._update_user_profile(user_id, user_preferences)
            
            # 计算推荐分数
            recommendations = self._calculate_recommendations(user_id, user_preferences)
            
            # 生成个性化推荐
            personalized_recommendations = self._generate_personalized_recommendations(
                user_id, recommendations, user_preferences
            )
            
            result = {
                "user_id": user_id,
                "tender_id": tender_id,
                "recommendation_time": datetime.now().isoformat(),
                "personalized_recommendations": personalized_recommendations,
                "user_profile": self.user_profiles.get(user_id, {}),
                "confidence_score": 0.85
            }
            
            self.logger.info(f"推荐解决方案完成: 用户ID {user_id}, 推荐数量: {len(personalized_recommendations)}")
            return result
            
        except Exception as e:
            self.logger.error(f"推荐解决方案失败: 用户ID {user_id}, 错误: {str(e)}")
            raise
    
    def _update_user_profile(self, user_id: int, user_preferences: Dict[str, Any]):
        """更新用户画像"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "preferences": {},
                "risk_profile": "medium",
                "interaction_count": 0
            }
        
        profile = self.user_profiles[user_id]
        profile["preferences"].update(user_preferences)
        profile["interaction_count"] += 1
    
    def _calculate_recommendations(self, user_id: int, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """计算推荐分数"""
        recommendations = []
        
        for product_id, features in self.product_features.items():
            # 基础匹配分数
            base_score = self._calculate_base_match_score(user_preferences, features)
            
            # 流行度分数
            popularity_score = features.get("popularity_score", 0.5)
            
            # 综合分数
            total_score = base_score * 0.8 + popularity_score * 0.2
            
            recommendations.append({
                "product_id": product_id,
                "base_score": base_score,
                "popularity_score": popularity_score,
                "total_score": total_score,
                "features": features
            })
        
        # 按总分排序
        recommendations.sort(key=lambda x: x["total_score"], reverse=True)
        return recommendations
    
    def _calculate_base_match_score(self, user_preferences: Dict[str, Any], 
                                  product_features: Dict[str, Any]) -> float:
        """计算基础匹配分数"""
        score = 0.0
        
        # 金额匹配
        user_amount = user_preferences.get("loan_amount", 0)
        amount_range = product_features.get("amount_range", (0, 0))
        if amount_range[0] <= user_amount <= amount_range[1]:
            score += 0.3
        else:
            if user_amount < amount_range[0]:
                score += 0.3 * max(0, 1 - (amount_range[0] - user_amount) / amount_range[0])
            else:
                score += 0.3 * max(0, 1 - (user_amount - amount_range[1]) / amount_range[1])
        
        # 期限匹配
        user_term = user_preferences.get("loan_term", 12)
        term_range = product_features.get("term_range", (0, 0))
        if term_range[0] <= user_term <= term_range[1]:
            score += 0.2
        else:
            if user_term < term_range[0]:
                score += 0.2 * max(0, 1 - (term_range[0] - user_term) / term_range[0])
            else:
                score += 0.2 * max(0, 1 - (user_term - term_range[1]) / term_range[1])
        
        # 利率匹配
        user_rate = user_preferences.get("preferred_rate", 0.08)
        rate_range = product_features.get("rate_range", (0, 1))
        if rate_range[0] <= user_rate <= rate_range[1]:
            score += 0.2
        else:
            if user_rate < rate_range[0]:
                score += 0.2 * max(0, 1 - (rate_range[0] - user_rate) / rate_range[0])
            else:
                score += 0.2 * max(0, 1 - (user_rate - rate_range[1]) / rate_range[1])
        
        # 行业匹配
        user_industry = user_preferences.get("industry", "")
        target_industries = product_features.get("target_industry", [])
        if user_industry and any(user_industry in industry for industry in target_industries):
            score += 0.2
        
        # 风险偏好匹配
        user_risk_tolerance = user_preferences.get("risk_tolerance", "medium")
        product_risk_level = product_features.get("risk_level", "medium")
        risk_mapping = {"low": "中低", "medium": "中等", "high": "中高"}
        if risk_mapping.get(user_risk_tolerance) == product_risk_level:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_personalized_recommendations(self, user_id: int, 
                                             recommendations: List[Dict[str, Any]], 
                                             user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成个性化推荐"""
        personalized = []
        
        for i, rec in enumerate(recommendations[:5]):  # 只取前5个
            product_id = rec["product_id"]
            features = rec["features"]
            
            personalized.append({
                "rank": i + 1,
                "product_id": product_id,
                "product_name": self._get_product_name(product_id),
                "category": features.get("category", ""),
                "total_score": rec["total_score"],
                "personalized_score": rec["total_score"],
                "personalized_description": f"推荐{features.get('category', '')}产品，匹配度{rec['total_score']:.1%}",
                "key_benefits": features.get("features", [])[:3],
                "estimated_approval_rate": "85%",
                "estimated_processing_time": "3-5个工作日"
            })
        
        return personalized
    
    def _get_product_name(self, product_id: int) -> str:
        """获取产品名称"""
        names = {
            1: "小微企业流动资金贷款",
            2: "企业经营性贷款",
            3: "设备购置贷款",
            4: "供应链金融贷款",
            5: "信用贷款"
        }
        return names.get(product_id, f"产品{product_id}")
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "status": "running",
            "version": "1.0.0",
            "users_profiled": len(self.user_profiles),
            "products_loaded": len(self.product_features)
        }
