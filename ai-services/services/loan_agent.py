#!/usr/bin/env python3
"""
AI贷款智能体核心服务
实现：对话引导收集要素 → 结构化申请 → 调用风控/定价/征信 → 生成可解释方案
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from .information_extractor import InformationExtractor
from .risk_pricing_service import RiskPricingService

logger = logging.getLogger(__name__)

class LoanPurpose(Enum):
    """贷款用途枚举"""
    CONSUMPTION = "消费"  # 个人消费
    BUSINESS = "经营"     # 企业经营
    EDUCATION = "教育"    # 教育培训
    MEDICAL = "医疗"      # 医疗费用
    TRAVEL = "旅游"       # 旅游出行
    DECORATION = "装修"   # 房屋装修
    OTHER = "其他"        # 其他用途

class LoanStatus(Enum):
    """贷款状态枚举"""
    DIALOG_COLLECTING = "对话收集中"      # 对话引导收集要素
    FORM_FILLING = "表单填写中"           # 结构化表单填写
    RISK_ASSESSING = "风控评估中"         # 风控评估
    PRICING = "定价中"                   # 定价计算
    QUOTATION = "报价中"                 # 生成报价方案
    MATERIAL_GUIDANCE = "材料指引中"      # 材料补充指引
    COMPLETED = "已完成"                 # 流程完成

@dataclass
class ApplicantProfile:
    """申请人档案"""
    # 基本信息
    user_id: str
    name: str = ""
    phone: str = ""
    id_card: str = ""
    
    # 贷款需求
    purpose: Optional[LoanPurpose] = None
    amount: Optional[float] = None  # 申请金额（万元）
    term: Optional[int] = None      # 申请期限（月）
    region: str = ""                # 申请地区
    
    # 收入信息
    monthly_income: Optional[float] = None  # 月收入（元）
    income_source: str = ""                 # 收入来源
    work_years: Optional[int] = None        # 工作年限
    
    # 负债信息
    existing_loans: List[Dict] = None       # 现有贷款
    monthly_debt_payment: Optional[float] = None  # 月还款额（元）
    debt_ratio: Optional[float] = None      # 负债比率
    
    # 担保信息
    has_collateral: bool = False            # 是否有抵押物
    has_guarantor: bool = False             # 是否有担保人
    
    # 信用信息
    credit_score: Optional[int] = None      # 信用评分
    credit_history: str = ""                # 信用历史
    
    # 材料清单
    required_documents: List[str] = None    # 必需材料
    uploaded_documents: List[str] = None    # 已上传材料
    
    # 状态信息
    status: LoanStatus = LoanStatus.DIALOG_COLLECTING
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.existing_loans is None:
            self.existing_loans = []
        if self.required_documents is None:
            self.required_documents = []
        if self.uploaded_documents is None:
            self.uploaded_documents = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

@dataclass
class LoanQuotation:
    """贷款报价方案"""
    bank_name: str
    product_name: str
    approved_amount: float          # 批准金额（万元）
    interest_rate: float            # 年化利率（%）
    term_months: int                # 期限（月）
    monthly_payment: float          # 月还款额（元）
    total_interest: float           # 总利息（元）
    total_amount: float             # 总还款额（元）
    processing_fee: float           # 手续费（元）
    conditions: List[str]           # 附加条件
    risk_level: str                 # 风险等级
    approval_probability: float     # 批准概率（%）
    reasons: List[str]              # 批准/拒绝原因

class LoanAgent:
    """AI贷款智能体"""
    
    def __init__(self, llm_service=None, rag_service=None, risk_service=None, pricing_service=None):
        self.llm_service = llm_service
        self.rag_service = rag_service
        self.risk_service = risk_service
        self.pricing_service = pricing_service
        
        # 信息提取器
        self.info_extractor = InformationExtractor(llm_service=llm_service)
        
        # 风控定价服务
        self.risk_pricing_service = RiskPricingService()
        
        # 存储用户档案
        self.profiles: Dict[str, ApplicantProfile] = {}
        
        # 对话状态机
        self.dialog_states = {
            "greeting": self._handle_greeting,
            "collecting_loan_need": self._handle_loan_need,
            "collecting_income_info": self._handle_income_info,
            "collecting_debt_info": self._handle_debt_info,
            "collecting_credit_info": self._handle_credit_info,
            "confirming_profile": self._handle_profile_confirmation,
            "risk_assessment": self._handle_risk_assessment,
            "quotation": self._handle_quotation,
            "material_guidance": self._handle_material_guidance
        }
    
    async def process_message(self, user_id: str, message: str, session_id: str = None) -> Dict[str, Any]:
        """处理用户消息"""
        try:
            # 获取或创建用户档案
            if user_id not in self.profiles:
                self.profiles[user_id] = ApplicantProfile(user_id=user_id)
            
            profile = self.profiles[user_id]
            
            # 确定当前对话状态
            current_state = self._determine_dialog_state(profile)
            
            # 处理消息
            if current_state in self.dialog_states:
                response = await self.dialog_states[current_state](profile, message)
            else:
                response = await self._handle_default(profile, message)
            
            # 更新档案状态
            profile.updated_at = datetime.now()
            
            # 转换枚举和datetime为字符串
            profile_dict = asdict(profile)
            if 'status' in profile_dict and hasattr(profile_dict['status'], 'value'):
                profile_dict['status'] = profile_dict['status'].value
            if 'purpose' in profile_dict and hasattr(profile_dict['purpose'], 'value'):
                profile_dict['purpose'] = profile_dict['purpose'].value
            if 'created_at' in profile_dict and profile_dict['created_at']:
                profile_dict['created_at'] = profile_dict['created_at'].isoformat()
            if 'updated_at' in profile_dict and profile_dict['updated_at']:
                profile_dict['updated_at'] = profile_dict['updated_at'].isoformat()
            
            return {
                "success": True,
                "response": response,
                "profile": profile_dict,
                "current_state": current_state,
                "next_actions": self._get_next_actions(profile)
            }
            
        except Exception as e:
            logger.error(f"处理消息失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "抱歉，处理您的请求时出现错误，请稍后再试。"
            }
    
    def _determine_dialog_state(self, profile: ApplicantProfile) -> str:
        """确定当前对话状态"""
        if not profile.name:
            return "greeting"
        elif not profile.purpose or not profile.amount:
            return "collecting_loan_need"
        elif not profile.monthly_income:
            return "collecting_income_info"
        elif profile.monthly_debt_payment is None:
            return "collecting_debt_info"
        elif not profile.credit_score:
            return "collecting_credit_info"
        elif profile.status == LoanStatus.DIALOG_COLLECTING:
            return "confirming_profile"
        elif profile.status == LoanStatus.RISK_ASSESSING:
            return "risk_assessment"
        elif profile.status == LoanStatus.QUOTATION:
            return "quotation"
        elif profile.status == LoanStatus.MATERIAL_GUIDANCE:
            return "material_guidance"
        else:
            return "default"
    
    async def _handle_greeting(self, profile: ApplicantProfile, message: str) -> str:
        """处理问候和基本信息收集"""
        # 使用LLM提取基本信息
        if self.llm_service:
            extracted_info = await self._extract_basic_info(message)
            if extracted_info:
                profile.name = extracted_info.get("name", profile.name)
                profile.phone = extracted_info.get("phone", profile.phone)
        
        if not profile.name:
            return """您好！我是AI智能助贷顾问，很高兴为您服务！

