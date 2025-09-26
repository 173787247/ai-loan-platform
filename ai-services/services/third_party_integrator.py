"""
第三方服务集成器
提供征信、KYC、反欺诈等外部API的统一集成
"""

import json
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from dataclasses import dataclass
from enum import Enum
import uuid
import hashlib
import hmac
import base64

class ServiceType(Enum):
    """服务类型"""
    CREDIT_BUREAU = "credit_bureau"
    KYC_VERIFICATION = "kyc_verification"
    ANTI_FRAUD = "anti_fraud"
    BANK_ACCOUNT_VERIFICATION = "bank_account_verification"
    EMPLOYMENT_VERIFICATION = "employment_verification"
    INCOME_VERIFICATION = "income_verification"
    BLACKLIST_CHECK = "blacklist_check"
    SANCTIONS_CHECK = "sanctions_check"

class ServiceStatus(Enum):
    """服务状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"

@dataclass
class ServiceConfig:
    """服务配置"""
    service_name: str
    service_type: ServiceType
    base_url: str
    api_key: str
    secret_key: str
    timeout: int
    retry_count: int
    rate_limit: int
    status: ServiceStatus
    priority: int

@dataclass
class ServiceResponse:
    """服务响应"""
    service_name: str
    success: bool
    data: Dict[str, Any]
    error_message: str
    response_time: float
    timestamp: datetime
    request_id: str

class ThirdPartyServiceIntegrator:
    """第三方服务集成器"""
    
    def __init__(self):
        self.services: Dict[str, ServiceConfig] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self._initialize_services()
    
    def _initialize_services(self):
        """初始化第三方服务配置"""
        # 征信服务
        self.services["credit_bureau_1"] = ServiceConfig(
            service_name="征信中心API",
            service_type=ServiceType.CREDIT_BUREAU,
            base_url="https://api.credit-bureau.com/v1",
            api_key="cb_api_key_123",
            secret_key="cb_secret_456",
            timeout=30,
            retry_count=3,
            rate_limit=100,
            status=ServiceStatus.ACTIVE,
            priority=1
        )
        
        # KYC验证服务
        self.services["kyc_service_1"] = ServiceConfig(
            service_name="身份验证API",
            service_type=ServiceType.KYC_VERIFICATION,
            base_url="https://api.kyc-service.com/v2",
            api_key="kyc_api_key_789",
            secret_key="kyc_secret_012",
            timeout=20,
            retry_count=2,
            rate_limit=200,
            status=ServiceStatus.ACTIVE,
            priority=1
        )
        
        # 反欺诈服务
        self.services["anti_fraud_1"] = ServiceConfig(
            service_name="反欺诈检测API",
            service_type=ServiceType.ANTI_FRAUD,
            base_url="https://api.anti-fraud.com/v1",
            api_key="af_api_key_345",
            secret_key="af_secret_678",
            timeout=15,
            retry_count=2,
            rate_limit=500,
            status=ServiceStatus.ACTIVE,
            priority=1
        )
        
        # 银行账户验证
        self.services["bank_verify_1"] = ServiceConfig(
            service_name="银行账户验证API",
            service_type=ServiceType.BANK_ACCOUNT_VERIFICATION,
            base_url="https://api.bank-verify.com/v1",
            api_key="bv_api_key_901",
            secret_key="bv_secret_234",
            timeout=25,
            retry_count=3,
            rate_limit=150,
            status=ServiceStatus.ACTIVE,
            priority=2
        )
        
        # 就业验证服务
        self.services["employment_verify_1"] = ServiceConfig(
            service_name="就业验证API",
            service_type=ServiceType.EMPLOYMENT_VERIFICATION,
            base_url="https://api.employment-verify.com/v1",
            api_key="ev_api_key_567",
            secret_key="ev_secret_890",
            timeout=20,
            retry_count=2,
            rate_limit=100,
            status=ServiceStatus.ACTIVE,
            priority=2
        )
        
        # 黑名单检查
        self.services["blacklist_check_1"] = ServiceConfig(
            service_name="黑名单检查API",
            service_type=ServiceType.BLACKLIST_CHECK,
            base_url="https://api.blacklist-check.com/v1",
            api_key="bl_api_key_123",
            secret_key="bl_secret_456",
            timeout=10,
            retry_count=2,
            rate_limit=1000,
            status=ServiceStatus.ACTIVE,
            priority=1
        )
        
        # 制裁名单检查
        self.services["sanctions_check_1"] = ServiceConfig(
            service_name="制裁名单检查API",
            service_type=ServiceType.SANCTIONS_CHECK,
            base_url="https://api.sanctions-check.com/v1",
            api_key="sc_api_key_789",
            secret_key="sc_secret_012",
            timeout=10,
            retry_count=2,
            rate_limit=1000,
            status=ServiceStatus.ACTIVE,
            priority=1
        )
        
        # 初始化熔断器
        for service_name in self.services:
            self.circuit_breakers[service_name] = {
                "failure_count": 0,
                "last_failure_time": None,
                "state": "closed",  # closed, open, half-open
                "failure_threshold": 5,
                "timeout": 60
            }
    
    async def initialize(self):
        """初始化HTTP会话"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        logger.info("第三方服务集成器初始化完成")
    
    async def close(self):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def get_credit_report(self, user_id: str, id_number: str) -> ServiceResponse:
        """获取征信报告"""
        service_name = "credit_bureau_1"
        request_data = {
            "user_id": user_id,
            "id_number": id_number,
            "report_type": "comprehensive"
        }
        
        return await self._call_service(service_name, "credit-report", request_data)
    
    async def verify_identity(self, id_number: str, name: str, phone: str) -> ServiceResponse:
        """身份验证"""
        service_name = "kyc_service_1"
        request_data = {
            "id_number": id_number,
            "name": name,
            "phone": phone,
            "verification_type": "comprehensive"
        }
        
        return await self._call_service(service_name, "verify-identity", request_data)
    
    async def check_fraud_risk(self, user_data: Dict[str, Any]) -> ServiceResponse:
        """反欺诈检查"""
        service_name = "anti_fraud_1"
        request_data = {
            "user_data": user_data,
            "check_type": "comprehensive",
            "risk_level": "high"
        }
        
        return await self._call_service(service_name, "fraud-check", request_data)
    
    async def verify_bank_account(self, account_number: str, bank_code: str, account_name: str) -> ServiceResponse:
        """银行账户验证"""
        service_name = "bank_verify_1"
        request_data = {
            "account_number": account_number,
            "bank_code": bank_code,
            "account_name": account_name,
            "verification_type": "account_verification"
        }
        
        return await self._call_service(service_name, "verify-account", request_data)
    
    async def verify_employment(self, company_name: str, employee_id: str, phone: str) -> ServiceResponse:
        """就业验证"""
        service_name = "employment_verify_1"
        request_data = {
            "company_name": company_name,
            "employee_id": employee_id,
            "phone": phone,
            "verification_type": "employment_status"
        }
        
        return await self._call_service(service_name, "verify-employment", request_data)
    
    async def check_blacklist(self, id_number: str, phone: str, name: str) -> ServiceResponse:
        """黑名单检查"""
        service_name = "blacklist_check_1"
        request_data = {
            "id_number": id_number,
            "phone": phone,
            "name": name,
            "check_type": "comprehensive"
        }
        
        return await self._call_service(service_name, "blacklist-check", request_data)
    
    async def check_sanctions(self, id_number: str, name: str, nationality: str) -> ServiceResponse:
        """制裁名单检查"""
        service_name = "sanctions_check_1"
        request_data = {
            "id_number": id_number,
            "name": name,
            "nationality": nationality,
            "check_type": "sanctions_screening"
        }
        
        return await self._call_service(service_name, "sanctions-check", request_data)
    
    async def _call_service(self, service_name: str, endpoint: str, data: Dict[str, Any]) -> ServiceResponse:
        """调用第三方服务"""
        if service_name not in self.services:
            return ServiceResponse(
                service_name=service_name,
                success=False,
                data={},
                error_message="服务不存在",
                response_time=0.0,
                timestamp=datetime.now(),
                request_id=str(uuid.uuid4())
            )
        
        service_config = self.services[service_name]
        request_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # 检查熔断器状态
        if self._is_circuit_breaker_open(service_name):
            return ServiceResponse(
                service_name=service_name,
                success=False,
                data={},
                error_message="服务熔断器开启",
                response_time=0.0,
                timestamp=start_time,
                request_id=request_id
            )
        
        try:
            # 构建请求
            url = f"{service_config.base_url}/{endpoint}"
            headers = self._build_headers(service_config, data, request_id)
            
            # 发送请求
            async with self.session.post(url, json=data, headers=headers) as response:
                response_time = (datetime.now() - start_time).total_seconds()
                
                if response.status == 200:
                    result_data = await response.json()
                    self._reset_circuit_breaker(service_name)
                    
                    return ServiceResponse(
                        service_name=service_name,
                        success=True,
                        data=result_data,
                        error_message="",
                        response_time=response_time,
                        timestamp=start_time,
                        request_id=request_id
                    )
                else:
                    error_text = await response.text()
                    self._record_circuit_breaker_failure(service_name)
                    
                    return ServiceResponse(
                        service_name=service_name,
                        success=False,
                        data={},
                        error_message=f"HTTP {response.status}: {error_text}",
                        response_time=response_time,
                        timestamp=start_time,
                        request_id=request_id
                    )
                    
        except asyncio.TimeoutError:
            response_time = (datetime.now() - start_time).total_seconds()
            self._record_circuit_breaker_failure(service_name)
            
            return ServiceResponse(
                service_name=service_name,
                success=False,
                data={},
                error_message="请求超时",
                response_time=response_time,
                timestamp=start_time,
                request_id=request_id
            )
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            self._record_circuit_breaker_failure(service_name)
            
            return ServiceResponse(
                service_name=service_name,
                success=False,
                data={},
                error_message=str(e),
                response_time=response_time,
                timestamp=start_time,
                request_id=request_id
            )
    
    def _build_headers(self, service_config: ServiceConfig, data: Dict[str, Any], request_id: str) -> Dict[str, str]:
        """构建请求头"""
        timestamp = str(int(datetime.now().timestamp()))
        nonce = str(uuid.uuid4())
        
        # 构建签名字符串
        signature_string = f"{service_config.api_key}{timestamp}{nonce}{json.dumps(data, sort_keys=True)}"
        signature = hmac.new(
            service_config.secret_key.encode(),
            signature_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return {
            "Content-Type": "application/json",
            "X-API-Key": service_config.api_key,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Signature": signature,
            "X-Request-ID": request_id,
            "User-Agent": "AI-Loan-Platform/2.1.0"
        }
    
    def _is_circuit_breaker_open(self, service_name: str) -> bool:
        """检查熔断器是否开启"""
        if service_name not in self.circuit_breakers:
            return False
        
        breaker = self.circuit_breakers[service_name]
        
        if breaker["state"] == "open":
            # 检查是否可以尝试半开状态
            if breaker["last_failure_time"]:
                time_since_failure = (datetime.now() - breaker["last_failure_time"]).total_seconds()
                if time_since_failure > breaker["timeout"]:
                    breaker["state"] = "half-open"
                    return False
            return True
        
        return False
    
    def _record_circuit_breaker_failure(self, service_name: str):
        """记录熔断器失败"""
        if service_name not in self.circuit_breakers:
            return
        
        breaker = self.circuit_breakers[service_name]
        breaker["failure_count"] += 1
        breaker["last_failure_time"] = datetime.now()
        
        if breaker["failure_count"] >= breaker["failure_threshold"]:
            breaker["state"] = "open"
            logger.warning(f"服务 {service_name} 熔断器开启")
    
    def _reset_circuit_breaker(self, service_name: str):
        """重置熔断器"""
        if service_name not in self.circuit_breakers:
            return
        
        breaker = self.circuit_breakers[service_name]
        breaker["failure_count"] = 0
        breaker["last_failure_time"] = None
        breaker["state"] = "closed"
    
    async def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        status_info = {}
        
        for service_name, config in self.services.items():
            breaker = self.circuit_breakers.get(service_name, {})
            status_info[service_name] = {
                "service_name": config.service_name,
                "service_type": config.service_type.value,
                "status": config.status.value,
                "circuit_breaker_state": breaker.get("state", "closed"),
                "failure_count": breaker.get("failure_count", 0),
                "priority": config.priority,
                "rate_limit": config.rate_limit,
                "timeout": config.timeout
            }
        
        return status_info
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        health_results = {}
        
        for service_name, config in self.services.items():
            try:
                # 发送简单的健康检查请求
                url = f"{config.base_url}/health"
                headers = {"X-API-Key": config.api_key}
                
                async with self.session.get(url, headers=headers) as response:
                    health_results[service_name] = {
                        "status": "healthy" if response.status == 200 else "unhealthy",
                        "response_time": response.headers.get("X-Response-Time", "N/A"),
                        "last_check": datetime.now().isoformat()
                    }
            except Exception as e:
                health_results[service_name] = {
                    "status": "error",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        return health_results
    
    def update_service_config(self, service_name: str, config_updates: Dict[str, Any]):
        """更新服务配置"""
        if service_name in self.services:
            config = self.services[service_name]
            for key, value in config_updates.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            logger.info(f"服务 {service_name} 配置已更新")
    
    def add_service(self, service_name: str, config: ServiceConfig):
        """添加新服务"""
        self.services[service_name] = config
        self.circuit_breakers[service_name] = {
            "failure_count": 0,
            "last_failure_time": None,
            "state": "closed",
            "failure_threshold": 5,
            "timeout": 60
        }
        logger.info(f"新服务 {service_name} 已添加")
    
    def remove_service(self, service_name: str):
        """移除服务"""
        if service_name in self.services:
            del self.services[service_name]
            if service_name in self.circuit_breakers:
                del self.circuit_breakers[service_name]
            logger.info(f"服务 {service_name} 已移除")

# 全局实例
third_party_integrator = ThirdPartyServiceIntegrator()
