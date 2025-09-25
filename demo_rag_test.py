#!/usr/bin/env python3
"""
AI智能助贷平台 - 向量RAG功能DEMO测试
测试PDF、Office文档处理和OCR功能
"""

import requests
import json
import os
import time
from datetime import datetime
import base64

# API配置
API_BASE_URL = "http://localhost:8000/api/v1"

class RAGDemoTester:
    def __init__(self):
        self.session_id = None
        self.test_results = []
        
    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def test_api_health(self):
        """测试API健康状态"""
        self.log("🔍 测试API健康状态...")
        try:
            response = requests.get(f"{API_BASE_URL}/rag/stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ API健康检查通过: {data['data']['total_count']}条知识记录")
                return True
            else:
                self.log(f"❌ API健康检查失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ API连接失败: {e}", "ERROR")
            return False
    
    def create_chat_session(self):
        """创建聊天会话"""
        self.log("💬 创建聊天会话...")
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/session",
                json={"user_id": "demo_user", "chatbot_role": "general"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.session_id = data['data']['session_id']
                self.log(f"✅ 聊天会话创建成功: {self.session_id}")
                return True
            else:
                self.log(f"❌ 聊天会话创建失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ 聊天会话创建异常: {e}", "ERROR")
            return False
    
    def test_rag_question(self, question, expected_keywords=None):
        """测试RAG问答"""
        self.log(f"🤖 测试RAG问答: {question}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/message",
                json={
                    "session_id": self.session_id,
                    "message": question,
                    "user_id": "demo_user"
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                answer = data['data']['response']
                self.log(f"✅ AI回复: {answer[:100]}...")
                
                # 检查关键词
                if expected_keywords:
                    found_keywords = [kw for kw in expected_keywords if kw in answer]
                    if found_keywords:
                        self.log(f"✅ 找到预期关键词: {found_keywords}")
                    else:
                        self.log(f"⚠️ 未找到预期关键词: {expected_keywords}", "WARNING")
                
                self.test_results.append({
                    "question": question,
                    "answer": answer,
                    "status": "success"
                })
                return True
            else:
                self.log(f"❌ RAG问答失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ RAG问答异常: {e}", "ERROR")
            return False
    
    def test_document_upload(self, file_path, category, file_type):
        """测试文档上传和处理"""
        self.log(f"📄 测试文档上传: {file_path} ({file_type})")
        try:
            if not os.path.exists(file_path):
                self.log(f"❌ 文件不存在: {file_path}", "ERROR")
                return False
                
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'category': category,
                    'metadata': json.dumps({
                        'source': 'demo_test',
                        'upload_time': datetime.now().isoformat(),
                        'file_type': file_type
                    })
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/rag/process-document",
                    files=files,
                    data=data,
                    timeout=60
                )
                
            if response.status_code == 200:
                result = response.json()
                self.log(f"✅ 文档处理成功: {result['data']['chunks_created']}个文档块")
                return True
            else:
                self.log(f"❌ 文档处理失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ 文档处理异常: {e}", "ERROR")
            return False
    
    def test_knowledge_search(self, query, search_type="hybrid"):
        """测试知识搜索"""
        self.log(f"🔍 测试知识搜索: {query} ({search_type})")
        try:
            response = requests.post(
                f"{API_BASE_URL}/rag/search",
                json={
                    "query": query,
                    "search_type": search_type,
                    "max_results": 5
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                results = data['data']['results']
                self.log(f"✅ 搜索成功: 找到{len(results)}条结果")
                for i, result in enumerate(results[:3], 1):
                    self.log(f"  {i}. {result['title']} (相似度: {result.get('similarity_score', 'N/A')})")
                return True
            else:
                self.log(f"❌ 知识搜索失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ 知识搜索异常: {e}", "ERROR")
            return False
    
    def create_test_documents(self):
        """创建测试文档"""
        self.log("📝 创建测试文档...")
        
        # 创建测试目录
        test_dir = "demo_test_documents"
        os.makedirs(test_dir, exist_ok=True)
        
        # 创建测试PDF文档
        pdf_content = """
        AI智能助贷平台 - 产品说明
        
        1. 个人信用贷款
        - 贷款额度: 1万-50万元
        - 贷款期限: 6-36个月
        - 年利率: 4.5%-12%
        - 申请条件: 年满18周岁，有稳定收入
        
        2. 企业流动资金贷款
        - 贷款额度: 10万-500万元
        - 贷款期限: 3-24个月
        - 年利率: 3.8%-8.5%
        - 申请条件: 企业成立满1年，有正常经营
        
        3. 抵押贷款
        - 贷款额度: 房产评估价的70%
        - 贷款期限: 1-20年
        - 年利率: 3.2%-6.8%
        - 申请条件: 有房产抵押
        """
        
        # 创建测试Word文档内容
        word_content = """
        贷款申请流程指南
        
        第一步：在线申请
        - 访问AI智能助贷平台
        - 填写基本信息
        - 上传必要材料
        
        第二步：智能评估
        - AI风险评估系统分析
        - 信用评分计算
        - 风险等级确定
        
        第三步：产品匹配
        - 智能匹配最优产品
        - 多维度对比分析
        - 个性化推荐
        
        第四步：审核放款
        - 人工审核确认
        - 合同签署
        - 资金到账
        """
        
        # 创建测试Excel内容
        excel_content = """
        贷款产品对比表
        产品名称,贷款额度,年利率,期限,申请条件
        个人信用贷,1-50万,4.5%-12%,6-36月,年满18周岁
        企业流贷,10-500万,3.8%-8.5%,3-24月,企业成立1年
        抵押贷款,房产70%,3.2%-6.8%,1-20年,有房产抵押
        消费贷款,5-30万,5.5%-15%,6-60月,有稳定收入
        """
        
        # 保存测试文档
        with open(f"{test_dir}/loan_products.pdf", "w", encoding="utf-8") as f:
            f.write(pdf_content)
        
        with open(f"{test_dir}/application_guide.txt", "w", encoding="utf-8") as f:
            f.write(word_content)
        
        with open(f"{test_dir}/product_comparison.csv", "w", encoding="utf-8") as f:
            f.write(excel_content)
        
        self.log(f"✅ 测试文档创建完成: {test_dir}/")
        return test_dir
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        self.log("🚀 开始向量RAG功能综合测试...")
        print("=" * 80)
        
        # 1. API健康检查
        if not self.test_api_health():
            self.log("❌ API健康检查失败，测试终止", "ERROR")
            return False
        
        # 2. 创建聊天会话
        if not self.create_chat_session():
            self.log("❌ 聊天会话创建失败，测试终止", "ERROR")
            return False
        
        # 3. 测试基础RAG问答
        self.log("\n📋 测试1: 基础RAG问答功能")
        test_questions = [
            ("什么是个人信用贷款？", ["个人信用", "贷款", "额度"]),
            ("如何申请企业贷款？", ["企业", "申请", "流程"]),
            ("贷款利率是多少？", ["利率", "年利率", "费用"]),
            ("需要什么申请材料？", ["材料", "证件", "证明"]),
            ("贷款审批需要多长时间？", ["审批", "时间", "工作日"])
        ]
        
        for question, keywords in test_questions:
            self.test_rag_question(question, keywords)
            time.sleep(2)  # 避免请求过快
        
        # 4. 创建并上传测试文档
        self.log("\n📋 测试2: 文档处理和上传功能")
        test_dir = self.create_test_documents()
        
        # 上传测试文档
        test_files = [
            (f"{test_dir}/loan_products.pdf", "loan_products", "pdf"),
            (f"{test_dir}/application_guide.txt", "faq", "txt"),
            (f"{test_dir}/product_comparison.csv", "policies", "csv")
        ]
        
        for file_path, category, file_type in test_files:
            self.test_document_upload(file_path, category, file_type)
            time.sleep(3)  # 给文档处理时间
        
        # 5. 测试知识搜索
        self.log("\n📋 测试3: 知识搜索功能")
        search_queries = [
            "个人信用贷款额度",
            "企业贷款申请条件",
            "贷款利率范围",
            "申请流程步骤"
        ]
        
        for query in search_queries:
            self.test_knowledge_search(query, "hybrid")
            time.sleep(1)
        
        # 6. 测试基于新文档的问答
        self.log("\n📋 测试4: 基于新文档的智能问答")
        new_questions = [
            "个人信用贷款的最高额度是多少？",
            "企业贷款需要什么条件？",
            "抵押贷款的利率范围是多少？",
            "贷款申请有哪些步骤？"
        ]
        
        for question in new_questions:
            self.test_rag_question(question)
            time.sleep(2)
        
        # 7. 测试不同搜索类型
        self.log("\n📋 测试5: 不同搜索类型对比")
        test_query = "贷款利率"
        
        for search_type in ["vector", "text", "hybrid"]:
            self.log(f"测试{search_type}搜索:")
            self.test_knowledge_search(test_query, search_type)
            time.sleep(1)
        
        # 8. 生成测试报告
        self.generate_test_report()
        
        return True
    
    def generate_test_report(self):
        """生成测试报告"""
        self.log("\n📊 生成测试报告...")
        
        report = {
            "test_time": datetime.now().isoformat(),
            "total_questions": len(self.test_results),
            "successful_questions": len([r for r in self.test_results if r["status"] == "success"]),
            "test_results": self.test_results
        }
        
        # 保存报告
        with open("demo_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print("\n" + "=" * 80)
        print("🎉 向量RAG功能测试完成！")
        print("=" * 80)
        print(f"📊 测试时间: {report['test_time']}")
        print(f"📝 总问题数: {report['total_questions']}")
        print(f"✅ 成功回答: {report['successful_questions']}")
        print(f"📈 成功率: {report['successful_questions']/report['total_questions']*100:.1f}%")
        print(f"📄 详细报告: demo_test_report.json")
        print("=" * 80)
        
        # 清理测试文件
        import shutil
        if os.path.exists("demo_test_documents"):
            shutil.rmtree("demo_test_documents")
            self.log("🧹 清理测试文件完成")

def main():
    """主函数"""
    print("🤖 AI智能助贷平台 - 向量RAG功能DEMO测试")
    print("=" * 80)
    
    tester = RAGDemoTester()
    
    try:
        success = tester.run_comprehensive_test()
        if success:
            print("\n🎉 所有测试完成！")
        else:
            print("\n❌ 测试过程中出现错误")
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试出现异常: {e}")

if __name__ == "__main__":
    main()
