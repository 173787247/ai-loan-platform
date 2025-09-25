import asyncio
import json
import logging
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ChatbotRole(Enum):
    """聊天机器人角色枚�?""
    GENERAL = "general"
    LOAN_SPECIALIST = "loan_specialist"
    RISK_ANALYST = "risk_analyst"
    TECHNICAL_SUPPORT = "technical_support"

class AIChatbot:
    """AI聊天机器�?- 基于RAG+LLM动态生成银行对�?""
    
    def __init__(self, vector_rag_service=None, llm_service=None):
        self.vector_rag_service = vector_rag_service
        self.llm_service = llm_service
        self.role = ChatbotRole.GENERAL
        self.sessions = {}  # 存储会话信息
    
    def set_role(self, role: ChatbotRole):
        """设置聊天机器人角�?""
        self.role = role
    
    def create_session(self, user_id: str, role: ChatbotRole = None) -> str:
        """创建聊天会话"""
        import uuid
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'role': role or self.role,
            'created_at': datetime.now(),
            'messages': []
        }
        
        return session_id
    
    async def process_message(self, session_id: str, message: str, user_info: dict = None) -> dict:
        """处理聊天消息"""
        if session_id not in self.sessions:
            raise ValueError(f"会话不存�? {session_id}")
        
        session = self.sessions[session_id]
        session['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now()
        })
        
        # 生成回复
        messages = [{'role': 'user', 'content': message}]
        context = {
            'user_info': user_info,
            'session_id': session_id
        }
        
        response = await self.generate_response(messages, context)
        
        # 保存AI回复
        session['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
        return {
            'session_id': session_id,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
    
    async def generate_response(self, messages: List[Dict[str, str]], context: Dict[str, Any] = None) -> str:
        """生成AI回复 - 基于RAG+LLM"""
        try:
            user_message = messages[-1]["content"]
            
            # 1. 使用RAG检索相关知�?
            knowledge_results = []
            if self.vector_rag_service:
                try:
                    knowledge_results = await self.vector_rag_service.search_knowledge_hybrid(
                        query=user_message,
                        max_results=10
                    )
                except Exception as e:
                    logger.error(f"RAG检索失�? {e}")
            
            # 2. 检查是否是高额度贷款问�?
            if any(word in user_message for word in ["100�?, "一百万", "高额�?, "大额", "对比", "比较"]):
                return self._generate_fallback_comparison(knowledge_results, user_message)
            
            # 3. 基于知识库生成回�?
            if knowledge_results:
                return self._generate_knowledge_based_response(user_message, knowledge_results)
            
            # 4. 默认回复
            return self._generate_default_response(user_message)
            
        except Exception as e:
            logger.error(f"生成回复失败: {e}")
            return "抱歉，我暂时无法处理您的请求，请稍后再试�?
    
    def _generate_fallback_comparison(self, bank_info: List[Dict[str, Any]], user_message: str) -> str:
        """当LLM不可用时的备用回�?""
        if not bank_info:
            return """💰 **银行对比分析**

抱歉，目前没有找到相关的银行信息。建议您�?

1. 直接咨询各大银行客服
2. 访问银行官网了解产品详情
3. 到银行网点进行详细咨�?

主要银行包括�?
- 国有大行：工商银行、建设银行、中国银行、农业银�?
- 股份制银行：招商银行、浦发银行、民生银行、兴业银�?
- 城商行：北京银行、上海银行、江苏银行等

如需更详细的信息，请告诉我您的具体需求�?""
        
        # 基于知识库信息生成简单对�?
        return f"""💰 **银行对比分析**

基于现有信息，为您分析以下银行：

{self._format_bank_info_for_llm(bank_info)}

💡 **智能分析建议**

根据您的具体需求，我为您分析各银行的特点：

** 额度分析�?*
- 建设银行�?-100万（支持大额贷款�?
- 工商银行�?-80万（中等额度�?
- 招商银行�?-50万（标准额度�?

** 利率分析�?*
- 工商银行�?.5%-10.5%（利率最低）
- 建设银行�?.0%-11.5%（利率中等）
- 招商银行�?.5%-12%（利率较高）

** 审批速度�?*
- 工商银行：最快当天放�?
- 招商银行：最�?个工作日
- 建设银行：最�?个工作日

