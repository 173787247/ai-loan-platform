#!/usr/bin/env python3
"""
信息提取服务
使用LLM进行自然语言信息提取和结构化
"""

import json
import re
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class InformationExtractor:
    """信息提取器"""
    
    def __init__(self, llm_service=None):
        self.llm_service = llm_service
        
        # 预定义的正则表达式模式
        self.patterns = {
            "phone": r"1[3-9]\d{9}",
            "id_card": r"\d{17}[\dXx]",
            "amount": r"(\d+(?:\.\d+)?)\s*万",
            "income": r"月收入[：:]?\s*(\d+(?:\.\d+)?)\s*元",
            "term": r"(\d+)\s*个月?",
            "credit_score": r"信用评分[：:]?\s*(\d+)",
            "debt_payment": r"月还款[：:]?\s*(\d+(?:\.\d+)?)\s*元"
        }
    
    async def extract_basic_info(self, message: str) -> Dict[str, Any]:
        """提取基本信息"""
        try:
            if self.llm_service:
                # 使用LLM提取信息
                prompt = f"""
请从以下用户消息中提取基本信息，返回JSON格式：
{message}

需要提取的字段：
- name: 姓名
- phone: 电话号码
- id_card: 身份证号（如果有）

返回格式：
{{"name": "张三", "phone": "13800138000", "id_card": ""}}
"""
                
                response = await self._call_llm(prompt)
                if response:
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError:
                        pass
            
            # 回退到正则表达式提取
            result = {}
            
            # 提取姓名（简单模式）
            name_match = re.search(r"我叫([^，,，\s]+)", message)
            if name_match:
                result["name"] = name_match.group(1)
            
            # 提取电话
            phone_match = re.search(self.patterns["phone"], message)
            if phone_match:
                result["phone"] = phone_match.group(0)
            
            # 提取身份证
            id_match = re.search(self.patterns["id_card"], message)
            if id_match:
                result["id_card"] = id_match.group(0)
            
            return result
            
        except Exception as e:
            logger.error(f"提取基本信息失败: {e}")
            return {}
    
    async def extract_loan_need(self, message: str) -> Dict[str, Any]:
        """提取贷款需求"""
        try:
            if self.llm_service:
                prompt = f"""
请从以下用户消息中提取贷款需求信息，返回JSON格式：
{message}

需要提取的字段：
- purpose: 贷款用途（消费/经营/教育/医疗/旅游/装修/其他）
- amount: 申请金额（万元）
- term: 贷款期限（月）
- region: 申请地区

返回格式：
{{"purpose": "装修", "amount": 30, "term": 24, "region": "北京"}}
"""
                
                response = await self._call_llm(prompt)
                if response:
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError:
                        pass
            
            # 回退到正则表达式提取
            result = {}
            
            # 提取金额
            amount_match = re.search(self.patterns["amount"], message)
            if amount_match:
                result["amount"] = float(amount_match.group(1))
            
            # 提取期限
            term_match = re.search(self.patterns["term"], message)
            if term_match:
                result["term"] = int(term_match.group(1))
            
            # 提取用途
            purpose_keywords = {
                "消费": ["消费", "购物", "生活"],
                "经营": ["经营", "生意", "创业", "投资"],
                "教育": ["教育", "培训", "学习", "学费"],
                "医疗": ["医疗", "看病", "治疗", "手术"],
                "旅游": ["旅游", "旅行", "度假"],
                "装修": ["装修", "装潢", "翻新"],
                "其他": ["其他", "其他用途"]
            }
            
            for purpose, keywords in purpose_keywords.items():
                if any(keyword in message for keyword in keywords):
                    result["purpose"] = purpose
                    break
            
            # 提取地区
            region_keywords = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "重庆"]
            for region in region_keywords:
                if region in message:
                    result["region"] = region
                    break
            
            return result
            
        except Exception as e:
            logger.error(f"提取贷款需求失败: {e}")
            return {}
    
    async def extract_income_info(self, message: str) -> Dict[str, Any]:
        """提取收入信息"""
        try:
            if self.llm_service:
                prompt = f"""
请从以下用户消息中提取收入信息，返回JSON格式：
{message}

需要提取的字段：
- monthly_income: 月收入（元）
- income_source: 收入来源（工资/经营/其他）
- work_years: 工作年限（年）

返回格式：
{{"monthly_income": 8000, "income_source": "工资", "work_years": 3}}
"""
                
                response = await self._call_llm(prompt)
                if response:
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError:
                        pass
            
            # 回退到正则表达式提取
            result = {}
            
            # 提取月收入
            income_match = re.search(self.patterns["income"], message)
            if income_match:
                result["monthly_income"] = float(income_match.group(1))
            
            # 提取收入来源
            if "工资" in message or "薪水" in message:
                result["income_source"] = "工资"
            elif "经营" in message or "生意" in message:
                result["income_source"] = "经营"
            else:
                result["income_source"] = "其他"
            
            # 提取工作年限
            work_match = re.search(r"工作(\d+)年", message)
            if work_match:
                result["work_years"] = int(work_match.group(1))
            
            return result
            
        except Exception as e:
            logger.error(f"提取收入信息失败: {e}")
            return {}
    
    async def extract_debt_info(self, message: str) -> Dict[str, Any]:
        """提取负债信息"""
        try:
            if self.llm_service:
                prompt = f"""
请从以下用户消息中提取负债信息，返回JSON格式：
{message}

需要提取的字段：
- monthly_debt_payment: 月还款额（元）
- existing_loans: 现有贷款列表（JSON数组）

返回格式：
{{"monthly_debt_payment": 3500, "existing_loans": [{{"type": "房贷", "amount": 3000}}, {{"type": "信用卡", "amount": 500}}]}}
"""
                
                response = await self._call_llm(prompt)
                if response:
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError:
                        pass
            
            # 回退到正则表达式提取
            result = {}
            
            # 提取月还款额
            debt_match = re.search(self.patterns["debt_payment"], message)
            if debt_match:
                result["monthly_debt_payment"] = float(debt_match.group(1))
            
            # 简单提取现有贷款
            existing_loans = []
            if "房贷" in message:
                mortgage_match = re.search(r"房贷[月供]?[：:]?\s*(\d+(?:\.\d+)?)\s*元", message)
                if mortgage_match:
                    existing_loans.append({
                        "type": "房贷",
                        "amount": float(mortgage_match.group(1))
                    })
            
            if "信用卡" in message:
                credit_match = re.search(r"信用卡[月还款]?[：:]?\s*(\d+(?:\.\d+)?)\s*元", message)
                if credit_match:
                    existing_loans.append({
                        "type": "信用卡",
                        "amount": float(credit_match.group(1))
                    })
            
            result["existing_loans"] = existing_loans
            
            return result
            
        except Exception as e:
            logger.error(f"提取负债信息失败: {e}")
            return {}
    
    async def extract_credit_info(self, message: str) -> Dict[str, Any]:
        """提取信用信息"""
        try:
            if self.llm_service:
                prompt = f"""
请从以下用户消息中提取信用信息，返回JSON格式：
{message}

需要提取的字段：
- credit_score: 信用评分（数字）
- credit_history: 信用历史描述

返回格式：
{{"credit_score": 750, "credit_history": "没有逾期记录"}}
"""
                
                response = await self._call_llm(prompt)
                if response:
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError:
                        pass
            
            # 回退到正则表达式提取
            result = {}
            
            # 提取信用评分
            score_match = re.search(self.patterns["credit_score"], message)
            if score_match:
                result["credit_score"] = int(score_match.group(1))
            
            # 提取信用历史
            if "逾期" in message or "违约" in message:
                result["credit_history"] = "有逾期记录"
            elif "良好" in message or "优秀" in message:
                result["credit_history"] = "信用记录良好"
            else:
                result["credit_history"] = "信用记录一般"
            
            return result
            
        except Exception as e:
            logger.error(f"提取信用信息失败: {e}")
            return {}
    
    async def _call_llm(self, prompt: str) -> Optional[str]:
        """调用LLM服务"""
        try:
            if not self.llm_service:
                return None
            
            # 这里应该调用实际的LLM服务
            # 暂时返回None，使用正则表达式回退
            return None
            
        except Exception as e:
            logger.error(f"调用LLM失败: {e}")
            return None
