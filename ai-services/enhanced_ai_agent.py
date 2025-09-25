"""
增强版AI助贷招标智能体
集成多种LLM模型，提供更智能的对话和决策能力

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

from llm_integration import LLMManager, create_llm_manager
from ai_loan_agent import AILoanAgent, AgentState, UserProfile, LoanPurpose, AgentResponse

class ConversationMode(Enum):
    """对话模式"""
    PROFESSIONAL = "professional"    # 专业模式
    FRIENDLY = "friendly"           # 友好模式
    TECHNICAL = "technical"         # 技术模式
    SIMPLE = "simple"              # 简单模式

@dataclass
class AgentCapabilities:
    """智能体能力"""
    llm_enabled: bool = True
    risk_assessment: bool = True
    smart_matching: bool = True
    document_processing: bool = True
    recommendation: bool = True
    multi_language: bool = True
    voice_support: bool = False
    image_analysis: bool = False

class EnhancedAILoanAgent(AILoanAgent):
    """增强版AI助贷招标智能体"""
    
    def __init__(self, base_url: str = "http://localhost:8000", llm_name: str = "gpt-3.5-turbo"):
        super().__init__(base_url)
        self.llm_manager = create_llm_manager()
        self.llm_name = llm_name
        self.conversation_mode = ConversationMode.PROFESSIONAL
        self.capabilities = AgentCapabilities()
        self.conversation_context = []
        self.user_preferences = {}
        
        logger.info(f"增强版AI助贷招标智能体初始化完成，使用LLM: {llm_name}")
    
    async def start_conversation(self, user_id: int, mode: ConversationMode = ConversationMode.PROFESSIONAL) -> AgentResponse:
        """开始对话（增强版）"""
        self.state = AgentState.PROCESSING
        self.user_profile = None
        self.current_application = None
        self.conversation_mode = mode
        self.conversation_context = []
        
        # 使用LLM生成个性化欢迎消息
        welcome_prompt = self._generate_welcome_prompt(mode)
        
        try:
            welcome_message = await self.llm_manager.generate(
                welcome_prompt,
                llm_name=self.llm_name,
                temperature=0.8,
                max_tokens=500
            )
        except Exception as e:
            logger.warning(f"LLM生成欢迎消息失败，使用默认消息: {str(e)}")
            welcome_message = self._get_default_welcome_message()
        
        self.conversation_history.append({
            "role": "assistant",
            "message": welcome_message,
            "timestamp": datetime.now().isoformat(),
            "mode": mode.value
        })
        
        return AgentResponse(
            success=True,
            message=welcome_message,
            data={
                "user_id": user_id,
                "state": self.state.value,
                "mode": mode.value,
                "capabilities": self.capabilities.__dict__
            },
            next_action="collect_user_info",
            confidence=1.0,
            timestamp=datetime.now().isoformat()
        )
    
    async def intelligent_collect_user_info(self, user_data: Dict[str, Any]) -> AgentResponse:
        """智能收集用户信息"""
        try:
            self.state = AgentState.PROCESSING
            
            # 使用LLM分析用户信息
            analysis_prompt = self._generate_user_analysis_prompt(user_data)
            
            try:
                analysis = await self.llm_manager.generate(
                    analysis_prompt,
                    llm_name=self.llm_name,
                    temperature=0.7,
                    max_tokens=800
                )
            except Exception as e:
                logger.warning(f"LLM分析用户信息失败: {str(e)}")
                analysis = self._analyze_user_needs()
            
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
            
            # 生成个性化回复
            response_prompt = self._generate_user_info_response_prompt(user_data, analysis)
            
            try:
                message = await self.llm_manager.generate(
                    response_prompt,
                    llm_name=self.llm_name,
                    temperature=0.8,
                    max_tokens=1000
                )
            except Exception as e:
                logger.warning(f"LLM生成回复失败: {str(e)}")
                message = self._get_default_user_info_message()
            
            self.conversation_history.append({
                "role": "assistant",
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis
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
            logger.error(f"智能收集用户信息失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"信息收集失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    async def intelligent_risk_assessment(self) -> AgentResponse:
        """智能风险评估"""
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
            
            # 调用原有风险评估
            risk_response = self.assess_risk()
            
            if not risk_response.success:
                return risk_response
            
            # 使用LLM增强风险评估结果
            enhancement_prompt = self._generate_risk_enhancement_prompt(risk_response.data)
            
            try:
                enhanced_analysis = await self.llm_manager.generate(
                    enhancement_prompt,
                    llm_name=self.llm_name,
                    temperature=0.7,
                    max_tokens=1200
                )
            except Exception as e:
                logger.warning(f"LLM增强风险评估失败: {str(e)}")
                enhanced_analysis = risk_response.message
            
            # 生成个性化风险建议
            advice_prompt = self._generate_risk_advice_prompt(risk_response.data)
            
            try:
                personalized_advice = await self.llm_manager.generate(
                    advice_prompt,
                    llm_name=self.llm_name,
                    temperature=0.8,
                    max_tokens=800
                )
            except Exception as e:
                logger.warning(f"LLM生成风险建议失败: {str(e)}")
                personalized_advice = "建议咨询专业金融顾问获取详细建议。"
            
            enhanced_message = f"""
{risk_response.message}

