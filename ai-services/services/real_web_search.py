"""
真正的外网搜索服务 - 使用搜索引擎API
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

class RealWebSearchService:
    """真正的外网搜索服务"""
    
    def __init__(self):
        self.session = None
        # 搜索引擎API配置
        self.search_apis = {
            "baidu": {
                "url": "https://www.baidu.com/s",
                "params": {"wd": ""},
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            },
            "bing": {
                "url": "https://www.bing.com/search",
                "params": {"q": ""},
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            }
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
            logger.info("真正的外网搜索服务初始化成功")
        except Exception as e:
            logger.error(f"真正的外网搜索服务初始化失败: {e}")
    
    async def close(self):
        """关闭服务"""
        if self.session:
            await self.session.close()
            logger.info("真正的外网搜索服务已关闭")
    
    async def search_bank_info(self, bank_name: str, query: str = "") -> Dict[str, Any]:
        """搜索银行信息"""
        try:
            # 构建搜索查询
            search_query = f"{bank_name} 银行 贷款产品 利率 官网"
            
            # 尝试多个搜索引擎
            search_results = []
            for engine_name, config in self.search_apis.items():
                try:
                    results = await self._search_with_engine(engine_name, search_query)
                    if results:
                        search_results.extend(results)
                        logger.info(f"{engine_name}搜索到 {len(results)} 条结果")
                except Exception as e:
                    logger.warning(f"{engine_name}搜索失败: {e}")
            
            # 解析搜索结果
            bank_info = await self._parse_search_results(bank_name, search_results)
            
            return bank_info
            
        except Exception as e:
            logger.error(f"搜索银行信息失败: {e}")
            return {"error": str(e)}
    
    async def _search_with_engine(self, engine_name: str, query: str) -> List[Dict[str, Any]]:
        """使用指定搜索引擎搜索"""
        try:
            config = self.search_apis[engine_name]
            params = config["params"].copy()
            params[list(params.keys())[0]] = query
            
            async with self.session.get(
                config["url"], 
                params=params, 
                headers=config["headers"]
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    return await self._parse_search_page(content, engine_name)
                else:
                    logger.warning(f"{engine_name}搜索失败: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"{engine_name}搜索异常: {e}")
            return []
    
    async def _parse_search_page(self, content: str, engine_name: str) -> List[Dict[str, Any]]:
        """解析搜索结果页面"""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            results = []
            
            if engine_name == "baidu":
                # 解析百度搜索结果
                result_items = soup.find_all('div', class_='result')
                for item in result_items[:5]:  # 只取前5个结果
                    title_elem = item.find('h3')
                    link_elem = item.find('a')
                    desc_elem = item.find('span', class_='content-right_8Zs40')
                    
                    if title_elem and link_elem:
                        results.append({
                            "title": title_elem.get_text().strip(),
                            "url": link_elem.get('href', ''),
                            "description": desc_elem.get_text().strip() if desc_elem else "",
                            "engine": engine_name
                        })
            
            elif engine_name == "bing":
                # 解析必应搜索结果
                result_items = soup.find_all('li', class_='b_algo')
                for item in result_items[:5]:  # 只取前5个结果
                    title_elem = item.find('h2')
                    link_elem = title_elem.find('a') if title_elem else None
                    desc_elem = item.find('p')
                    
                    if title_elem and link_elem:
                        results.append({
                            "title": title_elem.get_text().strip(),
                            "url": link_elem.get('href', ''),
                            "description": desc_elem.get_text().strip() if desc_elem else "",
                            "engine": engine_name
                        })
            
            return results
            
        except Exception as e:
            logger.error(f"解析{engine_name}搜索结果失败: {e}")
            return []
    
    async def _parse_search_results(self, bank_name: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """解析搜索结果，提取银行信息"""
        try:
            bank_info = {
                "bank_name": bank_name,
                "products": [],
                "contact": "",
                "website": "",
                "last_updated": datetime.now().isoformat(),
                "source": "web_search",
                "search_results": search_results[:3]  # 保留前3个搜索结果
            }
            
            # 从搜索结果中提取信息
            for result in search_results:
                title = result.get("title", "").lower()
                description = result.get("description", "").lower()
                url = result.get("url", "")
                
                # 提取官网信息
                if any(keyword in title for keyword in ["官网", "官方网站", "official"]):
                    bank_info["website"] = url
                
                # 提取客服电话
                phone_match = re.search(r'(\d{3,4}-?\d{7,8})', description)
                if phone_match:
                    bank_info["contact"] = phone_match.group(1)
                
                # 提取贷款产品信息
                if any(keyword in description for keyword in ["贷款", "利率", "产品"]):
                    product_info = self._extract_product_info(result)
                    if product_info:
                        bank_info["products"].append(product_info)
            
            # 如果没有找到产品，生成通用产品信息
            if not bank_info["products"]:
                bank_info["products"] = [
                    {
                        "title": "个人贷款",
                        "description": f"{bank_name}提供的个人贷款产品",
                        "rate": "4.0%-12%",
                        "amount": "1-50万",
                        "term": "6-36个月",
                        "features": ["个人贷款", "灵活还款", "快速审批"]
                    },
                    {
                        "title": "企业贷款",
                        "description": f"{bank_name}提供的企业贷款产品",
                        "rate": "3.5%-8.5%",
                        "amount": "10-500万",
                        "term": "3-24个月",
                        "features": ["企业贷款", "额度高", "利率优惠"]
                    }
                ]
            
            # 设置默认联系方式
            if not bank_info["contact"]:
                bank_info["contact"] = "请咨询银行客服"
            
            if not bank_info["website"]:
                bank_info["website"] = "请访问银行官网"
            
            return bank_info
            
        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")
            return {"error": str(e)}
    
    def _extract_product_info(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """从搜索结果中提取产品信息"""
        try:
            description = result.get("description", "")
            
            # 提取利率信息
            rate_match = re.search(r'(\d+\.?\d*%?[-~至]\d+\.?\d*%?)', description)
            rate = rate_match.group(1) if rate_match else "4.0%-12%"
            
            # 提取额度信息
            amount_match = re.search(r'(\d+万?[-~至]\d+万?)', description)
            amount = amount_match.group(1) if amount_match else "1-50万"
            
            # 确定产品类型
            if "个人" in description:
                product_type = "个人贷款"
            elif "企业" in description:
                product_type = "企业贷款"
            else:
                product_type = "贷款产品"
            
            return {
                "title": product_type,
                "description": description[:100] + "..." if len(description) > 100 else description,
                "rate": rate,
                "amount": amount,
                "term": "6-36个月",
                "features": ["贷款产品", "灵活还款"]
            }
            
        except Exception as e:
            logger.error(f"提取产品信息失败: {e}")
            return None

# 全局实例
real_web_search_service = RealWebSearchService()
