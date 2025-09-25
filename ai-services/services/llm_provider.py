"""
LLM提供商管理服务
支持多种LLM API：OpenAI、DeepSeek、通义千问、智谱AI、百度文心一言、月之暗面等

@author AI Loan Platform Team
@version 1.0.0
"""

import os
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from enum import Enum
from loguru import logger
import json

class LLMProvider(Enum):
    """LLM提供商枚举"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    ZHIPU = "zhipu"
    BAIDU = "baidu"
    KIMI = "kimi"

class LLMProviderManager:
    """LLM提供商管理器"""
    
    def __init__(self):
        self.providers = {}
        self.default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "deepseek")
        self._initialize_providers()
    
    async def initialize(self):
        """初始化LLM提供商管理器"""
        try:
            self._initialize_providers()
            logger.info(f"LLM提供商管理器初始化成功，支持 {len(self.providers)} 个提供商")
            return True
        except Exception as e:
            logger.error(f"LLM提供商管理器初始化失败: {e}")
            return False
    
    def _initialize_providers(self):
        """初始化所有LLM提供商配置"""
        # OpenAI配置
        if os.getenv("OPENAI_API_KEY"):
            self.providers[LLMProvider.OPENAI] = {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
                "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
                "headers": {
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    "Content-Type": "application/json"
                }
            }
        
        # DeepSeek配置
        if os.getenv("DEEPSEEK_API_KEY"):
            self.providers[LLMProvider.DEEPSEEK] = {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
                "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
                "headers": {
                    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                    "Content-Type": "application/json"
                }
            }
        
        # 通义千问配置
        if os.getenv("QWEN_API_KEY"):
            self.providers[LLMProvider.QWEN] = {
                "api_key": os.getenv("QWEN_API_KEY"),
                "base_url": os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1"),
                "model": os.getenv("QWEN_MODEL", "qwen-turbo"),
                "headers": {
                    "Authorization": f"Bearer {os.getenv('QWEN_API_KEY')}",
                    "Content-Type": "application/json"
                }
            }
        
        # 智谱AI配置
        if os.getenv("ZHIPU_API_KEY"):
            self.providers[LLMProvider.ZHIPU] = {
                "api_key": os.getenv("ZHIPU_API_KEY"),
                "base_url": os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4"),
                "model": os.getenv("ZHIPU_MODEL", "glm-4"),
                "headers": {
                    "Authorization": f"Bearer {os.getenv('ZHIPU_API_KEY')}",
                    "Content-Type": "application/json"
                }
            }
        
        # 百度文心一言配置
        if os.getenv("BAIDU_API_KEY") and os.getenv("BAIDU_SECRET_KEY"):
            self.providers[LLMProvider.BAIDU] = {
                "api_key": os.getenv("BAIDU_API_KEY"),
                "secret_key": os.getenv("BAIDU_SECRET_KEY"),
                "base_url": os.getenv("BAIDU_BASE_URL", "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"),
                "model": os.getenv("BAIDU_MODEL", "ernie-bot-turbo"),
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        
        # 月之暗面配置
        if os.getenv("KIMI_API_KEY"):
            self.providers[LLMProvider.KIMI] = {
                "api_key": os.getenv("KIMI_API_KEY"),
                "base_url": os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1"),
                "model": os.getenv("KIMI_MODEL", "moonshot-v1-8k"),
                "headers": {
                    "Authorization": f"Bearer {os.getenv('KIMI_API_KEY')}",
                    "Content-Type": "application/json"
                }
            }
        
        logger.info(f"已初始化 {len(self.providers)} 个LLM提供商: {list(self.providers.keys())}")
    
    def get_available_providers(self) -> List[str]:
        """获取可用的LLM提供商列表"""
        return [provider.value for provider in self.providers.keys()]
    
    def get_default_provider(self) -> Optional[str]:
        """获取默认提供商"""
        if self.default_provider in self.get_available_providers():
            return self.default_provider
        elif self.providers:
            return list(self.providers.keys())[0].value
        return None
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """生成AI回复"""
        try:
            # 确定使用的提供商
            if not provider:
                provider = self.get_default_provider()
            
            if not provider or provider not in self.get_available_providers():
                raise ValueError(f"未找到可用的LLM提供商: {provider}")
            
            provider_enum = LLMProvider(provider)
            provider_config = self.providers[provider_enum]
            
            # 使用指定的模型或默认模型
            model_name = model or provider_config["model"]
            
            # 根据提供商调用相应的API
            if provider_enum == LLMProvider.OPENAI:
                return await self._call_openai_api(provider_config, messages, model_name, temperature, max_tokens)
            elif provider_enum == LLMProvider.DEEPSEEK:
                return await self._call_deepseek_api(provider_config, messages, model_name, temperature, max_tokens)
            elif provider_enum == LLMProvider.QWEN:
                return await self._call_qwen_api(provider_config, messages, model_name, temperature, max_tokens)
            elif provider_enum == LLMProvider.ZHIPU:
                return await self._call_zhipu_api(provider_config, messages, model_name, temperature, max_tokens)
            elif provider_enum == LLMProvider.BAIDU:
                return await self._call_baidu_api(provider_config, messages, model_name, temperature, max_tokens)
            elif provider_enum == LLMProvider.KIMI:
                return await self._call_kimi_api(provider_config, messages, model_name, temperature, max_tokens)
            else:
                raise ValueError(f"不支持的LLM提供商: {provider}")
                
        except Exception as e:
            logger.error(f"LLM生成回复失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "抱歉，我暂时无法处理您的请求，请稍后再试。"
            }
    
    async def _call_openai_api(self, config: Dict, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """调用OpenAI API"""
        url = f"{config['base_url']}/chat/completions"
        
        # GPT-5使用max_completion_tokens，其他模型使用max_tokens
        if model.startswith("gpt-5") or model.startswith("gpt-4o"):
            token_param = "max_completion_tokens"
        else:
            token_param = "max_tokens"
        
        # GPT-5只支持temperature=1.0
        if model.startswith("gpt-5"):
            temperature = 1.0
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            token_param: max_tokens
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=config["headers"], json=payload, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result["choices"][0]["message"]["content"],
                        "provider": "openai",
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API调用失败: {response.status} - {error_text}")
    
    async def _call_deepseek_api(self, config: Dict, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """调用DeepSeek API"""
        url = f"{config['base_url']}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=config["headers"], json=payload, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result["choices"][0]["message"]["content"],
                        "provider": "deepseek",
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"DeepSeek API调用失败: {response.status} - {error_text}")
    
    async def _call_qwen_api(self, config: Dict, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """调用通义千问API"""
        url = f"{config['base_url']}/services/aigc/text-generation/generation"
        payload = {
            "model": model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=config["headers"], json=payload, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result["output"]["text"],
                        "provider": "qwen",
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"通义千问API调用失败: {response.status} - {error_text}")
    
    async def _call_zhipu_api(self, config: Dict, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """调用智谱AI API"""
        url = f"{config['base_url']}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=config["headers"], json=payload, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result["choices"][0]["message"]["content"],
                        "provider": "zhipu",
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"智谱AI API调用失败: {response.status} - {error_text}")
    
    async def _call_baidu_api(self, config: Dict, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """调用百度文心一言API"""
        # 百度API需要先获取access_token
        access_token = await self._get_baidu_access_token(config["api_key"], config["secret_key"])
        
        url = f"{config['base_url']}?access_token={access_token}"
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=config["headers"], json=payload, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result["result"],
                        "provider": "baidu",
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"百度文心一言API调用失败: {response.status} - {error_text}")
    
    async def _call_kimi_api(self, config: Dict, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """调用月之暗面API"""
        url = f"{config['base_url']}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=config["headers"], json=payload, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result["choices"][0]["message"]["content"],
                        "provider": "kimi",
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"月之暗面API调用失败: {response.status} - {error_text}")
    
    async def _get_baidu_access_token(self, api_key: str, secret_key: str) -> str:
        """获取百度API的access_token"""
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": secret_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["access_token"]
                else:
                    raise Exception(f"获取百度access_token失败: {response.status}")

# 创建全局实例
llm_provider_manager = LLMProviderManager()