🤖 AI智能分析：
{enhanced_analysis}

💡 个性化建议：
{personalized_advice}
            """
            
            self.conversation_history.append({
                "role": "assistant",
                "message": enhanced_message,
                "timestamp": datetime.now().isoformat(),
                "enhanced_analysis": enhanced_analysis,
                "personalized_advice": personalized_advice
            })
            
            return AgentResponse(
                success=True,
                message=enhanced_message,
                data={
                    **risk_response.data,
                    "enhanced_analysis": enhanced_analysis,
                    "personalized_advice": personalized_advice
                },
                next_action="smart_matching",
                confidence=0.95,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"智能风险评估失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"风险评估失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    async def intelligent_smart_matching(self) -> AgentResponse:
        """智能匹配（增强版）"""
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
            
            # 调用原有智能匹配
            match_response = self.smart_matching()
            
            if not match_response.success:
                return match_response
            
            # 使用LLM分析匹配结果
            analysis_prompt = self._generate_matching_analysis_prompt(match_response.data)
            
            try:
                intelligent_analysis = await self.llm_manager.generate(
                    analysis_prompt,
                    llm_name=self.llm_name,
                    temperature=0.7,
                    max_tokens=1000
                )
            except Exception as e:
                logger.warning(f"LLM分析匹配结果失败: {str(e)}")
                intelligent_analysis = "基于您的需求，我们为您找到了合适的贷款产品。"
            
            # 生成个性化推荐理由
            reasoning_prompt = self._generate_recommendation_reasoning_prompt(match_response.data)
            
            try:
                personalized_reasoning = await self.llm_manager.generate(
                    reasoning_prompt,
                    llm_name=self.llm_name,
                    temperature=0.8,
                    max_tokens=800
                )
            except Exception as e:
                logger.warning(f"LLM生成推荐理由失败: {str(e)}")
                personalized_reasoning = "这些产品符合您的贷款需求。"
            
            enhanced_message = f"""
{match_response.message}

🧠 AI智能分析：
{intelligent_analysis}

🎯 个性化推荐理由：
{personalized_reasoning}
            """
            
            self.conversation_history.append({
                "role": "assistant",
                "message": enhanced_message,
                "timestamp": datetime.now().isoformat(),
                "intelligent_analysis": intelligent_analysis,
                "personalized_reasoning": personalized_reasoning
            })
            
            return AgentResponse(
                success=True,
                message=enhanced_message,
                data={
                    **match_response.data,
                    "intelligent_analysis": intelligent_analysis,
                    "personalized_reasoning": personalized_reasoning
                },
                next_action="generate_recommendations",
                confidence=0.9,
                timestamp=datetime.now().isoformat()
            )
            
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
    
    async def chat_with_llm(self, user_message: str) -> AgentResponse:
        """与LLM对话"""
        try:
            self.state = AgentState.PROCESSING
            
            # 构建对话上下文
            messages = [
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                }
            ]
            
            # 添加对话历史
            for msg in self.conversation_history[-5:]:  # 只保留最近5条
                messages.append({
                    "role": msg["role"],
                    "content": msg["message"]
                })
            
            # 添加用户消息
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # 调用LLM
            response = await self.llm_manager.chat(
                messages,
                llm_name=self.llm_name,
                temperature=0.8,
                max_tokens=1000
            )
            
            self.conversation_history.append({
                "role": "assistant",
                "message": response,
                "timestamp": datetime.now().isoformat(),
                "llm_generated": True
            })
            
            return AgentResponse(
                success=True,
                message=response,
                data={"llm_generated": True},
                next_action="continue",
                confidence=0.9,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"LLM对话失败: {str(e)}")
            return AgentResponse(
                success=False,
                message=f"对话失败: {str(e)}",
                data={},
                next_action="retry",
                confidence=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def switch_llm(self, llm_name: str) -> bool:
        """切换LLM模型"""
        try:
            if llm_name in self.llm_manager.list_llms():
                self.llm_name = llm_name
                logger.info(f"LLM模型已切换到: {llm_name}")
                return True
            else:
                logger.error(f"LLM模型 {llm_name} 不可用")
                return False
        except Exception as e:
            logger.error(f"切换LLM模型失败: {str(e)}")
            return False
    
    def set_conversation_mode(self, mode: ConversationMode):
        """设置对话模式"""
        self.conversation_mode = mode
        logger.info(f"对话模式已设置为: {mode.value}")
    
    def get_available_llms(self) -> List[str]:
        """获取可用的LLM模型"""
        return self.llm_manager.list_llms()
    
    # 私有方法
    def _generate_welcome_prompt(self, mode: ConversationMode) -> str:
        """生成欢迎消息提示"""
        mode_descriptions = {
            ConversationMode.PROFESSIONAL: "专业、正式、权威",
            ConversationMode.FRIENDLY: "友好、亲切、温暖",
            ConversationMode.TECHNICAL: "技术、详细、精确",
            ConversationMode.SIMPLE: "简单、易懂、直接"
        }
        
        return f"""
