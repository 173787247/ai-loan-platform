#!/usr/bin/env python3
"""
AI服务API测试脚本

@author AI Loan Platform Team
@version 1.0.0
"""

import requests
import json
import time
import numpy as np
from datetime import datetime

# API基础URL - 直接访问AI服务
API_BASE_URL = "http://localhost:8000/api/v1"

def test_ai_health():
    """测试AI服务健康状态"""
    print("🔍 测试AI服务健康状态...")
    try:
        response = requests.get(f"{API_BASE_URL}/ai/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI服务状态: {data.get('message', 'Unknown')}")
            if data.get('data'):
                print(f"   - 文档处理器: {data['data'].get('document_processor', {}).get('status', 'Unknown')}")
                print(f"   - 风险评估器: {data['data'].get('risk_assessor', {}).get('status', 'Unknown')}")
                print(f"   - 智能匹配器: {data['data'].get('smart_matcher', {}).get('status', 'Unknown')}")
                print(f"   - 推荐引擎: {data['data'].get('recommendation_engine', {}).get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ AI服务健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI服务连接失败: {str(e)}")
        return False

def test_model_status():
    """测试模型状态API"""
    print("\n🔍 测试模型状态API...")
    try:
        response = requests.get(f"{API_BASE_URL}/ai/model/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 模型状态获取成功: {data.get('message', 'Unknown')}")
            if data.get('data'):
                for model_name, status in data['data'].items():
                    print(f"   - {model_name}: {'已加载' if status.get('loaded') else '未加载'}")
                    if status.get('metrics'):
                        print(f"     准确率: {status['metrics'].get('accuracy', 0):.2%}")
            return True
        else:
            print(f"❌ 模型状态获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 模型状态API调用失败: {str(e)}")
        return False

def test_model_training():
    """测试模型训练API"""
    print("\n🔍 测试模型训练API...")
    try:
        # 生成模拟训练数据
        training_data = {
            "X_train": np.random.rand(100, 20).tolist(),
            "y_train": np.random.randint(0, 5, 100).tolist(),
            "X_val": np.random.rand(20, 20).tolist(),
            "y_val": np.random.randint(0, 5, 20).tolist()
        }
        
        payload = {
            "model_name": "risk_prediction",
            "training_data": training_data
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ai/model/train",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 模型训练成功: {data.get('message', 'Unknown')}")
            if data.get('data'):
                print(f"   - 最终准确率: {data['data'].get('final_accuracy', 0):.2%}")
                print(f"   - 训练轮数: {data['data'].get('training_epochs', 0)}")
            return True
        else:
            print(f"❌ 模型训练失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 模型训练API调用失败: {str(e)}")
        return False

def test_model_prediction():
    """测试模型预测API"""
    print("\n🔍 测试模型预测API...")
    try:
        # 生成模拟输入数据
        input_data = np.random.rand(20).tolist()
        
        payload = {
            "model_name": "risk_prediction",
            "input_data": input_data
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ai/model/predict",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 模型预测成功: {data.get('message', 'Unknown')}")
            if data.get('data'):
                print(f"   - 预测结果: {data['data'].get('prediction', 'Unknown')}")
                print(f"   - 置信度: {data['data'].get('confidence', 0):.2%}")
            return True
        else:
            print(f"❌ 模型预测失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 模型预测API调用失败: {str(e)}")
        return False

def test_risk_assessment():
    """测试风险评估API"""
    print("\n🔍 测试风险评估API...")
    try:
        payload = {
            "user_id": 1,
            "business_data": {
                "revenue": 1000,
                "profit": 100,
                "assets": 2000,
                "liabilities": 800,
                "industry": "制造业",
                "credit_rating": "A",
                "management_experience": 5,
                "employee_count": 50
            },
            "market_data": {
                "gdp_growth": 5.5,
                "interest_rate": 0.035,
                "inflation": 0.025,
                "exchange_rate_volatility": 0.02
            }
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ai/risk/assess",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 风险评估成功: {data.get('message', 'Unknown')}")
            if data.get('data'):
                risk_data = data['data']
                print(f"   - 风险等级: {risk_data.get('risk_level', 'Unknown')}")
                print(f"   - 风险概率: {risk_data.get('risk_probability', 0):.2%}")
                if risk_data.get('risk_scores'):
                    scores = risk_data['risk_scores']
                    print(f"   - 综合风险分数: {scores.get('total_risk_score', 0):.2f}")
            return True
        else:
            print(f"❌ 风险评估失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 风险评估API调用失败: {str(e)}")
        return False

def test_risk_trends_analysis():
    """测试风险趋势分析API"""
    print("\n🔍 测试风险趋势分析API...")
    try:
        # 生成模拟历史数据
        historical_data = np.random.rand(30, 20).tolist()
        
        payload = {
            "historical_data": historical_data
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ai/analyze/risk-trends",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 风险趋势分析成功: {data.get('message', 'Unknown')}")
            if data.get('data'):
                trend_data = data['data']
                print(f"   - 风险趋势: {trend_data.get('risk_trend', 'Unknown')}")
                print(f"   - 平均置信度: {trend_data.get('average_confidence', 0):.2%}")
            return True
        else:
            print(f"❌ 风险趋势分析失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 风险趋势分析API调用失败: {str(e)}")
        return False

def test_market_sentiment_analysis():
    """测试市场情绪分析API"""
    print("\n🔍 测试市场情绪分析API...")
    try:
        # 生成模拟市场数据
        market_data = np.random.rand(10, 10).tolist()
        
        payload = {
            "market_data": market_data
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ai/analyze/market-sentiment",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 市场情绪分析成功: {data.get('message', 'Unknown')}")
            if data.get('data'):
                sentiment_data = data['data']
                print(f"   - 市场情绪: {sentiment_data.get('market_sentiment', 'Unknown')}")
                print(f"   - 置信度: {sentiment_data.get('confidence', 0):.2%}")
            return True
        else:
            print(f"❌ 市场情绪分析失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 市场情绪分析API调用失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始AI服务API测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(5)
    
    # 测试结果统计
    test_results = []
    
    # 执行测试
    test_results.append(("AI服务健康检查", test_ai_health()))
    test_results.append(("模型状态API", test_model_status()))
    test_results.append(("模型训练API", test_model_training()))
    test_results.append(("模型预测API", test_model_prediction()))
    test_results.append(("风险评估API", test_risk_assessment()))
    test_results.append(("风险趋势分析API", test_risk_trends_analysis()))
    test_results.append(("市场情绪分析API", test_market_sentiment_analysis()))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！AI服务运行正常。")
    else:
        print("⚠️  部分测试失败，请检查服务状态。")
    
    return passed == total

if __name__ == "__main__":
    main()
