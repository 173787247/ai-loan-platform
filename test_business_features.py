"""
业务功能测试脚本
测试新实现的高级风控、定价、审批和合规功能
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_advanced_risk_assessment():
    """测试高级风险评估"""
    print("🔍 测试高级风险评估")
    print("=" * 50)
    
    # 测试用例1：低风险客户
    low_risk_data = {
        "credit_score": 750,
        "annual_income": 200000,
        "monthly_income": 16667,
        "monthly_debt": 5000,
        "employment_years": 5,
        "age": 35,
        "marital_status": "married",
        "education": "bachelor",
        "industry": "科技",
        "credit_history_years": 10,
        "payment_delinquencies": 0,
        "credit_utilization": 0.3,
        "loan_count": 2,
        "default_count": 0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/risk/advanced-assessment",
            json=low_risk_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 低风险客户评估成功")
                print(f"   风险得分: {data['overall_risk_score']:.3f}")
                print(f"   风险等级: {data['risk_level']}")
                print(f"   审批建议: {data['approval_recommendation']}")
                print(f"   置信度: {data['confidence_score']:.3f}")
            else:
                print(f"❌ 低风险客户评估失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
    
    print()
    
    # 测试用例2：高风险客户
    high_risk_data = {
        "credit_score": 580,
        "annual_income": 40000,
        "monthly_income": 3333,
        "monthly_debt": 2000,
        "employment_years": 0.5,
        "age": 20,
        "marital_status": "single",
        "education": "high_school",
        "industry": "娱乐",
        "credit_history_years": 1,
        "payment_delinquencies": 3,
        "credit_utilization": 0.9,
        "loan_count": 0,
        "default_count": 1
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/risk/advanced-assessment",
            json=high_risk_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 高风险客户评估成功")
                print(f"   风险得分: {data['overall_risk_score']:.3f}")
                print(f"   风险等级: {data['risk_level']}")
                print(f"   审批建议: {data['approval_recommendation']}")
                print(f"   置信度: {data['confidence_score']:.3f}")
            else:
                print(f"❌ 高风险客户评估失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def test_advanced_pricing():
    """测试高级定价"""
    print("\n💰 测试高级定价")
    print("=" * 50)
    
    # 测试贷款定价
    loan_request = {
        "loan_amount": 100000,
        "loan_term_months": 24,
        "loan_type": "personal_loan"
    }
    
    risk_assessment = {
        "overall_risk_score": 0.3,
        "risk_level": "low"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/pricing/calculate",
            json={
                "loan_request": loan_request,
                "risk_assessment": risk_assessment,
                "pricing_strategy": "risk_based"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 贷款定价计算成功")
                print(f"   基础利率: {data['base_interest_rate']:.1%}")
                print(f"   最终利率: {data['final_interest_rate']:.1%}")
                print(f"   月供: ¥{data['monthly_payment']:,.2f}")
                print(f"   总利息: ¥{data['total_interest']:,.2f}")
                print(f"   总费用: ¥{data['total_fees']:,.2f}")
                print(f"   APR: {data['apr']:.1%}")
                print(f"   利润空间: {data['profit_margin']:.1%}")
            else:
                print(f"❌ 贷款定价计算失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
    
    print()
    
    # 测试定价优化
    try:
        response = requests.post(
            f"{BASE_URL}/pricing/optimize",
            json={
                "loan_request": loan_request,
                "risk_assessment": risk_assessment,
                "target_profit_margin": 0.05
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 定价方案优化成功")
                print(f"   推荐方案: {data['recommended']['strategy']}")
                print(f"   推荐利率: {data['recommended']['interest_rate']:.1%}")
                print(f"   推荐月供: ¥{data['recommended']['monthly_payment']:,.2f}")
                print(f"   方案数量: {len(data['scenarios'])}")
            else:
                print(f"❌ 定价方案优化失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def test_approval_workflow():
    """测试审批流程"""
    print("\n📋 测试审批流程")
    print("=" * 50)
    
    # 测试审批处理
    application_data = {
        "application_id": "APP001",
        "loan_amount": 50000,
        "loan_term_months": 12,
        "credit_score": 720,
        "monthly_income": 10000,
        "monthly_debt": 3000,
        "employment_years": 3,
        "age": 30,
        "marital_status": "married",
        "education": "bachelor",
        "industry": "科技"
    }
    
    risk_assessment = {
        "overall_risk_score": 0.4,
        "risk_level": "medium"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/approval/process",
            json={
                "application_data": application_data,
                "risk_assessment": risk_assessment
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 审批处理成功")
                print(f"   申请ID: {data['application_id']}")
                print(f"   审批状态: {data['status']}")
                print(f"   审批级别: {data['approval_level']}")
                print(f"   决策原因: {data['decision_reason']}")
                print(f"   批准金额: ¥{data['approval_amount']:,.2f}")
                print(f"   批准期限: {data['approved_term']}个月")
                print(f"   置信度: {data['confidence_score']:.3f}")
                
                # 测试审批状态查询
                time.sleep(1)
                test_approval_status(data['application_id'])
                
            else:
                print(f"❌ 审批处理失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def test_approval_status(application_id):
    """测试审批状态查询"""
    try:
        response = requests.get(
            f"{BASE_URL}/approval/status/{application_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 审批状态查询成功")
                print(f"   状态: {data['status']}")
                print(f"   审批级别: {data['approval_level']}")
                print(f"   决策时间: {data['decision_timestamp']}")
            else:
                print(f"❌ 审批状态查询失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def test_compliance_check():
    """测试合规检查"""
    print("\n🛡️ 测试合规检查")
    print("=" * 50)
    
    # 测试合规检查
    application_data = {
        "application_id": "APP001",
        "loan_amount": 100000,
        "interest_rate": 0.12,
        "credit_score": 700,
        "annual_income": 120000,
        "monthly_income": 10000,
        "monthly_debt": 4000,
        "age": 35,
        "marital_status": "married",
        "education": "bachelor",
        "industry": "科技",
        "identity_verified": True,
        "address_verified": True,
        "income_verified": True,
        "data_consent": True,
        "data_encrypted": True,
        "disclosures": ["年化利率", "总费用", "还款条件"],
        "concentration_risk": 0.05,
        "stress_test_passed": True
    }
    
    risk_assessment = {
        "overall_risk_score": 0.3,
        "risk_level": "low"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/compliance/check",
            json={
                "application_data": application_data,
                "risk_assessment": risk_assessment
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 合规检查成功")
                print(f"   报告ID: {data['report_id']}")
                print(f"   合规得分: {data['overall_compliance_score']:.3f}")
                print(f"   合规等级: {data['compliance_level']}")
                print(f"   检查项目: {len(data['checks'])}项")
                print(f"   关键违规: {len(data['critical_violations'])}项")
                print(f"   需要人工审核: {data['requires_manual_review']}")
                
                # 显示检查详情
                print("\n   检查详情:")
                for check in data['checks']:
                    status = "✅" if check['is_compliant'] else "❌"
                    print(f"     {status} {check['rule_type']}: {check['compliance_level']}")
                    if check['violation_details']:
                        for violation in check['violation_details']:
                            print(f"       - {violation}")
                
            else:
                print(f"❌ 合规检查失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def test_risk_model_info():
    """测试风控模型信息"""
    print("\n📊 测试风控模型信息")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/risk/model-info", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result["data"]
                print(f"✅ 风控模型信息获取成功")
                print(f"   模型版本: {data['model_version']}")
                print(f"   风险权重: {len(data['risk_weights'])}项")
                print(f"   风险阈值: {len(data['risk_thresholds'])}项")
                print(f"   行业风险: {len(data['industry_risks'])}项")
                print(f"   支持因子: {len(data['supported_factors'])}项")
            else:
                print(f"❌ 风控模型信息获取失败: {result.get('message')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def main():
    """主测试函数"""
    print("🚀 业务功能测试开始")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试目标: {BASE_URL}")
    print("=" * 60)
    
    # 检查服务健康状态
    try:
        health_response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 服务健康检查通过")
        else:
            print("❌ 服务健康检查失败")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        return
    
    print()
    
    # 执行各项测试
    test_advanced_risk_assessment()
    test_advanced_pricing()
    test_approval_workflow()
    test_compliance_check()
    test_risk_model_info()
    
    print("\n" + "=" * 60)
    print("🎉 业务功能测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