为了为您提供最合适的贷款方案，我需要了解一些基本信息：

**请告诉我：**
1. 您的姓名
2. 联系电话
3. 您希望申请什么类型的贷款？

我会根据您的具体情况，为您推荐最适合的银行产品。"""
        else:
            return f"""您好 {profile.name}！

接下来请告诉我您的贷款需求：

**贷款用途：** 您申请贷款主要用于什么？（如：消费、经营、教育、医疗等）
**申请金额：** 您希望申请多少金额？（单位：万元）
**贷款期限：** 您希望多长时间还清？（单位：月）"""
    
    async def _handle_loan_need(self, profile: ApplicantProfile, message: str) -> str:
        """处理贷款需求收集"""
        # 使用LLM提取贷款需求
        if self.llm_service:
            extracted_info = await self._extract_loan_need(message)
            if extracted_info:
                profile.purpose = LoanPurpose(extracted_info.get("purpose", "其他"))
                profile.amount = extracted_info.get("amount")
                profile.term = extracted_info.get("term")
                profile.region = extracted_info.get("region", profile.region)
        
        if not profile.purpose or not profile.amount:
            return """请提供更详细的贷款需求信息：

**贷款用途：** 消费/经营/教育/医疗/旅游/装修/其他
**申请金额：** 具体金额（万元）
**贷款期限：** 具体期限（月）
**申请地区：** 您所在的城市

