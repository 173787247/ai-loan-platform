"""
AI模型管理服务

@author AI Loan Platform Team
@version 1.0.0
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import os
from loguru import logger
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
# import seaborn as sns  # 暂时注释掉，避免依赖问题

class AIModelManager:
    """AI模型管理服务类"""
    
    def __init__(self):
        self.logger = logger
        self.models = {}
        self.model_metrics = {}
        self.training_history = {}
        self.model_configs = {}
        self._initialize_models()
        
    def _initialize_models(self):
        """初始化AI模型"""
        try:
            # 加载预训练模型
            self._load_pretrained_models()
            
            # 初始化模型配置
            self._setup_model_configs()
            
            self.logger.info("AI模型初始化完成")
        except Exception as e:
            self.logger.error(f"AI模型初始化失败: {str(e)}")
            raise
    
    def _load_pretrained_models(self):
        """加载预训练模型"""
        # 风险预测模型
        self.models['risk_prediction'] = self._create_risk_prediction_model()
        
        # 信用评分模型
        self.models['credit_scoring'] = self._create_credit_scoring_model()
        
        # 市场分析模型
        self.models['market_analysis'] = self._create_market_analysis_model()
        
        # 推荐系统模型
        self.models['recommendation'] = self._create_recommendation_model()
        
        # 异常检测模型
        self.models['anomaly_detection'] = self._create_anomaly_detection_model()
    
    def _create_risk_prediction_model(self) -> nn.Module:
        """创建风险预测模型"""
        class RiskPredictionModel(nn.Module):
            def __init__(self, input_size=20, hidden_size=128, num_classes=5):
                super().__init__()
                self.fc1 = nn.Linear(input_size, hidden_size)
                self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
                self.fc3 = nn.Linear(hidden_size // 2, hidden_size // 4)
                self.fc4 = nn.Linear(hidden_size // 4, num_classes)
                self.dropout = nn.Dropout(0.3)
                self.relu = nn.ReLU()
                self.softmax = nn.Softmax(dim=1)
                
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.dropout(x)
                x = self.relu(self.fc2(x))
                x = self.dropout(x)
                x = self.relu(self.fc3(x))
                x = self.fc4(x)
                return self.softmax(x)
        
        return RiskPredictionModel()
    
    def _create_credit_scoring_model(self) -> nn.Module:
        """创建信用评分模型"""
        class CreditScoringModel(nn.Module):
            def __init__(self, input_size=15, hidden_size=64):
                super().__init__()
                self.fc1 = nn.Linear(input_size, hidden_size)
                self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
                self.fc3 = nn.Linear(hidden_size // 2, 1)
                self.dropout = nn.Dropout(0.2)
                self.relu = nn.ReLU()
                self.sigmoid = nn.Sigmoid()
                
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.dropout(x)
                x = self.relu(self.fc2(x))
                x = self.sigmoid(self.fc3(x))
                return x
        
        return CreditScoringModel()
    
    def _create_market_analysis_model(self) -> nn.Module:
        """创建市场分析模型"""
        class MarketAnalysisModel(nn.Module):
            def __init__(self, input_size=10, hidden_size=32):
                super().__init__()
                self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
                self.fc1 = nn.Linear(hidden_size, 16)
                self.fc2 = nn.Linear(16, 3)  # 上涨、下跌、平稳
                self.relu = nn.ReLU()
                self.softmax = nn.Softmax(dim=1)
                
            def forward(self, x):
                lstm_out, _ = self.lstm(x)
                x = self.relu(self.fc1(lstm_out[:, -1, :]))
                x = self.softmax(self.fc2(x))
                return x
        
        return MarketAnalysisModel()
    
    def _create_recommendation_model(self) -> nn.Module:
        """创建推荐系统模型"""
        class RecommendationModel(nn.Module):
            def __init__(self, user_size=1000, item_size=100, embedding_size=50):
                super().__init__()
                self.user_embedding = nn.Embedding(user_size, embedding_size)
                self.item_embedding = nn.Embedding(item_size, embedding_size)
                self.fc1 = nn.Linear(embedding_size * 2, 64)
                self.fc2 = nn.Linear(64, 32)
                self.fc3 = nn.Linear(32, 1)
                self.relu = nn.ReLU()
                self.sigmoid = nn.Sigmoid()
                
            def forward(self, user_ids, item_ids):
                user_emb = self.user_embedding(user_ids)
                item_emb = self.item_embedding(item_ids)
                x = torch.cat([user_emb, item_emb], dim=1)
                x = self.relu(self.fc1(x))
                x = self.relu(self.fc2(x))
                x = self.sigmoid(self.fc3(x))
                return x
        
        return RecommendationModel()
    
    def _create_anomaly_detection_model(self) -> nn.Module:
        """创建异常检测模型"""
        class AnomalyDetectionModel(nn.Module):
            def __init__(self, input_size=12, hidden_size=32):
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Linear(input_size, hidden_size),
                    nn.ReLU(),
                    nn.Linear(hidden_size, hidden_size // 2),
                    nn.ReLU(),
                    nn.Linear(hidden_size // 2, hidden_size // 4)
                )
                self.decoder = nn.Sequential(
                    nn.Linear(hidden_size // 4, hidden_size // 2),
                    nn.ReLU(),
                    nn.Linear(hidden_size // 2, hidden_size),
                    nn.ReLU(),
                    nn.Linear(hidden_size, input_size)
                )
                
            def forward(self, x):
                encoded = self.encoder(x)
                decoded = self.decoder(encoded)
                return decoded, encoded
        
        return AnomalyDetectionModel()
    
    def _setup_model_configs(self):
        """设置模型配置"""
        self.model_configs = {
            'risk_prediction': {
                'input_size': 20,
                'hidden_size': 128,
                'num_classes': 5,
                'learning_rate': 0.001,
                'batch_size': 32,
                'epochs': 100
            },
            'credit_scoring': {
                'input_size': 15,
                'hidden_size': 64,
                'learning_rate': 0.001,
                'batch_size': 64,
                'epochs': 50
            },
            'market_analysis': {
                'input_size': 10,
                'hidden_size': 32,
                'learning_rate': 0.001,
                'batch_size': 16,
                'epochs': 30
            },
            'recommendation': {
                'user_size': 1000,
                'item_size': 100,
                'embedding_size': 50,
                'learning_rate': 0.01,
                'batch_size': 128,
                'epochs': 20
            },
            'anomaly_detection': {
                'input_size': 12,
                'hidden_size': 32,
                'learning_rate': 0.001,
                'batch_size': 32,
                'epochs': 50
            }
        }
    
    def train_model(self, model_name: str, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """训练模型"""
        try:
            if model_name not in self.models:
                raise ValueError(f"模型 {model_name} 不存在")
            
            self.logger.info(f"开始训练模型: {model_name}")
            
            # 准备训练数据
            X_train = training_data['X_train']
            y_train = training_data['y_train']
            X_val = training_data.get('X_val', None)
            y_val = training_data.get('y_val', None)
            
            # 转换为PyTorch张量
            X_train_tensor = torch.FloatTensor(X_train)
            y_train_tensor = torch.LongTensor(y_train) if model_name != 'credit_scoring' else torch.FloatTensor(y_train)
            
            if X_val is not None:
                X_val_tensor = torch.FloatTensor(X_val)
                y_val_tensor = torch.LongTensor(y_val) if model_name != 'credit_scoring' else torch.FloatTensor(y_val)
            
            # 获取模型和配置
            model = self.models[model_name]
            config = self.model_configs[model_name]
            
            # 设置优化器和损失函数
            optimizer = torch.optim.Adam(model.parameters(), lr=config['learning_rate'])
            
            if model_name == 'credit_scoring':
                criterion = nn.BCELoss()
            else:
                criterion = nn.CrossEntropyLoss()
            
            # 训练循环
            training_losses = []
            validation_losses = []
            training_accuracies = []
            validation_accuracies = []
            
            for epoch in range(config['epochs']):
                # 训练阶段
                model.train()
                total_loss = 0
                correct = 0
                total = 0
                
                # 批量训练
                for i in range(0, len(X_train_tensor), config['batch_size']):
                    batch_X = X_train_tensor[i:i+config['batch_size']]
                    batch_y = y_train_tensor[i:i+config['batch_size']]
                    
                    optimizer.zero_grad()
                    outputs = model(batch_X)
                    
                    if model_name == 'credit_scoring':
                        loss = criterion(outputs.squeeze(), batch_y)
                    else:
                        loss = criterion(outputs, batch_y)
                    
                    loss.backward()
                    optimizer.step()
                    
                    total_loss += loss.item()
                    
                    # 计算准确率
                    if model_name == 'credit_scoring':
                        predicted = (outputs.squeeze() > 0.5).float()
                        correct += (predicted == batch_y).sum().item()
                    else:
                        _, predicted = torch.max(outputs.data, 1)
                        correct += (predicted == batch_y).sum().item()
                    
                    total += batch_y.size(0)
                
                avg_loss = total_loss / (len(X_train_tensor) // config['batch_size'])
                accuracy = correct / total
                
                training_losses.append(avg_loss)
                training_accuracies.append(accuracy)
                
                # 验证阶段
                if X_val is not None:
                    model.eval()
                    with torch.no_grad():
                        val_outputs = model(X_val_tensor)
                        if model_name == 'credit_scoring':
                            val_loss = criterion(val_outputs.squeeze(), y_val_tensor)
                            val_predicted = (val_outputs.squeeze() > 0.5).float()
                            val_correct = (val_predicted == y_val_tensor).sum().item()
                        else:
                            val_loss = criterion(val_outputs, y_val_tensor)
                            _, val_predicted = torch.max(val_outputs.data, 1)
                            val_correct = (val_predicted == y_val_tensor).sum().item()
                        
                        val_accuracy = val_correct / len(y_val_tensor)
                        validation_losses.append(val_loss.item())
                        validation_accuracies.append(val_accuracy)
                
                # 记录训练进度
                if epoch % 10 == 0:
                    self.logger.info(f"Epoch {epoch}/{config['epochs']}, Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")
            
            # 保存训练历史
            self.training_history[model_name] = {
                'training_losses': training_losses,
                'validation_losses': validation_losses,
                'training_accuracies': training_accuracies,
                'validation_accuracies': validation_accuracies,
                'final_accuracy': training_accuracies[-1],
                'training_time': datetime.now().isoformat()
            }
            
            # 计算最终指标
            final_metrics = self._calculate_model_metrics(model_name, X_train_tensor, y_train_tensor)
            self.model_metrics[model_name] = final_metrics
            
            # 保存模型
            self._save_model(model_name)
            
            result = {
                'success': True,
                'model_name': model_name,
                'final_accuracy': training_accuracies[-1],
                'final_loss': training_losses[-1],
                'training_epochs': config['epochs'],
                'metrics': final_metrics,
                'training_history': self.training_history[model_name]
            }
            
            self.logger.info(f"模型 {model_name} 训练完成，最终准确率: {training_accuracies[-1]:.4f}")
            return result
            
        except Exception as e:
            self.logger.error(f"模型训练失败: {model_name}, 错误: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model_name': model_name
            }
    
    def predict(self, model_name: str, input_data: np.ndarray) -> Dict[str, Any]:
        """模型预测"""
        try:
            if model_name not in self.models:
                raise ValueError(f"模型 {model_name} 不存在")
            
            model = self.models[model_name]
            model.eval()
            
            # 转换为张量
            input_tensor = torch.FloatTensor(input_data)
            if len(input_tensor.shape) == 1:
                input_tensor = input_tensor.unsqueeze(0)
            
            with torch.no_grad():
                outputs = model(input_tensor)
                
                if model_name == 'credit_scoring':
                    prediction = outputs.squeeze().item()
                    confidence = abs(prediction - 0.5) * 2
                else:
                    probabilities = torch.softmax(outputs, dim=1)
                    prediction = torch.argmax(probabilities, dim=1).item()
                    confidence = torch.max(probabilities, dim=1)[0].item()
            
            return {
                'success': True,
                'prediction': prediction,
                'confidence': confidence,
                'probabilities': probabilities.tolist() if model_name != 'credit_scoring' else [prediction, 1-prediction]
            }
            
        except Exception as e:
            self.logger.error(f"模型预测失败: {model_name}, 错误: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def evaluate_model(self, model_name: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估模型"""
        try:
            if model_name not in self.models:
                raise ValueError(f"模型 {model_name} 不存在")
            
            model = self.models[model_name]
            model.eval()
            
            X_test = test_data['X_test']
            y_test = test_data['y_test']
            
            X_test_tensor = torch.FloatTensor(X_test)
            y_test_tensor = torch.LongTensor(y_test) if model_name != 'credit_scoring' else torch.FloatTensor(y_test)
            
            with torch.no_grad():
                outputs = model(X_test_tensor)
                
                if model_name == 'credit_scoring':
                    predictions = (outputs.squeeze() > 0.5).float()
                    accuracy = accuracy_score(y_test, predictions.numpy())
                    precision = precision_score(y_test, predictions.numpy())
                    recall = recall_score(y_test, predictions.numpy())
                    f1 = f1_score(y_test, predictions.numpy())
                else:
                    _, predictions = torch.max(outputs, 1)
                    accuracy = accuracy_score(y_test, predictions.numpy())
                    precision = precision_score(y_test, predictions.numpy(), average='weighted')
                    recall = recall_score(y_test, predictions.numpy(), average='weighted')
                    f1 = f1_score(y_test, predictions.numpy(), average='weighted')
            
            metrics = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }
            
            self.model_metrics[model_name] = metrics
            
            return {
                'success': True,
                'model_name': model_name,
                'metrics': metrics
            }
            
        except Exception as e:
            self.logger.error(f"模型评估失败: {model_name}, 错误: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_model_metrics(self, model_name: str, X: torch.Tensor, y: torch.Tensor) -> Dict[str, float]:
        """计算模型指标"""
        model = self.models[model_name]
        model.eval()
        
        with torch.no_grad():
            outputs = model(X)
            
            if model_name == 'credit_scoring':
                predictions = (outputs.squeeze() > 0.5).float()
                accuracy = (predictions == y).float().mean().item()
            else:
                _, predictions = torch.max(outputs, 1)
                accuracy = (predictions == y).float().mean().item()
        
        return {
            'accuracy': accuracy,
            'model_size': sum(p.numel() for p in model.parameters()),
            'trainable_parameters': sum(p.numel() for p in model.parameters() if p.requires_grad)
        }
    
    def _save_model(self, model_name: str):
        """保存模型"""
        try:
            os.makedirs('models', exist_ok=True)
            model_path = f'models/{model_name}_model.pth'
            torch.save(self.models[model_name].state_dict(), model_path)
            self.logger.info(f"模型 {model_name} 已保存到 {model_path}")
        except Exception as e:
            self.logger.error(f"保存模型失败: {model_name}, 错误: {str(e)}")
    
    def load_model(self, model_name: str, model_path: str):
        """加载模型"""
        try:
            if model_name not in self.models:
                raise ValueError(f"模型 {model_name} 不存在")
            
            self.models[model_name].load_state_dict(torch.load(model_path))
            self.logger.info(f"模型 {model_name} 已从 {model_path} 加载")
        except Exception as e:
            self.logger.error(f"加载模型失败: {model_name}, 错误: {str(e)}")
    
    def get_model_status(self) -> Dict[str, Any]:
        """获取模型状态"""
        status = {}
        for model_name, model in self.models.items():
            status[model_name] = {
                'loaded': True,
                'parameters': sum(p.numel() for p in model.parameters()),
                'trainable_parameters': sum(p.numel() for p in model.parameters() if p.requires_grad),
                'metrics': self.model_metrics.get(model_name, {}),
                'training_history': self.training_history.get(model_name, {})
            }
        
        return status
    
    def get_training_insights(self, model_name: str) -> Dict[str, Any]:
        """获取训练洞察"""
        if model_name not in self.training_history:
            return {'error': '模型训练历史不存在'}
        
        history = self.training_history[model_name]
        
        # 分析训练趋势
        training_losses = history['training_losses']
        validation_losses = history.get('validation_losses', [])
        
        # 计算训练稳定性
        loss_variance = np.var(training_losses[-10:]) if len(training_losses) >= 10 else np.var(training_losses)
        
        # 检测过拟合
        overfitting_detected = False
        if validation_losses:
            if len(validation_losses) >= 10:
                recent_train_loss = np.mean(training_losses[-10:])
                recent_val_loss = np.mean(validation_losses[-10:])
                if recent_val_loss > recent_train_loss * 1.2:
                    overfitting_detected = True
        
        # 生成建议
        recommendations = []
        if overfitting_detected:
            recommendations.append("检测到过拟合，建议增加正则化或减少模型复杂度")
        
        if loss_variance > 0.01:
            recommendations.append("训练不稳定，建议降低学习率")
        
        if history['final_accuracy'] < 0.8:
            recommendations.append("模型准确率较低，建议增加训练数据或调整模型架构")
        
        return {
            'model_name': model_name,
            'training_stability': 'stable' if loss_variance < 0.01 else 'unstable',
            'overfitting_detected': overfitting_detected,
            'final_performance': {
                'accuracy': history['final_accuracy'],
                'loss': training_losses[-1]
            },
            'recommendations': recommendations,
            'training_curve': {
                'epochs': list(range(len(training_losses))),
                'training_losses': training_losses,
                'validation_losses': validation_losses
            }
        }
    
    def generate_model_report(self, model_name: str) -> Dict[str, Any]:
        """生成模型报告"""
        if model_name not in self.models:
            return {'error': '模型不存在'}
        
        model = self.models[model_name]
        config = self.model_configs[model_name]
        metrics = self.model_metrics.get(model_name, {})
        history = self.training_history.get(model_name, {})
        
        report = {
            'model_name': model_name,
            'model_type': type(model).__name__,
            'configuration': config,
            'performance_metrics': metrics,
            'training_summary': {
                'total_epochs': config['epochs'],
                'final_accuracy': history.get('final_accuracy', 0),
                'training_time': history.get('training_time', ''),
                'model_size': sum(p.numel() for p in model.parameters())
            },
            'insights': self.get_training_insights(model_name),
            'recommendations': self._get_model_recommendations(model_name, metrics)
        }
        
        return report
    
    def _get_model_recommendations(self, model_name: str, metrics: Dict[str, Any]) -> List[str]:
        """获取模型建议"""
        recommendations = []
        
        accuracy = metrics.get('accuracy', 0)
        
        if accuracy < 0.7:
            recommendations.append("模型准确率较低，建议增加训练数据或调整超参数")
        elif accuracy < 0.85:
            recommendations.append("模型准确率中等，可以考虑数据增强或模型集成")
        else:
            recommendations.append("模型性能良好，可以部署到生产环境")
        
        return recommendations
