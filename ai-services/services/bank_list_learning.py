#!/usr/bin/env python3
"""
银行清单学习系统
按照预定义的银行清单，系统性地学习各银行的贷款产品
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

class BankListLearningSystem:
    """银行清单学习系统"""
    
    def __init__(self, vector_rag_service=None, llm_service=None):
        self.vector_rag_service = vector_rag_service
        self.llm_service = llm_service
        
        # 国内银行清单（按重要性排序）
        self.bank_list = [
            # 国有大型银行
            {
                "name": "工商银行",
                "english_name": "ICBC",
                "type": "国有大型银行",
                "priority": 1,
                "products": ["融e借", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "建设银行",
                "english_name": "CCB", 
                "type": "国有大型银行",
                "priority": 1,
                "products": ["快贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "农业银行",
                "english_name": "ABC",
                "type": "国有大型银行", 
                "priority": 1,
                "products": ["网捷贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "中国银行",
                "english_name": "BOC",
                "type": "国有大型银行",
                "priority": 1,
                "products": ["中银E贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "交通银行",
                "english_name": "BOCOM",
                "type": "国有大型银行",
                "priority": 1,
                "products": ["好享贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            
            # 股份制银行
            {
                "name": "招商银行",
                "english_name": "CMB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["闪电贷", "招行信用贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "浦发银行",
                "english_name": "SPDB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["浦银点贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "民生银行",
                "english_name": "CMBC",
                "type": "股份制银行",
                "priority": 2,
                "products": ["民生易贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "兴业银行",
                "english_name": "CIB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["兴闪贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "光大银行",
                "english_name": "CEB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["光速贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "华夏银行",
                "english_name": "HXB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["华夏易贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "中信银行",
                "english_name": "CITIC",
                "type": "股份制银行",
                "priority": 2,
                "products": ["信秒贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "广发银行",
                "english_name": "CGB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["广发E秒贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "平安银行",
                "english_name": "PAB",
                "type": "股份制银行",
                "priority": 2,
                "products": ["新一贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            
            # 城市商业银行
            {
                "name": "北京银行",
                "english_name": "BOB",
                "type": "城市商业银行",
                "priority": 3,
                "products": ["京e贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "上海银行",
                "english_name": "BOSC",
                "type": "城市商业银行",
                "priority": 3,
                "products": ["上行快线", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "江苏银行",
                "english_name": "JSB",
                "type": "城市商业银行",
                "priority": 3,
                "products": ["江苏银行e贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            {
                "name": "浙商银行",
                "english_name": "CZB",
                "type": "城市商业银行",
                "priority": 3,
                "products": ["浙商e贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            
            # 农村商业银行
            {
                "name": "邮储银行",
                "english_name": "PSBC",
                "type": "农村商业银行",
                "priority": 3,
                "products": ["邮享贷", "个人消费贷款", "经营贷款", "房贷", "车贷"]
            },
            
            # 更多小银行和民营银行
            {
                "name": "微众银行",
                "english_name": "WeBank",
                "type": "民营银行",
                "priority": 4,
                "products": ["微粒贷", "微业贷", "微车贷", "微房贷", "微众银行APP贷款"]
            },
            {
                "name": "网商银行",
                "english_name": "MYbank",
                "type": "民营银行",
                "priority": 4,
                "products": ["网商贷", "旺农贷", "网商银行APP贷款", "小微企业贷款"]
            },
            {
                "name": "新网银行",
                "english_name": "XWBank",
                "type": "民营银行",
                "priority": 4,
                "products": ["好人贷", "好企贷", "新网银行APP贷款", "个人消费贷款"]
            },
            {
                "name": "苏宁银行",
                "english_name": "SuningBank",
                "type": "民营银行",
                "priority": 4,
                "products": ["苏宁任性贷", "苏宁银行APP贷款", "个人消费贷款", "小微企业贷款"]
            },
            {
                "name": "华瑞银行",
                "english_name": "SHRCB",
                "type": "民营银行",
                "priority": 4,
                "products": ["华瑞银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "三湘银行",
                "english_name": "SXB",
                "type": "民营银行",
                "priority": 4,
                "products": ["三湘银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "蓝海银行",
                "english_name": "LHB",
                "type": "民营银行",
                "priority": 4,
                "products": ["蓝海银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "中关村银行",
                "english_name": "ZGCB",
                "type": "民营银行",
                "priority": 4,
                "products": ["中关村银行APP贷款", "个人消费贷款", "小微企业贷款", "科技金融"]
            },
            {
                "name": "富民银行",
                "english_name": "FMB",
                "type": "民营银行",
                "priority": 4,
                "products": ["富民银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "振兴银行",
                "english_name": "ZXB",
                "type": "民营银行",
                "priority": 4,
                "products": ["振兴银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "新安银行",
                "english_name": "XAB",
                "type": "民营银行",
                "priority": 4,
                "products": ["新安银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "华通银行",
                "english_name": "HTB",
                "type": "民营银行",
                "priority": 4,
                "products": ["华通银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "客商银行",
                "english_name": "KSB",
                "type": "民营银行",
                "priority": 4,
                "products": ["客商银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "裕民银行",
                "english_name": "YMB",
                "type": "民营银行",
                "priority": 4,
                "products": ["裕民银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "锡商银行",
                "english_name": "XSB",
                "type": "民营银行",
                "priority": 4,
                "products": ["锡商银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "亿联银行",
                "english_name": "YLB",
                "type": "民营银行",
                "priority": 4,
                "products": ["亿联银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "众邦银行",
                "english_name": "ZBB",
                "type": "民营银行",
                "priority": 4,
                "products": ["众邦银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "新网银行",
                "english_name": "XWB",
                "type": "民营银行",
                "priority": 4,
                "products": ["新网银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "金城银行",
                "english_name": "JCB",
                "type": "民营银行",
                "priority": 4,
                "products": ["金城银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            },
            {
                "name": "华兴银行",
                "english_name": "HXB",
                "type": "民营银行",
                "priority": 4,
                "products": ["华兴银行APP贷款", "个人消费贷款", "小微企业贷款", "供应链金融"]
            }
        ]
        
        # 学习状态
        self.learning_state = {
            "is_learning": False,
            "current_bank_index": 0,
            "learned_banks": [],
            "failed_banks": [],
            "total_banks": len(self.bank_list),
            "start_time": None,
            "last_learning_time": None
        }
    
    async def start_bank_list_learning(self):
        """启动银行清单学习"""
        try:
            logger.info("启动银行清单学习系统...")
            
            self.learning_state["is_learning"] = True
            self.learning_state["start_time"] = datetime.now()
            self.learning_state["current_bank_index"] = 0
            
            # 启动学习循环
            asyncio.create_task(self._learning_loop())
            
            logger.info(f"银行清单学习已启动，共 {len(self.bank_list)} 家银行")
            
        except Exception as e:
            logger.error(f"启动银行清单学习失败: {e}")
    
    async def _learning_loop(self):
        """学习循环"""
        try:
            while (self.learning_state["is_learning"] and 
                   self.learning_state["current_bank_index"] < len(self.bank_list)):
                
                current_index = self.learning_state["current_bank_index"]
                bank_info = self.bank_list[current_index]
                
                logger.info(f"开始学习第 {current_index + 1}/{len(self.bank_list)} 家银行: {bank_info['name']}")
                
                # 学习当前银行
                success = await self._learn_bank(bank_info)
                
                if success:
                    self.learning_state["learned_banks"].append(bank_info["name"])
                    logger.info(f"✅ {bank_info['name']} 学习成功")
                else:
                    self.learning_state["failed_banks"].append(bank_info["name"])
                    logger.info(f"❌ {bank_info['name']} 学习失败")
                
                # 移动到下一家银行
                self.learning_state["current_bank_index"] += 1
                self.learning_state["last_learning_time"] = datetime.now()
                
                # 学习间隔（避免过于频繁）
                await asyncio.sleep(2)
            
            # 学习完成
            self.learning_state["is_learning"] = False
            logger.info("银行清单学习完成！")
            
        except Exception as e:
            logger.error(f"银行清单学习循环错误: {e}")
            self.learning_state["is_learning"] = False
    
    async def _learn_bank(self, bank_info: Dict[str, Any]) -> bool:
        """学习特定银行信息"""
        try:
            bank_name = bank_info["name"]
            bank_type = bank_info["type"]
            products = bank_info["products"]
            
            # 生成银行信息内容
            content = await self._generate_bank_content(bank_info)
            
            if content and self.vector_rag_service:
                # 保存到知识库
                await self.vector_rag_service.add_knowledge(
                    category="银行清单学习",
                    title=f"{bank_name} 个人信贷产品详细介绍",
                    content=content,
                    metadata={
                        "learning_source": "bank_list_learning",
                        "learning_time": datetime.now().isoformat(),
                        "bank_name": bank_name,
                        "bank_type": bank_type,
                        "bank_english_name": bank_info.get("english_name", ""),
                        "priority": bank_info.get("priority", 3),
                        "products": products
                    }
                )
                
                logger.info(f"银行信息已保存到知识库: {bank_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"学习银行信息失败 {bank_info['name']}: {e}")
            return False
    
    async def _generate_bank_content(self, bank_info: Dict[str, Any]) -> str:
        """生成银行信息内容"""
        try:
            bank_name = bank_info["name"]
            bank_type = bank_info["type"]
            products = bank_info["products"]
            english_name = bank_info.get("english_name", "")
            
            # 根据银行类型生成不同的介绍
            if bank_type == "国有大型银行":
                bank_intro = f"{bank_name}是中国四大国有银行之一，拥有最广泛的网点覆盖和客户基础，在个人信贷领域提供全面的产品和服务。"
            elif bank_type == "股份制银行":
                bank_intro = f"{bank_name}是中国领先的股份制商业银行，以创新金融产品和服务著称，在个人信贷领域有着丰富的产品线和优质的服务。"
            elif bank_type == "城市商业银行":
                bank_intro = f"{bank_name}是重要的城市商业银行，专注于区域市场，为当地客户提供专业的个人信贷服务。"
            else:
                bank_intro = f"{bank_name}是重要的商业银行，为客户提供全面的个人信贷产品和服务。"
            
            content = f"""**{bank_name} 个人信贷产品详细介绍**

