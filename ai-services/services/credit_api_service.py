"""
征信API服务 - 集成第三方征信查询
支持京东万象、企查查等免费试用API
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from loguru import logger
from datetime import datetime
import hashlib
import hmac
import base64

class CreditAPIService:
    """征信API服务"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # API配置
        self.apis = {
            'jingdong': {
                'name': '京东万象',
                'base_url': 'https://way.jd.com',
                'app_key': 'your_jd_app_key',  # 需要申请
                'secret': 'your_jd_secret',    # 需要申请
                'free_quota': 1000,  # 免费额度
                'endpoints': {
                    'enterprise_credit': '/jisuapi/enterprisecredit',
                    'dishonest_person': '/jisuapi/dishonestperson',
                    'court_execution': '/jisuapi/courtexecution'
                }
            },
            'qichacha': {
                'name': '企查查',
                'base_url': 'https://api.qichacha.com',
                'app_key': 'your_qcc_app_key',  # 需要申请
                'secret': 'your_qcc_secret',    # 需要申请
                'free_quota': 100,  # 免费额度
                'endpoints': {
                    'enterprise_info': '/ECIV4/GetBasicDetailsByName',
                    'enterprise_credit': '/ECIV4/GetCreditScore',
                    'enterprise_risk': '/ECIV4/GetRiskInfo'
                }
            },
            'apispace': {
                'name': 'APISpace',
                'base_url': 'https://eolink.o.apispace.com',
                'api_key': 'your_apispace_key',  # 需要申请
                'free_quota': 500,  # 免费额度
                'endpoints': {
                    'enterprise_credit': '/credit-rating/query',
                    'enterprise_info': '/enterprise-info/query'
                }
            }
        }
        
        # 使用统计
        self.usage_stats = {
            'jingdong': {'used': 0, 'last_reset': datetime.now()},
            'qichacha': {'used': 0, 'last_reset': datetime.now()},
            'apispace': {'used': 0, 'last_reset': datetime.now()}
        }
    
    def _check_quota(self, provider: str) -> bool:
        """检查API使用额度"""
        if provider not in self.usage_stats:
            return False
            
        stats = self.usage_stats[provider]
        quota = self.apis[provider]['free_quota']
        
        # 检查是否超过免费额度
        if stats['used'] >= quota:
            logger.warning(f"{provider} API 免费额度已用完")
            return False
            
        return True
    
    def _update_usage(self, provider: str):
        """更新使用统计"""
        if provider in self.usage_stats:
            self.usage_stats[provider]['used'] += 1
    
    def _generate_jd_signature(self, params: Dict[str, Any], secret: str) -> str:
        """生成京东万象签名"""
        # 按参数名排序
        sorted_params = sorted(params.items())
        # 拼接参数
        query_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
        # 添加密钥
        sign_string = f"{secret}&{query_string}"
        # MD5加密
        return hashlib.md5(sign_string.encode('utf-8')).hexdigest()
    
    def _call_jingdong_api(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用京东万象API"""
        if not self._check_quota('jingdong'):
            return {'error': '免费额度已用完', 'provider': 'jingdong'}
        
        config = self.apis['jingdong']
        url = f"{config['base_url']}{config['endpoints'][endpoint]}"
        
        # 添加公共参数
        params.update({
            'appkey': config['app_key'],
            'timestamp': str(int(time.time()))
        })
        
        # 生成签名
        signature = self._generate_jd_signature(params, config['secret'])
        params['sign'] = signature
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            self._update_usage('jingdong')
            
            if result.get('code') == '10000':  # 成功
                return {
                    'success': True,
                    'data': result.get('result', {}),
                    'provider': 'jingdong',
                    'quota_remaining': config['free_quota'] - self.usage_stats['jingdong']['used']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('msg', 'API调用失败'),
                    'provider': 'jingdong'
                }
                
        except Exception as e:
            logger.error(f"京东万象API调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'provider': 'jingdong'
            }
    
    def _call_qichacha_api(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用企查查API"""
        if not self._check_quota('qichacha'):
            return {'error': '免费额度已用完', 'provider': 'qichacha'}
        
        config = self.apis['qichacha']
        url = f"{config['base_url']}{config['endpoints'][endpoint]}"
        
        # 添加认证头
        headers = {
            'Token': config['app_key'],
            'Timespan': str(int(time.time())),
            'Content-Type': 'application/json'
        }
        
        try:
            response = self.session.post(url, json=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            self._update_usage('qichacha')
            
            if result.get('Status') == '200':  # 成功
                return {
                    'success': True,
                    'data': result.get('Result', {}),
                    'provider': 'qichacha',
                    'quota_remaining': config['free_quota'] - self.usage_stats['qichacha']['used']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('Message', 'API调用失败'),
                    'provider': 'qichacha'
                }
                
        except Exception as e:
            logger.error(f"企查查API调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'provider': 'qichacha'
            }
    
    def _call_apispace_api(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用APISpace API"""
        if not self._check_quota('apispace'):
            return {'error': '免费额度已用完', 'provider': 'apispace'}
        
        config = self.apis['apispace']
        url = f"{config['base_url']}{config['endpoints'][endpoint]}"
        
        # 添加API密钥
        headers = {
            'X-APISpace-Token': config['api_key'],
            'Authorization-Type': 'apikey'
        }
        
        try:
            response = self.session.post(url, json=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            self._update_usage('apispace')
            
            if result.get('code') == 200:  # 成功
                return {
                    'success': True,
                    'data': result.get('data', {}),
                    'provider': 'apispace',
                    'quota_remaining': config['free_quota'] - self.usage_stats['apispace']['used']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'API调用失败'),
                    'provider': 'apispace'
                }
                
        except Exception as e:
            logger.error(f"APISpace API调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'provider': 'apispace'
            }
    
    def query_enterprise_credit(self, company_name: str, provider: str = 'jingdong') -> Dict[str, Any]:
        """查询企业信用评分"""
        logger.info(f"查询企业信用: {company_name}, 提供商: {provider}")
        
        if provider == 'jingdong':
            params = {'companyName': company_name}
            return self._call_jingdong_api('enterprise_credit', params)
        
        elif provider == 'qichacha':
            params = {'keyword': company_name}
            return self._call_qichacha_api('enterprise_credit', params)
        
        elif provider == 'apispace':
            params = {'company_name': company_name}
            return self._call_apispace_api('enterprise_credit', params)
        
        else:
            return {
                'success': False,
                'error': f'不支持的提供商: {provider}',
                'provider': provider
            }
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        stats = {}
        for provider, config in self.apis.items():
            usage = self.usage_stats[provider]
            stats[provider] = {
                'name': config['name'],
                'used': usage['used'],
                'quota': config['free_quota'],
                'remaining': config['free_quota'] - usage['used'],
                'last_reset': usage['last_reset'].isoformat()
            }
        return stats
    
    def reset_usage_stats(self, provider: str = None):
        """重置使用统计"""
        if provider:
            if provider in self.usage_stats:
                self.usage_stats[provider] = {'used': 0, 'last_reset': datetime.now()}
        else:
            for p in self.usage_stats:
                self.usage_stats[p] = {'used': 0, 'last_reset': datetime.now()}

# 创建全局实例
credit_api_service = CreditAPIService()
