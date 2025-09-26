"""
个性化推荐引擎
基于用户历史和行为提供个性化建议
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import hashlib

class UserProfileType(Enum):
    """用户画像类型"""
    FIRST_TIME = "first_time"
    REGULAR_USER = "regular_user"
    PREMIUM_USER = "premium_user"
    ENTERPRISE_USER = "enterprise_user"

class InterestCategory(Enum):
    """兴趣分类"""
    PERSONAL_LOAN = "personal_loan"
    BUSINESS_LOAN = "business_loan"
    MORTGAGE = "mortgage"
    INVESTMENT = "investment"
    INSURANCE = "insurance"
    CREDIT_CARD = "credit_card"

@dataclass
class UserProfile:
    """用户画像"""
    user_id: str
    profile_type: UserProfileType
    interests: List[InterestCategory]
    risk_tolerance: str  # low, medium, high
    income_range: str    # low, medium, high
    age_group: str       # young, middle, senior
    preferred_banks: List[str]
    interaction_history: List[Dict[str, Any]]
    last_activity: datetime
    preferences: Dict[str, Any]
    behavior_patterns: Dict[str, Any]

@dataclass
class Recommendation:
    """推荐项"""
    id: str
    title: str
    description: str
    category: InterestCategory
    relevance_score: float
    confidence: float
    reason: str
    action_url: str
    metadata: Dict[str, Any]

class PersonalizationEngine:
    """个性化推荐引擎"""
    
    def __init__(self):
        self.user_profiles: Dict[str, UserProfile] = {}
        self.recommendation_templates = self._initialize_recommendation_templates()
    
    def _initialize_recommendation_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """初始化推荐模板"""
        return {
            InterestCategory.PERSONAL_LOAN.value: [
                {
                    "title": "个人信用贷款推荐",
                    "description": "根据您的收入情况，推荐适合的个人信用贷款产品",
                    "reason": "基于您的收入水平和信用状况",
                    "action_url": "/loan-application?type=personal"
                },
                {
                    "title": "低利率贷款产品",
                    "description": "为您精选当前利率最低的贷款产品",
                    "reason": "您关注利率优惠",
                    "action_url": "/products?filter=low-rate"
                }
            ],
            InterestCategory.BUSINESS_LOAN.value: [
                {
                    "title": "企业经营贷款",
                    "description": "适合企业发展的经营贷款产品推荐",
                    "reason": "您有企业经营需求",
                    "action_url": "/loan-application?type=business"
                }
            ],
            InterestCategory.MORTGAGE.value: [
                {
                    "title": "房贷产品推荐",
                    "description": "首套房、二套房等房贷产品对比",
                    "reason": "您关注房产投资",
                    "action_url": "/products?category=mortgage"
                }
            ]
        }
    
    def create_user_profile(self, user_id: str, initial_data: Dict[str, Any] = None) -> UserProfile:
        """创建用户画像"""
        profile = UserProfile(
            user_id=user_id,
            profile_type=UserProfileType.FIRST_TIME,
            interests=[],
            risk_tolerance="medium",
            income_range="medium",
            age_group="middle",
            preferred_banks=[],
            interaction_history=[],
            last_activity=datetime.now(),
            preferences={},
            behavior_patterns={}
        )
        
        if initial_data:
            profile = self._update_profile_from_data(profile, initial_data)
        
        self.user_profiles[user_id] = profile
        logger.info(f"创建用户画像: {user_id}")
        return profile
    
    def _update_profile_from_data(self, profile: UserProfile, data: Dict[str, Any]) -> UserProfile:
        """从数据更新用户画像"""
        if "income" in data:
            income = data["income"]
            if income < 50000:
                profile.income_range = "low"
            elif income > 200000:
                profile.income_range = "high"
            else:
                profile.income_range = "medium"
        
        if "age" in data:
            age = data["age"]
            if age < 30:
                profile.age_group = "young"
            elif age > 50:
                profile.age_group = "senior"
            else:
                profile.age_group = "middle"
        
        if "risk_tolerance" in data:
            profile.risk_tolerance = data["risk_tolerance"]
        
        return profile
    
    def update_user_interaction(self, user_id: str, interaction: Dict[str, Any]) -> None:
        """更新用户交互记录"""
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        
        # 添加交互记录
        interaction["timestamp"] = datetime.now().isoformat()
        profile.interaction_history.append(interaction)
        
        # 保持历史记录在合理范围内
        if len(profile.interaction_history) > 100:
            profile.interaction_history = profile.interaction_history[-100:]
        
        # 更新最后活动时间
        profile.last_activity = datetime.now()
        
        # 分析行为模式
        self._analyze_behavior_patterns(profile)
        
        # 更新兴趣偏好
        self._update_interests(profile, interaction)
    
    def _analyze_behavior_patterns(self, profile: UserProfile) -> None:
        """分析用户行为模式"""
        recent_interactions = profile.interaction_history[-20:]  # 最近20次交互
        
        # 分析访问时间模式
        visit_times = [datetime.fromisoformat(i["timestamp"]) for i in recent_interactions if "timestamp" in i]
        if visit_times:
            hour_counts = {}
            for visit_time in visit_times:
                hour = visit_time.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            
            most_active_hour = max(hour_counts.items(), key=lambda x: x[1])[0]
            profile.behavior_patterns["most_active_hour"] = most_active_hour
        
        # 分析查询类型模式
        query_types = [i.get("query_type", "unknown") for i in recent_interactions]
        type_counts = {}
        for query_type in query_types:
            type_counts[query_type] = type_counts.get(query_type, 0) + 1
        
        if type_counts:
            most_common_type = max(type_counts.items(), key=lambda x: x[1])[0]
            profile.behavior_patterns["most_common_query_type"] = most_common_type
    
    def _update_interests(self, profile: UserProfile, interaction: Dict[str, Any]) -> None:
        """更新用户兴趣"""
        query = interaction.get("query", "").lower()
        query_type = interaction.get("query_type", "")
        
        # 基于查询内容推断兴趣
        interest_keywords = {
            InterestCategory.PERSONAL_LOAN: ["个人贷款", "信用贷款", "消费贷款"],
            InterestCategory.BUSINESS_LOAN: ["经营贷款", "企业贷款", "商业贷款"],
            InterestCategory.MORTGAGE: ["房贷", "房屋贷款", "按揭"],
            InterestCategory.INVESTMENT: ["投资", "理财", "基金"],
            InterestCategory.INSURANCE: ["保险", "保障"],
            InterestCategory.CREDIT_CARD: ["信用卡", "贷记卡"]
        }
        
        for category, keywords in interest_keywords.items():
            if any(keyword in query for keyword in keywords):
                if category not in profile.interests:
                    profile.interests.append(category)
        
        # 基于查询类型推断兴趣
        if query_type == "loan_inquiry":
            if InterestCategory.PERSONAL_LOAN not in profile.interests:
                profile.interests.append(InterestCategory.PERSONAL_LOAN)
    
    def generate_personalized_recommendations(self, user_id: str, max_recommendations: int = 5) -> List[Recommendation]:
        """生成个性化推荐"""
        if user_id not in self.user_profiles:
            return []
        
        profile = self.user_profiles[user_id]
        recommendations = []
        
        # 基于兴趣生成推荐
        for interest in profile.interests:
            if interest.value in self.recommendation_templates:
                templates = self.recommendation_templates[interest.value]
                for template in templates[:2]:  # 每个兴趣最多2个推荐
                    recommendation = self._create_recommendation(template, profile, interest)
                    recommendations.append(recommendation)
        
        # 基于行为模式生成推荐
        behavior_recommendations = self._generate_behavior_based_recommendations(profile)
        recommendations.extend(behavior_recommendations)
        
        # 基于用户画像类型生成推荐
        profile_recommendations = self._generate_profile_based_recommendations(profile)
        recommendations.extend(profile_recommendations)
        
        # 按相关性排序并去重
        recommendations = self._deduplicate_and_rank(recommendations)
        
        return recommendations[:max_recommendations]
    
    def _create_recommendation(self, template: Dict[str, Any], profile: UserProfile, 
                             category: InterestCategory) -> Recommendation:
        """创建推荐项"""
        recommendation_id = hashlib.md5(f"{profile.user_id}_{template['title']}".encode()).hexdigest()[:8]
        
        # 计算相关性得分
        relevance_score = self._calculate_recommendation_relevance(template, profile, category)
        
        return Recommendation(
            id=recommendation_id,
            title=template["title"],
            description=template["description"],
            category=category,
            relevance_score=relevance_score,
            confidence=0.8,
            reason=template["reason"],
            action_url=template["action_url"],
            metadata={
                "user_profile_type": profile.profile_type.value,
                "income_range": profile.income_range,
                "age_group": profile.age_group
            }
        )
    
    def _calculate_recommendation_relevance(self, template: Dict[str, Any], 
                                          profile: UserProfile, category: InterestCategory) -> float:
        """计算推荐相关性得分"""
        score = 0.5  # 基础得分
        
        # 基于兴趣匹配
        if category in profile.interests:
            score += 0.3
        
        # 基于收入匹配
        if "低利率" in template["title"] and profile.income_range == "low":
            score += 0.2
        elif "高端" in template["title"] and profile.income_range == "high":
            score += 0.2
        
        # 基于年龄匹配
        if "年轻" in template["description"] and profile.age_group == "young":
            score += 0.1
        elif "成熟" in template["description"] and profile.age_group == "senior":
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_behavior_based_recommendations(self, profile: UserProfile) -> List[Recommendation]:
        """基于行为模式生成推荐"""
        recommendations = []
        
        # 基于最活跃时间推荐
        if "most_active_hour" in profile.behavior_patterns:
            hour = profile.behavior_patterns["most_active_hour"]
            if 9 <= hour <= 17:  # 工作时间
                recommendations.append(Recommendation(
                    id=f"work_time_{profile.user_id}",
                    title="工作时间专属服务",
                    description="工作时间享受专属客服和快速审批服务",
                    category=InterestCategory.PERSONAL_LOAN,
                    relevance_score=0.7,
                    confidence=0.8,
                    reason="您经常在工作时间咨询",
                    action_url="/vip-service",
                    metadata={"time_based": True}
                ))
        
        return recommendations
    
    def _generate_profile_based_recommendations(self, profile: UserProfile) -> List[Recommendation]:
        """基于用户画像类型生成推荐"""
        recommendations = []
        
        if profile.profile_type == UserProfileType.FIRST_TIME:
            recommendations.append(Recommendation(
                id=f"new_user_{profile.user_id}",
                title="新用户专享优惠",
                description="首次申请享受利率优惠和快速审批",
                category=InterestCategory.PERSONAL_LOAN,
                relevance_score=0.9,
                confidence=0.9,
                reason="您是新用户",
                action_url="/new-user-offer",
                metadata={"new_user": True}
            ))
        
        elif profile.profile_type == UserProfileType.PREMIUM_USER:
            recommendations.append(Recommendation(
                id=f"premium_{profile.user_id}",
                title="VIP专属产品",
                description="专为VIP用户设计的高端金融产品",
                category=InterestCategory.INVESTMENT,
                relevance_score=0.8,
                confidence=0.9,
                reason="您是VIP用户",
                action_url="/vip-products",
                metadata={"premium": True}
            ))
        
        return recommendations
    
    def _deduplicate_and_rank(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """去重并排序推荐"""
        # 去重
        seen_titles = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec.title not in seen_titles:
                seen_titles.add(rec.title)
                unique_recommendations.append(rec)
        
        # 按相关性排序
        unique_recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return unique_recommendations
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """获取用户画像"""
        return self.user_profiles.get(user_id)
    
    def get_recommendation_analytics(self) -> Dict[str, Any]:
        """获取推荐分析数据"""
        total_users = len(self.user_profiles)
        total_interactions = sum(len(profile.interaction_history) for profile in self.user_profiles.values())
        
        interest_distribution = {}
        for profile in self.user_profiles.values():
            for interest in profile.interests:
                interest_distribution[interest.value] = interest_distribution.get(interest.value, 0) + 1
        
        return {
            "total_users": total_users,
            "total_interactions": total_interactions,
            "average_interactions_per_user": total_interactions / total_users if total_users > 0 else 0,
            "interest_distribution": interest_distribution,
            "profile_type_distribution": {
                profile_type.value: sum(1 for p in self.user_profiles.values() if p.profile_type == profile_type)
                for profile_type in UserProfileType
            }
        }
