#!/usr/bin/env python3
"""
AI助贷招标智能体测试脚本
测试完整的智能体工作流程

@author AI Loan Platform Team
@version 1.1.0
"""

import asyncio
import json
import time
from datetime import datetime
from ai_loan_agent import AILoanAgent

async def test_ai_agent():
    """测试AI助贷招标智能体"""
    print("🤖 AI助贷招标智能体测试")
    print("=" * 50)
    
    # 创建智能体
    agent = AILoanAgent()
    
    # 初始化服务
    print("🔧 初始化AI服务...")
    if not await agent.initialize_services():
        print("❌ AI服务初始化失败")
        return False
    
    print("✅ AI服务初始化成功")
    
    # 测试用例1：完整工作流程
    print("\n📋 测试用例1：完整工作流程")
    print("-" * 30)
    
    # 1. 开始对话
    print("1️⃣ 开始对话...")
    response = agent.start_conversation(user_id=1)
    print(f"✅ {response.message[:100]}...")
    
    # 2. 收集用户信息
    print("\n2️⃣ 收集用户信息...")
    user_data = {
        "user_id": 1,
        "company_name": "测试科技有限公司",
        "industry": "制造业",
        "company_size": "small",
        "business_age": 3,
        "annual_revenue": 2000000,
        "monthly_income": 200000,
        "credit_score": 720,
        "management_experience": 5,
        "risk_tolerance": "medium",
        "preferred_loan_amount": 500000,
        "preferred_term": 24,
        "preferred_rate": 0.08
    }
    
    response = agent.collect_user_info(user_data)
    print(f"✅ {response.message[:100]}...")
    
    # 3. 风险评估
    print("\n3️⃣ 风险评估...")
    response = agent.assess_risk()
    print(f"✅ {response.message[:100]}...")
    
    # 4. 智能匹配
    print("\n4️⃣ 智能匹配...")
    response = agent.smart_matching()
    print(f"✅ {response.message[:100]}...")
    
    # 5. 生成推荐
    print("\n5️⃣ 生成推荐方案...")
    response = agent.generate_recommendations()
    print(f"✅ {response.message[:100]}...")
    
    # 测试用例2：不同企业类型
    print("\n📋 测试用例2：不同企业类型")
    print("-" * 30)
    
    # 重置智能体
    agent.reset_agent()
    
    # 大型制造企业
    print("🏭 大型制造企业测试...")
    response = agent.start_conversation(user_id=2)
    
    user_data_large = {
        "user_id": 2,
        "company_name": "大型制造集团",
        "industry": "制造业",
        "company_size": "large",
        "business_age": 15,
        "annual_revenue": 50000000,
        "monthly_income": 5000000,
        "credit_score": 800,
        "management_experience": 15,
        "risk_tolerance": "low",
        "preferred_loan_amount": 10000000,
        "preferred_term": 60,
        "preferred_rate": 0.05
    }
    
    response = agent.collect_user_info(user_data_large)
    print(f"✅ {response.message[:100]}...")
    
    response = agent.assess_risk()
    print(f"✅ 风险评估完成，风险等级: {response.data.get('risk_level', '未知')}")
    
    # 测试用例3：高风险企业
    print("\n📋 测试用例3：高风险企业")
    print("-" * 30)
    
    # 重置智能体
    agent.reset_agent()
    
    # 高风险企业
    print("⚠️ 高风险企业测试...")
    response = agent.start_conversation(user_id=3)
    
    user_data_high_risk = {
        "user_id": 3,
        "company_name": "初创科技公司",
        "industry": "科技",
        "company_size": "micro",
        "business_age": 1,
        "annual_revenue": 500000,
        "monthly_income": 50000,
        "credit_score": 600,
        "management_experience": 2,
        "risk_tolerance": "high",
        "preferred_loan_amount": 2000000,
        "preferred_term": 36,
        "preferred_rate": 0.12
    }
    
    response = agent.collect_user_info(user_data_high_risk)
    print(f"✅ {response.message[:100]}...")
    
    response = agent.assess_risk()
    print(f"✅ 风险评估完成，风险等级: {response.data.get('risk_level', '未知')}")
    
    # 测试用例4：错误处理
    print("\n📋 测试用例4：错误处理")
    print("-" * 30)
    
    # 测试无用户信息时的风险评估
    agent.reset_agent()
    response = agent.assess_risk()
    print(f"✅ 错误处理测试: {response.message}")
    
    # 测试总结
    print("\n📊 测试总结")
    print("=" * 50)
    
    # 获取对话历史
    history = agent.get_conversation_history()
    print(f"总对话轮数: {len(history)}")
    
    # 统计成功和失败
    success_count = 0
    total_tests = 0
    
    for message in history:
        if "✅" in message.get("message", ""):
            success_count += 1
        total_tests += 1
    
    print(f"成功操作: {success_count}")
    print(f"总操作数: {total_tests}")
    print(f"成功率: {success_count / total_tests * 100:.1f}%" if total_tests > 0 else "成功率: 0%")
    
    # 保存测试结果
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "success_count": success_count,
        "success_rate": success_count / total_tests * 100 if total_tests > 0 else 0,
        "conversation_history": history,
        "agent_state": agent.state.value
    }
    
    filename = f"ai_agent_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存到: {filename}")
    
    return success_count == total_tests

async def main():
    """主函数"""
    print("AI助贷招标智能体 - 综合测试工具")
    print("版本: 1.1.0")
    print("作者: AI Loan Platform Team")
    print()
    
    start_time = time.time()
    
    try:
        success = await test_ai_agent()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n⏱️ 总测试时间: {total_time:.2f}秒")
        
        if success:
            print("\n🎉 所有测试通过！AI助贷招标智能体运行正常！")
            return 0
        else:
            print("\n⚠️ 部分测试失败，请检查相关功能")
            return 1
            
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