**银行简介**
{bank_intro}

**银行基本信息：**
- 银行名称：{bank_name}
- 英文名称：{english_name}
- 银行类型：{bank_type}
- 服务特色：专业、安全、便捷

**主要个人信贷产品：**

"""
            
            # 为每个产品生成详细介绍
            for i, product in enumerate(products, 1):
                content += f"""
{i}. **{product}**：
   - 产品特点：{self._get_product_features(product)}
   - 申请条件：{self._get_application_conditions(bank_type)}
   - 额度范围：{self._get_amount_range(product, bank_type)}
   - 利率水平：{self._get_interest_rate(product, bank_type)}
   - 期限选择：{self._get_term_options(product)}
   - 申请方式：{self._get_application_methods()}
   - 适用人群：{self._get_target_customers(product)}

"""
            
            content += f"""
**申请条件：**
- 年龄要求：18-65周岁
- 收入要求：月收入3000元以上
- 信用要求：征信记录良好，无逾期记录
- 工作要求：稳定工作6个月以上
- 身份要求：中国大陆居民
- 其他要求：符合银行具体规定

**申请方式：**
- 网上银行申请
- 手机银行APP申请
- 银行网点申请
- 客服热线咨询
- 客户经理协助

**银行优势：**
- 专业金融服务团队
- 丰富的产品选择
- 便捷的申请流程
- 优质的客户服务
- 安全的资金保障

