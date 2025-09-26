"""
合规性检查器
提供监管合规检查和风险控制功能
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid

class ComplianceRule(Enum):
    """合规规则"""
    ANTI_MONEY_LAUNDERING = "anti_money_laundering"
    KNOW_YOUR_CUSTOMER = "know_your_customer"
    CREDIT_LIMIT = "credit_limit"
    INTEREST_RATE_CAP = "interest_rate_cap"
    DATA_PROTECTION = "data_protection"
    FAIR_LENDING = "fair_lending"
    DISCLOSURE_REQUIREMENTS = "disclosure_requirements"
    RISK_MANAGEMENT = "risk_management"

class ComplianceLevel(Enum):
    """合规等级"""
    COMPLIANT = "compliant"
    MINOR_VIOLATION = "minor_violation"
    MAJOR_VIOLATION = "major_violation"
    CRITICAL_VIOLATION = "critical_violation"

class RiskCategory(Enum):
    """风险类别"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    REGULATORY = "regulatory"
    REPUTATIONAL = "reputational"
    LEGAL = "legal"

@dataclass
class ComplianceCheck:
    """合规检查结果"""
    check_id: str
    rule_type: ComplianceRule
    compliance_level: ComplianceLevel
    is_compliant: bool
    violation_details: List[str]
    risk_score: float
    recommendations: List[str]
    check_timestamp: datetime
    checker_version: str

@dataclass
class ComplianceReport:
    """合规报告"""
    report_id: str
    application_id: str
    overall_compliance_score: float
    compliance_level: ComplianceLevel
    checks: List[ComplianceCheck]
    critical_violations: List[str]
    recommendations: List[str]
    report_timestamp: datetime
    requires_manual_review: bool