例如：我想申请30万元用于装修，期限24个月，在北京市申请。"""
        else:
            return f"""好的，我了解到您的贷款需求：

**用途：** {profile.purpose.value}
**金额：** {profile.amount}万元
**期限：** {profile.term}个月
**地区：** {profile.region}

接下来请告诉我您的收入情况：

**月收入：** 您每月的收入是多少？（元）
**收入来源：** 工资/经营/其他
**工作年限：** 您工作多长时间了？（年）"""
    
    async def _handle_income_info(self, profile: ApplicantProfile, message: str) -> str:
        """处理收入信息收集"""
        # 使用LLM提取收入信息
        if self.llm_service:
            extracted_info = await self._extract_income_info(message)
            if extracted_info:
                profile.monthly_income = extracted_info.get("monthly_income")
                profile.income_source = extracted_info.get("income_source", profile.income_source)
                profile.work_years = extracted_info.get("work_years")
        
        if not profile.monthly_income:
            return """请提供您的收入信息：

**月收入：** 具体金额（元）
**收入来源：** 工资/经营收入/其他
**工作年限：** 在当前单位工作多长时间（年）

例如：我月收入8000元，是工资收入，工作3年了。"""
        else:
            return f"""收入信息已记录：

**月收入：** {profile.monthly_income}元
**收入来源：** {profile.income_source}
**工作年限：** {profile.work_years}年

接下来请告诉我您的负债情况：

**现有贷款：** 您目前有其他贷款吗？月还款多少？
**负债情况：** 信用卡、房贷、车贷等月还款总额（元）"""
    
    async def _handle_debt_info(self, profile: ApplicantProfile, message: str) -> str:
        """处理负债信息收集"""
        # 使用LLM提取负债信息
        if self.llm_service:
            extracted_info = await self._extract_debt_info(message)
            if extracted_info:
                profile.monthly_debt_payment = extracted_info.get("monthly_debt_payment", 0)
                profile.existing_loans = extracted_info.get("existing_loans", [])
                # 计算负债比率
                if profile.monthly_income and profile.monthly_debt_payment:
                    profile.debt_ratio = profile.monthly_debt_payment / profile.monthly_income
        
        if profile.monthly_debt_payment is None:
            return """请提供您的负债信息：

**现有贷款：** 房贷、车贷、其他贷款等
**月还款额：** 所有贷款的月还款总额（元）
**信用卡：** 信用卡月还款额（元）

例如：我有房贷月供3000元，信用卡月还款500元，总计3500元。"""
        else:
            return f"""负债信息已记录：

**月还款额：** {profile.monthly_debt_payment}元
**负债比率：** {profile.debt_ratio:.1%}（月还款/月收入）

接下来请告诉我您的信用情况：

**信用评分：** 您知道自己的信用评分吗？
**信用历史：** 是否有逾期记录？"""
    
    async def _handle_credit_info(self, profile: ApplicantProfile, message: str) -> str:
        """处理信用信息收集"""
        # 使用LLM提取信用信息
        if self.llm_service:
            extracted_info = await self._extract_credit_info(message)
            if extracted_info:
                profile.credit_score = extracted_info.get("credit_score")
                profile.credit_history = extracted_info.get("credit_history", profile.credit_history)
        
        if not profile.credit_score:
            return """请提供您的信用信息：

**信用评分：** 如果知道请提供，不知道可以填"未知"
**信用历史：** 是否有逾期、违约等不良记录？
**担保情况：** 是否有抵押物或担保人？

例如：我信用评分750分，没有逾期记录，没有抵押物。"""
        else:
            # 开始风控评估
            profile.status = LoanStatus.RISK_ASSESSING
            return f"""信用信息已记录：

**信用评分：** {profile.credit_score}分
**信用历史：** {profile.credit_history}

现在我将为您进行风控评估和产品匹配，请稍候..."""
    
    async def _handle_profile_confirmation(self, profile: ApplicantProfile, message: str) -> str:
        """处理档案确认"""
        if "确认" in message or "是的" in message or "正确" in message:
            profile.status = LoanStatus.RISK_ASSESSING
            return await self._handle_risk_assessment(profile, message)
        else:
            return f"""请确认您的申请信息：

**基本信息：**
- 姓名：{profile.name}
- 电话：{profile.phone}

