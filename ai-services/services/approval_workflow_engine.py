"""
审批流程引擎
实现自动化审批和人工审核结合的智能审批系统
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid

class ApprovalStatus(Enum):
    """审批状态"""
    PENDING = "pending"
    AUTO_APPROVED = "auto_approved"
    AUTO_REJECTED = "auto_rejected"
    MANUAL_REVIEW = "manual_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class ApprovalLevel(Enum):
    """审批级别"""
    SYSTEM = "system"
    JUNIOR_OFFICER = "junior_officer"
    SENIOR_OFFICER = "senior_officer"
    MANAGER = "manager"
    DIRECTOR = "director"

class ApprovalRule(Enum):
    """审批规则"""
    CREDIT_SCORE_MIN = "credit_score_min"
    INCOME_DEBT_RATIO_MAX = "income_debt_ratio_max"
    LOAN_AMOUNT_MAX = "loan_amount_max"
    EMPLOYMENT_YEARS_MIN = "employment_years_min"
    AGE_RANGE = "age_range"
    INDUSTRY_RESTRICTION = "industry_restriction"

@dataclass
class ApprovalDecision:
    """审批决策"""
    decision_id: str
    application_id: str
    status: ApprovalStatus
    approval_level: ApprovalLevel
    decision_reason: str
    conditions: List[str]
    risk_factors: List[str]
    approval_amount: float
    approved_term: int
    special_conditions: List[str]
    decision_timestamp: datetime
    decision_officer: str
    confidence_score: float

@dataclass
class ApprovalRuleConfig:
    """审批规则配置"""
    rule_type: ApprovalRule
    threshold_value: Any
    operator: str  # ">", "<", ">=", "<=", "==", "in", "not_in"
    weight: float
    is_mandatory: bool
    error_message: str

class ApprovalWorkflowEngine:
    """审批流程引擎"""
    
    def __init__(self):
        self.approval_rules = self._initialize_approval_rules()
        self.workflow_stages = self._initialize_workflow_stages()
        self.approval_decisions: Dict[str, ApprovalDecision] = {}
        self.pending_applications: Dict[str, Dict[str, Any]] = {}
    
    def _initialize_approval_rules(self) -> List[ApprovalRuleConfig]:
        """初始化审批规则"""
        return [
            ApprovalRuleConfig(
                rule_type=ApprovalRule.CREDIT_SCORE_MIN,
                threshold_value=600,
                operator=">=",
                weight=0.3,
                is_mandatory=True,
                error_message="信用评分不足，最低要求600分"
            ),
            ApprovalRuleConfig(
                rule_type=ApprovalRule.INCOME_DEBT_RATIO_MAX,
                threshold_value=0.5,
                operator="<=",
                weight=0.25,
                is_mandatory=True,
                error_message="负债比率过高，不能超过50%"
            ),
            ApprovalRuleConfig(
                rule_type=ApprovalRule.LOAN_AMOUNT_MAX,
                threshold_value=1000000,
                operator="<=",
                weight=0.2,
                is_mandatory=True,
                error_message="贷款金额超过系统限额"
            ),
            ApprovalRuleConfig(
                rule_type=ApprovalRule.EMPLOYMENT_YEARS_MIN,
                threshold_value=1,
                operator=">=",
                weight=0.15,
                is_mandatory=False,
                error_message="就业时间不足，建议提供担保"
            ),
            ApprovalRuleConfig(
                rule_type=ApprovalRule.AGE_RANGE,
                threshold_value=[22, 65],
                operator="in",
                weight=0.1,
                is_mandatory=True,
                error_message="年龄不符合要求，应在22-65岁之间"
            )
        ]
    
    def _initialize_workflow_stages(self) -> List[Dict[str, Any]]:
        """初始化工作流阶段"""
        return [
            {
                "stage": "initial_review",
                "description": "初步审核",
                "auto_approval_threshold": 0.8,
                "auto_rejection_threshold": 0.3,
                "required_level": ApprovalLevel.SYSTEM
            },
            {
                "stage": "risk_assessment",
                "description": "风险评估",
                "auto_approval_threshold": 0.7,
                "auto_rejection_threshold": 0.4,
                "required_level": ApprovalLevel.JUNIOR_OFFICER
            },
            {
                "stage": "final_review",
                "description": "最终审核",
                "auto_approval_threshold": 0.6,
                "auto_rejection_threshold": 0.5,
                "required_level": ApprovalLevel.SENIOR_OFFICER
            },
            {
                "stage": "manager_approval",
                "description": "经理审批",
                "auto_approval_threshold": 0.0,
                "auto_rejection_threshold": 1.0,
                "required_level": ApprovalLevel.MANAGER
            }
        ]
    
    def process_application(self, application_data: Dict[str, Any], 
                          risk_assessment: Dict[str, Any]) -> ApprovalDecision:
        """处理贷款申请"""
        try:
            application_id = application_data.get("application_id", str(uuid.uuid4()))
            
            # 保存申请数据
            self.pending_applications[application_id] = {
                "application_data": application_data,
                "risk_assessment": risk_assessment,
                "created_at": datetime.now()
            }
            
            # 执行审批流程
            decision = self._execute_approval_workflow(application_id, application_data, risk_assessment)
            
            # 保存决策结果
            self.approval_decisions[application_id] = decision
            
            logger.info(f"审批完成: {application_id}, 状态: {decision.status.value}")
            return decision
            
        except Exception as e:
            logger.error(f"审批处理失败: {e}")
            return self._create_default_decision(application_data)
    
    def _execute_approval_workflow(self, application_id: str, 
                                 application_data: Dict[str, Any],
                                 risk_assessment: Dict[str, Any]) -> ApprovalDecision:
        """执行审批工作流"""
        current_stage = 0
        decision_reason = ""
        conditions = []
        risk_factors = []
        
        # 逐步执行审批阶段
        for stage_config in self.workflow_stages:
            stage_result = self._process_approval_stage(
                application_data, risk_assessment, stage_config
            )
            
            if stage_result["status"] == "auto_approved":
                return self._create_approval_decision(
                    application_id, ApprovalStatus.AUTO_APPROVED,
                    stage_config["required_level"], stage_result["reason"],
                    conditions, risk_factors, application_data
                )
            elif stage_result["status"] == "auto_rejected":
                return self._create_approval_decision(
                    application_id, ApprovalStatus.AUTO_REJECTED,
                    stage_config["required_level"], stage_result["reason"],
                    conditions, risk_factors, application_data
                )
            elif stage_result["status"] == "manual_review":
                conditions.extend(stage_result["conditions"])
                risk_factors.extend(stage_result["risk_factors"])
                decision_reason = stage_result["reason"]
                current_stage += 1
            else:
                break
        
        # 如果所有阶段都需要人工审核
        if current_stage >= len(self.workflow_stages):
            return self._create_approval_decision(
                application_id, ApprovalStatus.MANUAL_REVIEW,
                ApprovalLevel.MANAGER, decision_reason,
                conditions, risk_factors, application_data
            )
        
        return self._create_approval_decision(
            application_id, ApprovalStatus.PENDING,
            ApprovalLevel.SYSTEM, "审批进行中",
            conditions, risk_factors, application_data
        )
    
    def _process_approval_stage(self, application_data: Dict[str, Any],
                              risk_assessment: Dict[str, Any],
                              stage_config: Dict[str, Any]) -> Dict[str, Any]:
        """处理审批阶段"""
        # 执行规则检查
        rule_results = self._check_approval_rules(application_data, risk_assessment)
        
        # 计算综合得分
        approval_score = self._calculate_approval_score(rule_results, risk_assessment)
        
        # 确定阶段结果
        if approval_score >= stage_config["auto_approval_threshold"]:
            return {
                "status": "auto_approved",
                "reason": f"自动批准 - 得分: {approval_score:.2f}",
                "score": approval_score
            }
        elif approval_score <= stage_config["auto_rejection_threshold"]:
            return {
                "status": "auto_rejected",
                "reason": f"自动拒绝 - 得分: {approval_score:.2f}",
                "score": approval_score
            }
        else:
            return {
                "status": "manual_review",
                "reason": f"需要人工审核 - 得分: {approval_score:.2f}",
                "score": approval_score,
                "conditions": self._get_failed_conditions(rule_results),
                "risk_factors": self._get_risk_factors(risk_assessment)
            }
    
    def _check_approval_rules(self, application_data: Dict[str, Any],
                            risk_assessment: Dict[str, Any]) -> Dict[ApprovalRule, bool]:
        """检查审批规则"""
        rule_results = {}
        
        for rule in self.approval_rules:
            result = self._evaluate_rule(rule, application_data, risk_assessment)
            rule_results[rule.rule_type] = result
        
        return rule_results
    
    def _evaluate_rule(self, rule: ApprovalRuleConfig, application_data: Dict[str, Any],
                      risk_assessment: Dict[str, Any]) -> bool:
        """评估单个规则"""
        try:
            if rule.rule_type == ApprovalRule.CREDIT_SCORE_MIN:
                credit_score = application_data.get("credit_score", 0)
                return self._compare_values(credit_score, rule.threshold_value, rule.operator)
            
            elif rule.rule_type == ApprovalRule.INCOME_DEBT_RATIO_MAX:
                monthly_income = application_data.get("monthly_income", 0)
                monthly_debt = application_data.get("monthly_debt", 0)
                if monthly_income == 0:
                    return False
                debt_ratio = monthly_debt / monthly_income
                return self._compare_values(debt_ratio, rule.threshold_value, rule.operator)
            
            elif rule.rule_type == ApprovalRule.LOAN_AMOUNT_MAX:
                loan_amount = application_data.get("loan_amount", 0)
                return self._compare_values(loan_amount, rule.threshold_value, rule.operator)
            
            elif rule.rule_type == ApprovalRule.EMPLOYMENT_YEARS_MIN:
                employment_years = application_data.get("employment_years", 0)
                return self._compare_values(employment_years, rule.threshold_value, rule.operator)
            
            elif rule.rule_type == ApprovalRule.AGE_RANGE:
                age = application_data.get("age", 0)
                min_age, max_age = rule.threshold_value
                return min_age <= age <= max_age
            
            return True
            
        except Exception as e:
            logger.error(f"规则评估失败: {rule.rule_type.value}, {e}")
            return False
    
    def _compare_values(self, actual: Any, expected: Any, operator: str) -> bool:
        """比较值"""
        try:
            if operator == ">":
                return actual > expected
            elif operator == "<":
                return actual < expected
            elif operator == ">=":
                return actual >= expected
            elif operator == "<=":
                return actual <= expected
            elif operator == "==":
                return actual == expected
            elif operator == "in":
                return actual in expected
            elif operator == "not_in":
                return actual not in expected
            else:
                return False
        except Exception:
            return False
    
    def _calculate_approval_score(self, rule_results: Dict[ApprovalRule, bool],
                                risk_assessment: Dict[str, Any]) -> float:
        """计算审批得分"""
        total_weight = 0
        weighted_score = 0
        
        # 基于规则结果计算得分
        for rule in self.approval_rules:
            rule_passed = rule_results.get(rule.rule_type, False)
            weight = rule.weight
            
            if rule.is_mandatory and not rule_passed:
                # 强制规则未通过，得分大幅降低
                weighted_score += 0
            else:
                # 非强制规则，按权重计算
                weighted_score += (1 if rule_passed else 0) * weight
            
            total_weight += weight
        
        # 基于风险评估调整得分
        risk_score = risk_assessment.get("overall_risk_score", 0.5)
        risk_adjustment = 1 - risk_score  # 风险越高，得分越低
        
        # 综合得分
        if total_weight > 0:
            rule_score = weighted_score / total_weight
            final_score = (rule_score + risk_adjustment) / 2
        else:
            final_score = risk_adjustment
        
        return min(max(final_score, 0), 1)
    
    def _get_failed_conditions(self, rule_results: Dict[ApprovalRule, bool]) -> List[str]:
        """获取未通过的条件"""
        failed_conditions = []
        
        for rule in self.approval_rules:
            if not rule_results.get(rule.rule_type, True):
                failed_conditions.append(rule.error_message)
        
        return failed_conditions
    
    def _get_risk_factors(self, risk_assessment: Dict[str, Any]) -> List[str]:
        """获取风险因子"""
        risk_factors = []
        
        risk_explanations = risk_assessment.get("risk_explanations", {})
        for factor, explanation in risk_explanations.items():
            if "风险" in explanation or "高" in explanation:
                risk_factors.append(f"{factor}: {explanation}")
        
        return risk_factors
    
    def _create_approval_decision(self, application_id: str, status: ApprovalStatus,
                                approval_level: ApprovalLevel, reason: str,
                                conditions: List[str], risk_factors: List[str],
                                application_data: Dict[str, Any]) -> ApprovalDecision:
        """创建审批决策"""
        return ApprovalDecision(
            decision_id=str(uuid.uuid4()),
            application_id=application_id,
            status=status,
            approval_level=approval_level,
            decision_reason=reason,
            conditions=conditions,
            risk_factors=risk_factors,
            approval_amount=application_data.get("loan_amount", 0),
            approved_term=application_data.get("loan_term_months", 12),
            special_conditions=self._generate_special_conditions(status, conditions),
            decision_timestamp=datetime.now(),
            decision_officer="system" if status in [ApprovalStatus.AUTO_APPROVED, ApprovalStatus.AUTO_REJECTED] else "pending",
            confidence_score=self._calculate_decision_confidence(status, conditions, risk_factors)
        )
    
    def _generate_special_conditions(self, status: ApprovalStatus, conditions: List[str]) -> List[str]:
        """生成特殊条件"""
        special_conditions = []
        
        if status == ApprovalStatus.AUTO_APPROVED:
            special_conditions.append("按时还款")
            special_conditions.append("保持良好信用记录")
        elif status == ApprovalStatus.MANUAL_REVIEW:
            special_conditions.append("提供额外担保")
            special_conditions.append("增加首付比例")
            special_conditions.append("缩短贷款期限")
        
        return special_conditions
    
    def _calculate_decision_confidence(self, status: ApprovalStatus, 
                                     conditions: List[str], 
                                     risk_factors: List[str]) -> float:
        """计算决策置信度"""
        if status == ApprovalStatus.AUTO_APPROVED:
            return 0.9
        elif status == ApprovalStatus.AUTO_REJECTED:
            return 0.8
        elif status == ApprovalStatus.MANUAL_REVIEW:
            # 基于条件和风险因子数量调整置信度
            complexity_factor = len(conditions) + len(risk_factors)
            confidence = max(0.3, 0.8 - complexity_factor * 0.1)
            return confidence
        else:
            return 0.5
    
    def _create_default_decision(self, application_data: Dict[str, Any]) -> ApprovalDecision:
        """创建默认决策"""
        return ApprovalDecision(
            decision_id=str(uuid.uuid4()),
            application_id=application_data.get("application_id", str(uuid.uuid4())),
            status=ApprovalStatus.PENDING,
            approval_level=ApprovalLevel.SYSTEM,
            decision_reason="系统处理中",
            conditions=[],
            risk_factors=[],
            approval_amount=0,
            approved_term=0,
            special_conditions=[],
            decision_timestamp=datetime.now(),
            decision_officer="system",
            confidence_score=0.3
        )
    
    def get_approval_status(self, application_id: str) -> Optional[ApprovalDecision]:
        """获取审批状态"""
        return self.approval_decisions.get(application_id)
    
    def update_approval_decision(self, application_id: str, 
                               new_status: ApprovalStatus,
                               officer: str, reason: str) -> bool:
        """更新审批决策"""
        if application_id in self.approval_decisions:
            decision = self.approval_decisions[application_id]
            decision.status = new_status
            decision.decision_officer = officer
            decision.decision_reason = reason
            decision.decision_timestamp = datetime.now()
            return True
        return False
    
    def get_approval_statistics(self) -> Dict[str, Any]:
        """获取审批统计信息"""
        total_decisions = len(self.approval_decisions)
        
        status_counts = {}
        for decision in self.approval_decisions.values():
            status = decision.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_applications": total_decisions,
            "status_distribution": status_counts,
            "approval_rate": status_counts.get("approved", 0) / total_decisions if total_decisions > 0 else 0,
            "auto_approval_rate": status_counts.get("auto_approved", 0) / total_decisions if total_decisions > 0 else 0,
            "manual_review_rate": status_counts.get("manual_review", 0) / total_decisions if total_decisions > 0 else 0
        }
