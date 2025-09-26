#!/usr/bin/env python3
"""
助贷招标服务
实现RFQ生成、资金方投标、排名撮合等功能
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class RFQStatus(Enum):
    """RFQ状态枚举"""
    DRAFT = "草稿"
    PUBLISHED = "已发布"
    BIDDING = "招标中"
    CLOSED = "已关闭"
    AWARDED = "已中标"
    CANCELLED = "已取消"

class BidStatus(Enum):
    """投标状态枚举"""
    SUBMITTED = "已提交"
    UNDER_REVIEW = "审核中"
    APPROVED = "已批准"
    REJECTED = "已拒绝"
    AWARDED = "已中标"
    WITHDRAWN = "已撤回"

@dataclass
class LoanRFQ:
    """贷款招标需求"""
    rfq_id: str
    borrower_id: str
    borrower_name: str
    loan_amount: float  # 万元
    loan_term: int  # 月
    loan_purpose: str
    max_interest_rate: float  # 最高可接受利率
    min_interest_rate: float  # 最低可接受利率
    required_conditions: List[str]  # 必需条件
    preferred_conditions: List[str]  # 偏好条件
    risk_level: str
    credit_score: int
    monthly_income: float
    debt_ratio: float
    has_collateral: bool
    collateral_type: str
    status: RFQStatus
    created_at: datetime
    published_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    description: str = ""
    documents: List[str] = None
    
    def __post_init__(self):
        if self.documents is None:
            self.documents = []

@dataclass
class Bid:
    """投标方案"""
    bid_id: str
    rfq_id: str
    lender_id: str
    lender_name: str
    bank_name: str
    product_name: str
    offered_amount: float  # 万元
    offered_rate: float  # 年化利率
    offered_term: int  # 月
    processing_fee: float  # 手续费
    conditions: List[str]  # 附加条件
    approval_time: int  # 审批时间（天）
    status: BidStatus
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    notes: str = ""
    score: float = 0.0  # 综合评分

class LoanRFQService:
    """助贷招标服务"""
    
    def __init__(self):
        self.rfqs: Dict[str, LoanRFQ] = {}
        self.bids: Dict[str, Bid] = {}
        self.lenders: Dict[str, Dict] = {}  # 资金方信息
        
        # 初始化示例资金方
        self._initialize_lenders()
    
    def _initialize_lenders(self):
        """初始化资金方信息"""
        self.lenders = {
            "bank_001": {
                "lender_id": "bank_001",
                "lender_name": "招商银行",
                "bank_name": "招商银行",
                "contact_person": "张经理",
                "contact_phone": "400-820-5555",
                "min_amount": 1,
                "max_amount": 100,
                "min_term": 3,
                "max_term": 60,
                "base_rate_range": [4.0, 8.0],
                "specialties": ["个人消费贷款", "经营贷款"],
                "approval_time": 3
            },
            "bank_002": {
                "lender_id": "bank_002",
                "lender_name": "工商银行",
                "bank_name": "工商银行",
                "contact_person": "李经理",
                "contact_phone": "95588",
                "min_amount": 5,
                "max_amount": 200,
                "min_term": 6,
                "max_term": 72,
                "base_rate_range": [3.8, 7.5],
                "specialties": ["个人信用贷款", "抵押贷款"],
                "approval_time": 5
            },
            "bank_003": {
                "lender_id": "bank_003",
                "lender_name": "建设银行",
                "bank_name": "建设银行",
                "contact_person": "王经理",
                "contact_phone": "95533",
                "min_amount": 2,
                "max_amount": 150,
                "min_term": 3,
                "max_term": 60,
                "base_rate_range": [4.2, 8.2],
                "specialties": ["快贷", "消费贷款"],
                "approval_time": 2
            }
        }
    
    async def create_rfq(self, borrower_profile: Dict[str, Any]) -> Dict[str, Any]:
        """创建贷款招标需求"""
        try:
            rfq_id = str(uuid.uuid4())
            
            # 从借款人档案提取信息
            rfq = LoanRFQ(
                rfq_id=rfq_id,
                borrower_id=borrower_profile.get("user_id", ""),
                borrower_name=borrower_profile.get("name", ""),
                loan_amount=borrower_profile.get("amount", 0),
                loan_term=borrower_profile.get("term", 12),
                loan_purpose=borrower_profile.get("purpose", ""),
                max_interest_rate=8.0,  # 默认最高利率
                min_interest_rate=3.5,  # 默认最低利率
                required_conditions=self._generate_required_conditions(borrower_profile),
                preferred_conditions=self._generate_preferred_conditions(borrower_profile),
                risk_level=borrower_profile.get("risk_level", "中风险"),
                credit_score=borrower_profile.get("credit_score", 0),
                monthly_income=borrower_profile.get("monthly_income", 0),
                debt_ratio=borrower_profile.get("debt_ratio", 0),
                has_collateral=borrower_profile.get("has_collateral", False),
                collateral_type=borrower_profile.get("collateral_type", ""),
                status=RFQStatus.DRAFT,
                created_at=datetime.now(),
                description=f"借款人{borrower_profile.get('name', '')}申请{borrower_profile.get('amount', 0)}万元{borrower_profile.get('purpose', '')}贷款"
            )
            
            self.rfqs[rfq_id] = rfq
            
            return {
                "success": True,
                "rfq_id": rfq_id,
                "message": "RFQ创建成功"
            }
            
        except Exception as e:
            logger.error(f"创建RFQ失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def publish_rfq(self, rfq_id: str, deadline_hours: int = 72) -> Dict[str, Any]:
        """发布RFQ"""
        try:
            if rfq_id not in self.rfqs:
                return {
                    "success": False,
                    "error": "RFQ不存在"
                }
            
            rfq = self.rfqs[rfq_id]
            rfq.status = RFQStatus.PUBLISHED
            rfq.published_at = datetime.now()
            rfq.deadline = datetime.now() + timedelta(hours=deadline_hours)
            
            # 通知相关资金方
            await self._notify_lenders(rfq)
            
            return {
                "success": True,
                "message": "RFQ发布成功",
                "deadline": rfq.deadline.isoformat()
            }
            
        except Exception as e:
            logger.error(f"发布RFQ失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def submit_bid(self, rfq_id: str, lender_id: str, bid_data: Dict[str, Any]) -> Dict[str, Any]:
        """提交投标方案"""
        try:
            if rfq_id not in self.rfqs:
                return {
                    "success": False,
                    "error": "RFQ不存在"
                }
            
            if lender_id not in self.lenders:
                return {
                    "success": False,
                    "error": "资金方不存在"
                }
            
            rfq = self.rfqs[rfq_id]
            lender = self.lenders[lender_id]
            
            # 验证投标条件
            validation_result = self._validate_bid(rfq, lender, bid_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"]
                }
            
            bid_id = str(uuid.uuid4())
            bid = Bid(
                bid_id=bid_id,
                rfq_id=rfq_id,
                lender_id=lender_id,
                lender_name=lender["lender_name"],
                bank_name=lender["bank_name"],
                product_name=bid_data.get("product_name", ""),
                offered_amount=bid_data.get("offered_amount", 0),
                offered_rate=bid_data.get("offered_rate", 0),
                offered_term=bid_data.get("offered_term", 0),
                processing_fee=bid_data.get("processing_fee", 0),
                conditions=bid_data.get("conditions", []),
                approval_time=bid_data.get("approval_time", lender["approval_time"]),
                status=BidStatus.SUBMITTED,
                submitted_at=datetime.now(),
                notes=bid_data.get("notes", "")
            )
            
            # 计算投标评分
            bid.score = self._calculate_bid_score(rfq, bid)
            
            self.bids[bid_id] = bid
            
            return {
                "success": True,
                "bid_id": bid_id,
                "message": "投标提交成功"
            }
            
        except Exception as e:
            logger.error(f"提交投标失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_rfq_bids(self, rfq_id: str) -> Dict[str, Any]:
        """获取RFQ的所有投标"""
        try:
            if rfq_id not in self.rfqs:
                return {
                    "success": False,
                    "error": "RFQ不存在"
                }
            
            rfq_bids = [bid for bid in self.bids.values() if bid.rfq_id == rfq_id]
            
            # 按评分排序
            rfq_bids.sort(key=lambda x: x.score, reverse=True)
            
            # 转换枚举为字符串
            rfq_dict = asdict(self.rfqs[rfq_id])
            if 'status' in rfq_dict and hasattr(rfq_dict['status'], 'value'):
                rfq_dict['status'] = rfq_dict['status'].value
            # 转换datetime为字符串
            if 'created_at' in rfq_dict and rfq_dict['created_at']:
                rfq_dict['created_at'] = rfq_dict['created_at'].isoformat()
            if 'updated_at' in rfq_dict and rfq_dict['updated_at']:
                rfq_dict['updated_at'] = rfq_dict['updated_at'].isoformat()
            if 'published_at' in rfq_dict and rfq_dict['published_at']:
                rfq_dict['published_at'] = rfq_dict['published_at'].isoformat()
            if 'deadline' in rfq_dict and rfq_dict['deadline']:
                rfq_dict['deadline'] = rfq_dict['deadline'].isoformat()
            
            bids_list = []
            for bid in rfq_bids:
                bid_dict = asdict(bid)
                if 'status' in bid_dict and hasattr(bid_dict['status'], 'value'):
                    bid_dict['status'] = bid_dict['status'].value
                # 转换datetime为字符串
                if 'created_at' in bid_dict and bid_dict['created_at']:
                    bid_dict['created_at'] = bid_dict['created_at'].isoformat()
                if 'updated_at' in bid_dict and bid_dict['updated_at']:
                    bid_dict['updated_at'] = bid_dict['updated_at'].isoformat()
                bids_list.append(bid_dict)
            
            return {
                "success": True,
                "rfq": rfq_dict,
                "bids": bids_list,
                "total_bids": len(rfq_bids)
            }
            
        except Exception as e:
            logger.error(f"获取投标列表失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def award_bid(self, rfq_id: str, bid_id: str) -> Dict[str, Any]:
        """中标投标方案"""
        try:
            if rfq_id not in self.rfqs:
                return {
                    "success": False,
                    "error": "RFQ不存在"
                }
            
            if bid_id not in self.bids:
                return {
                    "success": False,
                    "error": "投标不存在"
                }
            
            bid = self.bids[bid_id]
            if bid.rfq_id != rfq_id:
                return {
                    "success": False,
                    "error": "投标与RFQ不匹配"
                }
            
            # 更新RFQ状态
            rfq = self.rfqs[rfq_id]
            rfq.status = RFQStatus.AWARDED
            
            # 更新投标状态
            bid.status = BidStatus.AWARDED
            
            # 通知中标方
            await self._notify_award(bid)
            
            return {
                "success": True,
                "message": "中标成功",
                "awarded_bid": asdict(bid)
            }
            
        except Exception as e:
            logger.error(f"中标处理失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_required_conditions(self, profile: Dict[str, Any]) -> List[str]:
        """生成必需条件"""
        conditions = []
        
        if profile.get("amount", 0) > 50:
            conditions.append("需要提供收入证明和银行流水")
        
        if profile.get("risk_level") in ["中高风险", "高风险"]:
            conditions.append("需要提供担保人")
        
        if profile.get("purpose") == "经营":
            conditions.append("需要提供营业执照和财务报表")
        
        return conditions
    
    def _generate_preferred_conditions(self, profile: Dict[str, Any]) -> List[str]:
        """生成偏好条件"""
        conditions = []
        
        if profile.get("has_collateral", False):
            conditions.append("优先考虑有抵押物的方案")
        
        if profile.get("credit_score", 0) >= 750:
            conditions.append("优先考虑利率较低的方案")
        
        return conditions
    
    def _validate_bid(self, rfq: LoanRFQ, lender: Dict, bid_data: Dict) -> Dict[str, Any]:
        """验证投标条件"""
        offered_amount = bid_data.get("offered_amount", 0)
        offered_rate = bid_data.get("offered_rate", 0)
        offered_term = bid_data.get("offered_term", 0)
        
        # 检查金额范围
        if offered_amount < lender["min_amount"] or offered_amount > lender["max_amount"]:
            return {
                "valid": False,
                "error": f"投标金额超出范围 ({lender['min_amount']}-{lender['max_amount']}万元)"
            }
        
        # 检查期限范围
        if offered_term < lender["min_term"] or offered_term > lender["max_term"]:
            return {
                "valid": False,
                "error": f"投标期限超出范围 ({lender['min_term']}-{lender['max_term']}个月)"
            }
        
        # 检查利率范围
        if offered_rate < lender["base_rate_range"][0] or offered_rate > lender["base_rate_range"][1]:
            return {
                "valid": False,
                "error": f"投标利率超出范围 ({lender['base_rate_range'][0]}-{lender['base_rate_range'][1]}%)"
            }
        
        return {"valid": True}
    
    def _calculate_bid_score(self, rfq: LoanRFQ, bid: Bid) -> float:
        """计算投标评分"""
        score = 0.0
        
        # 利率评分 (40%)
        rate_score = max(0, (rfq.max_interest_rate - bid.offered_rate) / (rfq.max_interest_rate - rfq.min_interest_rate))
        score += rate_score * 40
        
        # 金额匹配度 (20%)
        amount_score = min(1.0, bid.offered_amount / rfq.loan_amount)
        score += amount_score * 20
        
        # 期限匹配度 (15%)
        term_score = 1.0 - abs(bid.offered_term - rfq.loan_term) / rfq.loan_term
        score += max(0, term_score) * 15
        
        # 审批时间 (10%)
        time_score = max(0, 1.0 - bid.approval_time / 30)  # 30天为基准
        score += time_score * 10
        
        # 手续费 (10%)
        fee_score = max(0, 1.0 - bid.processing_fee / (rfq.loan_amount * 1000))  # 1%为基准
        score += fee_score * 10
        
        # 条件匹配度 (5%)
        condition_score = len([c for c in bid.conditions if c in rfq.required_conditions]) / len(rfq.required_conditions)
        score += condition_score * 5
        
        return min(100.0, score)
    
    async def _notify_lenders(self, rfq: LoanRFQ):
        """通知资金方"""
        # 这里应该实现实际的通知逻辑
        logger.info(f"通知资金方新的RFQ: {rfq.rfq_id}")
    
    async def _notify_award(self, bid: Bid):
        """通知中标"""
        # 这里应该实现实际的通知逻辑
        logger.info(f"通知中标: {bid.bid_id}")