**贷款需求：**
- 用途：{profile.purpose.value}
- 金额：{profile.amount}万元
- 期限：{profile.term}个月
- 地区：{profile.region}

**收入情况：**
- 月收入：{profile.monthly_income}元
- 收入来源：{profile.income_source}
- 工作年限：{profile.work_years}年

**负债情况：**
- 月还款：{profile.monthly_debt_payment}元
- 负债比率：{profile.debt_ratio:.1%}

**信用情况：**
- 信用评分：{profile.credit_score}分
- 信用历史：{profile.credit_history}

**请确认以上信息是否正确？**（回复"确认"或"修改"）"""
    
    async def _handle_risk_assessment(self, profile: ApplicantProfile, message: str) -> str:
        """处理风控评估"""
        try:
            # 调用风控服务
            risk_result = await self._call_risk_service(profile)
            
            if risk_result.get("approved", False):
                profile.status = LoanStatus.QUOTATION
                return await self._handle_quotation(profile, message)
            else:
                return f"""风控评估结果：

**评估结果：** 暂不符合申请条件
**主要风险：** {', '.join(risk_result.get('risks', []))}
**建议：** {risk_result.get('suggestion', '请改善相关条件后重新申请')}

如需详细了解，请联系我们的客服人员。"""
                
        except Exception as e:
            logger.error(f"风控评估失败: {e}")
            return "风控评估服务暂时不可用，请稍后再试。"
    
    async def _handle_quotation(self, profile: ApplicantProfile, message: str) -> str:
        """处理报价生成"""
        try:
            # 调用定价服务
            quotations = await self._call_pricing_service(profile)
            
            if quotations:
                profile.status = LoanStatus.MATERIAL_GUIDANCE
                return self._format_quotations(quotations)
            else:
                return "暂无可匹配的贷款产品，请联系客服了解详情。"
                
        except Exception as e:
            logger.error(f"报价生成失败: {e}")
            return "报价服务暂时不可用，请稍后再试。"
    
    async def _handle_material_guidance(self, profile: ApplicantProfile, message: str) -> str:
        """处理材料指引"""
        # 生成材料清单
        required_docs = self._generate_required_documents(profile)
        profile.required_documents = required_docs
        
        return f"""**材料清单：**

请准备以下材料：

{chr(10).join([f"• {doc}" for doc in required_docs])}

**下一步操作：**
1. 点击下方链接填写详细申请表
2. 上传相关材料
3. 等待银行审核