你是一个专业的AI助贷招标智能体，请用{mode_descriptions[mode]}的语气生成一段欢迎消息。

要求：
1. 介绍你的身份和能力
2. 说明你能提供的服务
3. 引导用户开始贷款申请流程
4. 体现专业性和可信度
5. 语言要自然流畅，符合中文表达习惯

请生成一段200-300字的欢迎消息。
        """
    
    def _generate_user_analysis_prompt(self, user_data: Dict[str, Any]) -> str:
        """生成用户分析提示"""
        return f"""
请分析以下用户信息，并提供专业的贷款建议：

用户信息：
- 企业名称：{user_data.get('company_name', '未知')}
- 所属行业：{user_data.get('industry', '未知')}
- 企业规模：{user_data.get('company_size', '未知')}
- 经营年限：{user_data.get('business_age', 0)}年
- 年营业收入：{user_data.get('annual_revenue', 0):,.0f}元
- 月收入：{user_data.get('monthly_income', 0):,.0f}元
- 信用评分：{user_data.get('credit_score', 0)}
- 管理经验：{user_data.get('management_experience', 0)}年
- 风险偏好：{user_data.get('risk_tolerance', '未知')}
- 期望贷款金额：{user_data.get('preferred_loan_amount', 0):,.0f}元
- 期望贷款期限：{user_data.get('preferred_term', 0)}个月
- 期望利率：{user_data.get('preferred_rate', 0):.2%}

请从以下角度进行分析：
1. 企业基本情况评估
2. 贷款需求合理性分析
3. 风险因素识别
4. 推荐贷款类型和条件
5. 申请建议和注意事项

请用专业、客观的语言进行分析，并提供具体的建议。
        """
    
    def _generate_user_info_response_prompt(self, user_data: Dict[str, Any], analysis: str) -> str:
        """生成用户信息回复提示"""
        return f"""
基于以下用户信息和AI分析，生成一段个性化的回复：

用户信息：{json.dumps(user_data, ensure_ascii=False, indent=2)}

AI分析：{analysis}

请生成一段回复，要求：
1. 确认用户信息收集完成
2. 简要总结用户的企业情况
3. 基于分析结果提供初步建议
4. 引导用户进入下一步（风险评估）
5. 语言要专业且友好
6. 长度控制在300-400字

请生成回复内容。
        """
    
    def _generate_risk_enhancement_prompt(self, risk_data: Dict[str, Any]) -> str:
        """生成风险增强分析提示"""
        return f"""
基于以下风险评估数据，提供更深入的风险分析：

风险数据：{json.dumps(risk_data, ensure_ascii=False, indent=2)}

请从以下角度进行深入分析：
1. 风险等级的具体含义和影响
2. 各项风险评分的详细解释
3. 行业和市场因素对风险的影响
4. 历史数据和趋势分析
5. 风险缓解的具体建议
6. 对贷款条件的影响分析

