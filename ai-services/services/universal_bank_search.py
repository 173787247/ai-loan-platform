"""
通用银行搜索服务 - 支持动态搜索任何银行
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
from .real_web_search import real_web_search_service

class UniversalBankSearchService:
    """通用银行搜索服务"""
    
    def __init__(self):
        self.session = None
        # 银行关键词映射
        self.bank_keywords = {
            "人民银行": ["人民银行", "央行", "pboc", "中国人民银行", "央行", "人民银行", "人行"],
            "招商银行": ["招商银行", "招行", "cmb", "招商"],
            "中国银行": ["中国银行", "中行", "boc", "中国"],
            "工商银行": ["工商银行", "工行", "icbc", "工商"],
            "建设银行": ["建设银行", "建行", "ccb", "建设"],
            "农业银行": ["农业银行", "农行", "abchina", "农业"],
            "光大银行": ["光大银行", "光大", "cebbank", "光大"],
            "民生银行": ["民生银行", "民生", "cmbc", "民生"],
            "兴业银行": ["兴业银行", "兴业", "cib", "兴业"],
            "浦发银行": ["浦发银行", "浦发", "spdb", "浦发"],
            "交通银行": ["交通银行", "交行", "bocom", "交通"],
            "中信银行": ["中信银行", "中信", "citic", "中信"],
            "华夏银行": ["华夏银行", "华夏", "hxb", "华夏"],
            "广发银行": ["广发银行", "广发", "cgb", "广发"],
            "平安银行": ["平安银行", "平安", "pab", "平安"],
            "邮储银行": ["邮储银行", "邮储", "psbc", "邮储"],
            "北京银行": ["北京银行", "北京", "bob", "北京"],
            "上海银行": ["上海银行", "上海", "bosc", "上海"],
            "江苏银行": ["江苏银行", "江苏", "jsb", "江苏"],
            "浙商银行": ["浙商银行", "浙商", "czb", "浙商"],
            "渤海银行": ["渤海银行", "渤海", "cbhb", "渤海"]
        }
        
        # 银行官网信息
        self.bank_websites = {
            "人民银行": "https://www.pbc.gov.cn",
            "招商银行": "https://www.cmbchina.com",
            "中国银行": "https://www.boc.cn",
            "工商银行": "https://www.icbc.com.cn",
            "建设银行": "https://www.ccb.com",
            "农业银行": "https://www.abchina.com",
            "光大银行": "https://www.cebbank.com",
            "民生银行": "https://www.cmbc.com.cn",
            "兴业银行": "https://www.cib.com.cn",
            "浦发银行": "https://www.spdb.com.cn",
            "交通银行": "https://www.bankcomm.com",
            "中信银行": "https://www.citicbank.com",
            "华夏银行": "https://www.hxb.com.cn",
            "广发银行": "https://www.cgbchina.com.cn",
            "平安银行": "https://bank.pingan.com",
            "邮储银行": "https://www.psbc.com",
            "北京银行": "https://www.bankofbeijing.com.cn",
            "上海银行": "https://www.bankofshanghai.com",
            "江苏银行": "https://www.jsbchina.cn",
            "浙商银行": "https://www.czbank.com",
            "渤海银行": "https://www.cbhb.com.cn"
        }
        
        # 银行客服电话
        self.bank_contacts = {
            "人民银行": "010-66194114",
            "招商银行": "95555",
            "中国银行": "95566",
            "工商银行": "95588",
            "建设银行": "95533",
            "农业银行": "95599",
            "光大银行": "95595",
            "民生银行": "95568",
            "兴业银行": "95561",
            "浦发银行": "95528",
            "交通银行": "95559",
            "中信银行": "95558",
            "华夏银行": "95577",
            "广发银行": "95508",
            "平安银行": "95511",
            "邮储银行": "95580",
            "北京银行": "95526",
            "上海银行": "95594",
            "江苏银行": "95319",
            "浙商银行": "95527",
            "渤海银行": "400-888-8811"
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
            logger.info("通用银行搜索服务初始化成功")
        except Exception as e:
            logger.error(f"通用银行搜索服务初始化失败: {e}")
    
    async def close(self):
        """关闭服务"""
        if self.session:
            await self.session.close()
            logger.info("通用银行搜索服务已关闭")
    
    def detect_bank_name(self, user_message: str) -> Optional[str]:
        """检测用户消息中的银行名称"""
        user_message_lower = user_message.lower()
        
        # 直接关键词匹配 - 优先匹配完整的银行名称
        for bank_name, keywords in self.bank_keywords.items():
            # 优先匹配完整的银行名称
            if bank_name in user_message:
                return bank_name
        
        # 然后匹配其他关键词，但需要更严格的匹配
        for bank_name, keywords in self.bank_keywords.items():
            for keyword in keywords:
                if keyword == bank_name:  # 跳过银行名称本身，避免重复匹配
                    continue
                if keyword in user_message_lower:
                    # 对于短关键词（如"中国"），需要检查是否在银行名称的上下文中
                    if len(keyword) <= 2:  # 短关键词
                        # 检查关键词前后是否有银行相关的词
                        keyword_pos = user_message_lower.find(keyword)
                        if keyword_pos > 0:
                            # 检查关键词前面是否有"银行"等词
                            before_context = user_message_lower[max(0, keyword_pos-10):keyword_pos]
                            if "银行" in before_context:
                                return bank_name
                        else:
                            # 检查关键词后面是否有"银行"等词
                            after_context = user_message_lower[keyword_pos:keyword_pos+10]
                            if "银行" in after_context:
                                return bank_name
                    else:
                        # 长关键词直接匹配
                        return bank_name
        
        # 模糊匹配
        for bank_name, keywords in self.bank_keywords.items():
            for keyword in keywords:
                if keyword in user_message:
                    return bank_name
        
        # 检测未知银行 - 匹配"XX银行"模式
        bank_pattern = r'([^，。！？\s]+银行)'
        matches = re.findall(bank_pattern, user_message)
        if matches:
            # 过滤掉常见的干扰词
            filtered_matches = []
            for match in matches:
                # 跳过"中国银行"如果句子中还有其他银行名称
                if match == "中国银行" and len(matches) > 1:
                    continue
                # 跳过"银行"本身
                if match == "银行":
                    continue
                filtered_matches.append(match)
            
            if filtered_matches:
                # 优先返回更具体的银行名称（更长的匹配）
                bank_name = max(filtered_matches, key=len)
                return bank_name
            elif matches:
                # 如果没有过滤后的结果，返回第一个匹配
                return matches[0]
        
        return None
    
    async def detect_bank_name_with_llm(self, user_message: str) -> Optional[str]:
        """使用LLM推理检测银行名称"""
        try:
            # 构建LLM提示词
            prompt = f"""