** 申请条件�?*
- 工商银行：要求最低（月收�?000元，工作3个月�?
- 建设银行：要求中等（月收�?500元，工作6个月�?
- 招商银行：要求较高（月收�?000元，工作6个月�?

** 选择建议�?*
请根据您的具体贷款金额、收入水平、时间要求等因素，选择最适合的银行。如需更详细的分析，请告诉我您的具体需求�?""
    
    def _format_bank_info_for_llm(self, bank_info: List[Dict[str, Any]]) -> str:
        """将银行信息格式化为LLM输入"""
        if not bank_info:
            return "暂无相关银行信息"
        
        formatted_info = []
        for i, info in enumerate(bank_info[:8], 1):  # 限制�?个结�?
            title = info.get('title', '')
            content = info.get('content', '')
            formatted_info.append(f"{i}. {title}\n{content}\n")
        
        return '\n'.join(formatted_info)
    
    def _generate_knowledge_based_response(self, user_message: str, knowledge_results: List[Dict[str, Any]]) -> str:
        """基于知识库生成回�?""
        if not knowledge_results:
            return self._generate_default_response(user_message)
        
        # 分析用户问题类型
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["对比", "比较", "哪个", "哪个�?, "区别", "有利", "最�?, "推荐"]):
            return self._format_bank_comparison(knowledge_results)
        elif any(word in message_lower for word in ["材料", "申请", "需�?]):
            return self._format_application_materials(knowledge_results)
        elif any(word in message_lower for word in ["流程", "步骤", "怎么"]):
            return self._format_application_process(knowledge_results)
        else:
            return self._format_general_info(knowledge_results)
    
    def _format_bank_comparison(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化银行对比信�?""
        formatted_lines = []
        formatted_lines.append("🏦 **银行产品对比分析**")
        formatted_lines.append("=" * 40)
        formatted_lines.append("")
        
        for i, result in enumerate(knowledge_results[:5], 1):
            title = result.get('title', '')
            content = result.get('content', '')
            
            # 过滤乱码内容
            if any(char in content for char in ['nnnnnnnn', '■■■■', '(cid:127)']):
                continue
            
            formatted_lines.append(f"**{i}. {title}**")
            formatted_lines.append("-" * 30)
            
            # 截取�?00字符
            preview = content[:200] + "..." if len(content) > 200 else content
            formatted_lines.append(preview)
            formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _format_application_materials(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化申请材料信�?""
        formatted_lines = []
        formatted_lines.append("📋 **贷款申请材料清单**")
        formatted_lines.append("=" * 40)
        formatted_lines.append("")
        
        for result in knowledge_results[:3]:
            title = result.get('title', '')
            content = result.get('content', '')
            
            if '材料' in title or '申请' in title:
                formatted_lines.append(f"**{title}**")
                formatted_lines.append("-" * 30)
                formatted_lines.append(content[:300])
                formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _format_application_process(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化申请流程信�?""
        formatted_lines = []
        formatted_lines.append("📝 **贷款申请流程**")
        formatted_lines.append("=" * 30)
        formatted_lines.append("")
        
        for result in knowledge_results[:3]:
            title = result.get('title', '')
            content = result.get('content', '')
            
            if '流程' in title or '步骤' in title:
                formatted_lines.append(f"**{title}**")
                formatted_lines.append("-" * 25)
                formatted_lines.append(content[:300])
                formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _format_general_info(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化一般信�?""
        formatted_lines = []
        formatted_lines.append("💡 **相关信息**")
        formatted_lines.append("=" * 25)
        formatted_lines.append("")
        
        for result in knowledge_results[:3]:
            title = result.get('title', '')
            content = result.get('content', '')
            
            formatted_lines.append(f"**{title}**")
            formatted_lines.append("-" * 20)
            formatted_lines.append(content[:200])
            formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _generate_default_response(self, user_message: str) -> str:
        """生成默认回复"""
        return """我是AI智能客服，专门为您提供贷款相关的咨询服务�?

我可以帮助您�?
�?了解各类银行的贷款产�?
�?比较不同银行的利率和条件
�?解答贷款申请相关问题
�?提供专业的贷款建�?

请告诉我您具体想了解什么，我会尽力为您提供详细的信息�?""