请用专业、客观的语言进行分析，并提供可操作的建议。
        """
    
    def _generate_risk_advice_prompt(self, risk_data: Dict[str, Any]) -> str:
        """生成风险建议提示"""
        return f"""
基于以下风险评估结果，为用户提供个性化的风险建议：

风险数据：{json.dumps(risk_data, ensure_ascii=False, indent=2)}

请提供以下建议：
1. 针对当前风险等级的具体建议
2. 如何降低风险的具体措施
3. 申请贷款时的注意事项
4. 可能需要提供的额外材料
5. 建议的贷款条件调整
6. 风险监控和管理的建议

请用实用、具体的语言提供建议，让用户能够理解和执行。
        """
    
    def _generate_matching_analysis_prompt(self, match_data: Dict[str, Any]) -> str:
        """生成匹配分析提示"""
        return f"""
基于以下智能匹配结果，提供深入的产品分析：

匹配数据：{json.dumps(match_data, ensure_ascii=False, indent=2)}

请从以下角度进行分析：
1. 匹配算法的逻辑和依据
2. 各推荐产品的优劣势分析
3. 产品与用户需求的匹配度分析
4. 利率、期限、条件的具体分析
5. 申请难度和成功率评估
6. 产品组合建议

请用专业、客观的语言进行分析，帮助用户做出明智的选择。
        """
    
    def _generate_recommendation_reasoning_prompt(self, match_data: Dict[str, Any]) -> str:
        """生成推荐理由提示"""
        return f"""
基于以下匹配结果，为用户生成个性化的推荐理由：

匹配数据：{json.dumps(match_data, ensure_ascii=False, indent=2)}

请为每个推荐产品生成推荐理由：
1. 为什么这个产品适合用户
2. 产品的核心优势是什么
3. 与用户需求的匹配点
4. 申请成功的可能性
5. 需要注意的风险点
6. 申请建议和技巧

请用简洁、有说服力的语言生成推荐理由。
        """
    
    def _get_system_prompt(self) -> str:
        """获取系统提示"""
        return """
你是一个专业的AI助贷招标智能体，专门为小微企业提供贷款咨询服务。

你的能力包括：
1. 风险评估和分析
2. 智能产品匹配
3. 个性化推荐
4. 贷款流程指导
5. 金融知识解答

你的特点：
- 专业、准确、可靠
- 语言简洁明了
- 提供实用建议
- 保护用户隐私
- 遵守金融法规

请始终以专业、友好的态度为用户提供服务。
        """
    
    def _get_default_welcome_message(self) -> str:
        """获取默认欢迎消息"""
        return """
🤖 欢迎使用AI智能助贷招标平台！

我是您的专属AI助贷顾问，拥有先进的人工智能技术，可以为您提供：

• 📊 智能风险评估 - 基于大数据和AI算法
• 🎯 精准产品匹配 - 从海量产品中找到最适合的
• 💡 个性化推荐 - 根据您的具体情况定制方案
• 📋 全程流程指导 - 从申请到放款的完整服务
• 🔍 专业金融咨询 - 解答您的各种疑问

请告诉我您的基本信息，我将为您提供最专业的贷款解决方案！
        """
    
    def _get_default_user_info_message(self) -> str:
        """获取默认用户信息消息"""
        return """
✅ 用户信息收集完成！

感谢您提供详细的企业信息。基于您的情况，我已经初步分析了您的贷款需求。

接下来，我将为您进行专业的风险评估，这将帮助我们找到最适合您的贷款产品。

请稍等，风险评估即将开始...
        """

# 使用示例
async def main():
    """使用示例"""
    # 创建增强版智能体
    agent = EnhancedAILoanAgent()
    
    # 列出可用的LLM模型
    print("可用的LLM模型:")
    for llm in agent.get_available_llms():
        print(f"- {llm}")
    
    # 开始对话
    response = await agent.start_conversation(user_id=1, mode=ConversationMode.PROFESSIONAL)
    print(f"欢迎消息: {response.message}")
    
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
    
    # 智能收集用户信息
    response = await agent.intelligent_collect_user_info(user_data)
    print(f"用户信息分析: {response.message}")
    
    # 智能风险评估
    response = await agent.intelligent_risk_assessment()
    print(f"风险评估: {response.message}")
    
    # 智能匹配
    response = await agent.intelligent_smart_matching()
    print(f"智能匹配: {response.message}")

if __name__ == "__main__":
    asyncio.run(main())
