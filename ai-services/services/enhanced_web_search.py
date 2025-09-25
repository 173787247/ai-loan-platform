"""
增强版网络搜索服务 - 实时获取银行官网数据
支持LLM reasoning和实时数据获取
"""

import requests
import json
import re
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from loguru import logger
from datetime import datetime
import time

class EnhancedWebSearchService:
    """增强版网络搜索服务"""
    
    def __init__(self):
        self.session = None
        self.bank_apis = {
            "招商银行": {
                "name": "招商银行",
                "website": "https://www.cmbchina.com",
                "loan_page": "https://www.cmbchina.com/personal/loan/",
                "search_api": "https://www.cmbchina.com/api/search",
                "contact": "95555",
                "keywords": ["招商银行", "cmb", "招行"]
            },
            "中国银行": {
                "name": "中国银行",
                "website": "https://www.boc.cn",
                "loan_page": "https://www.boc.cn/personal/loan/",
                "search_api": "https://www.boc.cn/api/search",
                "contact": "95566",
                "keywords": ["中国银行", "boc", "中行"]
            },
            "工商银行": {
                "name": "工商银行",
                "website": "https://www.icbc.com.cn",
                "loan_page": "https://www.icbc.com.cn/personal/loan/",
                "search_api": "https://www.icbc.com.cn/api/search",
                "contact": "95588",
                "keywords": ["工商银行", "icbc", "工行"]
            },
            "建设银行": {
                "name": "建设银行",
                "website": "https://www.ccb.com",
                "loan_page": "https://www.ccb.com/personal/loan/",
                "search_api": "https://www.ccb.com/api/search",
                "contact": "95533",
                "keywords": ["建设银行", "ccb", "建行"]
            },
            "农业银行": {
                "name": "农业银行",
                "website": "https://www.abchina.com",
                "loan_page": "https://www.abchina.com/personal/loan/",
                "search_api": "https://www.abchina.com/api/search",
                "contact": "95599",
                "keywords": ["农业银行", "abchina", "农行"]
            },
            "光大银行": {
                "name": "光大银行",
                "website": "https://www.cebbank.com",
                "loan_page": "https://www.cebbank.com/personal/loan/",
                "search_api": "https://www.cebbank.com/api/search",
                "contact": "95595",
                "keywords": ["光大银行", "cebbank", "光大"]
            },
            "民生银行": {
                "name": "民生银行",
                "website": "https://www.cmbc.com.cn",
                "loan_page": "https://www.cmbc.com.cn/personal/loan/",
                "search_api": "https://www.cmbc.com.cn/api/search",
                "contact": "95568",
                "keywords": ["民生银行", "cmbc", "民生"]
            },
            "兴业银行": {
                "name": "兴业银行",
                "website": "https://www.cib.com.cn",
                "loan_page": "https://www.cib.com.cn/personal/loan/",
                "search_api": "https://www.cib.com.cn/api/search",
                "contact": "95561",
                "keywords": ["兴业银行", "cib", "兴业"]
            },
            "浦发银行": {
                "name": "浦发银行",
                "website": "https://www.spdb.com.cn",
                "loan_page": "https://www.spdb.com.cn/personal/loan/",
                "search_api": "https://www.spdb.com.cn/api/search",
                "contact": "95528",
                "keywords": ["浦发银行", "spdb", "浦发"]
            }
        }
        
        # 预设的银行产品信息（作为备用）
        self.preset_products = {
            "招商银行": [
                {
                    "title": "个人信用贷款",
                    "description": "无需抵押，凭信用申请，审批快速",
                    "rate": "4.5%-12%",
                    "amount": "1-50万",
                    "term": "6-36个月",
                    "features": ["无抵押", "快速审批", "灵活还款"]
                },
                {
                    "title": "企业经营贷款",
                    "description": "支持企业资金周转，助力企业发展",
                    "rate": "3.8%-8.5%",
                    "amount": "10-500万",
                    "term": "3-24个月",
                    "features": ["企业专用", "额度高", "利率优惠"]
                },
                {
                    "title": "住房抵押贷款",
                    "description": "以房产作为抵押，额度高利率低",
                    "rate": "3.5%-8%",
                    "amount": "房产评估价70%",
                    "term": "1-20年",
                    "features": ["抵押贷款", "额度高", "期限长"]
                }
            ],
            "中国银行": [
                {
                    "title": "个人消费贷款",
                    "description": "用于个人消费支出，手续简便",
                    "rate": "4.2%-11%",
                    "amount": "1-30万",
                    "term": "6-60个月",
                    "features": ["消费专用", "手续简便", "放款快"]
                },
                {
                    "title": "企业经营贷款",
                    "description": "支持企业生产经营，提供资金支持",
                    "rate": "3.5%-7.8%",
                    "amount": "10-1000万",
                    "term": "3-36个月",
                    "features": ["企业专用", "额度大", "期限灵活"]
                }
            ],
            "工商银行": [
                {
                    "title": "个人信用贷款",
                    "description": "纯信用无抵押贷款，申请便捷",
                    "rate": "4.0%-10%",
                    "amount": "1-50万",
                    "term": "6-36个月",
                    "features": ["纯信用", "申请便捷", "利率优惠"]
                },
                {
                    "title": "小微企业贷款",
                    "description": "支持小微企业发展，提供专项服务",
                    "rate": "3.2%-6.5%",
                    "amount": "5-300万",
                    "term": "6-24个月",
                    "features": ["小微企业", "专项服务", "利率低"]
                }
            ],
            "光大银行": [
                {
                    "title": "个人消费贷款",
                    "description": "用于个人消费支出，手续简便，放款快速",
                    "rate": "4.2%-11.5%",
                    "amount": "1-30万",
                    "term": "6-60个月",
                    "features": ["消费专用", "手续简便", "放款快"]
                },
                {
                    "title": "企业经营贷款",
                    "description": "支持企业生产经营，提供资金支持",
                    "rate": "3.8%-8.2%",
                    "amount": "10-500万",
                    "term": "3-36个月",
                    "features": ["企业专用", "额度大", "期限灵活"]
                },
                {
                    "title": "住房抵押贷款",
                    "description": "以房产作为抵押，额度高利率低",
                    "rate": "3.6%-7.8%",
                    "amount": "房产评估价70%",
                    "term": "1-20年",
                    "features": ["抵押贷款", "额度高", "期限长"]
                }
            ],
            "民生银行": [
                {
                    "title": "个人信用贷款",
                    "description": "无需抵押，凭信用申请，审批快速",
                    "rate": "4.5%-12%",
                    "amount": "1-50万",
                    "term": "6-36个月",
                    "features": ["无抵押", "快速审批", "灵活还款"]
                },
                {
                    "title": "小微企业贷款",
                    "description": "支持小微企业发展，提供专项服务",
                    "rate": "3.5%-7.2%",
                    "amount": "5-200万",
                    "term": "6-24个月",
                    "features": ["小微企业", "专项服务", "利率低"]
                }
            ],
            "兴业银行": [
                {
                    "title": "个人消费贷款",
                    "description": "用于个人消费支出，手续简便",
                    "rate": "4.0%-10.8%",
                    "amount": "1-30万",
                    "term": "6-60个月",
                    "features": ["消费专用", "手续简便", "放款快"]
                },
                {
                    "title": "企业经营贷款",
                    "description": "支持企业生产经营，提供资金支持",
                    "rate": "3.6%-7.8%",
                    "amount": "10-1000万",
                    "term": "3-36个月",
                    "features": ["企业专用", "额度大", "期限灵活"]
                }
            ],
            "浦发银行": [
                {
                    "title": "个人信用贷款",
                    "description": "纯信用无抵押贷款，申请便捷",
                    "rate": "4.2%-11%",
                    "amount": "1-50万",
                    "term": "6-36个月",
                    "features": ["纯信用", "申请便捷", "利率优惠"]
                },
                {
                    "title": "小微企业贷款",
                    "description": "支持小微企业发展，提供专项服务",
                    "rate": "3.4%-6.8%",
                    "amount": "5-300万",
                    "term": "6-24个月",
                    "features": ["小微企业", "专项服务", "利率低"]
                }
            ]
        }
    
    async def initialize(self):
        """初始化服务"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
            )
            logger.info("增强版网络搜索服务初始化成功")
        except Exception as e:
            logger.error(f"增强版网络搜索服务初始化失败: {e}")
    
    async def close(self):
        """关闭服务"""
        if self.session:
            await self.session.close()
            logger.info("增强版网络搜索服务已关闭")
    
    async def search_bank_info(self, bank_name: str, query: str = "") -> Dict[str, Any]:
        """搜索银行信息（支持实时获取）"""
        try:
            bank_info = self.bank_apis.get(bank_name)
            if not bank_info:
                return {"error": f"未找到银行信息: {bank_name}"}
            
            # 尝试实时获取银行信息
            real_time_info = await self._fetch_real_time_bank_info(bank_name, query)
            
            # 如果实时获取失败，使用预设信息
            if real_time_info.get("error"):
                logger.warning(f"实时获取{bank_name}信息失败，使用预设信息")
                return await self._get_preset_bank_info(bank_name, query)
            
            return real_time_info
            
        except Exception as e:
            logger.error(f"搜索银行信息失败: {e}")
            return await self._get_preset_bank_info(bank_name, query)
    
    async def _fetch_real_time_bank_info(self, bank_name: str, query: str) -> Dict[str, Any]:
        """实时获取银行信息"""
        try:
            bank_info = self.bank_apis[bank_name]
            
            # 构建搜索URL
            search_url = f"{bank_info['website']}/search"
            params = {
                "q": query or "贷款产品",
                "type": "product",
                "category": "loan"
            }
            
            async with self.session.get(search_url, params=params) as response:
                if response.status == 200:
                    content = await response.text()
                    return await self._parse_bank_website(bank_name, content, query)
                else:
                    return {"error": f"HTTP {response.status}"}
                    
        except Exception as e:
            logger.error(f"实时获取银行信息失败: {e}")
            return {"error": str(e)}
    
    async def _parse_bank_website(self, bank_name: str, content: str, query: str) -> Dict[str, Any]:
        """解析银行官网内容"""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            result = {
                "bank_name": bank_name,
                "query": query,
                "products": [],
                "rates": [],
                "contact": self.bank_apis[bank_name]["contact"],
                "website": self.bank_apis[bank_name]["website"],
                "last_updated": datetime.now().isoformat(),
                "source": "real_time"
            }
            
            # 查找贷款产品信息
            product_selectors = [
                'div[class*="product"]',
                'div[class*="loan"]',
                'div[class*="credit"]',
                'section[class*="product"]',
                '.loan-item',
                '.product-item'
            ]
            
            for selector in product_selectors:
                products = soup.select(selector)
                for product in products:
                    title_elem = product.find(['h1', 'h2', 'h3', 'h4', 'h5'], string=re.compile(r'贷款|信用|个人|企业', re.I))
                    if title_elem:
                        product_info = {
                            "title": title_elem.get_text().strip(),
                            "description": "",
                            "rate": "",
                            "amount": "",
                            "term": "",
                            "features": []
                        }
                        
                        # 提取描述
                        desc_elem = product.find(['p', 'div', 'span'], string=re.compile(r'额度|利率|期限|特点', re.I))
                        if desc_elem:
                            product_info["description"] = desc_elem.get_text().strip()
                        
                        # 提取利率信息
                        text_content = product.get_text()
                        rate_match = re.search(r'(\d+\.?\d*%?[-~至]\d+\.?\d*%?)', text_content)
                        if rate_match:
                            product_info["rate"] = rate_match.group(1)
                        
                        # 提取额度信息
                        amount_match = re.search(r'(\d+万?[-~至]\d+万?)', text_content)
                        if amount_match:
                            product_info["amount"] = amount_match.group(1)
                        
                        # 提取期限信息
                        term_match = re.search(r'(\d+[个月年]?[-~至]\d+[个月年]?)', text_content)
                        if term_match:
                            product_info["term"] = term_match.group(1)
                        
                        result["products"].append(product_info)
            
            # 如果没有找到产品，使用预设信息
            if not result["products"]:
                result["products"] = self.preset_products.get(bank_name, [])
                result["source"] = "preset"
            
            return result
            
        except Exception as e:
            logger.error(f"解析银行官网失败: {e}")
            return {"error": str(e)}
    
    async def _get_preset_bank_info(self, bank_name: str, query: str) -> Dict[str, Any]:
        """获取预设银行信息"""
        products = self.preset_products.get(bank_name, [])
        bank_info = self.bank_apis.get(bank_name, {})
        
        return {
            "bank_name": bank_name,
            "query": query,
            "products": products,
            "contact": bank_info.get("contact", ""),
            "website": bank_info.get("website", ""),
            "last_updated": "2025-09-23",
            "source": "preset"
        }
    
    async def search_loan_products(self, bank_name: str) -> Dict[str, Any]:
        """搜索贷款产品"""
        return await self.search_bank_info(bank_name, "贷款产品")
    
    async def get_bank_contact_info(self, bank_name: str) -> Dict[str, Any]:
        """获取银行联系方式"""
        bank_info = self.bank_apis.get(bank_name)
        if not bank_info:
            return {"error": f"未找到银行信息: {bank_name}"}
        
        return {
            "bank_name": bank_name,
            "hotline": bank_info["contact"],
            "website": bank_info["website"],
            "online_service": "7×24小时在线服务",
            "keywords": bank_info["keywords"]
        }
    
    async def search_multiple_banks(self, query: str) -> Dict[str, Any]:
        """搜索多个银行信息"""
        results = {}
        
        # 并行搜索多个银行
        tasks = []
        for bank_name in self.bank_apis.keys():
            task = self.search_bank_info(bank_name, query)
            tasks.append((bank_name, task))
        
        # 等待所有任务完成
        for bank_name, task in tasks:
            try:
                result = await task
                results[bank_name] = result
            except Exception as e:
                logger.error(f"搜索{bank_name}失败: {e}")
                results[bank_name] = {"error": str(e)}
        
        return {
            "query": query,
            "banks": results,
            "total_banks": len(results),
            "successful_banks": len([r for r in results.values() if not r.get("error")]),
            "search_time": datetime.now().isoformat()
        }

# 全局实例
enhanced_web_search_service = EnhancedWebSearchService()
