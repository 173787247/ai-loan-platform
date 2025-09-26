"""
对话增强服务
提供智能对话理解、上下文管理和情感分析
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    """用户意图类型"""
    GREETING = "greeting"
    QUESTION = "question"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    REQUEST_HELP = "request_help"
    REQUEST_INFO = "request_info"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"

class EmotionType(Enum):
    """情感类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    CONFUSED = "confused"
    SATISFIED = "satisfied"

@dataclass
class ConversationContext:
    """对话上下文"""
    user_id: str
    session_id: str
    current_topic: str
    conversation_history: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    last_activity: datetime
    conversation_flow: str
    entities: Dict[str, Any]
    sentiment_score: float
    confidence_level: float

@dataclass
class IntentResult:
    """意图识别结果"""
    intent: IntentType
    confidence: float
    entities: Dict[str, Any]
    sentiment: EmotionType
    sentiment_score: float
    keywords: List[str]
    requires_clarification: bool

class ConversationEnhancer:
    """对话增强器"""
    
    def __init__(self, llm_service=None):
        self.llm_service = llm_service
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        
        # 意图识别关键词
        self.intent_keywords = {
            IntentType.GREETING: ["你好", "hi", "hello", "早上好", "下午好", "晚上好", "您好"],
            IntentType.QUESTION: ["什么", "怎么", "如何", "为什么", "哪里", "什么时候", "多少", "?", "？"],
            IntentType.COMPLAINT: ["问题", "错误", "不好", "不行", "失败", "投诉", "抱怨"],
            IntentType.COMPLIMENT: ["好", "棒", "优秀", "满意", "感谢", "谢谢"],
            IntentType.REQUEST_HELP: ["帮助", "帮忙", "协助", "支持", "指导"],
            IntentType.REQUEST_INFO: ["信息", "资料", "详情", "介绍", "说明"],
            IntentType.CLARIFICATION: ["澄清", "确认", "是不是", "对吗", "对吗"],
            IntentType.CONFIRMATION: ["是的", "对", "正确", "确认", "同意"],
            IntentType.GOODBYE: ["再见", "拜拜", "bye", "goodbye", "结束"]
        }
        
        # 情感分析关键词
        self.emotion_keywords = {
            EmotionType.POSITIVE: ["好", "棒", "优秀", "满意", "开心", "高兴", "喜欢"],
            EmotionType.NEGATIVE: ["不好", "差", "糟糕", "失望", "生气", "愤怒", "讨厌"],
            EmotionType.FRUSTRATED: ["烦", "急", "着急", "焦虑", "担心", "困惑"],
            EmotionType.EXCITED: ["兴奋", "激动", "期待", "兴奋", "惊喜"],
            EmotionType.CONFUSED: ["不懂", "不明白", "困惑", "疑惑", "不清楚"],
            EmotionType.SATISFIED: ["满意", "满足", "不错", "可以", "还行"]
        }
    
    def analyze_intent(self, message: str, context: ConversationContext = None) -> IntentResult:
        """分析用户意图"""
        try:
            message_lower = message.lower()
            intent_scores = {}
            
            # 基于关键词的意图识别
            for intent, keywords in self.intent_keywords.items():
                score = 0
                matched_keywords = []
                for keyword in keywords:
                    if keyword.lower() in message_lower:
                        score += 1
                        matched_keywords.append(keyword)
                intent_scores[intent] = {
                    'score': score,
                    'keywords': matched_keywords
                }
            
            # 选择得分最高的意图
            best_intent = max(intent_scores.items(), key=lambda x: x[1]['score'])
            intent_type = best_intent[0]
            confidence = min(best_intent[1]['score'] / len(self.intent_keywords[intent_type]), 1.0)
            
            # 情感分析
            sentiment_result = self.analyze_sentiment(message)
            
            # 实体提取
            entities = self.extract_entities(message)
            
            # 判断是否需要澄清
            requires_clarification = self._needs_clarification(message, context)
            
            return IntentResult(
                intent=intent_type,
                confidence=confidence,
                entities=entities,
                sentiment=sentiment_result['emotion'],
                sentiment_score=sentiment_result['score'],
                keywords=best_intent[1]['keywords'],
                requires_clarification=requires_clarification
            )
            
        except Exception as e:
            logger.error(f"意图分析失败: {e}")
            return IntentResult(
                intent=IntentType.UNKNOWN,
                confidence=0.0,
                entities={},
                sentiment=EmotionType.NEUTRAL,
                sentiment_score=0.0,
                keywords=[],
                requires_clarification=False
            )
    
    def analyze_sentiment(self, message: str) -> Dict[str, Any]:
        """情感分析"""
        try:
            message_lower = message.lower()
            emotion_scores = {}
            
            for emotion, keywords in self.emotion_keywords.items():
                score = 0
                for keyword in keywords:
                    if keyword.lower() in message_lower:
                        score += 1
                emotion_scores[emotion] = score
            
            # 选择得分最高的情感
            best_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            emotion_type = best_emotion[0]
            score = min(best_emotion[1] / len(self.emotion_keywords[emotion_type]), 1.0)
            
            return {
                'emotion': emotion_type,
                'score': score
            }
            
        except Exception as e:
            logger.error(f"情感分析失败: {e}")
            return {
                'emotion': EmotionType.NEUTRAL,
                'score': 0.0
            }
    
    def extract_entities(self, message: str) -> Dict[str, Any]:
        """实体提取"""
        entities = {}
        
        # 提取金额
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(?:万|千|百|元|块|块钱)'
        amounts = re.findall(amount_pattern, message)
        if amounts:
            entities['amounts'] = amounts
        
        # 提取银行名称
        bank_pattern = r'(招商银行|工商银行|建设银行|农业银行|中国银行|交通银行|民生银行|兴业银行|浦发银行|光大银行)'
        banks = re.findall(bank_pattern, message)
        if banks:
            entities['banks'] = banks
        
        # 提取贷款类型
        loan_types = ['个人信用贷款', '经营贷款', '房贷', '车贷', '消费贷款', '企业贷款']
        found_loan_types = [loan_type for loan_type in loan_types if loan_type in message]
        if found_loan_types:
            entities['loan_types'] = found_loan_types
        
        # 提取时间
        time_pattern = r'(\d+)\s*(?:年|月|日|天|小时|分钟)'
        times = re.findall(time_pattern, message)
        if times:
            entities['times'] = times
        
        return entities
    
    def _needs_clarification(self, message: str, context: ConversationContext = None) -> bool:
        """判断是否需要澄清"""
        if not context:
            return False
        
        # 检查是否有模糊的代词
        ambiguous_pronouns = ['它', '这个', '那个', '这样', '那样']
        if any(pronoun in message for pronoun in ambiguous_pronouns):
            return True
        
        # 检查是否有多个可能的解释
        if len(message.split()) < 3:  # 消息太短
            return True
        
        return False
    
    def update_context(self, session_id: str, message: str, intent_result: IntentResult) -> ConversationContext:
        """更新对话上下文"""
        if session_id not in self.conversation_contexts:
            self.conversation_contexts[session_id] = ConversationContext(
                user_id="",
                session_id=session_id,
                current_topic="",
                conversation_history=[],
                user_preferences={},
                last_activity=datetime.now(),
                conversation_flow="",
                entities={},
                sentiment_score=0.0,
                confidence_level=0.0
            )
        
        context = self.conversation_contexts[session_id]
        
        # 更新上下文信息
        context.last_activity = datetime.now()
        context.sentiment_score = intent_result.sentiment_score
        context.confidence_level = intent_result.confidence
        
        # 更新实体信息
        context.entities.update(intent_result.entities)
        
        # 更新话题
        if intent_result.intent == IntentType.QUESTION:
            context.current_topic = self._extract_topic(message)
        
        # 更新对话历史
        context.conversation_history.append({
            'message': message,
            'intent': intent_result.intent.value,
            'sentiment': intent_result.sentiment.value,
            'timestamp': datetime.now().isoformat()
        })
        
        # 保持历史记录在合理范围内
        if len(context.conversation_history) > 20:
            context.conversation_history = context.conversation_history[-20:]
        
        return context
    
    def _extract_topic(self, message: str) -> str:
        """提取话题"""
        # 简单的关键词匹配来提取话题
        topic_keywords = {
            '贷款': ['贷款', '借贷', '借款', '融资'],
            '利率': ['利率', '利息', '费率', '成本'],
            '申请': ['申请', '办理', '提交', '流程'],
            '条件': ['条件', '要求', '资格', '门槛'],
            '材料': ['材料', '资料', '证件', '文件']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message for keyword in keywords):
                return topic
        
        return "一般咨询"
    
    def generate_contextual_response(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """生成上下文相关的响应"""
        response_strategies = {
            IntentType.GREETING: self._handle_greeting,
            IntentType.QUESTION: self._handle_question,
            IntentType.COMPLAINT: self._handle_complaint,
            IntentType.COMPLIMENT: self._handle_compliment,
            IntentType.REQUEST_HELP: self._handle_help_request,
            IntentType.REQUEST_INFO: self._handle_info_request,
            IntentType.CLARIFICATION: self._handle_clarification,
            IntentType.CONFIRMATION: self._handle_confirmation,
            IntentType.GOODBYE: self._handle_goodbye
        }
        
        handler = response_strategies.get(intent_result.intent, self._handle_unknown)
        return handler(intent_result, context)
    
    def _handle_greeting(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理问候"""
        greetings = [
            "您好！我是AI智能客服，很高兴为您服务！",
            "您好！有什么可以帮助您的吗？",
            "欢迎！我是您的专属AI助手，请告诉我您需要什么帮助。"
        ]
        
        return {
            'response': greetings[0],
            'suggestions': ['贷款咨询', '利率查询', '申请流程', '常见问题'],
            'emotion': 'friendly'
        }
    
    def _handle_question(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理问题"""
        if intent_result.requires_clarification:
            return {
                'response': "您的问题我需要更多信息来准确回答。能否详细说明一下您的具体需求？",
                'suggestions': ['具体说明', '举例说明', '重新提问'],
                'emotion': 'helpful'
            }
        
        return {
            'response': "我来为您详细解答这个问题。",
            'suggestions': ['了解更多', '相关咨询', '申请办理'],
            'emotion': 'helpful'
        }
    
    def _handle_complaint(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理投诉"""
        return {
            'response': "非常抱歉给您带来不便。我会认真记录您的问题并尽快为您解决。",
            'suggestions': ['详细说明问题', '联系人工客服', '提交反馈'],
            'emotion': 'apologetic'
        }
    
    def _handle_compliment(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理赞美"""
        return {
            'response': "谢谢您的认可！我会继续努力为您提供更好的服务。",
            'suggestions': ['继续咨询', '推荐给朋友', '评价服务'],
            'emotion': 'grateful'
        }
    
    def _handle_help_request(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理帮助请求"""
        return {
            'response': "我很乐意为您提供帮助！请告诉我您需要什么具体的帮助。",
            'suggestions': ['操作指导', '功能介绍', '问题解答'],
            'emotion': 'helpful'
        }
    
    def _handle_info_request(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理信息请求"""
        return {
            'response': "我来为您提供相关信息。",
            'suggestions': ['详细信息', '相关链接', '下载资料'],
            'emotion': 'informative'
        }
    
    def _handle_clarification(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理澄清请求"""
        return {
            'response': "让我为您澄清一下。",
            'suggestions': ['详细说明', '举例说明', '继续咨询'],
            'emotion': 'clarifying'
        }
    
    def _handle_confirmation(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理确认"""
        return {
            'response': "好的，我明白了。",
            'suggestions': ['继续下一步', '了解更多', '其他问题'],
            'emotion': 'confirming'
        }
    
    def _handle_goodbye(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理告别"""
        return {
            'response': "再见！感谢您的咨询，祝您生活愉快！",
            'suggestions': ['再次咨询', '评价服务', '推荐朋友'],
            'emotion': 'friendly'
        }
    
    def _handle_unknown(self, intent_result: IntentResult, context: ConversationContext) -> Dict[str, Any]:
        """处理未知意图"""
        return {
            'response': "抱歉，我没有完全理解您的意思。能否换个方式表达一下？",
            'suggestions': ['重新提问', '具体说明', '寻求帮助'],
            'emotion': 'confused'
        }
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """获取对话摘要"""
        if session_id not in self.conversation_contexts:
            return {}
        
        context = self.conversation_contexts[session_id]
        
        return {
            'session_id': session_id,
            'conversation_count': len(context.conversation_history),
            'current_topic': context.current_topic,
            'sentiment_trend': self._calculate_sentiment_trend(context),
            'key_entities': context.entities,
            'last_activity': context.last_activity.isoformat(),
            'conversation_flow': context.conversation_flow
        }
    
    def _calculate_sentiment_trend(self, context: ConversationContext) -> str:
        """计算情感趋势"""
        if len(context.conversation_history) < 2:
            return "stable"
        
        recent_sentiments = [msg.get('sentiment', 'neutral') for msg in context.conversation_history[-5:]]
        positive_count = sum(1 for s in recent_sentiments if s in ['positive', 'satisfied', 'excited'])
        negative_count = sum(1 for s in recent_sentiments if s in ['negative', 'frustrated'])
        
        if positive_count > negative_count:
            return "improving"
        elif negative_count > positive_count:
            return "declining"
        else:
            return "stable"