**申请链接：** [点击填写申请表](http://localhost:3000/loan-application?profile_id={profile.user_id})

**或者直接访问：** `http://localhost:3000/loan-application?profile_id={profile.user_id}`

如有疑问，请随时联系我！"""
    
    async def _handle_default(self, profile: ApplicantProfile, message: str) -> str:
        """处理默认情况"""
        return "请告诉我您需要什么帮助？我可以协助您申请贷款。"
    
    def _get_next_actions(self, profile: ApplicantProfile) -> List[str]:
        """获取下一步操作建议"""
        if profile.status == LoanStatus.DIALOG_COLLECTING:
            return ["继续提供信息", "查看已填写内容"]
        elif profile.status == LoanStatus.FORM_FILLING:
            return ["填写申请表", "上传材料"]
        elif profile.status == LoanStatus.QUOTATION:
            return ["查看报价方案", "选择产品"]
        elif profile.status == LoanStatus.MATERIAL_GUIDANCE:
            return ["填写申请表", "上传材料", "联系客服"]
        else:
            return ["重新开始", "联系客服"]
    
    # LLM信息提取方法
    async def _extract_basic_info(self, message: str) -> Dict[str, Any]:
        """提取基本信息"""
        return await self.info_extractor.extract_basic_info(message)
    
    async def _extract_loan_need(self, message: str) -> Dict[str, Any]:
        """提取贷款需求"""
        return await self.info_extractor.extract_loan_need(message)
    
    async def _extract_income_info(self, message: str) -> Dict[str, Any]:
        """提取收入信息"""
        return await self.info_extractor.extract_income_info(message)
    
    async def _extract_debt_info(self, message: str) -> Dict[str, Any]:
        """提取负债信息"""
        return await self.info_extractor.extract_debt_info(message)
    
    async def _extract_credit_info(self, message: str) -> Dict[str, Any]:
        """提取信用信息"""
        return await self.info_extractor.extract_credit_info(message)
    
    # 外部服务调用方法
    async def _call_risk_service(self, profile: ApplicantProfile) -> Dict[str, Any]:
        """调用风控服务"""
        try:
            # 转换档案为字典格式
            profile_dict = asdict(profile)
            
            # 调用真实的风控服务
            result = await self.risk_pricing_service.process_application(profile_dict)
            
            if result.get("success"):
                risk_assessment = result.get("risk_assessment", {})
                return {
                    "approved": risk_assessment.get("approved", False),
                    "risk_level": risk_assessment.get("risk_level", "中风险"),
                    "risk_score": risk_assessment.get("risk_score", 0.5),
                    "risk_report": risk_assessment.get("risk_report", ""),
                    "recommendations": risk_assessment.get("recommendations", [])
                }
            else:
                return {
                    "approved": False,
                    "risk_level": "高风险",
                    "error": result.get("error", "风控评估失败")
                }
        except Exception as e:
            logger.error(f"风控服务调用失败: {e}")
            return {
                "approved": False,
                "risk_level": "高风险",
                "error": str(e)
            }
    
    async def _call_pricing_service(self, profile: ApplicantProfile) -> List[LoanQuotation]:
        """调用定价服务"""
        try:
            # 转换档案为字典格式
            profile_dict = asdict(profile)
            
            # 调用真实的风控定价服务
            result = await self.risk_pricing_service.process_application(profile_dict)
            
            if result.get("success"):
                quotations_data = result.get("quotations", [])
                quotations = []
                
                for quote_data in quotations_data:
                    quotation = LoanQuotation(
                        bank_name=quote_data.get("bank_name", ""),
                        product_name=quote_data.get("product_name", ""),
                        approved_amount=quote_data.get("approved_amount", 0),
                        interest_rate=quote_data.get("interest_rate", 0),
                        term_months=quote_data.get("term_months", 0),
                        monthly_payment=quote_data.get("monthly_payment", 0),
                        total_interest=quote_data.get("total_interest", 0),
                        total_amount=quote_data.get("total_amount", 0),
                        processing_fee=quote_data.get("processing_fee", 0),
                        conditions=quote_data.get("conditions", []),
                        risk_level=quote_data.get("risk_level", "中风险"),
                        approval_probability=quote_data.get("approval_probability", 0),
                        reasons=quote_data.get("reasons", [])
                    )
                    quotations.append(quotation)
                
                return quotations
            else:
                logger.error(f"定价服务调用失败: {result.get('error')}")
                return []
                
        except Exception as e:
            logger.error(f"定价服务调用失败: {e}")
            return []
    
    def _format_quotations(self, quotations: List[LoanQuotation]) -> str:
        """格式化报价方案"""
        if not quotations:
            return "暂无可匹配的贷款产品。"
        
        result = "**为您匹配到以下贷款方案：**\n\n"
        
        for i, quote in enumerate(quotations, 1):
            result += f"**方案 {i}：{quote.bank_name} - {quote.product_name}**\n"
            result += f"• 批准金额：{quote.approved_amount}万元\n"
            result += f"• 年化利率：{quote.interest_rate}%\n"
            result += f"• 贷款期限：{quote.term_months}个月\n"
            result += f"• 月还款额：{quote.monthly_payment:.2f}元\n"
            result += f"• 总利息：{quote.total_interest:.2f}元\n"
            result += f"• 手续费：{quote.processing_fee}元\n"
            result += f"• 批准概率：{quote.approval_probability}%\n"
            result += f"• 附加条件：{', '.join(quote.conditions)}\n"
            result += f"• 批准原因：{', '.join(quote.reasons)}\n\n"
        
        result += "**请选择您感兴趣的方案，我将为您提供详细的申请指引。**"
        return result
    
    def _generate_required_documents(self, profile: ApplicantProfile) -> List[str]:
        """生成必需材料清单"""
        docs = [
            "身份证正反面复印件",
            "收入证明（工资单或银行流水）",
            "工作证明或劳动合同",
            "居住证明（水电费账单等）"
        ]
        
        if profile.purpose == LoanPurpose.BUSINESS:
            docs.extend([
                "营业执照",
                "税务登记证",
                "财务报表"
            ])
        
        if profile.purpose == LoanPurpose.EDUCATION:
            docs.append("录取通知书或培训合同")
        
        if profile.purpose == LoanPurpose.DECORATION:
            docs.append("装修合同或预算单")
        
        return docs