class ComplianceChecker:
    """合规性检查器"""
    
    def __init__(self):
        self.checker_version = "v2.1.0"
        self.compliance_rules = self._initialize_compliance_rules()
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.regulatory_limits = self._initialize_regulatory_limits()
    
    def _initialize_compliance_rules(self) -> Dict[ComplianceRule, Dict[str, Any]]:
        """初始化合规规则"""
        return {
            ComplianceRule.ANTI_MONEY_LAUNDERING: {
                "description": "反洗钱检查",
                "max_single_transaction": 50000,
                "suspicious_patterns": ["频繁大额交易", "异常资金来源", "高风险地区"],
                "required_documents": ["身份证", "收入证明", "银行流水"]
            },
            ComplianceRule.KNOW_YOUR_CUSTOMER: {
                "description": "了解客户检查",
                "required_verification": ["身份验证", "地址验证", "收入验证"],
                "risk_categories": ["政治人物", "高风险行业", "制裁名单"]
            },
            ComplianceRule.CREDIT_LIMIT: {
                "description": "信贷限额检查",
                "max_credit_ratio": 0.5,
                "max_annual_income_multiple": 10,
                "reserve_requirements": 0.1
            },
            ComplianceRule.INTEREST_RATE_CAP: {
                "description": "利率上限检查",
                "max_annual_rate": 0.24,  # 24%
                "max_daily_rate": 0.0007,  # 0.07%
                "usury_threshold": 0.36  # 36%
            },
            ComplianceRule.DATA_PROTECTION: {
                "description": "数据保护检查",
                "required_consent": True,
                "data_retention_years": 5,
                "encryption_required": True
            },
            ComplianceRule.FAIR_LENDING: {
                "description": "公平放贷检查",
                "prohibited_discrimination": ["种族", "性别", "年龄", "宗教"],
                "equal_opportunity_required": True
            },
            ComplianceRule.DISCLOSURE_REQUIREMENTS: {
                "description": "信息披露要求",
                "required_disclosures": ["年化利率", "总费用", "还款条件", "提前还款条款"],
                "clear_language_required": True
            },
            ComplianceRule.RISK_MANAGEMENT: {
                "description": "风险管理检查",
                "max_concentration_risk": 0.1,
                "stress_test_required": True,
                "monitoring_frequency": "daily"
            }
        }
    
    def _initialize_risk_thresholds(self) -> Dict[str, float]:
        """初始化风险阈值"""
        return {
            "low_risk_max": 0.3,
            "medium_risk_max": 0.6,
            "high_risk_max": 0.8,
            "critical_risk_max": 1.0
        }
    
    def _initialize_regulatory_limits(self) -> Dict[str, Any]:
        """初始化监管限制"""
        return {
            "max_loan_amount": 1000000,
            "max_interest_rate": 0.24,
            "min_credit_score": 600,
            "max_debt_ratio": 0.5,
            "min_employment_years": 1,
            "max_age": 65,
            "min_age": 22
        }
    
    def check_compliance(self, application_data: Dict[str, Any], 
                        risk_assessment: Dict[str, Any]) -> ComplianceReport:
        """执行合规检查"""
        try:
            report_id = str(uuid.uuid4())
            application_id = application_data.get("application_id", "unknown")
            
            # 执行各项合规检查
            checks = []
            for rule_type in ComplianceRule:
                check_result = self._perform_compliance_check(
                    rule_type, application_data, risk_assessment
                )
                checks.append(check_result)
            
            # 计算总体合规得分
            overall_score = self._calculate_overall_compliance_score(checks)
            
            # 确定合规等级
            compliance_level = self._determine_compliance_level(overall_score)
            
            # 识别关键违规
            critical_violations = self._identify_critical_violations(checks)
            
            # 生成建议
            recommendations = self._generate_compliance_recommendations(checks, critical_violations)
            
            # 判断是否需要人工审核
            requires_manual_review = self._requires_manual_review(compliance_level, critical_violations)
            
            return ComplianceReport(
                report_id=report_id,
                application_id=application_id,
                overall_compliance_score=overall_score,
                compliance_level=compliance_level,
                checks=checks,
                critical_violations=critical_violations,
                recommendations=recommendations,
                report_timestamp=datetime.now(),
                requires_manual_review=requires_manual_review
            )
            
        except Exception as e:
            logger.error(f"合规检查失败: {e}")
            return self._create_default_compliance_report(application_data)
    
    def _perform_compliance_check(self, rule_type: ComplianceRule,
                                application_data: Dict[str, Any],
                                risk_assessment: Dict[str, Any]) -> ComplianceCheck:
        """执行单个合规检查"""
        check_id = str(uuid.uuid4())
        rule_config = self.compliance_rules[rule_type]
        
        try:
            if rule_type == ComplianceRule.ANTI_MONEY_LAUNDERING:
                return self._check_anti_money_laundering(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.KNOW_YOUR_CUSTOMER:
                return self._check_know_your_customer(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.CREDIT_LIMIT:
                return self._check_credit_limit(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.INTEREST_RATE_CAP:
                return self._check_interest_rate_cap(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.DATA_PROTECTION:
                return self._check_data_protection(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.FAIR_LENDING:
                return self._check_fair_lending(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.DISCLOSURE_REQUIREMENTS:
                return self._check_disclosure_requirements(check_id, application_data, rule_config)
            elif rule_type == ComplianceRule.RISK_MANAGEMENT:
                return self._check_risk_management(check_id, application_data, risk_assessment, rule_config)
            else:
                return self._create_default_check(check_id, rule_type)
                
        except Exception as e:
            logger.error(f"合规检查失败: {rule_type.value}, {e}")
            return self._create_default_check(check_id, rule_type)
    
    def _check_anti_money_laundering(self, check_id: str, 
                                   application_data: Dict[str, Any],
                                   rule_config: Dict[str, Any]) -> ComplianceCheck:
        """反洗钱检查"""
        violations = []
        risk_score = 0.0
        
        # 检查单笔交易金额
        loan_amount = application_data.get("loan_amount", 0)
        if loan_amount > rule_config["max_single_transaction"]:
            violations.append(f"单笔贷款金额{loan_amount}超过反洗钱限额{rule_config['max_single_transaction']}")
            risk_score += 0.3
        
        # 检查资金来源
        income_source = application_data.get("income_source", "")
        if any(pattern in income_source for pattern in rule_config["suspicious_patterns"]):
            violations.append("资金来源可疑，需要进一步核实")
            risk_score += 0.4
        
        # 检查必要文档
        provided_docs = application_data.get("provided_documents", [])
        missing_docs = [doc for doc in rule_config["required_documents"] if doc not in provided_docs]
        if missing_docs:
            violations.append(f"缺少必要文档: {', '.join(missing_docs)}")
            risk_score += 0.2
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.ANTI_MONEY_LAUNDERING,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_aml_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_know_your_customer(self, check_id: str,
                                application_data: Dict[str, Any],
                                rule_config: Dict[str, Any]) -> ComplianceCheck:
        """了解客户检查"""
        violations = []
        risk_score = 0.0
        
        # 检查身份验证
        identity_verified = application_data.get("identity_verified", False)
        if not identity_verified:
            violations.append("身份验证未完成")
            risk_score += 0.3
        
        # 检查地址验证
        address_verified = application_data.get("address_verified", False)
        if not address_verified:
            violations.append("地址验证未完成")
            risk_score += 0.2
        
        # 检查收入验证
        income_verified = application_data.get("income_verified", False)
        if not income_verified:
            violations.append("收入验证未完成")
            risk_score += 0.3
        
        # 检查高风险类别
        customer_category = application_data.get("customer_category", "")
        if customer_category in rule_config["risk_categories"]:
            violations.append(f"客户属于高风险类别: {customer_category}")
            risk_score += 0.4
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.KNOW_YOUR_CUSTOMER,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_kyc_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_credit_limit(self, check_id: str,
                          application_data: Dict[str, Any],
                          rule_config: Dict[str, Any]) -> ComplianceCheck:
        """信贷限额检查"""
        violations = []
        risk_score = 0.0
        
        loan_amount = application_data.get("loan_amount", 0)
        annual_income = application_data.get("annual_income", 0)
        monthly_debt = application_data.get("monthly_debt", 0)
        monthly_income = application_data.get("monthly_income", 0)
        
        # 检查年收入倍数
        if annual_income > 0:
            income_multiple = loan_amount / annual_income
            if income_multiple > rule_config["max_annual_income_multiple"]:
                violations.append(f"贷款金额超过年收入{rule_config['max_annual_income_multiple']}倍限制")
                risk_score += 0.4
        
        # 检查负债比率
        if monthly_income > 0:
            debt_ratio = monthly_debt / monthly_income
            if debt_ratio > rule_config["max_credit_ratio"]:
                violations.append(f"负债比率{debt_ratio:.1%}超过{rule_config['max_credit_ratio']:.1%}限制")
                risk_score += 0.3
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.CREDIT_LIMIT,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_credit_limit_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_interest_rate_cap(self, check_id: str,
                               application_data: Dict[str, Any],
                               rule_config: Dict[str, Any]) -> ComplianceCheck:
        """利率上限检查"""
        violations = []
        risk_score = 0.0
        
        interest_rate = application_data.get("interest_rate", 0)
        
        # 检查年利率上限
        if interest_rate > rule_config["max_annual_rate"]:
            violations.append(f"年利率{interest_rate:.1%}超过{rule_config['max_annual_rate']:.1%}上限")
            risk_score += 0.5
        
        # 检查高利贷阈值
        if interest_rate > rule_config["usury_threshold"]:
            violations.append(f"年利率{interest_rate:.1%}超过高利贷{rule_config['usury_threshold']:.1%}阈值")
            risk_score += 0.8
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.INTEREST_RATE_CAP,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_interest_rate_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_data_protection(self, check_id: str,
                             application_data: Dict[str, Any],
                             rule_config: Dict[str, Any]) -> ComplianceCheck:
        """数据保护检查"""
        violations = []
        risk_score = 0.0
        
        # 检查数据使用同意
        data_consent = application_data.get("data_consent", False)
        if not data_consent:
            violations.append("未获得数据使用同意")
            risk_score += 0.4
        
        # 检查数据加密
        data_encrypted = application_data.get("data_encrypted", False)
        if not data_encrypted:
            violations.append("数据未加密存储")
            risk_score += 0.3
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.DATA_PROTECTION,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_data_protection_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_fair_lending(self, check_id: str,
                          application_data: Dict[str, Any],
                          rule_config: Dict[str, Any]) -> ComplianceCheck:
        """公平放贷检查"""
        violations = []
        risk_score = 0.0
        
        # 检查是否存在歧视性因素
        for prohibited_factor in rule_config["prohibited_discrimination"]:
            if prohibited_factor in str(application_data):
                violations.append(f"发现禁止的歧视因素: {prohibited_factor}")
                risk_score += 0.5
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.FAIR_LENDING,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_fair_lending_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_disclosure_requirements(self, check_id: str,
                                     application_data: Dict[str, Any],
                                     rule_config: Dict[str, Any]) -> ComplianceCheck:
        """信息披露要求检查"""
        violations = []
        risk_score = 0.0
        
        # 检查必要披露信息
        provided_disclosures = application_data.get("disclosures", [])
        missing_disclosures = [disclosure for disclosure in rule_config["required_disclosures"] 
                             if disclosure not in provided_disclosures]
        if missing_disclosures:
            violations.append(f"缺少必要披露信息: {', '.join(missing_disclosures)}")
            risk_score += 0.3
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.DISCLOSURE_REQUIREMENTS,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_disclosure_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _check_risk_management(self, check_id: str,
                             application_data: Dict[str, Any],
                             risk_assessment: Dict[str, Any],
                             rule_config: Dict[str, Any]) -> ComplianceCheck:
        """风险管理检查"""
        violations = []
        risk_score = 0.0
        
        # 检查集中度风险
        concentration_risk = application_data.get("concentration_risk", 0)
        if concentration_risk > rule_config["max_concentration_risk"]:
            violations.append(f"集中度风险{concentration_risk:.1%}超过{rule_config['max_concentration_risk']:.1%}限制")
            risk_score += 0.4
        
        # 检查压力测试
        stress_test_passed = application_data.get("stress_test_passed", False)
        if not stress_test_passed:
            violations.append("压力测试未通过")
            risk_score += 0.3
        
        compliance_level = self._determine_compliance_level_by_score(risk_score)
        
        return ComplianceCheck(
            check_id=check_id,
            rule_type=ComplianceRule.RISK_MANAGEMENT,
            compliance_level=compliance_level,
            is_compliant=len(violations) == 0,
            violation_details=violations,
            risk_score=risk_score,
            recommendations=self._generate_risk_management_recommendations(violations),
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    def _determine_compliance_level_by_score(self, risk_score: float) -> ComplianceLevel:
        """根据风险得分确定合规等级"""
        if risk_score <= self.risk_thresholds["low_risk_max"]:
            return ComplianceLevel.COMPLIANT
        elif risk_score <= self.risk_thresholds["medium_risk_max"]:
            return ComplianceLevel.MINOR_VIOLATION
        elif risk_score <= self.risk_thresholds["high_risk_max"]:
            return ComplianceLevel.MAJOR_VIOLATION
        else:
            return ComplianceLevel.CRITICAL_VIOLATION
    
    def _calculate_overall_compliance_score(self, checks: List[ComplianceCheck]) -> float:
        """计算总体合规得分"""
        if not checks:
            return 0.0
        
        total_score = sum(check.risk_score for check in checks)
        return 1.0 - (total_score / len(checks))
    
    def _determine_compliance_level(self, overall_score: float) -> ComplianceLevel:
        """确定总体合规等级"""
        if overall_score >= 0.8:
            return ComplianceLevel.COMPLIANT
        elif overall_score >= 0.6:
            return ComplianceLevel.MINOR_VIOLATION
        elif overall_score >= 0.4:
            return ComplianceLevel.MAJOR_VIOLATION
        else:
            return ComplianceLevel.CRITICAL_VIOLATION
    
    def _identify_critical_violations(self, checks: List[ComplianceCheck]) -> List[str]:
        """识别关键违规"""
        critical_violations = []
        
        for check in checks:
            if check.compliance_level == ComplianceLevel.CRITICAL_VIOLATION:
                critical_violations.extend(check.violation_details)
        
        return critical_violations
    
    def _generate_compliance_recommendations(self, checks: List[ComplianceCheck],
                                           critical_violations: List[str]) -> List[str]:
        """生成合规建议"""
        recommendations = []
        
        for check in checks:
            recommendations.extend(check.recommendations)
        
        if critical_violations:
            recommendations.append("存在关键违规，建议立即停止处理并上报合规部门")
        
        return list(set(recommendations))  # 去重
    
    def _requires_manual_review(self, compliance_level: ComplianceLevel,
                              critical_violations: List[str]) -> bool:
        """判断是否需要人工审核"""
        return (compliance_level in [ComplianceLevel.MAJOR_VIOLATION, ComplianceLevel.CRITICAL_VIOLATION] 
                or len(critical_violations) > 0)
    
    def _create_default_compliance_report(self, application_data: Dict[str, Any]) -> ComplianceReport:
        """创建默认合规报告"""
        return ComplianceReport(
            report_id=str(uuid.uuid4()),
            application_id=application_data.get("application_id", "unknown"),
            overall_compliance_score=0.5,
            compliance_level=ComplianceLevel.MINOR_VIOLATION,
            checks=[],
            critical_violations=[],
            recommendations=["需要进一步合规检查"],
            report_timestamp=datetime.now(),
            requires_manual_review=True
        )
    
    def _create_default_check(self, check_id: str, rule_type: ComplianceRule) -> ComplianceCheck:
        """创建默认检查结果"""
        return ComplianceCheck(
            check_id=check_id,
            rule_type=rule_type,
            compliance_level=ComplianceLevel.MINOR_VIOLATION,
            is_compliant=False,
            violation_details=["检查失败"],
            risk_score=0.5,
            recommendations=["需要重新检查"],
            check_timestamp=datetime.now(),
            checker_version=self.checker_version
        )
    
    # 生成各种建议的方法
    def _generate_aml_recommendations(self, violations: List[str]) -> List[str]:
        """生成反洗钱建议"""
        recommendations = []
        if violations:
            recommendations.append("加强客户身份验证")
            recommendations.append("核实资金来源")
            recommendations.append("完善文档收集")
        return recommendations
    
    def _generate_kyc_recommendations(self, violations: List[str]) -> List[str]:
        """生成了解客户建议"""
        recommendations = []
        if violations:
            recommendations.append("完善客户身份验证流程")
            recommendations.append("加强收入验证")
            recommendations.append("建立客户风险分类体系")
        return recommendations
    
    def _generate_credit_limit_recommendations(self, violations: List[str]) -> List[str]:
        """生成信贷限额建议"""
        recommendations = []
        if violations:
            recommendations.append("调整贷款金额")
            recommendations.append("要求提供担保")
            recommendations.append("延长还款期限")
        return recommendations
    
    def _generate_interest_rate_recommendations(self, violations: List[str]) -> List[str]:
        """生成利率建议"""
        recommendations = []
        if violations:
            recommendations.append("降低贷款利率至合规范围")
            recommendations.append("调整费用结构")
            recommendations.append("提供利率优惠")
        return recommendations
    
    def _generate_data_protection_recommendations(self, violations: List[str]) -> List[str]:
        """生成数据保护建议"""
        recommendations = []
        if violations:
            recommendations.append("获得明确的数据使用同意")
            recommendations.append("实施数据加密")
            recommendations.append("建立数据保护制度")
        return recommendations
    
    def _generate_fair_lending_recommendations(self, violations: List[str]) -> List[str]:
        """生成公平放贷建议"""
        recommendations = []
        if violations:
            recommendations.append("消除歧视性因素")
            recommendations.append("建立公平放贷政策")
            recommendations.append("加强员工培训")
        return recommendations
    
    def _generate_disclosure_recommendations(self, violations: List[str]) -> List[str]:
        """生成信息披露建议"""
        recommendations = []
        if violations:
            recommendations.append("完善信息披露内容")
            recommendations.append("使用清晰易懂的语言")
            recommendations.append("确保信息透明度")
        return recommendations
    
    def _generate_risk_management_recommendations(self, violations: List[str]) -> List[str]:
        """生成风险管理建议"""
        recommendations = []
        if violations:
            recommendations.append("加强风险监控")
            recommendations.append("完善压力测试")
            recommendations.append("建立风险预警机制")
        return recommendations
