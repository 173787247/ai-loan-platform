"""
AI助贷招标智能体 - LLM模型集成
支持多种大语言模型的统一接口

@author AI Loan Platform Team
@version 1.1.0
"""

import os
import json
import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from dataclasses import dataclass
import openai
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from loguru import logger

class LLMProvider(Enum):
    """LLM提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    BAIDU = "baidu"
    ALIBABA = "alibaba"
    TENCENT = "tencent"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    CHATGLM = "chatglm"
    LOCAL = "local"

@dataclass
class LLMConfig:
    """LLM配置"""
    provider: LLMProvider
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

class BaseLLM(ABC):
    """LLM基类"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass
    
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话生成"""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI模型"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        openai.api_key = config.api_key
        if config.base_url:
            openai.api_base = config.base_url
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                top_p=kwargs.get("top_p", self.config.top_p),
                frequency_penalty=kwargs.get("frequency_penalty", self.config.frequency_penalty),
                presence_penalty=kwargs.get("presence_penalty", self.config.presence_penalty)
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI生成失败: {str(e)}")
            raise
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话生成"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=messages,
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                top_p=kwargs.get("top_p", self.config.top_p),
                frequency_penalty=kwargs.get("frequency_penalty", self.config.frequency_penalty),
                presence_penalty=kwargs.get("presence_penalty", self.config.presence_penalty)
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI对话失败: {str(e)}")
            raise

class AnthropicLLM(BaseLLM):
    """Anthropic Claude模型"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = config.base_url or "https://api.anthropic.com"
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                }
                
                data = {
                    "model": self.config.model_name,
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": kwargs.get("max_tokens", self.config.max_tokens),
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "top_p": kwargs.get("top_p", self.config.top_p)
                }
                
                async with session.post(
                    f"{self.base_url}/v1/complete",
                    headers=headers,
                    json=data
                ) as response:
                    result = await response.json()
                    return result["completion"]
        except Exception as e:
            self.logger.error(f"Anthropic生成失败: {str(e)}")
            raise
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话生成"""
        # 将消息转换为Claude格式
        prompt = ""
        for msg in messages:
            role = "Human" if msg["role"] == "user" else "Assistant"
            prompt += f"\n\n{role}: {msg['content']}"
        prompt += "\n\nAssistant:"
        
        return await self.generate(prompt, **kwargs)

class GoogleLLM(BaseLLM):
    """Google Gemini模型"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = config.base_url or "https://generativelanguage.googleapis.com/v1beta"
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/models/{self.config.model_name}:generateContent"
                params = {"key": self.api_key}
                
                data = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": kwargs.get("temperature", self.config.temperature),
                        "maxOutputTokens": kwargs.get("max_tokens", self.config.max_tokens),
                        "topP": kwargs.get("top_p", self.config.top_p)
                    }
                }
                
                async with session.post(url, params=params, json=data) as response:
                    result = await response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            self.logger.error(f"Google生成失败: {str(e)}")
            raise
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话生成"""
        # 将消息转换为Gemini格式
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/models/{self.config.model_name}:generateContent"
                params = {"key": self.api_key}
                
                data = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": kwargs.get("temperature", self.config.temperature),
                        "maxOutputTokens": kwargs.get("max_tokens", self.config.max_tokens),
                        "topP": kwargs.get("top_p", self.config.top_p)
                    }
                }
                
                async with session.post(url, params=params, json=data) as response:
                    result = await response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            self.logger.error(f"Google对话失败: {str(e)}")
            raise

class BaiduLLM(BaseLLM):
    """百度文心一言模型"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.secret_key = config.secret_key
        self.base_url = config.base_url or "https://aip.baidubce.com"
    
    async def get_access_token(self) -> str:
        """获取访问令牌"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/oauth/2.0/token"
                params = {
                    "grant_type": "client_credentials",
                    "client_id": self.api_key,
                    "client_secret": self.secret_key
                }
                
                async with session.post(url, params=params) as response:
                    result = await response.json()
                    return result["access_token"]
        except Exception as e:
            self.logger.error(f"获取百度访问令牌失败: {str(e)}")
            raise
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        try:
            access_token = await self.get_access_token()
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
                params = {"access_token": access_token}
                
                data = {
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "max_output_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                    "top_p": kwargs.get("top_p", self.config.top_p)
                }
                
                async with session.post(url, params=params, json=data) as response:
                    result = await response.json()
                    return result["result"]
        except Exception as e:
            self.logger.error(f"百度生成失败: {str(e)}")
            raise
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话生成"""
        try:
            access_token = await self.get_access_token()
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
                params = {"access_token": access_token}
                
                data = {
                    "messages": messages,
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "max_output_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                    "top_p": kwargs.get("top_p", self.config.top_p)
                }
                
                async with session.post(url, params=params, json=data) as response:
                    result = await response.json()
                    return result["result"]
        except Exception as e:
            self.logger.error(f"百度对话失败: {str(e)}")
            raise

