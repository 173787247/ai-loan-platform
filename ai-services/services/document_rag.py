"""
文档RAG服务 - 将文档处理与向量RAG结合
支持多种文档格式的智能检索

@author AI Loan Platform Team
@version 1.0.0
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
import asyncio

from .document_processor import DocumentProcessor
from .vector_rag import vector_rag_service

class DocumentRAGService:
    """文档RAG服务"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_rag = vector_rag_service
        self.logger = logger
        
    async def process_and_index_document(
        self, 
        file_path: str, 
        file_type: str,
        category: str = "documents",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """处理文档并索引到向量数据库"""
        try:
            # 1. 处理文档
            self.logger.info(f"开始处理文档: {file_path}")
            doc_result = self.document_processor.process_document(file_path, file_type)
            
            if not doc_result.get("text"):
                raise ValueError("文档处理失败，未提取到文本内容")
            
            # 2. 将文档内容分块
            chunks = self._chunk_document(doc_result["text"], doc_result["document_type"])
            
            # 3. 为每个块生成嵌入并存储
            indexed_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{os.path.basename(file_path)}_{i}"
                chunk_title = f"{os.path.basename(file_path)} - 第{i+1}部分"
                
                # 合并元数据
                chunk_metadata = {
                    "file_path": file_path,
                    "file_type": file_type,
                    "document_type": doc_result["document_type"],
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "original_metadata": doc_result.get("structured_data", {}),
                    **(metadata or {})
                }
                
                # 存储到向量数据库
                knowledge_id = await self.vector_rag.add_knowledge(
                    category=category,
                    title=chunk_title,
                    content=chunk,
                    metadata=chunk_metadata
                )
                
                if knowledge_id:
                    indexed_chunks.append({
                        "chunk_id": chunk_id,
                        "knowledge_id": knowledge_id,
                        "content": chunk,
                        "metadata": chunk_metadata
                    })
            
            self.logger.info(f"文档索引完成: {file_path}, 共{len(indexed_chunks)}个块")
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": file_type,
                "document_type": doc_result["document_type"],
                "total_chunks": len(chunks),
                "indexed_chunks": len(indexed_chunks),
                "chunks": indexed_chunks,
                "processing_result": doc_result
            }
            
        except Exception as e:
            self.logger.error(f"文档处理索引失败: {file_path}, 错误: {str(e)}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }
    
    def _chunk_document(self, text: str, document_type: str) -> List[str]:
        """将文档分块"""
        if not text.strip():
            return []
        
        # 根据文档类型使用不同的分块策略
        if document_type == "bank_statement":
            return self._chunk_bank_statement(text)
        elif document_type == "loan_application":
            return self._chunk_loan_application(text)
        elif document_type == "financial_report":
            return self._chunk_financial_report(text)
        else:
            return self._chunk_general_document(text)
    
    def _chunk_general_document(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """通用文档分块"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # 尝试在句号、问号、感叹号处分割
            if end < len(text):
                for i in range(end, max(start + chunk_size - overlap, start), -1):
                    if text[i] in '。！？\n':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def _chunk_bank_statement(self, text: str) -> List[str]:
        """银行流水分块"""
        # 按交易记录分块
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 如果是日期行（新交易记录开始）
            if self._is_date_line(line):
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
            
            current_chunk.append(line)
            
            # 每10条交易记录一个块
            if len(current_chunk) >= 10:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks if chunks else [text]
    
    def _chunk_loan_application(self, text: str) -> List[str]:
        """贷款申请分块"""
        # 按章节分块
        sections = [
            "基本信息", "收入证明", "资产证明", "负债情况", 
            "担保信息", "贷款用途", "还款计划"
        ]
        
        chunks = []
        lines = text.split('\n')
        current_section = []
        current_title = "基本信息"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是新的章节
            is_new_section = False
            for section in sections:
                if section in line:
                    if current_section:
                        chunks.append(f"{current_title}:\n" + '\n'.join(current_section))
                    current_section = []
                    current_title = section
                    is_new_section = True
                    break
            
            if not is_new_section:
                current_section.append(line)
        
        if current_section:
            chunks.append(f"{current_title}:\n" + '\n'.join(current_section))
        
        return chunks if chunks else [text]
    
    def _chunk_financial_report(self, text: str) -> List[str]:
        """财务报表分块"""
        # 按表格和段落分块
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 如果是表格行（包含多个数字）
            if self._is_table_row(line):
                current_chunk.append(line)
                # 表格行积累到一定数量就分块
                if len(current_chunk) >= 20:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
            else:
                # 非表格行，先处理之前的表格
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                
                # 段落文本
                if len(line) > 50:  # 长段落单独成块
                    chunks.append(line)
                else:
                    current_chunk.append(line)
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks if chunks else [text]
    
    def _is_date_line(self, line: str) -> bool:
        """判断是否是日期行"""
        import re
        date_pattern = r'\d{4}[-/]\d{1,2}[-/]\d{1,2}'
        return bool(re.search(date_pattern, line))
    
    def _is_table_row(self, line: str) -> bool:
        """判断是否是表格行"""
        import re
        # 包含多个数字的行可能是表格行
        numbers = re.findall(r'\d+\.?\d*', line)
        return len(numbers) >= 3
    
    async def search_documents(
        self, 
        query: str, 
        category: str = None,
        file_types: List[str] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """搜索文档"""
        try:
            # 构建搜索条件
            search_metadata = {}
            if file_types:
                search_metadata["file_type"] = file_types
            
            # 执行向量搜索
            results = await self.vector_rag.search_knowledge_hybrid(
                query=query,
                category=category,
                max_results=max_results
            )
            
            # 按文档分组结果
            document_groups = {}
            for result in results:
                file_path = result.get("metadata", {}).get("file_path", "unknown")
                if file_path not in document_groups:
                    document_groups[file_path] = {
                        "file_path": file_path,
                        "file_type": result.get("metadata", {}).get("file_type", "unknown"),
                        "document_type": result.get("metadata", {}).get("document_type", "unknown"),
                        "chunks": [],
                        "total_relevance": 0
                    }
                
                document_groups[file_path]["chunks"].append(result)
                document_groups[file_path]["total_relevance"] += result.get("similarity_score", 0)
            
            # 按相关性排序文档
            sorted_documents = sorted(
                document_groups.values(),
                key=lambda x: x["total_relevance"],
                reverse=True
            )
            
            return {
                "success": True,
                "query": query,
                "total_results": len(results),
                "documents": sorted_documents,
                "search_metadata": {
                    "category": category,
                    "file_types": file_types,
                    "max_results": max_results
                }
            }
            
        except Exception as e:
            self.logger.error(f"文档搜索失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def batch_process_documents(
        self, 
        file_paths: List[str],
        category: str = "documents",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """批量处理文档"""
        results = {}
        success_count = 0
        error_count = 0
        
        for file_path in file_paths:
            try:
                file_type = os.path.splitext(file_path)[1][1:]
                result = await self.process_and_index_document(
                    file_path=file_path,
                    file_type=file_type,
                    category=category,
                    metadata=metadata
                )
                results[file_path] = result
                
                if result.get("success"):
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                self.logger.error(f"批量处理失败: {file_path}, 错误: {str(e)}")
                results[file_path] = {
                    "success": False,
                    "error": str(e)
                }
                error_count += 1
        
        return {
            "results": results,
            "summary": {
                "total": len(file_paths),
                "success": success_count,
                "error": error_count
            }
        }
    
    async def get_document_stats(self) -> Dict[str, Any]:
        """获取文档统计信息"""
        try:
            # 获取RAG统计信息
            rag_stats = await self.vector_rag.get_knowledge_stats()
            
            # 按文件类型统计
            file_type_stats = {}
            if "category_stats" in rag_stats:
                for category, count in rag_stats["category_stats"].items():
                    if category == "documents":
                        # 这里可以进一步分析文档类型分布
                        file_type_stats[category] = count
            
            return {
                "rag_stats": rag_stats,
                "file_type_stats": file_type_stats,
                "supported_formats": self.document_processor.supported_types
            }
            
        except Exception as e:
            self.logger.error(f"获取文档统计失败: {str(e)}")
            return {"error": str(e)}
    
    async def process_and_add_document(
        self, 
        file_path: str, 
        file_type: str,
        category: str = "documents",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """处理并添加文档到RAG系统（API接口方法）"""
        result = await self.process_and_index_document(
            file_path=file_path,
            file_type=file_type,
            category=category,
            metadata=metadata
        )
        
        if result.get("success"):
            return {
                "document_id": str(uuid.uuid4()),
                "chunks_created": result.get("indexed_chunks", 0),
                "total_chunks": result.get("total_chunks", 0),
                "processing_time": 0,  # 可以添加实际处理时间
                "file_type": file_type,
                "category": category,
                "document_type": result.get("document_type", "unknown"),
                "processing_result": result.get("processing_result", {}),
                "text": result.get("processing_result", {}).get("text", ""),
                "success": True
            }
        else:
            raise Exception(result.get("error", "文档处理失败"))
    
    async def batch_process_and_add_documents(
        self, 
        file_paths: List[str],
        category: str = "documents",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """批量处理并添加文档到RAG系统（API接口方法）"""
        return await self.batch_process_documents(
            file_paths=file_paths,
            category=category,
            metadata=metadata
        )

# 全局实例
document_rag_service = DocumentRAGService()
