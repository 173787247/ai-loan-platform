"""
多轮对话管理器
支持复杂的多轮对话场景和上下文管理
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid

class DialogState(Enum):
    """对话状态"""
    INITIAL = "initial"
    GREETING = "greeting"
    TOPIC_EXPLORATION = "topic_exploration"
    DETAILED_INQUIRY = "detailed_inquiry"
    CLARIFICATION = "clarification"
    SOLUTION_PRESENTATION = "solution_presentation"
    CONFIRMATION = "confirmation"
    FOLLOW_UP = "follow_up"
    CLOSING = "closing"

class DialogIntent(Enum):
    """对话意图"""
    EXPLORE_TOPIC = "explore_topic"
    SEEK_DETAILS = "seek_details"
    REQUEST_CLARIFICATION = "request_clarification"
    PROVIDE_INFORMATION = "provide_information"
    COMPARE_OPTIONS = "compare_options"
    MAKE_DECISION = "make_decision"
    SEEK_ALTERNATIVES = "seek_alternatives"
    END_CONVERSATION = "end_conversation"

@dataclass
class DialogContext:
    """对话上下文"""
    session_id: str
    user_id: str
    current_state: DialogState
    current_topic: str
    conversation_history: List[Dict[str, Any]]
    pending_questions: List[str]
    resolved_questions: List[str]
    user_preferences: Dict[str, Any]
    conversation_goals: List[str]
    last_activity: datetime
    turn_count: int
    context_entities: Dict[str, Any]
    conversation_flow: List[DialogState]

@dataclass
class DialogResponse:
    """对话响应"""
    response_text: str
    next_state: DialogState
    suggested_questions: List[str]
    follow_up_actions: List[str]
    confidence: float
    requires_clarification: bool
    context_updates: Dict[str, Any]

class MultiTurnDialogManager:
    """多轮对话管理器"""
    
    def __init__(self, conversation_enhancer=None, knowledge_enhancer=None):
        self.conversation_enhancer = conversation_enhancer
        self.knowledge_enhancer = knowledge_enhancer
        self.dialog_contexts: Dict[str, DialogContext] = {}
        
        # 对话流程模板
        self.dialog_templates = self._initialize_dialog_templates()
        
        # 状态转换规则
        self.state_transitions = self._initialize_state_transitions()
    
    def _initialize_dialog_templates(self) -> Dict[str, Dict[str, Any]]:
        """初始化对话模板"""
        return {
            "loan_inquiry": {
                "initial": "您好！我是AI贷款顾问，请问您想了解什么类型的贷款产品？",
                "exploration": "请告诉我更多关于您的贷款需求，比如用途、金额、期限等。",
                "clarification": "为了给您更准确的建议，能否详细说明一下您的具体情况？",
                "solution": "根据您的需求，我为您推荐以下贷款方案：",
                "follow_up": "您对这些方案还有什么疑问吗？"
            },
            "rate_inquiry": {
                "initial": "您想了解哪个银行的贷款利率？",
                "exploration": "请告诉我您关注的贷款类型和金额范围。",
                "comparison": "让我为您对比几家银行的利率情况：",
                "follow_up": "您还需要了解其他相关信息吗？"
            }
        }
    
    def _initialize_state_transitions(self) -> Dict[DialogState, List[DialogState]]:
        """初始化状态转换规则"""
        return {
            DialogState.INITIAL: [DialogState.GREETING],
            DialogState.GREETING: [DialogState.TOPIC_EXPLORATION, DialogState.DETAILED_INQUIRY],
            DialogState.TOPIC_EXPLORATION: [DialogState.DETAILED_INQUIRY, DialogState.CLARIFICATION],
            DialogState.DETAILED_INQUIRY: [DialogState.SOLUTION_PRESENTATION, DialogState.CLARIFICATION],
            DialogState.CLARIFICATION: [DialogState.DETAILED_INQUIRY, DialogState.SOLUTION_PRESENTATION],
            DialogState.SOLUTION_PRESENTATION: [DialogState.CONFIRMATION, DialogState.FOLLOW_UP],
            DialogState.CONFIRMATION: [DialogState.FOLLOW_UP, DialogState.CLOSING],
            DialogState.FOLLOW_UP: [DialogState.DETAILED_INQUIRY, DialogState.CLOSING],
            DialogState.CLOSING: [DialogState.INITIAL]
        }
    
    def start_dialog(self, session_id: str, user_id: str, initial_message: str = None) -> DialogContext:
        """开始对话"""
        context = DialogContext(
            session_id=session_id,
            user_id=user_id,
            current_state=DialogState.INITIAL,
            current_topic="",
            conversation_history=[],
            pending_questions=[],
            resolved_questions=[],
            user_preferences={},
            conversation_goals=[],
            last_activity=datetime.now(),
            turn_count=0,
            context_entities={},
            conversation_flow=[]
        )
        
        self.dialog_contexts[session_id] = context
        
        if initial_message:
            self.process_message(session_id, initial_message)
        
        logger.info(f"开始多轮对话: {session_id}")
        return context
    
    def process_message(self, session_id: str, message: str) -> DialogResponse:
        """处理对话消息"""
        if session_id not in self.dialog_contexts:
            raise ValueError(f"对话上下文不存在: {session_id}")
        
        context = self.dialog_contexts[session_id]
        
        # 更新对话历史
        context.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "turn": context.turn_count + 1
        })
        
        context.turn_count += 1
        context.last_activity = datetime.now()
        
        # 分析消息意图
        intent_result = self._analyze_message_intent(message, context)
        
        # 更新上下文
        self._update_context_from_intent(context, intent_result)
        
        # 生成响应
        response = self._generate_dialog_response(context, intent_result)
        
        # 更新对话历史
        context.conversation_history.append({
            "role": "assistant",
            "content": response.response_text,
            "timestamp": datetime.now().isoformat(),
            "turn": context.turn_count,
            "state": response.next_state.value,
            "confidence": response.confidence
        })
        
        # 更新状态
        context.current_state = response.next_state
        context.conversation_flow.append(response.next_state)
        
        # 更新上下文
        context.context_entities.update(response.context_updates)
        
        return response
    
    def _analyze_message_intent(self, message: str, context: DialogContext) -> Dict[str, Any]:
        """分析消息意图"""
        if self.conversation_enhancer:
            intent_result = self.conversation_enhancer.analyze_intent(message, context)
            return {
                "intent": intent_result.intent.value,
                "confidence": intent_result.confidence,
                "entities": intent_result.entities,
                "sentiment": intent_result.sentiment.value,
                "requires_clarification": intent_result.requires_clarification
            }
        else:
            # 简单的关键词匹配
            return self._simple_intent_analysis(message)
    
    def _simple_intent_analysis(self, message: str) -> Dict[str, Any]:
        """简单的意图分析"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["你好", "hi", "hello"]):
            return {"intent": "greeting", "confidence": 0.8, "entities": {}, "sentiment": "positive", "requires_clarification": False}
        elif any(word in message_lower for word in ["什么", "怎么", "如何", "为什么"]):
            return {"intent": "question", "confidence": 0.7, "entities": {}, "sentiment": "neutral", "requires_clarification": False}
        elif any(word in message_lower for word in ["谢谢", "感谢", "好的", "明白"]):
            return {"intent": "confirmation", "confidence": 0.8, "entities": {}, "sentiment": "positive", "requires_clarification": False}
        elif any(word in message_lower for word in ["再见", "拜拜", "结束"]):
            return {"intent": "goodbye", "confidence": 0.9, "entities": {}, "sentiment": "neutral", "requires_clarification": False}
        else:
            return {"intent": "unknown", "confidence": 0.3, "entities": {}, "sentiment": "neutral", "requires_clarification": True}
    
    def _update_context_from_intent(self, context: DialogContext, intent_result: Dict[str, Any]) -> None:
        """根据意图更新上下文"""
        intent = intent_result["intent"]
        entities = intent_result.get("entities", {})
        
        # 更新实体信息
        context.context_entities.update(entities)
        
        # 根据意图更新话题
        if intent == "question" and "贷款" in intent_result.get("entities", {}).get("content", ""):
            context.current_topic = "loan_inquiry"
        elif intent == "question" and "利率" in intent_result.get("entities", {}).get("content", ""):
            context.current_topic = "rate_inquiry"
        
        # 更新用户偏好
        if "amount" in entities:
            context.user_preferences["loan_amount"] = entities["amount"]
        if "bank" in entities:
            context.user_preferences["preferred_bank"] = entities["bank"]
    
    def _generate_dialog_response(self, context: DialogContext, intent_result: Dict[str, Any]) -> DialogResponse:
        """生成对话响应"""
        current_state = context.current_state
        intent = intent_result["intent"]
        confidence = intent_result["confidence"]
        
        # 确定下一个状态
        next_state = self._determine_next_state(current_state, intent, context)
        
        # 生成响应文本
        response_text = self._generate_response_text(context, next_state, intent_result)
        
        # 生成建议问题
        suggested_questions = self._generate_suggested_questions(context, next_state)
        
        # 生成后续行动
        follow_up_actions = self._generate_follow_up_actions(context, next_state)
        
        # 确定是否需要澄清
        requires_clarification = intent_result.get("requires_clarification", False) or confidence < 0.5
        
        return DialogResponse(
            response_text=response_text,
            next_state=next_state,
            suggested_questions=suggested_questions,
            follow_up_actions=follow_up_actions,
            confidence=confidence,
            requires_clarification=requires_clarification,
            context_updates={}
        )
    
    def _determine_next_state(self, current_state: DialogState, intent: str, context: DialogContext) -> DialogState:
        """确定下一个状态"""
        # 基于当前状态和意图确定下一个状态
        if current_state == DialogState.INITIAL:
            return DialogState.GREETING
        elif current_state == DialogState.GREETING:
            if intent == "question":
                return DialogState.TOPIC_EXPLORATION
            else:
                return DialogState.DETAILED_INQUIRY
        elif current_state == DialogState.TOPIC_EXPLORATION:
            if intent == "question":
                return DialogState.DETAILED_INQUIRY
            else:
                return DialogState.CLARIFICATION
        elif current_state == DialogState.DETAILED_INQUIRY:
            if context.current_topic:
                return DialogState.SOLUTION_PRESENTATION
            else:
                return DialogState.CLARIFICATION
        elif current_state == DialogState.SOLUTION_PRESENTATION:
            return DialogState.CONFIRMATION
        elif current_state == DialogState.CONFIRMATION:
            return DialogState.FOLLOW_UP
        elif current_state == DialogState.FOLLOW_UP:
            if intent == "goodbye":
                return DialogState.CLOSING
            else:
                return DialogState.DETAILED_INQUIRY
        else:
            return DialogState.INITIAL
    
    def _generate_response_text(self, context: DialogContext, next_state: DialogState, intent_result: Dict[str, Any]) -> str:
        """生成响应文本"""
        topic = context.current_topic or "general"
        state_key = next_state.value
        
        # 获取模板
        if topic in self.dialog_templates and state_key in self.dialog_templates[topic]:
            template = self.dialog_templates[topic][state_key]
        else:
            template = self._get_default_template(next_state)
        
        # 个性化响应
        personalized_response = self._personalize_response(template, context, intent_result)
        
        return personalized_response
    
    def _get_default_template(self, state: DialogState) -> str:
        """获取默认模板"""
        templates = {
            DialogState.GREETING: "您好！我是AI助手，很高兴为您服务！",
            DialogState.TOPIC_EXPLORATION: "请告诉我更多详细信息，这样我能更好地帮助您。",
            DialogState.DETAILED_INQUIRY: "我需要了解更多细节来为您提供准确的建议。",
            DialogState.CLARIFICATION: "能否详细说明一下您的具体需求？",
            DialogState.SOLUTION_PRESENTATION: "根据您的需求，我为您提供以下建议：",
            DialogState.CONFIRMATION: "您觉得这个方案如何？",
            DialogState.FOLLOW_UP: "您还有其他问题吗？",
            DialogState.CLOSING: "感谢您的咨询，祝您生活愉快！"
        }
        return templates.get(state, "我明白了，请继续。")
    
    def _personalize_response(self, template: str, context: DialogContext, intent_result: Dict[str, Any]) -> str:
        """个性化响应"""
        # 基于用户偏好个性化
        if "preferred_bank" in context.user_preferences:
            template = template.replace("银行", context.user_preferences["preferred_bank"])
        
        if "loan_amount" in context.user_preferences:
            template = template.replace("金额", context.user_preferences["loan_amount"])
        
        # 基于情感调整语调
        sentiment = intent_result.get("sentiment", "neutral")
        if sentiment == "frustrated":
            template = "我理解您的困扰，" + template
        elif sentiment == "excited":
            template = "很高兴看到您这么感兴趣，" + template
        
        return template
    
    def _generate_suggested_questions(self, context: DialogContext, next_state: DialogState) -> List[str]:
        """生成建议问题"""
        suggestions = []
        
        if next_state == DialogState.TOPIC_EXPLORATION:
            suggestions = [
                "您想了解什么类型的贷款？",
                "您的贷款用途是什么？",
                "您希望贷款多少金额？"
            ]
        elif next_state == DialogState.DETAILED_INQUIRY:
            suggestions = [
                "请告诉我您的收入情况",
                "您的信用记录如何？",
                "您希望多长期限？"
            ]
        elif next_state == DialogState.SOLUTION_PRESENTATION:
            suggestions = [
                "这个方案适合我吗？",
                "还有其他选择吗？",
                "如何申请这个产品？"
            ]
        
        return suggestions[:3]  # 最多3个建议
    
    def _generate_follow_up_actions(self, context: DialogContext, next_state: DialogState) -> List[str]:
        """生成后续行动"""
        actions = []
        
        if next_state == DialogState.SOLUTION_PRESENTATION:
            actions = ["查看详细产品信息", "开始申请流程", "对比其他产品"]
        elif next_state == DialogState.CONFIRMATION:
            actions = ["确认申请", "修改需求", "了解更多信息"]
        
        return actions
    
    def get_dialog_summary(self, session_id: str) -> Dict[str, Any]:
        """获取对话摘要"""
        if session_id not in self.dialog_contexts:
            return {}
        
        context = self.dialog_contexts[session_id]
        
        return {
            "session_id": session_id,
            "turn_count": context.turn_count,
            "current_state": context.current_state.value,
            "current_topic": context.current_topic,
            "conversation_goals": context.conversation_goals,
            "resolved_questions": context.resolved_questions,
            "pending_questions": context.pending_questions,
            "last_activity": context.last_activity.isoformat(),
            "conversation_flow": [state.value for state in context.conversation_flow]
        }
    
    def end_dialog(self, session_id: str) -> Dict[str, Any]:
        """结束对话"""
        if session_id in self.dialog_contexts:
            context = self.dialog_contexts[session_id]
            context.current_state = DialogState.CLOSING
            context.last_activity = datetime.now()
            
            summary = self.get_dialog_summary(session_id)
            del self.dialog_contexts[session_id]
            
            logger.info(f"结束多轮对话: {session_id}")
            return summary
        
        return {}