请分析以下用户消息，识别其中提到的银行名称。

用户消息: "{user_message}"

请从以下银行列表中选择最匹配的银行名称，如果没有匹配的银行，请返回"未知银行"。

支持的银行列表:
- 人民银行 (央行、中国人民银行、人行)
- 招商银行 (招行、CMB)
- 中国银行 (中行、BOC)
- 工商银行 (工行、ICBC)
- 建设银行 (建行、CCB)
- 农业银行 (农行、ABChina)
- 光大银行 (光大、CEB)
- 民生银行 (民生、CMBC)
- 兴业银行 (兴业、CIB)
- 浦发银行 (浦发、SPDB)
- 交通银行 (交行、BOCOM)
- 中信银行 (中信、CITIC)
- 华夏银行 (华夏、HXB)
- 广发银行 (广发、CGB)
- 平安银行 (平安、PAB)
- 邮储银行 (邮储、PSBC)
- 北京银行 (北京、BOB)
- 上海银行 (上海、BOSC)
- 江苏银行 (江苏、JSB)
- 浙商银行 (浙商、CZB)
- 渤海银行 (渤海、CBHB)
- 花旗银行 (花旗、Citi)
- 汇丰银行 (汇丰、HSBC)
- 渣打银行 (渣打、Standard Chartered)
- 台湾银行 (台银、Bank of Taiwan)
- 第一银行 (一银、First Bank)
- 华南银行 (华银、Hua Nan Bank)
- 彰化银行 (彰银、Chang Hwa Bank)
- 土地银行 (土银、Land Bank)
- 合作金库银行 (合库、Taiwan Cooperative Bank)

