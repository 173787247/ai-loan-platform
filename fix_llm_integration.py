#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件
with open('ai-services/services/ai_chatbot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 在AIChatbot类中添加动态银行对比方法
old_text = '''    def _generate_fallback_comparison(self, bank_info: List[Dict[str, Any]], user_message: str) -> str:
        """当LLM不可用时的备用回复"""
        if not bank_info:'''

new_text = '''    async def _generate_dynamic_bank_comparison(self, knowledge_results: List[Dict[str, Any]], user_message: str) -> str:
        """基于RAG+LLM动态生成银行对比"""
        # 1. 从知识库提取银行信息
        bank_info = self._extract_bank_info_from_knowledge(knowledge_results)
        
        # 2. 构建LLM提示词
        prompt = self._build_comparison_prompt(user_message, bank_info)
        
        # 3. 调用LLM生成回复
        try:
            if self.llm_service:
                response = await self.llm_service.generate_response([{"role": "user", "content": prompt}])
                return response
            else:
                return self._generate_fallback_comparison(bank_info, user_message)
        except Exception as e:
            logger.error(f"LLM生成失败: {e}")
            return self._generate_fallback_comparison(bank_info, user_message)
    
    def _extract_bank_info_from_knowledge(self, knowledge_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从知识库结果中提取银行信息"""
        bank_info = []
        
        for result in knowledge_results:
            title = result.get('title', '')
            content = result.get('content', '')
            
            # 过滤掉乱码内容
            if any(char in content for char in ['nnnnnnnn', '■■■■', '(cid:127)']):
                continue
            
            # 检查是否包含银行信息
            bank_keywords = ['银行', '贷款', '利率', '额度', '审批', '条件', '产品']
            if any(keyword in title or keyword in content for keyword in bank_keywords):
                bank_info.append({
                    'title': title,
                    'content': content[:1000],  # 限制长度
                    'source': result.get('source', ''),
                    'score': result.get('score', 0)
                })
        
        return bank_info
    
    def _build_comparison_prompt(self, user_message: str, bank_info: List[Dict[str, Any]]) -> str:
        """构建银行对比的LLM提示词"""
        prompt = f"""你是一个专业的贷款顾问。用户询问："{user_message}"

基于以下银行信息，为用户提供详细的银行对比分析：

银行信息：
{self._format_bank_info_for_llm(bank_info)}

请按照以下格式回复：
1. 分析各银行的产品特点和优势
2. 推荐最适合的银行（按优先级排序）
3. 提供具体的申请建议和注意事项
4. 列出必备材料清单

要求：
- 基于实际信息进行分析，不要编造数据
- 格式清晰，便于阅读
- 提供实用的建议
- 如果信息不足，请说明并建议用户咨询具体银行
- 如果用户明确要求对比N家银行，请尽量提供N家银行的对比，如果知识库中不足，请说明。
"""
        return prompt

    def _generate_fallback_comparison(self, bank_info: List[Dict[str, Any]], user_message: str) -> str:
        """当LLM不可用时的备用回复"""
        if not bank_info:'''

# 只替换第一个出现的位置（AIChatbot类中的）
content = content.replace(old_text, new_text, 1)

# 修改generate_response方法调用动态银行对比
old_call = 'return self._generate_fallback_comparison(knowledge_results, user_message)'
new_call = 'return await self._generate_dynamic_bank_comparison(knowledge_results, user_message)'

# 只替换第一个出现的位置
content = content.replace(old_call, new_call, 1)

# 写回文件
with open('ai-services/services/ai_chatbot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('已添加LLM动态银行对比功能！')
