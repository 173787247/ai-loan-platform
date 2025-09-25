"""
高级风险评估模型
基于深度学习和金融工程理论

@author AI Loan Platform Team
@version 1.1.0
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_recall_curve
import joblib
from typing import Dict, Any, List, Tuple
from loguru import logger
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AdvancedRiskModel:
    """高级风险评估模型"""
    
    def __init__(self):
        self.logger = logger
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_importance = {}
        
    def create_credit_risk_model(self) -> nn.Module:
        """创建信用风险深度学习模型"""
        class CreditRiskNet(nn.Module):
            def __init__(self, input_dim=20, hidden_dims=[128, 64, 32], dropout_rate=0.3):
                super().__init__()
                
                layers = []
                prev_dim = input_dim
                
                for hidden_dim in hidden_dims:
                    layers.extend([
                        nn.Linear(prev_dim, hidden_dim),
                        nn.BatchNorm1d(hidden_dim),
                        nn.ReLU(),
                        nn.Dropout(dropout_rate)
                    ])
                    prev_dim = hidden_dim
                
                # 输出层：违约概率
                layers.append(nn.Linear(prev_dim, 1))
                layers.append(nn.Sigmoid())
                
                self.network = nn.Sequential(*layers)
                
            def forward(self, x):
                return self.network(x)
        
        return CreditRiskNet()
    
    def create_market_risk_model(self) -> nn.Module:
        """创建市场风险LSTM模型"""
        class MarketRiskLSTM(nn.Module):
            def __init__(self, input_dim=10, hidden_dim=64, num_layers=2, dropout_rate=0.2):
                super().__init__()
                self.hidden_dim = hidden_dim
                self.num_layers = num_layers
                
                self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, 
                                  batch_first=True, dropout=dropout_rate)
                self.fc = nn.Sequential(
                    nn.Linear(hidden_dim, 32),
                    nn.ReLU(),
                    nn.Dropout(dropout_rate),
                    nn.Linear(32, 1),
                    nn.Sigmoid()
                )
                
            def forward(self, x):
                # x shape: (batch_size, seq_len, input_dim)
                lstm_out, _ = self.lstm(x)
                # 取最后一个时间步的输出
                last_output = lstm_out[:, -1, :]
                return self.fc(last_output)
        
        return MarketRiskLSTM()
    
    def create_operational_risk_model(self) -> nn.Module:
        """创建操作风险模型"""
        class OperationalRiskNet(nn.Module):
            def __init__(self, input_dim=15):
                super().__init__()
                self.network = nn.Sequential(
                    nn.Linear(input_dim, 64),
                    nn.BatchNorm1d(64),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(64, 32),
                    nn.BatchNorm1d(32),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(32, 16),
                    nn.ReLU(),
                    nn.Linear(16, 1),
                    nn.Sigmoid()
                )
                
            def forward(self, x):
                return self.network(x)
        
        return OperationalRiskNet()
    
    def create_liquidity_risk_model(self) -> nn.Module:
        """创建流动性风险模型"""
        class LiquidityRiskNet(nn.Module):
            def __init__(self, input_dim=12):
                super().__init__()
                self.network = nn.Sequential(
                    nn.Linear(input_dim, 48),
                    nn.ReLU(),
                    nn.Dropout(0.25),
                    nn.Linear(48, 24),
                    nn.ReLU(),
                    nn.Dropout(0.15),
                    nn.Linear(24, 12),
                    nn.ReLU(),
                    nn.Linear(12, 1),
                    nn.Sigmoid()
                )
                
            def forward(self, x):
                return self.network(x)
        
        return LiquidityRiskNet()
    
    def extract_credit_features(self, business_data: Dict[str, Any]) -> np.ndarray:
        """提取信用风险特征"""
        features = []
        
        # 基础财务指标
        features.append(business_data.get('revenue', 0) / 1000000)  # 收入（百万）
        features.append(business_data.get('profit_margin', 0))  # 利润率
        features.append(business_data.get('debt_ratio', 0))  # 负债率
        features.append(business_data.get('current_ratio', 0))  # 流动比率
        features.append(business_data.get('quick_ratio', 0))  # 速动比率
        
        # 信用历史
        features.append(business_data.get('credit_score', 0) / 850)  # 标准化信用评分
        features.append(business_data.get('payment_history_score', 0))  # 还款历史评分
        features.append(business_data.get('credit_utilization', 0))  # 信用利用率
        
        # 业务特征
        features.append(business_data.get('business_age', 0) / 20)  # 标准化经营年限
        features.append(business_data.get('employee_count', 0) / 1000)  # 标准化员工数
        features.append(business_data.get('industry_risk_score', 0))  # 行业风险评分
        
        # 管理质量
        features.append(business_data.get('management_experience', 0) / 20)  # 管理经验
        features.append(business_data.get('audit_quality_score', 0))  # 审计质量评分
        features.append(business_data.get('governance_score', 0))  # 治理评分
        
        # 市场地位
        features.append(business_data.get('market_share', 0))  # 市场份额
        features.append(business_data.get('competitive_position', 0))  # 竞争地位
        features.append(business_data.get('brand_value', 0) / 1000000)  # 品牌价值
        
        # 现金流质量
        features.append(business_data.get('cash_flow_stability', 0))  # 现金流稳定性
        features.append(business_data.get('working_capital_ratio', 0))  # 营运资本比率
        features.append(business_data.get('cash_conversion_cycle', 0) / 365)  # 现金转换周期
        
        # 增长潜力
        features.append(business_data.get('revenue_growth_rate', 0))  # 收入增长率
        features.append(business_data.get('profit_growth_rate', 0))  # 利润增长率
        
        return np.array(features, dtype=np.float32)
    
    def extract_market_features(self, market_data: Dict[str, Any]) -> np.ndarray:
        """提取市场风险特征"""
        features = []
        
        # 宏观经济指标
        features.append(market_data.get('gdp_growth_rate', 0))  # GDP增长率
        features.append(market_data.get('inflation_rate', 0))  # 通胀率
        features.append(market_data.get('interest_rate', 0))  # 利率
        features.append(market_data.get('unemployment_rate', 0))  # 失业率
        
        # 市场波动性
        features.append(market_data.get('market_volatility', 0))  # 市场波动率
        features.append(market_data.get('sector_volatility', 0))  # 行业波动率
        features.append(market_data.get('currency_volatility', 0))  # 汇率波动率
        
        # 行业指标
        features.append(market_data.get('sector_growth_rate', 0))  # 行业增长率
        features.append(market_data.get('sector_competition_index', 0))  # 行业竞争指数
        features.append(market_data.get('regulatory_risk_score', 0))  # 监管风险评分
        
        return np.array(features, dtype=np.float32)
    
    def extract_operational_features(self, business_data: Dict[str, Any]) -> np.ndarray:
        """提取操作风险特征"""
        features = []
        
        # 内部控制
        features.append(business_data.get('internal_control_score', 0))  # 内控评分
        features.append(business_data.get('audit_frequency', 0))  # 审计频率
        features.append(business_data.get('compliance_score', 0))  # 合规评分
        
        # 技术系统
        features.append(business_data.get('it_security_score', 0))  # IT安全评分
        features.append(business_data.get('system_reliability', 0))  # 系统可靠性
        features.append(business_data.get('data_quality_score', 0))  # 数据质量评分
        
        # 人员管理
        features.append(business_data.get('employee_turnover_rate', 0))  # 员工流失率
        features.append(business_data.get('training_completion_rate', 0))  # 培训完成率
        features.append(business_data.get('performance_score', 0))  # 绩效评分
        
        # 流程管理
        features.append(business_data.get('process_automation_rate', 0))  # 流程自动化率
        features.append(business_data.get('error_rate', 0))  # 错误率
        features.append(business_data.get('efficiency_score', 0))  # 效率评分
        
        # 外部依赖
        features.append(business_data.get('supplier_concentration', 0))  # 供应商集中度
        features.append(business_data.get('customer_concentration', 0))  # 客户集中度
        features.append(business_data.get('geographic_diversification', 0))  # 地理分散度
        
        return np.array(features, dtype=np.float32)
    
    def extract_liquidity_features(self, business_data: Dict[str, Any]) -> np.ndarray:
        """提取流动性风险特征"""
        features = []
        
        # 流动性比率
        features.append(business_data.get('current_ratio', 0))  # 流动比率
        features.append(business_data.get('quick_ratio', 0))  # 速动比率
        features.append(business_data.get('cash_ratio', 0))  # 现金比率
        
        # 现金流指标
        features.append(business_data.get('operating_cash_flow', 0) / 1000000)  # 经营现金流
        features.append(business_data.get('free_cash_flow', 0) / 1000000)  # 自由现金流
        features.append(business_data.get('cash_flow_coverage_ratio', 0))  # 现金流覆盖率
        
        # 资产流动性
        features.append(business_data.get('liquid_asset_ratio', 0))  # 流动资产比率
        features.append(business_data.get('inventory_turnover', 0))  # 存货周转率
        features.append(business_data.get('receivables_turnover', 0))  # 应收账款周转率
        
        # 融资能力
        features.append(business_data.get('credit_facility_utilization', 0))  # 信贷额度利用率
        features.append(business_data.get('banking_relationship_score', 0))  # 银行关系评分
        features.append(business_data.get('alternative_funding_sources', 0))  # 替代融资来源
        
        return np.array(features, dtype=np.float32)
    
    def train_models(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """训练所有风险模型"""
        self.logger.info("开始训练风险模型")
        
        # 准备训练数据
        credit_features = []
        market_features = []
        operational_features = []
        liquidity_features = []
        labels = []
        
        for data in training_data:
            credit_features.append(self.extract_credit_features(data['business_data']))
            market_features.append(self.extract_market_features(data['market_data']))
            operational_features.append(self.extract_operational_features(data['business_data']))
            liquidity_features.append(self.extract_liquidity_features(data['business_data']))
            labels.append(data['default_label'])
        
        # 转换为numpy数组
        credit_X = np.array(credit_features)
        market_X = np.array(market_features)
        operational_X = np.array(operational_features)
        liquidity_X = np.array(liquidity_features)
        y = np.array(labels)
        
        # 标准化特征
        credit_X_scaled = self.scaler.fit_transform(credit_X)
        
        # 训练信用风险模型
        credit_model = self.create_credit_risk_model().to(self.device)
        credit_optimizer = optim.Adam(credit_model.parameters(), lr=0.001)
        credit_criterion = nn.BCELoss()
        
        # 训练循环
        credit_model.train()
        for epoch in range(100):
            credit_optimizer.zero_grad()
            credit_output = credit_model(torch.FloatTensor(credit_X_scaled).to(self.device))
            credit_loss = credit_criterion(credit_output.squeeze(), torch.FloatTensor(y).to(self.device))
            credit_loss.backward()
            credit_optimizer.step()
        
        self.models['credit'] = credit_model
        
        # 计算特征重要性
        self.feature_importance['credit'] = self.calculate_feature_importance(credit_model, credit_X_scaled)
        
        self.logger.info("风险模型训练完成")
        return {
            'status': 'success',
            'models_trained': ['credit'],
            'training_samples': len(training_data),
            'feature_importance': self.feature_importance
        }
    
    def calculate_feature_importance(self, model: nn.Module, X: np.ndarray) -> List[float]:
        """计算特征重要性"""
        model.eval()
        with torch.no_grad():
            base_pred = model(torch.FloatTensor(X).to(self.device)).cpu().numpy()
            
            importance = []
            for i in range(X.shape[1]):
                X_perturbed = X.copy()
                X_perturbed[:, i] = 0  # 将第i个特征置零
                perturbed_pred = model(torch.FloatTensor(X_perturbed).to(self.device)).cpu().numpy()
                importance.append(np.mean(np.abs(base_pred - perturbed_pred)))
            
            return importance
    
    def predict_risk(self, business_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """预测风险"""
        try:
            # 提取特征
            credit_features = self.extract_credit_features(business_data)
            market_features = self.extract_market_features(market_data)
            operational_features = self.extract_operational_features(business_data)
            liquidity_features = self.extract_liquidity_features(business_data)
            
            # 标准化信用风险特征
            credit_features_scaled = self.scaler.transform(credit_features.reshape(1, -1))
            
            # 预测
            if 'credit' in self.models:
                self.models['credit'].eval()
                with torch.no_grad():
                    credit_risk = self.models['credit'](torch.FloatTensor(credit_features_scaled).to(self.device)).cpu().numpy()[0][0]
            else:
                credit_risk = 0.5  # 默认中等风险
            
            # 计算综合风险评分
            total_risk = self.calculate_comprehensive_risk(
                credit_risk, market_features, operational_features, liquidity_features
            )
            
            return {
                'credit_risk': float(credit_risk),
                'market_risk': float(np.mean(market_features)),
                'operational_risk': float(np.mean(operational_features)),
                'liquidity_risk': float(np.mean(liquidity_features)),
                'total_risk': float(total_risk),
                'risk_level': self.determine_risk_level(total_risk),
                'confidence': self.calculate_confidence(credit_risk, market_features, operational_features, liquidity_features)
            }
            
        except Exception as e:
            self.logger.error(f"风险预测失败: {str(e)}")
            raise
    
    def calculate_comprehensive_risk(self, credit_risk: float, market_features: np.ndarray, 
                                   operational_features: np.ndarray, liquidity_features: np.ndarray) -> float:
        """计算综合风险评分"""
        # 权重分配
        credit_weight = 0.4
        market_weight = 0.2
        operational_weight = 0.2
        liquidity_weight = 0.2
        
        market_risk = np.mean(market_features)
        operational_risk = np.mean(operational_features)
        liquidity_risk = np.mean(liquidity_features)
        
        total_risk = (credit_risk * credit_weight + 
                     market_risk * market_weight + 
                     operational_risk * operational_weight + 
                     liquidity_risk * liquidity_weight)
        
        return total_risk
    
    def determine_risk_level(self, total_risk: float) -> str:
        """确定风险等级"""
        if total_risk < 0.25:
            return "LOW"
        elif total_risk < 0.5:
            return "MEDIUM"
        elif total_risk < 0.75:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def calculate_confidence(self, credit_risk: float, market_features: np.ndarray, 
                           operational_features: np.ndarray, liquidity_features: np.ndarray) -> float:
        """计算预测置信度"""
        # 基于特征稳定性和模型确定性计算置信度
        feature_stability = 1.0 - np.std([credit_risk, np.mean(market_features), 
                                        np.mean(operational_features), np.mean(liquidity_features)])
        
        # 基于数据完整性
        data_completeness = np.mean([1.0 if f != 0 else 0.0 for f in 
                                   [credit_risk] + market_features.tolist() + 
                                   operational_features.tolist() + liquidity_features.tolist()])
        
        confidence = (feature_stability * 0.6 + data_completeness * 0.4)
        return max(0.0, min(1.0, confidence))
    
    def save_models(self, filepath: str):
        """保存模型"""
        model_data = {
            'models': {name: model.state_dict() for name, model in self.models.items()},
            'scaler': self.scaler,
            'feature_importance': self.feature_importance
        }
        torch.save(model_data, filepath)
        self.logger.info(f"模型已保存到: {filepath}")
    
    def load_models(self, filepath: str):
        """加载模型"""
        model_data = torch.load(filepath, map_location=self.device)
        
        # 重新创建模型结构
        self.models['credit'] = self.create_credit_risk_model().to(self.device)
        self.models['credit'].load_state_dict(model_data['models']['credit'])
        
        self.scaler = model_data['scaler']
        self.feature_importance = model_data['feature_importance']
        
        self.logger.info(f"模型已从 {filepath} 加载")