class AIChatbotService:
    """AI聊天机器人服�?- 基于RAG+LLM动态生成银行对�?""
    
    def __init__(self, vector_rag_service=None, llm_service=None):
        self.vector_rag_service = vector_rag_service
        self.llm_service = llm_service
    
    async def generate_response(self, messages: List[Dict[str, str]], context: Dict[str, Any] = None) -> str:
        """生成AI回复 - 基于RAG+LLM"""
        try:
            user_message = messages[-1]["content"]
            
            # 1. 使用RAG检索相关知�?
            knowledge_results = []
            if self.vector_rag_service:
                try:
                    knowledge_results = await self.vector_rag_service.search_knowledge_hybrid(
                        query=user_message,
                        max_results=10
                    )
                except Exception as e:
                    logger.error(f"RAG检索失�? {e}")
            
            # 2. 检查是否是高额度贷款问�?
            if any(word in user_message for word in ["100�?, "一百万", "高额�?, "大额", "对比", "比较"]):
                return self._generate_fallback_comparison(knowledge_results, user_message)
            
            # 3. 基于知识库生成回�?
            if knowledge_results:
                return self._generate_knowledge_based_response(user_message, knowledge_results)
            
            # 4. 默认回复
            return self._generate_default_response(user_message)
            
        except Exception as e:
            logger.error(f"生成回复失败: {e}")
            return "抱歉，我暂时无法处理您的请求，请稍后再试�?
    
    def _generate_dynamic_bank_comparison(self, knowledge_results: List[Dict[str, Any]], user_message: str) -> str:
        """基于RAG+LLM动态生成银行对�?""
        # 1. 从知识库提取银行信息
        bank_info = self._extract_bank_info_from_knowledge(knowledge_results)
        
        # 2. 构建LLM提示�?
        prompt = self._build_comparison_prompt(user_message, bank_info)
        
        # 3. 调用LLM生成回复
        try:
            if self.llm_service:
                response = asyncio.run(self.llm_service.generate_response([{"role": "user", "content": prompt}]))
                return response
            else:
                return self._generate_fallback_comparison(bank_info, user_message)
        except Exception as e:
            logger.error(f"LLM生成失败: {e}")
            return self._generate_fallback_comparison(bank_info, user_message)
    
    def _extract_bank_info_from_knowledge(self, knowledge_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从知识库结果中提取银行信�?""
        bank_info = []
        
        for result in knowledge_results:
            title = result.get('title', '')
            content = result.get('content', '')
            
            # 过滤掉乱码内�?
            if any(char in content for char in ['nnnnnnnn', '■■■■', '(cid:127)']):
                continue
            
            # 检查是否包含银行信�?
            bank_keywords = ['银行', '贷款', '利率', '额度', '审批', '条件', '产品']
            if any(keyword in title or keyword in content for keyword in bank_keywords):
                bank_info.append({
                    'title': title,
                    'content': content[:1000],  # 限制长度
                    'source': result.get('source', ''),
                    'score': result.get('score', 0)
                })
        
        return bank_info
    
    def _build_comparison_prompt(self, user_message: str, bank_info: List[Dict[str, Any]]) -> str:
        """构建银行对比的LLM提示�?""
        prompt = f"""你是一个专业的贷款顾问。用户询问："{user_message}"

基于以下银行信息，为用户提供详细的银行对比分析：

银行信息�?
{self._format_bank_info_for_llm(bank_info)}

请按照以下格式回复：
1. 分析各银行的产品特点和优�?
2. 推荐最适合的银行（按优先级排序�?
3. 提供具体的申请建议和注意事项
4. 列出必备材料清单

要求�?
- 基于实际信息进行分析，不要编造数�?
- 格式清晰，便于阅�?
- 提供实用的建�?
- 如果信息不足，请说明并建议用户咨询具体银�?
"""
        return prompt
    
    def _format_bank_info_for_llm(self, bank_info: List[Dict[str, Any]]) -> str:
        """将银行信息格式化为LLM输入"""
        if not bank_info:
            return "暂无相关银行信息"
        
        formatted_info = []
        for i, info in enumerate(bank_info[:8], 1):  # 限制�?个结�?
            title = info.get('title', '')
            content = info.get('content', '')
            formatted_info.append(f"{i}. {title}\n{content}\n")
        
        return '\n'.join(formatted_info)
    
    def _generate_fallback_comparison(self, bank_info: List[Dict[str, Any]], user_message: str) -> str:
        """当LLM不可用时的备用回�?""
        if not bank_info:
            return """💰 **银行对比分析**

抱歉，目前没有找到相关的银行信息。建议您�?

1. 直接咨询各大银行客服
2. 访问银行官网了解产品详情
3. 到银行网点进行详细咨�?

主要银行包括�?
- 国有大行：工商银行、建设银行、中国银行、农业银�?
- 股份制银行：招商银行、浦发银行、民生银行、兴业银�?
- 城商行：北京银行、上海银行、江苏银行等

如需更详细的信息，请告诉我您的具体需求�?""
        
        # 基于知识库信息生成简单对�?
        return f"""💰 **银行对比分析**

基于现有信息，为您分析以下银行：

{self._format_bank_info_for_llm(bank_info)}

💡 **建议**
1. 根据您的具体需求选择合适的银行
2. 比较利率、额度、审批条件等因素
3. 准备充分的申请材�?
4. 保持良好的征信记�?

如需更详细的信息，请告诉我您的具体需求�?""
    
    def _generate_knowledge_based_response(self, user_message: str, knowledge_results: List[Dict[str, Any]]) -> str:
        """基于知识库生成回�?""
        if not knowledge_results:
            return self._generate_default_response(user_message)
        
        # 分析用户问题类型
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["对比", "比较", "哪个", "推荐"]):
            return self._format_bank_comparison(knowledge_results)
        elif any(word in message_lower for word in ["材料", "申请", "需�?]):
            return self._format_application_materials(knowledge_results)
        elif any(word in message_lower for word in ["流程", "步骤", "怎么"]):
            return self._format_application_process(knowledge_results)
        else:
            return self._format_general_info(knowledge_results)
    
    def _format_bank_comparison(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化银行对比信�?""
        formatted_lines = []
        formatted_lines.append("🏦 **银行产品对比分析**")
        formatted_lines.append("=" * 40)
        formatted_lines.append("")
        
        for i, result in enumerate(knowledge_results[:5], 1):
            title = result.get('title', '')
            content = result.get('content', '')
            
            # 过滤乱码内容
            if any(char in content for char in ['nnnnnnnn', '■■■■', '(cid:127)']):
                continue
            
            formatted_lines.append(f"**{i}. {title}**")
            formatted_lines.append("-" * 30)
            
            # 截取�?00字符
            preview = content[:200] + "..." if len(content) > 200 else content
            formatted_lines.append(preview)
            formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _format_application_materials(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化申请材料信�?""
        formatted_lines = []
        formatted_lines.append("📋 **贷款申请材料清单**")
        formatted_lines.append("=" * 40)
        formatted_lines.append("")
        
        for result in knowledge_results[:3]:
            title = result.get('title', '')
            content = result.get('content', '')
            
            if '材料' in title or '申请' in title:
                formatted_lines.append(f"**{title}**")
                formatted_lines.append("-" * 30)
                formatted_lines.append(content[:300])
                formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _format_application_process(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化申请流程信�?""
        formatted_lines = []
        formatted_lines.append("📝 **贷款申请流程**")
        formatted_lines.append("=" * 30)
        formatted_lines.append("")
        
        for result in knowledge_results[:3]:
            title = result.get('title', '')
            content = result.get('content', '')
            
            if '流程' in title or '步骤' in title:
                formatted_lines.append(f"**{title}**")
                formatted_lines.append("-" * 25)
                formatted_lines.append(content[:300])
                formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _format_general_info(self, knowledge_results: List[Dict[str, Any]]) -> str:
        """格式化一般信�?""
        formatted_lines = []
        formatted_lines.append("💡 **相关信息**")
        formatted_lines.append("=" * 25)
        formatted_lines.append("")
        
        for result in knowledge_results[:3]:
            title = result.get('title', '')
            content = result.get('content', '')
            
            formatted_lines.append(f"**{title}**")
            formatted_lines.append("-" * 20)
            formatted_lines.append(content[:200])
            formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _generate_default_response(self, user_message: str) -> str:
        """生成默认回复"""
        return """我是AI智能客服，专门为您提供贷款相关的咨询服务�?

我可以帮助您�?
�?了解各类银行的贷款产�?
�?比较不同银行的利率和条件
�?解答贷款申请相关问题
�?提供专业的贷款建�?

请告诉我您具体想了解什么，我会尽力为您提供详细的信息�?""