**联系方式：**
- 客服热线：请咨询银行官网
- 官方网站：请搜索"{bank_name}官网"
- 营业网点：全国主要城市

**温馨提示：**
- 具体产品信息以银行最新公布为准
- 申请前请仔细阅读产品条款
- 建议提前了解申请条件和所需材料
- 可咨询银行客服获取最新信息
"""
            
            return content
            
        except Exception as e:
            logger.error(f"生成银行内容失败 {bank_info['name']}: {e}")
            return ""
    
    def _get_product_features(self, product: str) -> str:
        """获取产品特点"""
        features_map = {
            "融e借": "纯线上申请，审批快速，无需抵押担保",
            "快贷": "线上申请，秒级审批，随借随还",
            "网捷贷": "线上申请，快速审批，利率优惠",
            "中银E贷": "纯线上操作，审批快速，额度灵活",
            "好享贷": "消费分期，额度循环，使用便捷",
            "闪电贷": "纯线上申请，秒级放款，随借随还",
            "招行信用贷": "产品丰富，服务优质，审批快速",
            "浦银点贷": "线上申请，快速审批，利率优惠",
            "民生易贷": "申请简便，审批快速，额度灵活",
            "兴闪贷": "线上申请，快速审批，随借随还",
            "光速贷": "纯线上操作，审批快速，使用便捷",
            "华夏易贷": "申请简便，审批快速，额度灵活",
            "信秒贷": "线上申请，快速审批，利率优惠",
            "广发E秒贷": "纯线上操作，秒级审批，随借随还",
            "新一贷": "产品特色鲜明，审批快速，额度灵活",
            "京e贷": "区域特色产品，申请简便，审批快速",
            "上行快线": "区域特色产品，线上申请，快速审批",
            "江苏银行e贷": "区域特色产品，申请简便，审批快速",
            "浙商e贷": "区域特色产品，线上操作，快速审批",
            "邮享贷": "网点覆盖广，申请简便，审批快速"
        }
        return features_map.get(product, "申请简便，审批快速，额度灵活")
    
    def _get_application_conditions(self, bank_type: str) -> str:
        """获取申请条件"""
        if bank_type == "国有大型银行":
            return "年收入8万以上，征信良好，稳定工作6个月以上"
        elif bank_type == "股份制银行":
            return "年收入6万以上，征信良好，稳定工作3个月以上"
        else:
            return "年收入5万以上，征信良好，稳定工作3个月以上"
    
    def _get_amount_range(self, product: str, bank_type: str) -> str:
        """获取额度范围"""
        if "信用贷" in product or "e贷" in product:
            if bank_type == "国有大型银行":
                return "1-50万元"
            elif bank_type == "股份制银行":
                return "1-30万元"
            else:
                return "1-20万元"
        elif "消费贷款" in product:
            return "1-100万元"
        elif "经营贷款" in product:
            return "10-500万元"
        elif "房贷" in product:
            return "最高1000万元"
        elif "车贷" in product:
            return "5-200万元"
        else:
            return "1-30万元"
    
    def _get_interest_rate(self, product: str, bank_type: str) -> str:
        """获取利率水平"""
        if bank_type == "国有大型银行":
            return "年化3.5%-12%"
        elif bank_type == "股份制银行":
            return "年化4.0%-15%"
        else:
            return "年化4.5%-18%"
    
    def _get_term_options(self, product: str) -> str:
        """获取期限选择"""
        if "房贷" in product:
            return "1-30年"
        elif "车贷" in product:
            return "1-5年"
        elif "经营贷款" in product:
            return "1-10年"
        else:
            return "1-5年"
    
    def _get_application_methods(self) -> str:
        """获取申请方式"""
        return "网上银行、手机APP、银行网点、客服热线"
    
    def _get_target_customers(self, product: str) -> str:
        """获取适用人群"""
        if "信用贷" in product or "e贷" in product:
            return "有稳定收入的工薪族"
        elif "消费贷款" in product:
            return "有消费需求的个人客户"
        elif "经营贷款" in product:
            return "个体工商户和小微企业主"
        elif "房贷" in product:
            return "有购房需求的客户"
        elif "车贷" in product:
            return "有购车需求的客户"
        else:
            return "有资金需求的个人客户"
    
    async def get_learning_status(self) -> Dict[str, Any]:
        """获取学习状态"""
        current_index = self.learning_state["current_bank_index"]
        total_banks = len(self.bank_list)
        
        # 计算学习进度
        progress_percentage = (current_index / total_banks) * 100 if total_banks > 0 else 0
        
        # 计算学习时长
        learning_duration = None
        if self.learning_state["start_time"]:
            duration = datetime.now() - self.learning_state["start_time"]
            learning_duration = {
                "hours": duration.total_seconds() / 3600,
                "minutes": duration.total_seconds() / 60,
                "seconds": duration.total_seconds()
            }
        
        return {
            "learning_state": self.learning_state.copy(),
            "progress": {
                "current_index": current_index,
                "total_banks": total_banks,
                "progress_percentage": progress_percentage,
                "remaining_banks": total_banks - current_index
            },
            "bank_list": self.bank_list,
            "learning_duration": learning_duration,
            "is_learning": self.learning_state["is_learning"],
            "next_bank": self.bank_list[current_index] if current_index < total_banks else None
        }
    
    async def stop_learning(self):
        """停止学习"""
        self.learning_state["is_learning"] = False
        logger.info("银行清单学习已停止")
    
    async def get_bank_list(self) -> List[Dict[str, Any]]:
        """获取银行清单"""
        return self.bank_list

# 全局实例
bank_list_learning_system = BankListLearningSystem()
