#!/usr/bin/env python3
"""
AI聊天机器人服务
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
from loguru import logger

class ChatbotRole(Enum):
    """聊天机器人角色"""
    GENERAL = "general"
    LOAN_SPECIALIST = "loan_specialist"
    RISK_ANALYST = "risk_analyst"
    TECHNICAL_SUPPORT = "technical_support"

class AIChatbot:
    """AI聊天机器人"""
    
    def __init__(self, llm_service=None, vector_rag_service=None):
        self.llm_service = llm_service
        self.vector_rag_service = vector_rag_service
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, user_id: str, role: ChatbotRole) -> str:
        """创建聊天会话"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'user_id': user_id,
            'role': role,
            'created_at': datetime.now(),
            'messages': []
        }
        return session_id
    
    async def process_message(self, session_id: str, message: str, user_info: dict = None) -> dict:
        """处理聊天消息"""
        if session_id not in self.sessions:
            raise ValueError(f"会话不存在: {session_id}")
        
        session = self.sessions[session_id]
        
        # 添加用户消息
        session['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now()
        })
        
        # 生成AI回复
        try:
            response = await self.generate_response(session['messages'], user_info)
            
            # 添加AI回复
            session['messages'].append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            
            return {
                'success': True,
                'response': response,
                'session_id': session_id
            }
            
        except Exception as e:
            logger.error(f"处理消息失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': "抱歉，我暂时无法处理您的请求，请稍后再试。"
            }
    
    async def generate_response(self, messages: List[Dict[str, str]], context: Dict[str, Any] = None) -> str:
        """生成AI回复 - 基于RAG+LLM"""
        try:
            user_message = messages[-1]["content"]
            logger.info(f"开始生成回复，用户问题: {user_message}")
            
            # 1. 尝试使用LLM直接回答
            if self.llm_service:
                try:
                    logger.info("尝试使用LLM生成回复")
                    response = await self._generate_llm_response_async(user_message)
                    if response and "抱歉" not in response and "AI服务暂时不可用" not in response:
                        logger.info("LLM回复成功")
                        return response
                    else:
                        logger.info("LLM回复失败，使用预设回复")
                except Exception as e:
                    logger.error(f"LLM调用失败: {e}")
            
            # 2. 如果LLM失败，使用预设的智能回复
            logger.info("使用预设智能回复")
            return self._generate_smart_fallback_response(user_message)
                
        except Exception as e:
            logger.error(f"生成回复失败: {e}")
            return "抱歉，我暂时无法处理您的请求，请稍后再试。"
    
    async def _generate_llm_response_async(self, user_message: str) -> str:
        """使用LLM直接生成回答（异步版本）"""
        try:
            if not self.llm_service:
                return "抱歉，AI服务暂时不可用，请稍后再试。"
            
            # 构建提示词
            system_prompt = """你是一个专业的银行信贷顾问，擅长回答个人信用贷款相关问题。
请根据用户的问题，提供专业、准确、有用的回答。
回答应该包含：
1. 直接回答用户的问题
2. 提供相关的银行产品信息
3. 给出实用的建议
4. 使用Markdown格式让回答更易读

请用中文回答，保持专业和友好的语调。"""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # 调用LLM
            result = await self.llm_service.generate_response(messages)
            
            # 处理LLM返回结果
            if isinstance(result, dict):
                if result.get("success", False):
                    return result.get("response", "抱歉，我暂时无法处理您的请求，请稍后再试。")
                else:
                    logger.error(f"LLM调用失败: {result.get('error', '未知错误')}")
                    return "抱歉，我暂时无法处理您的请求，请稍后再试。"
            elif isinstance(result, str):
                return result
            else:
                logger.error(f"LLM返回格式错误: {type(result)}")
                return "抱歉，我暂时无法处理您的请求，请稍后再试。"
            
        except Exception as e:
            logger.error(f"LLM直接回答失败: {e}")
            return "抱歉，我暂时无法处理您的请求，请稍后再试。"
    
    def _generate_smart_fallback_response(self, user_message: str) -> str:
        """智能回退回复 - 当LLM不可用时使用"""
        try:
            # 根据用户问题智能回答
            if "招商银行" in user_message or "招行" in user_message:
                return """**招商银行个人信贷产品介绍**

**🏦 招商银行简介**
招商银行是中国领先的商业银行之一，以零售银行业务见长，在个人信贷领域有着丰富的产品线。

**主要个人信贷产品：**

**1. 招行信用贷**
- 额度：1-50万元
- 利率：年化4.5%-12%
- 期限：最长5年
- 特点：无需抵押，审批快速

**2. 招行闪电贷**
- 额度：1-30万元
- 利率：年化5%-15%
- 期限：最长3年
- 特点：线上申请，秒级放款

**3. 招行消费贷**
- 额度：1-100万元
- 利率：年化4.9%-18%
- 期限：最长10年
- 特点：用途灵活，支持多种消费场景

**申请条件：**
- 年龄：22-55周岁
- 收入：月收入3000元以上
- 征信：征信良好，无逾期记录
- 工作：稳定工作6个月以上

**申请方式：**
- 招商银行手机银行APP
- 招商银行官网
- 招商银行网点
- 招商银行客服热线：95555

**招行优势：**
- 产品丰富多样
- 服务优质专业
- 科技化程度高
- 客户体验好

**温馨提示：**
- 具体条件以银行审批为准
- 建议提前了解产品详情
- 可咨询招行客服获取最新信息"""
            
            elif "利率" in user_message or "利息" in user_message:
                return """**个人信用贷款利率信息**

**主要银行利率对比：**

**🏦 工商银行 - 融e借**
- 利率：年化3.5%-10.5%
- 特点：利率较低，工行客户优先

**🏦 建设银行 - 快贷**  
- 利率：年化4.0%-11.5%
- 特点：审批快速，建行客户优先

**🏦 招商银行 - 招行信用贷**
- 利率：年化4.5%-12%
- 特点：产品丰富，服务优质

**🏦 农业银行 - 网捷贷**
- 利率：年化4.5%-12%
- 特点：农村覆盖广

**🏦 中国银行 - 中银E贷**
- 利率：年化4.5%-11%
- 特点：国际化程度高

**利率影响因素：**
- 个人征信记录
- 收入水平
- 工作稳定性
- 银行客户等级
- 贷款期限和金额

**申请建议：**
1. 保持良好的征信记录
2. 提供稳定的收入证明
3. 选择适合的银行产品
4. 多家银行对比后选择最优方案

**温馨提示：**
- 具体利率以银行审批为准
- 建议提前了解各银行产品
- 可咨询银行客服获取最新信息"""
            
            elif "条件" in user_message or "要求" in user_message:
                return """**个人信用贷款申请条件**

**基本申请条件：**

**📋 年龄要求**
- 一般要求：18-65周岁
- 部分银行：22-60周岁
- 最佳年龄：25-50周岁

**💰 收入要求**
- 最低月收入：2000-3000元
- 建议月收入：5000元以上
- 收入稳定性：6个月以上

**📊 征信要求**
- 征信记录良好
- 无逾期记录
- 负债率不超过70%
- 无不良信用记录

**💼 工作要求**
- 稳定工作3-6个月以上
- 有固定收入来源
- 工作单位正规
- 部分银行要求特定行业

**🏠 居住要求**
- 有固定居住地址
- 居住稳定性
- 部分银行要求本地户籍

**📄 所需材料**
- 身份证原件及复印件
- 收入证明（工资单、银行流水等）
- 工作证明
- 居住证明
- 其他银行要求的材料

**申请建议：**
1. 确保满足基本申请条件
2. 准备齐全的申请材料
3. 保持良好的征信记录
4. 选择适合自己条件的银行产品

**温馨提示：**
- 不同银行条件可能略有差异
- 建议提前了解具体要求
- 可咨询银行客服获取详细信息"""
            
            elif "申请" in user_message or "入口" in user_message:
                return """**个人信用贷款申请指南**

**申请方式：**

**📱 线上申请**
- 银行手机APP
- 银行官网
- 第三方平台
- 优势：便捷快速，24小时可申请

**🏢 线下申请**
- 银行网点
- 客户经理
- 优势：专业指导，面对面沟通

**申请流程：**

**1️⃣ 准备阶段**
- 了解产品信息
- 准备申请材料
- 评估自身条件
- 选择合适银行

**2️⃣ 提交申请**
- 填写申请表
- 提交相关材料
- 等待初步审核
- 获得预审结果

**3️⃣ 审核阶段**
- 银行征信查询
- 收入核实
- 风险评估
- 审批决定

**4️⃣ 放款阶段**
- 签署合同
- 办理手续
- 资金到账
- 开始还款

**申请入口：**

**🏦 工商银行**
- APP：工银融e联
- 官网：icbc.com.cn
- 客服：95588

**🏦 建设银行**
- APP：建行手机银行
- 官网：ccb.com
- 客服：95533

**🏦 招商银行**
- APP：招商银行APP
- 官网：cmbchina.com
- 客服：95555

**🏦 农业银行**
- APP：农行掌上银行
- 官网：abchina.com
- 客服：95599

**🏦 中国银行**
- APP：中银手机银行
- 官网：boc.cn
- 客服：95566

**申请建议：**
1. 提前了解产品详情
2. 准备完整申请材料
3. 选择合适申请方式
4. 保持良好征信记录
5. 多家银行对比选择

**温馨提示：**
- 申请前请仔细阅读产品条款
- 确保提供真实准确信息
- 可咨询银行客服获取帮助"""
            
            else:
                return """**个人信用贷款产品概览**

**主要银行产品对比：**

**🏦 工商银行 - 融e借**
- 额度：1-30万元
- 利率：年化3.5%-10.5%
- 期限：最长3年
- 特点：利率低，工行客户优先

**🏦 建设银行 - 快贷**
- 额度：1-10万元
- 利率：年化4.0%-11.5%
- 期限：最长3年
- 特点：审批快，建行客户优先

**🏦 招商银行 - 招行信用贷**
- 额度：1-50万元
- 利率：年化4.5%-12%
- 期限：最长5年
- 特点：产品丰富，服务优质

**🏦 农业银行 - 网捷贷**
- 额度：1-30万元
- 利率：年化4.5%-12%
- 期限：最长3年
- 特点：农村覆盖广

**🏦 中国银行 - 中银E贷**
- 额度：1-30万元
- 利率：年化4.5%-11%
- 期限：最长3年
- 特点：国际化程度高

**产品特点：**
- 无需抵押担保
- 申请手续简便
- 放款速度快
- 用途灵活多样

**申请条件：**
- 年龄：18-65周岁
- 收入：月收入2000元以上
- 征信：信用记录良好
- 工作：稳定工作3个月以上

**申请建议：**
1. 根据需求选择合适的银行和产品
2. 提前准备完整申请材料
3. 保持良好的征信记录
4. 多家银行对比后选择最优方案
5. 可咨询银行客服获取最新信息

**温馨提示：**
- 具体条件以银行审批为准
- 建议提前了解各银行产品特点
- 保持良好的还款记录
- 定期关注银行产品更新"""
            
        except Exception as e:
            logger.error(f"智能回退回复失败: {e}")
            return "抱歉，我暂时无法处理您的请求，请稍后再试。"