注意:
1. 如果用户询问的是"有哪些银行"、"台湾银行"、"大陆银行"、"国外银行"、"外资银行"等泛指概念，请返回"未知银行"
2. 如果用户询问的是具体银行的产品或服务，请返回该银行名称
3. 如果用户询问的是银行比较或选择，请返回"未知银行"
4. 如果用户询问的是"国外有哪些银行在中国有业务"、"外资银行在中国"等泛指查询，请返回"未知银行"
5. 如果用户询问的是"花旗银行"、"汇丰银行"等具体银行，请返回该银行名称

请只返回银行名称，不要返回其他内容。
"""
            
            # 调用LLM进行推理
            from .llm_provider import llm_provider_manager
            
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            result = await llm_provider_manager.generate_response(
                messages=messages,
                provider="openai",
                model="gpt-4o",  # 使用GPT-4o替代GPT-5
                temperature=0.1,  # 低温度确保一致性
                max_tokens=50
            )
            
            if result and result.get("success") and result.get("response"):
                bank_name = result["response"].strip()
                
                # 验证返回的银行名称
                if bank_name == "未知银行":
                    logger.info("LLM推理识别为泛指查询，未检测到具体银行")
                    return "GENERIC_QUERY"  # 返回特殊标识，表示泛指查询
                elif bank_name in ["人民银行", "招商银行", "中国银行", "工商银行", "建设银行", "农业银行", 
                               "光大银行", "民生银行", "兴业银行", "浦发银行", "交通银行", "中信银行",
                               "华夏银行", "广发银行", "平安银行", "邮储银行", "北京银行", "上海银行",
                               "江苏银行", "浙商银行", "渤海银行", "花旗银行", "汇丰银行", "渣打银行",
                               "台湾银行", "第一银行", "华南银行", "彰化银行", "土地银行", "合作金库银行"]:
                    logger.info(f"LLM推理检测到具体银行: {bank_name}")
                    return bank_name
                else:
                    logger.warning(f"LLM返回了未知银行名称: {bank_name}")
                    return None
            else:
                logger.warning("LLM推理失败，使用传统方法")
                return None
                
        except Exception as e:
            logger.error(f"LLM推理银行检测失败: {e}")
            return None
    
    async def search_bank_info(self, bank_name: str, query: str = "") -> Dict[str, Any]:
        """搜索银行信息"""
        try:
            # 检查是否是已知银行
            if bank_name in self.bank_websites:
                return await self._search_known_bank(bank_name, query)
            else:
                return await self._search_unknown_bank(bank_name, query)
                
        except Exception as e:
            logger.error(f"搜索银行信息失败: {e}")
            return {"error": str(e)}
    
    async def _search_known_bank(self, bank_name: str, query: str) -> Dict[str, Any]:
        """搜索已知银行信息"""
        try:
            # 尝试实时获取
            real_time_info = await self._fetch_real_time_bank_info(bank_name, query)
            if real_time_info.get("error"):
                # 使用预设信息
                return await self._get_preset_bank_info(bank_name, query)
            return real_time_info
            
        except Exception as e:
            logger.error(f"搜索已知银行失败: {e}")
            return await self._get_preset_bank_info(bank_name, query)
    
    async def _search_unknown_bank(self, bank_name: str, query: str) -> Dict[str, Any]:
        """搜索未知银行信息"""
        try:
            # 使用真正的外网搜索
            logger.info(f"开始外网搜索银行信息: {bank_name}")
            search_results = await real_web_search_service.search_bank_info(bank_name, query)
            
            if search_results.get("error"):
                logger.warning(f"外网搜索失败，使用通用信息: {search_results.get('error')}")
                return await self._get_generic_bank_info(bank_name, query)
            
            logger.info(f"外网搜索成功: {bank_name}, 找到 {len(search_results.get('products', []))} 个产品")
            return search_results
            
        except Exception as e:
            logger.error(f"搜索未知银行失败: {e}")
            return await self._get_generic_bank_info(bank_name, query)
    
    async def _fetch_real_time_bank_info(self, bank_name: str, query: str) -> Dict[str, Any]:
        """实时获取银行信息"""
        try:
            website = self.bank_websites.get(bank_name)
            if not website:
                return {"error": "未知银行"}
            
            # 构建搜索URL
            search_url = f"{website}/search"
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
    
    async def _search_bank_via_search_engine(self, bank_name: str, query: str) -> Dict[str, Any]:
        """通过搜索引擎搜索银行信息"""
        try:
            # 构建搜索查询
            search_query = f"{bank_name} 贷款产品 利率 申请条件"
            
            # 这里可以集成百度、谷歌等搜索引擎API
            # 目前返回通用信息
            return await self._get_generic_bank_info(bank_name, query)
            
        except Exception as e:
            logger.error(f"搜索引擎搜索失败: {e}")
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
                "contact": self.bank_contacts.get(bank_name, ""),
                "website": self.bank_websites.get(bank_name, ""),
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
                result["products"] = await self._get_preset_products(bank_name)
                result["source"] = "preset"
            
            return result
            
        except Exception as e:
            logger.error(f"解析银行官网失败: {e}")
            return {"error": str(e)}
    
    async def _get_preset_bank_info(self, bank_name: str, query: str) -> Dict[str, Any]:
        """获取预设银行信息"""
        products = await self._get_preset_products(bank_name)
        
        return {
            "bank_name": bank_name,
            "query": query,
            "products": products,
            "contact": self.bank_contacts.get(bank_name, ""),
            "website": self.bank_websites.get(bank_name, ""),
            "last_updated": "2025-09-23",
            "source": "preset"
        }
    
    async def _get_generic_bank_info(self, bank_name: str, query: str) -> Dict[str, Any]:
        """获取通用银行信息"""
        return {
            "bank_name": bank_name,
            "query": query,
            "products": [
                {
                    "title": "个人信用贷款",
                    "description": "凭信用申请，无需抵押，审批快速",
                    "rate": "4.0%-12%",
                    "amount": "1-50万",
                    "term": "6-36个月",
                    "features": ["无抵押", "快速审批", "灵活还款"]
                },
                {
                    "title": "企业经营贷款",
                    "description": "支持企业资金周转，助力企业发展",
                    "rate": "3.5%-8.5%",
                    "amount": "10-500万",
                    "term": "3-24个月",
                    "features": ["企业专用", "额度高", "利率优惠"]
                }
            ],
            "contact": "请咨询银行客服",
            "website": "请访问银行官网",
            "last_updated": "2025-09-23",
            "source": "generic"
        }
    
    async def _get_preset_products(self, bank_name: str) -> List[Dict[str, Any]]:
        """获取预设产品信息"""
        # 这里可以扩展更多银行的预设产品信息
        preset_products = {
            "人民银行": [
                {
                    "title": "货币政策工具",
                    "description": "央行通过货币政策工具调节货币供应量和利率",
                    "rate": "基准利率",
                    "amount": "宏观调控",
                    "term": "长期政策",
                    "features": ["货币政策", "宏观调控", "金融稳定"]
                },
                {
                    "title": "金融监管政策",
                    "description": "制定和执行金融监管政策，维护金融稳定",
                    "rate": "监管要求",
                    "amount": "全行业",
                    "term": "持续监管",
                    "features": ["金融监管", "风险防控", "合规管理"]
                },
                {
                    "title": "支付清算服务",
                    "description": "提供支付清算基础设施和服务",
                    "rate": "服务费用",
                    "amount": "全国范围",
                    "term": "7×24小时",
                    "features": ["支付清算", "基础设施", "金融服务"]
                }
            ],
            "招商银行": [
                {
                    "title": "个人信用贷款",
                    "description": "无需抵押，凭信用申请，审批快速",
                    "rate": "4.5%-12%",
                    "amount": "1-50万",
                    "term": "6-36个月",
                    "features": ["无抵押", "快速审批", "灵活还款"]
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
                }
            ]
        }
        
        return preset_products.get(bank_name, [
            {
                "title": "个人信用贷款",
                "description": "凭信用申请，无需抵押",
                "rate": "4.0%-12%",
                "amount": "1-50万",
                "term": "6-36个月",
                "features": ["无抵押", "快速审批"]
            }
        ])
    
    async def search_all_banks(self, query: str = "") -> Dict[str, Any]:
        """搜索所有银行信息"""
        results = {}
        
        # 并行搜索所有已知银行
        tasks = []
        for bank_name in self.bank_websites.keys():
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
universal_bank_search_service = UniversalBankSearchService()
