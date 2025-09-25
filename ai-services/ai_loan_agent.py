"""
AI助贷招标智能体
整合所有AI功能，提供统一的智能体接口

@author AI Loan Platform Team
@version 1.1.0
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import requests
from loguru import logger

class AgentState(Enum):
    """智能体状态"""
    IDLE = "idle"                    # 空闲
    PROCESSING = "processing"         # 处理中
    WAITING_INPUT = "waiting_input"   # 等待输入
    COMPLETED = "completed"           # 完成
    ERROR = "error"                   # 错误

class LoanPurpose(Enum):
    """贷款用途"""
    WORKING_CAPITAL = "working_capital"      # 流动资金
    EQUIPMENT_PURCHASE = "equipment"         # 设备采购
    EXPANSION = "expansion"                  # 业务扩张
    DEBT_REFINANCING = "debt_refinancing"    # 债务重组
    EMERGENCY = "emergency"                  # 应急资金

@dataclass
class UserProfile:
    """用户画像"""
    user_id: int
    company_name: str
    industry: str
    company_size: str
    business_age: int
    annual_revenue: float
    monthly_income: float
    credit_score: int
    management_experience: int
    risk_tolerance: str
    preferred_loan_amount: float
    preferred_term: int
    preferred_rate: float

@dataclass
class LoanApplication:
    """贷款申请"""
    application_id: str
    user_profile: UserProfile
    loan_amount: float
    loan_purpose: LoanPurpose
    loan_term: int
    urgency_level: str
    collateral_available: bool
    guarantor_available: bool
    documents_ready: bool

@dataclass
class AgentResponse:
    """智能体响应"""
    success: bool
    message: str
    data: Dict[str, Any]
    next_action: str
    confidence: float
    timestamp: str

class AILoanAgent:
    """AI助贷招标智能体"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.state = AgentState.IDLE
        self.session = requests.Session()
        self.conversation_history = []
        self.current_application = None
        self.user_profile = None
        
        # 初始化AI服务
        self.document_processor = None
        self.risk_assessor = None
        self.smart_matcher = None
        self.recommendation_engine = None
        
        logger.info("AI助贷招标智能体初始化完成")
    
    async def initialize_services(self):
        """初始化AI服务"""
        try:
            # 检查AI服务健康状态
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                logger.info("AI服务连接成功")
                return True
            else:
                logger.error(f"AI服务连接失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"AI服务初始化失败: {str(e)}")
            return False
    
    def start_conversation(self, user_id: int) -> AgentResponse:
        """开始对话"""
        self.state = AgentState.PROCESSING
        self.user_profile = None
        self.current_application = None
        
        welcome_message = """
🤖 欢迎使用AI智能助贷招标平台！

我是您的专属AI助贷顾问，可以帮助您：
• 📊 智能评估贷款风险
• 🎯 精准匹配最优产品
• 📋 指导申请流程
• 💡 提供专业建议

请告诉我您的基本信息，我将为您提供个性化的贷款方案。
        """
        
        self.conversation_history.append({
            "role": "assistant",
            "message": welcome_message,
            "timestamp": datetime.now().isoformat()
        })
        
        return AgentResponse(
            success=True,
            message=welcome_message,
            data={"user_id": user_id, "state": self.state.value},
            next_action="collect_user_info",
            confidence=1.0,
            timestamp=datetime.now().isoformat()
        )
    
    def collect_user_info(self, user_data: Dict[str, Any]) -> AgentResponse:
        """收集用户信息"""
        try:
            self.state = AgentState.PROCESSING
            
            # 构建用户画像
            self.user_profile = UserProfile(
                user_id=user_data.get("user_id", 0),
                company_name=user_data.get("company_name", ""),
                industry=user_data.get("industry", ""),
                company_size=user_data.get("company_size", ""),
                business_age=user_data.get("business_age", 0),
                annual_revenue=user_data.get("annual_revenue", 0.0),
                monthly_income=user_data.get("monthly_income", 0.0),
                credit_score=user_data.get("credit_score", 0),
                management_experience=user_data.get("management_experience", 0),
                risk_tolerance=user_data.get("risk_tolerance", "medium"),
                preferred_loan_amount=user_data.get("preferred_loan_amount", 0.0),
                preferred_term=user_data.get("preferred_term", 12),
                preferred_rate=user_data.get("preferred_rate", 0.08)
            )
            
            # 分析用户需求
            analysis = self._analyze_user_needs()
            
            message = f"""
✅ 用户信息收集完成！

📋 您的企业概况：
• 企业名称：{self.user_profile.company_name}
• 所属行业：{self.user_profile.industry}
• 企业规模：{self.user_profile.company_size}
• 经营年限：{self.user_profile.business_age}年
• 年营业收入：{self.user_profile.annual_revenue:,.0f}元

💡 需求分析：
{analysis['needs_analysis']}

🎯 推荐方案：
{analysis['recommendations']}
            """
            
            self.conversation_history.append({
                "role": "assistant",
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
            
            return AgentResponse(
                success=True,
                message=message,
                data={
                    "user_profile": self.user_profile.__dict__,
                    "analysis": analysis,
                    "state": self.state.value
                },
                next_action="risk_assessment",
                confidence=0.9,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"收集用户信息失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"信息收集失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def assess_risk(self) -> AgentResponse:
        """风险评估"""
        try:
            self.state = AgentState.PROCESSING
            
            if not self.user_profile:
                return AgentResponse(
                    success=False,
                    message="请先提供用户信息",
                    data={},
                    next_action="collect_user_info",
                    confidence=0.0,
                    timestamp=datetime.now().isoformat()
                )
            
            # 构建风险评估数据
            risk_data = {
                "user_id": self.user_profile.user_id,
                "business_data": {
                    "revenue": self.user_profile.annual_revenue,
                    "profit_margin": 0.15,  # 默认利润率
                    "debt_ratio": 0.3,      # 默认负债率
                    "credit_score": self.user_profile.credit_score,
                    "business_age": self.user_profile.business_age,
                    "employee_count": self._estimate_employee_count(),
                    "industry_risk_score": self._get_industry_risk_score(),
                    "management_experience": self.user_profile.management_experience,
                    "audit_quality_score": 0.8,
                    "governance_score": 0.7,
                    "market_share": 0.05,
                    "competitive_position": 0.6,
                    "brand_value": self.user_profile.annual_revenue * 0.1,
                    "cash_flow_stability": 0.8,
                    "working_capital_ratio": 1.2,
                    "cash_conversion_cycle": 45,
                    "revenue_growth_rate": 0.12,
                    "profit_growth_rate": 0.15
                },
                "market_data": {
                    "gdp_growth_rate": 0.06,
                    "inflation_rate": 0.03,
                    "interest_rate": 0.045,
                    "unemployment_rate": 0.05,
                    "market_volatility": 0.2,
                    "sector_volatility": 0.25,
                    "currency_volatility": 0.15,
                    "sector_growth_rate": 0.08,
                    "sector_competition_index": 0.6,
                    "regulatory_risk_score": 0.3
                }
            }
            
            # 调用风险评估API
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/risk/assess",
                json=risk_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                risk_result = response.json()
                risk_data = risk_result["data"]
                
                message = f"""
🔍 风险评估完成！

📊 风险分析结果：
• 风险等级：{risk_data.get('risk_level', '未知')}
• 综合风险评分：{risk_data.get('total_risk_score', 0):.2f}
• 推荐利率：{risk_data.get('recommended_rate', 0):.2%}
• 最大贷款金额：{risk_data.get('max_loan_amount', 0):,.0f}元

⚠️ 风险因素：
{self._format_risk_factors(risk_data.get('risk_factors', []))}

💡 建议：
{self._format_recommendations(risk_data.get('recommendations', []))}
                """
                
                self.conversation_history.append({
                    "role": "assistant",
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                return AgentResponse(
                    success=True,
                    message=message,
                    data=risk_data,
                    next_action="smart_matching",
                    confidence=0.95,
                    timestamp=datetime.now().isoformat()
                )
            else:
                raise Exception(f"风险评估API调用失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"风险评估失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"风险评估失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def smart_matching(self) -> AgentResponse:
        """智能匹配"""
        try:
            self.state = AgentState.PROCESSING
            
            if not self.user_profile:
                return AgentResponse(
                    success=False,
                    message="请先完成风险评估",
                    data={},
                    next_action="assess_risk",
                    confidence=0.0,
                    timestamp=datetime.now().isoformat()
                )
            
            # 构建匹配数据
            matching_data = {
                "tender_id": 1,
                "user_requirements": {
                    "loan_amount": self.user_profile.preferred_loan_amount,
                    "loan_term": self.user_profile.preferred_term,
                    "preferred_rate": self.user_profile.preferred_rate,
                    "industry": self.user_profile.industry,
                    "company_size": self.user_profile.company_size,
                    "revenue": self.user_profile.annual_revenue,
                    "credit_score": self.user_profile.credit_score,
                    "business_age": self.user_profile.business_age
                },
                "available_products": self._get_available_products()
            }
            
            # 调用智能匹配API
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/match/proposals",
                json=matching_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                match_result = response.json()
                match_data = match_result["data"]
                
                message = f"""
🎯 智能匹配完成！

📋 匹配结果：
• 总产品数：{match_data.get('total_products', 0)}
• 匹配产品数：{match_data.get('matched_products', 0)}
• 推荐数量：{len(match_data.get('recommendations', []))}

🏆 推荐产品：
{self._format_recommendations(match_data.get('recommendations', []))}

📈 匹配分析：
{self._format_matching_analysis(match_data.get('matching_analysis', {}))}
                """
                
                self.conversation_history.append({
                    "role": "assistant",
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                return AgentResponse(
                    success=True,
                    message=message,
                    data=match_data,
                    next_action="generate_recommendations",
                    confidence=0.9,
                    timestamp=datetime.now().isoformat()
                )
            else:
                raise Exception(f"智能匹配API调用失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"智能匹配失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"智能匹配失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def generate_recommendations(self) -> AgentResponse:
        """生成推荐方案"""
        try:
            self.state = AgentState.PROCESSING
            
            if not self.user_profile:
                return AgentResponse(
                    success=False,
                    message="请先完成智能匹配",
                    data={},
                    next_action="smart_matching",
                    confidence=0.0,
                    timestamp=datetime.now().isoformat()
                )
            
            # 构建推荐数据
            recommendation_data = {
                "tender_id": 1,
                "user_id": self.user_profile.user_id,
                "user_preferences": {
                    "loan_amount": self.user_profile.preferred_loan_amount,
                    "loan_term": self.user_profile.preferred_term,
                    "preferred_rate": self.user_profile.preferred_rate,
                    "industry": self.user_profile.industry,
                    "company_size": self.user_profile.company_size,
                    "revenue": self.user_profile.annual_revenue,
                    "credit_score": self.user_profile.credit_score,
                    "business_age": self.user_profile.business_age
                }
            }
            
            # 调用推荐引擎API
            response = self.session.post(
                f"{self.base_url}/api/v1/ai/recommend/solutions",
                json=recommendation_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                rec_result = response.json()
                rec_data = rec_result["data"]
                
                message = f"""
💡 个性化推荐方案生成完成！

🎯 为您推荐以下方案：

{self._format_personalized_recommendations(rec_data.get('personalized_recommendations', []))}

🔥 热门推荐：

{self._format_popular_recommendations(rec_data.get('popular_recommendations', []))}

📋 下一步建议：
1. 仔细比较各方案的条件和利率
2. 准备相关申请材料
3. 联系推荐机构进行详细咨询
4. 提交正式申请
                """
                
                self.conversation_history.append({
                    "role": "assistant",
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                self.state = AgentState.COMPLETED
                
                return AgentResponse(
                    success=True,
                    message=message,
                    data=rec_data,
                    next_action="completed",
                    confidence=0.95,
                    timestamp=datetime.now().isoformat()
                )
            else:
                raise Exception(f"推荐引擎API调用失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"生成推荐方案失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"生成推荐方案失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def process_document(self, file_path: str, file_type: str) -> AgentResponse:
        """处理文档"""
        try:
            self.state = AgentState.PROCESSING
            
            with open(file_path, "rb") as f:
                files = {"file": (file_path, f, file_type)}
                response = self.session.post(
                    f"{self.base_url}/api/v1/ai/document/process",
                    files=files
                )
            
            if response.status_code == 200:
                doc_result = response.json()
                
                message = f"""
📄 文档处理完成！

✅ 处理结果：
• 文件类型：{file_type}
• 处理状态：{doc_result.get('message', '未知')}
• 提取信息：{doc_result.get('data', {})}

📋 提取的关键信息：
{self._format_document_data(doc_result.get('data', {}))}
                """
                
                self.conversation_history.append({
                    "role": "assistant",
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                return AgentResponse(
                    success=True,
                    message=message,
                    data=doc_result.get('data', {}),
                    next_action="continue",
                    confidence=0.9,
                    timestamp=datetime.now().isoformat()
                )
            else:
                raise Exception(f"文档处理API调用失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"文档处理失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"文档处理失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.conversation_history
    
    def reset_agent(self):
        """重置智能体"""
        self.state = AgentState.IDLE
        self.conversation_history = []
        self.current_application = None
        self.user_profile = None
        logger.info("AI助贷招标智能体已重置")
    
    # 私有方法
    def _analyze_user_needs(self) -> Dict[str, Any]:
        """分析用户需求"""
        if not self.user_profile:
            return {"needs_analysis": "无法分析", "recommendations": "请提供用户信息"}
        
        needs = []
        recommendations = []
        
        # 基于企业规模分析
        if self.user_profile.company_size == "micro":
            needs.append("小微企业，需要灵活便捷的贷款方案")
            recommendations.append("推荐小额快速贷款产品")
        elif self.user_profile.company_size == "small":
            needs.append("小型企业，需要稳定可靠的资金支持")
            recommendations.append("推荐标准企业贷款产品")
        elif self.user_profile.company_size == "medium":
            needs.append("中型企业，需要大额长期资金支持")
            recommendations.append("推荐大额企业贷款产品")
        
        # 基于行业分析
        if self.user_profile.industry in ["制造业", "加工业"]:
            needs.append("制造业企业，可能需要设备贷款")
            recommendations.append("推荐设备采购专项贷款")
        elif self.user_profile.industry in ["服务业", "贸易"]:
            needs.append("服务业企业，需要流动资金支持")
            recommendations.append("推荐流动资金贷款产品")
        
        # 基于信用评分分析
        if self.user_profile.credit_score >= 750:
            needs.append("信用状况优秀，可享受优惠利率")
            recommendations.append("推荐优质客户专享产品")
        elif self.user_profile.credit_score >= 650:
            needs.append("信用状况良好，可申请标准产品")
            recommendations.append("推荐标准利率产品")
        else:
            needs.append("信用状况一般，需要提供担保或抵押")
            recommendations.append("推荐担保贷款产品")
        
        return {
            "needs_analysis": "\n".join(f"• {need}" for need in needs),
            "recommendations": "\n".join(f"• {rec}" for rec in recommendations)
        }
    
    def _estimate_employee_count(self) -> int:
        """估算员工数量"""
        if not self.user_profile:
            return 0
        
        if self.user_profile.company_size == "micro":
            return 10
        elif self.user_profile.company_size == "small":
            return 50
        elif self.user_profile.company_size == "medium":
            return 200
        else:
            return 500
    
    def _get_industry_risk_score(self) -> float:
        """获取行业风险评分"""
        if not self.user_profile:
            return 0.5
        
        industry_risk_map = {
            "金融": 0.2,
            "科技": 0.3,
            "制造业": 0.4,
            "服务业": 0.5,
            "贸易": 0.6,
            "餐饮": 0.7,
            "零售": 0.7
        }
        
        return industry_risk_map.get(self.user_profile.industry, 0.5)
    
    def _get_available_products(self) -> List[Dict[str, Any]]:
        """获取可用产品列表"""
        return [
            {
                "product_id": 1,
                "product_name": "流动资金贷款",
                "interest_rate": 0.065,
                "term_months": 24,
                "max_amount": 1000000,
                "min_amount": 100000,
                "target_industry": ["制造业", "服务业", "贸易"],
                "features": ["快速审批", "灵活还款", "低门槛"]
            },
            {
                "product_id": 2,
                "product_name": "设备贷款",
                "interest_rate": 0.055,
                "term_months": 36,
                "max_amount": 2000000,
                "min_amount": 200000,
                "target_industry": ["制造业", "加工业", "农业"],
                "features": ["专项用途", "长期限", "设备抵押"]
            },
            {
                "product_id": 3,
                "product_name": "供应链贷款",
                "interest_rate": 0.045,
                "term_months": 12,
                "max_amount": 5000000,
                "min_amount": 500000,
                "target_industry": ["制造业", "贸易", "物流"],
                "features": ["供应链融资", "应收账款质押", "快速放款"]
            }
        ]
    
    def _format_risk_factors(self, risk_factors: List[str]) -> str:
        """格式化风险因素"""
        if not risk_factors:
            return "• 无特殊风险因素"
        return "\n".join(f"• {factor}" for factor in risk_factors)
    
    def _format_recommendations(self, recommendations: List[str]) -> str:
        """格式化建议"""
        if not recommendations:
            return "• 无特殊建议"
        return "\n".join(f"• {rec}" for rec in recommendations)
    
    def _format_matching_analysis(self, analysis: Dict[str, Any]) -> str:
        """格式化匹配分析"""
        if not analysis:
            return "• 无匹配分析数据"
        
        result = []
        for key, value in analysis.items():
            result.append(f"• {key}: {value}")
        return "\n".join(result)
    
    def _format_personalized_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """格式化个性化推荐"""
        if not recommendations:
            return "• 暂无个性化推荐"
        
        result = []
        for i, rec in enumerate(recommendations[:3], 1):  # 只显示前3个
            result.append(f"{i}. {rec.get('product_name', '未知产品')}")
            result.append(f"   利率: {rec.get('interest_rate', 0):.2%}")
            result.append(f"   期限: {rec.get('term_months', 0)}个月")
            result.append(f"   金额: {rec.get('max_amount', 0):,.0f}元")
            result.append(f"   匹配度: {rec.get('match_score', 0):.2f}")
            result.append("")
        
        return "\n".join(result)
    
    def _format_popular_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """格式化热门推荐"""
        if not recommendations:
            return "• 暂无热门推荐"
        
        result = []
        for i, rec in enumerate(recommendations[:2], 1):  # 只显示前2个
            result.append(f"{i}. {rec.get('product_name', '未知产品')}")
            result.append(f"   利率: {rec.get('interest_rate', 0):.2%}")
            result.append(f"   期限: {rec.get('term_months', 0)}个月")
            result.append(f"   金额: {rec.get('max_amount', 0):,.0f}元")
            result.append("")
        
        return "\n".join(result)
    
    def _format_document_data(self, data: Dict[str, Any]) -> str:
        """格式化文档数据"""
        if not data:
            return "• 无提取数据"
        
        result = []
        for key, value in data.items():
            result.append(f"• {key}: {value}")
        return "\n".join(result)

# 使用示例
async def main():
    """主函数示例"""
    # 创建AI助贷招标智能体
    agent = AILoanAgent()
    
    # 初始化服务
    if not await agent.initialize_services():
        print("❌ AI服务初始化失败")
        return
    
    # 开始对话
    response = agent.start_conversation(user_id=1)
    print(response.message)
    
    # 模拟用户信息
    user_data = {
        "user_id": 1,
        "company_name": "测试科技有限公司",
        "industry": "制造业",
        "company_size": "small",
        "business_age": 3,
        "annual_revenue": 2000000,
        "monthly_income": 200000,
        "credit_score": 720,
        "management_experience": 5,
        "risk_tolerance": "medium",
        "preferred_loan_amount": 500000,
        "preferred_term": 24,
        "preferred_rate": 0.08
    }
    
    # 收集用户信息
    response = agent.collect_user_info(user_data)
    print(response.message)
    
    # 风险评估
    response = agent.assess_risk()
    print(response.message)
    
    # 智能匹配
    response = agent.smart_matching()
    print(response.message)
    
    # 生成推荐
    response = agent.generate_recommendations()
    print(response.message)

if __name__ == "__main__":
    asyncio.run(main())