class LocalLLM(BaseLLM):
    """本地模型"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()
    
    def _load_model(self):
        """加载本地模型"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            self.logger.info(f"本地模型 {self.config.model_name} 加载成功")
        except Exception as e:
            self.logger.error(f"本地模型加载失败: {str(e)}")
            raise
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=kwargs.get("max_tokens", self.config.max_tokens),
                    temperature=kwargs.get("temperature", self.config.temperature),
                    top_p=kwargs.get("top_p", self.config.top_p),
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response[len(prompt):].strip()
        except Exception as e:
            self.logger.error(f"本地模型生成失败: {str(e)}")
            raise
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话生成"""
        # 将消息转换为对话格式
        prompt = ""
        for msg in messages:
            role = "用户" if msg["role"] == "user" else "助手"
            prompt += f"{role}: {msg['content']}\n"
        prompt += "助手: "
        
        return await self.generate(prompt, **kwargs)

class LLMManager:
    """LLM管理器"""
    
    def __init__(self):
        self.llms: Dict[str, BaseLLM] = {}
        self.default_llm: Optional[str] = None
        self.logger = logger
    
    def register_llm(self, name: str, llm: BaseLLM):
        """注册LLM"""
        self.llms[name] = llm
        if self.default_llm is None:
            self.default_llm = name
        self.logger.info(f"LLM {name} 注册成功")
    
    def get_llm(self, name: Optional[str] = None) -> BaseLLM:
        """获取LLM"""
        name = name or self.default_llm
        if name not in self.llms:
            raise ValueError(f"LLM {name} 未注册")
        return self.llms[name]
    
    async def generate(self, prompt: str, llm_name: Optional[str] = None, **kwargs) -> str:
        """生成文本"""
        llm = self.get_llm(llm_name)
        return await llm.generate(prompt, **kwargs)
    
    async def chat(self, messages: List[Dict[str, str]], llm_name: Optional[str] = None, **kwargs) -> str:
        """对话生成"""
        llm = self.get_llm(llm_name)
        return await llm.chat(messages, **kwargs)
    
    def list_llms(self) -> List[str]:
        """列出所有LLM"""
        return list(self.llms.keys())

# 预定义配置
LLM_CONFIGS = {
    "gpt-4": LLMConfig(
        provider=LLMProvider.OPENAI,
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=2000
    ),
    "gpt-3.5-turbo": LLMConfig(
        provider=LLMProvider.OPENAI,
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=2000
    ),
    "claude-3-opus": LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model_name="claude-3-opus-20240229",
        temperature=0.7,
        max_tokens=2000
    ),
    "claude-3-sonnet": LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model_name="claude-3-sonnet-20240229",
        temperature=0.7,
        max_tokens=2000
    ),
    "gemini-pro": LLMConfig(
        provider=LLMProvider.GOOGLE,
        model_name="gemini-pro",
        temperature=0.7,
        max_tokens=2000
    ),
    "gemini-pro-vision": LLMConfig(
        provider=LLMProvider.GOOGLE,
        model_name="gemini-pro-vision",
        temperature=0.7,
        max_tokens=2000
    ),
    "wenxin-4": LLMConfig(
        provider=LLMProvider.BAIDU,
        model_name="ernie-bot-4",
        temperature=0.7,
        max_tokens=2000
    ),
    "wenxin-3.5": LLMConfig(
        provider=LLMProvider.BAIDU,
        model_name="ernie-bot-turbo",
        temperature=0.7,
        max_tokens=2000
    ),
    "qwen-72b": LLMConfig(
        provider=LLMProvider.LOCAL,
        model_name="Qwen/Qwen-72B-Chat",
        temperature=0.7,
        max_tokens=2000
    ),
    "qwen-14b": LLMConfig(
        provider=LLMProvider.LOCAL,
        model_name="Qwen/Qwen-14B-Chat",
        temperature=0.7,
        max_tokens=2000
    ),
    "chatglm3-6b": LLMConfig(
        provider=LLMProvider.LOCAL,
        model_name="THUDM/chatglm3-6b",
        temperature=0.7,
        max_tokens=2000
    ),
    "deepseek-7b": LLMConfig(
        provider=LLMProvider.LOCAL,
        model_name="deepseek-ai/deepseek-llm-7b-chat",
        temperature=0.7,
        max_tokens=2000
    )
}

def create_llm_manager() -> LLMManager:
    """创建LLM管理器"""
    manager = LLMManager()
    
    # 从环境变量加载配置
    for name, config in LLM_CONFIGS.items():
        try:
            if config.provider == LLMProvider.OPENAI:
                if os.getenv("OPENAI_API_KEY"):
                    config.api_key = os.getenv("OPENAI_API_KEY")
                    config.base_url = os.getenv("OPENAI_BASE_URL")
                    llm = OpenAILLM(config)
                    manager.register_llm(name, llm)
            
            elif config.provider == LLMProvider.ANTHROPIC:
                if os.getenv("ANTHROPIC_API_KEY"):
                    config.api_key = os.getenv("ANTHROPIC_API_KEY")
                    config.base_url = os.getenv("ANTHROPIC_BASE_URL")
                    llm = AnthropicLLM(config)
                    manager.register_llm(name, llm)
            
            elif config.provider == LLMProvider.GOOGLE:
                if os.getenv("GOOGLE_API_KEY"):
                    config.api_key = os.getenv("GOOGLE_API_KEY")
                    config.base_url = os.getenv("GOOGLE_BASE_URL")
                    llm = GoogleLLM(config)
                    manager.register_llm(name, llm)
            
            elif config.provider == LLMProvider.BAIDU:
                if os.getenv("BAIDU_API_KEY") and os.getenv("BAIDU_SECRET_KEY"):
                    config.api_key = os.getenv("BAIDU_API_KEY")
                    config.secret_key = os.getenv("BAIDU_SECRET_KEY")
                    config.base_url = os.getenv("BAIDU_BASE_URL")
                    llm = BaiduLLM(config)
                    manager.register_llm(name, llm)
            
            elif config.provider == LLMProvider.LOCAL:
                if os.getenv("ENABLE_LOCAL_MODELS") == "true":
                    llm = LocalLLM(config)
                    manager.register_llm(name, llm)
        
        except Exception as e:
            logger.warning(f"LLM {name} 初始化失败: {str(e)}")
    
    return manager

# 使用示例
async def main():
    """使用示例"""
    # 创建LLM管理器
    manager = create_llm_manager()
    
    # 列出可用的LLM
    print("可用的LLM模型:")
    for name in manager.list_llms():
        print(f"- {name}")
    
    # 使用默认LLM生成文本
    prompt = "请分析一下小微企业的贷款风险因素"
    response = await manager.generate(prompt)
    print(f"\n生成结果: {response}")
    
    # 使用指定LLM进行对话
    messages = [
        {"role": "user", "content": "你好，我想了解贷款申请流程"},
        {"role": "assistant", "content": "您好！我很乐意为您介绍贷款申请流程。"},
        {"role": "user", "content": "需要准备哪些材料？"}
    ]
    
    response = await manager.chat(messages)
    print(f"\n对话结果: {response}")

if __name__ == "__main__":
    asyncio.run(main())
