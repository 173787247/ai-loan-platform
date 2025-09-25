import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import aiService from '../services/AIService';
import './AIEnhancements.css';

const AIEnhancements = () => {
  const [aiModels, setAiModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [modelPerformance, setModelPerformance] = useState({});
  const [trainingData, setTrainingData] = useState([]);
  const [isTraining, setIsTraining] = useState(false);
  const [predictionResults, setPredictionResults] = useState([]);
  const [modelTraining, setModelTraining] = useState({
    isTraining: false,
    progress: 0,
    currentEpoch: 0,
    totalEpochs: 100,
    loss: 0,
    accuracy: 0
  });
  const [aiInsights, setAiInsights] = useState([]);
  const [modelComparison, setModelComparison] = useState([]);
  const [featureImportance, setFeatureImportance] = useState([]);
  const [modelDeployment, setModelDeployment] = useState({
    isDeploying: false,
    deploymentStatus: 'idle',
    deploymentProgress: 0
  });
  const [aiChatbot, setAiChatbot] = useState({
    isEnabled: true,
    responseTime: 0,
    satisfaction: 0,
    totalQueries: 0
  });
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadAIModels();
    loadModelPerformance();
    loadTrainingData();
    loadAIServiceStatus();
  }, []);

  const loadAIModels = async () => {
    try {
      // 首先尝试从API获取模型状态
      try {
        const response = await aiService.getModelStatus();
        if (response.success && response.data) {
          const models = Object.entries(response.data).map(([name, status], index) => ({
            id: `${name}-v1`,
            name: getModelDisplayName(name),
            type: name,
            accuracy: (status.metrics?.accuracy || 0) * 100,
            status: status.loaded ? 'active' : 'inactive',
            lastUpdated: status.training_history?.training_time?.split('T')[0] || '未知',
            description: getModelDescription(name),
            parameters: status.parameters || 0,
            trainableParameters: status.trainable_parameters || 0
          }));
          setAiModels(models);
          return;
        }
      } catch (apiError) {
        console.warn('API获取模型状态失败，使用模拟数据:', apiError);
      }

      // 如果API失败，使用模拟数据
      const models = [
        {
          id: 'risk-assessment-v2',
          name: '风险评估模型 v2.0',
          type: 'risk_assessment',
          accuracy: 94.2,
          status: 'active',
          lastUpdated: '2025-09-20',
          description: '基于深度学习的风险评估模型，支持多维度风险分析',
          parameters: 50000,
          trainableParameters: 45000
        },
        {
          id: 'credit-scoring-v1',
          name: '信用评分模型 v1.0',
          type: 'credit_scoring',
          accuracy: 91.5,
          status: 'active',
          lastUpdated: '2025-09-18',
          description: '传统机器学习模型，用于快速信用评分',
          parameters: 30000,
          trainableParameters: 28000
        },
        {
          id: 'fraud-detection-v3',
          name: '欺诈检测模型 v3.0',
          type: 'fraud_detection',
          accuracy: 96.8,
          status: 'active',
          lastUpdated: '2025-09-21',
          description: '实时欺诈检测，支持异常行为识别',
          parameters: 40000,
          trainableParameters: 38000
        },
        {
          id: 'market-prediction-v1',
          name: '市场预测模型 v1.0',
          type: 'market_prediction',
          accuracy: 87.3,
          status: 'training',
          lastUpdated: '2025-09-19',
          description: '市场趋势预测，用于投资决策支持',
          parameters: 25000,
          trainableParameters: 23000
        }
      ];
      setAiModels(models);
    } catch (error) {
      showError('加载AI模型失败');
    }
  };

  const getModelDisplayName = (modelType) => {
    const nameMap = {
      'risk_prediction': '风险预测模型',
      'credit_scoring': '信用评分模型',
      'market_analysis': '市场分析模型',
      'recommendation': '推荐系统模型',
      'anomaly_detection': '异常检测模型'
    };
    return nameMap[modelType] || modelType;
  };

  const getModelDescription = (modelType) => {
    const descMap = {
      'risk_prediction': '基于深度学习的风险预测模型，支持多维度风险分析',
      'credit_scoring': '传统机器学习模型，用于快速信用评分',
      'market_analysis': '市场趋势分析模型，用于投资决策支持',
      'recommendation': '推荐系统模型，提供个性化推荐',
      'anomaly_detection': '异常检测模型，识别异常行为模式'
    };
    return descMap[modelType] || 'AI模型';
  };

  const loadModelPerformance = async () => {
    try {
      // 模拟性能数据
      const performance = {
        'risk-assessment-v2': {
          accuracy: 94.2,
          precision: 92.8,
          recall: 95.1,
          f1Score: 93.9,
          auc: 0.96,
          latency: 120,
          throughput: 1000
        },
        'credit-scoring-v1': {
          accuracy: 91.5,
          precision: 89.2,
          recall: 93.8,
          f1Score: 91.4,
          auc: 0.94,
          latency: 80,
          throughput: 1500
        },
        'fraud-detection-v3': {
          accuracy: 96.8,
          precision: 95.4,
          recall: 98.1,
          f1Score: 96.7,
          auc: 0.98,
          latency: 200,
          throughput: 800
        },
        'market-prediction-v1': {
          accuracy: 87.3,
          precision: 85.6,
          recall: 89.2,
          f1Score: 87.3,
          auc: 0.89,
          latency: 300,
          throughput: 500
        }
      };
      setModelPerformance(performance);
    } catch (error) {
      showError('加载模型性能数据失败');
    }
  };

  const loadTrainingData = async () => {
    try {
      // 模拟训练数据
      const data = [
        {
          id: 1,
          dataset: 'historical_loans_2024',
          size: '500K',
          quality: 'high',
          lastUsed: '2025-09-20',
          status: 'ready'
        },
        {
          id: 2,
          dataset: 'credit_scores_2024',
          size: '200K',
          quality: 'high',
          lastUsed: '2025-09-18',
          status: 'ready'
        },
        {
          id: 3,
          dataset: 'fraud_cases_2024',
          size: '50K',
          quality: 'medium',
          lastUsed: '2025-09-21',
          status: 'processing'
        },
        {
          id: 4,
          dataset: 'market_data_2024',
          size: '1M',
          quality: 'high',
          lastUsed: '2025-09-19',
          status: 'ready'
        }
      ];
      setTrainingData(data);
    } catch (error) {
      showError('加载训练数据失败');
    }
  };

  const loadAIServiceStatus = async () => {
    try {
      const response = await aiService.getAIStatus();
      if (response.success && response.data) {
        // 更新AI服务状态
        console.log('AI服务状态:', response.data);
      }
    } catch (error) {
      console.warn('获取AI服务状态失败:', error);
    }
  };

  const handleModelSelect = (modelId) => {
    setSelectedModel(modelId);
    showInfo(`已选择模型: ${aiModels.find(m => m.id === modelId)?.name}`);
  };

  const startTraining = async (modelId) => {
    setIsTraining(true);
    try {
      const model = aiModels.find(m => m.id === modelId);
      if (!model) {
        throw new Error('模型不存在');
      }

      showInfo('开始训练模型...');
      
      // 生成模拟训练数据
      const trainingData = aiService.generateMockTrainingData(model.type, 1000);
      
      // 调用API训练模型
      const response = await aiService.trainModel(model.type, trainingData);
      
      if (response.success) {
        // 更新模型状态
        setAiModels(prev => prev.map(m => 
          m.id === modelId 
            ? { 
                ...m, 
                status: 'active', 
                lastUpdated: new Date().toISOString().split('T')[0],
                accuracy: (response.data.final_accuracy || 0) * 100
              }
            : m
        ));
        
        showSuccess(`模型训练完成！准确率: ${((response.data.final_accuracy || 0) * 100).toFixed(1)}%`);
      } else {
        throw new Error(response.error || '训练失败');
      }
    } catch (error) {
      console.error('模型训练失败:', error);
      showError(`模型训练失败: ${error.message}`);
    } finally {
      setIsTraining(false);
    }
  };

  const runPrediction = async (modelId) => {
    try {
      const model = aiModels.find(m => m.id === modelId);
      if (!model) {
        throw new Error('模型不存在');
      }

      showInfo('正在运行预测...');
      
      // 生成模拟输入数据
      const inputData = aiService.generateMockTrainingData(model.type, 3);
      
      // 调用API进行预测
      const results = [];
      for (let i = 0; i < 3; i++) {
        const response = await aiService.predictModel(model.type, inputData.X_train[i]);
        if (response.success) {
          results.push({
            id: i + 1,
            input: `测试数据 ${i + 1}`,
            prediction: response.data.prediction,
            confidence: response.data.confidence,
            timestamp: new Date().toLocaleTimeString()
          });
        }
      }
      
      setPredictionResults(results);
      showSuccess('预测完成！');
    } catch (error) {
      console.error('预测失败:', error);
      showError(`预测失败: ${error.message}`);
    }
  };

  const getModelTypeIcon = (type) => {
    switch (type) {
      case 'risk_assessment': return '🎯';
      case 'credit_scoring': return '📊';
      case 'fraud_detection': return '🛡️';
      case 'market_prediction': return '📈';
      default: return '🤖';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#28a745';
      case 'training': return '#ffc107';
      case 'inactive': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const getQualityColor = (quality) => {
    switch (quality) {
      case 'high': return '#28a745';
      case 'medium': return '#ffc107';
      case 'low': return '#dc3545';
      default: return '#6c757d';
    }
  };

  return (
    <div className="ai-enhancements">
      <div className="ai-header">
        <h1>AI功能增强中心</h1>
        <p>管理和优化AI模型，提升智能决策能力</p>
      </div>

      <div className="ai-content">
        {/* AI模型管理 */}
        <div className="models-section">
          <div className="section-header">
            <h2>AI模型管理</h2>
            <button className="add-model-btn">
              <span className="btn-icon">➕</span>
              添加新模型
            </button>
          </div>
          
          <div className="models-grid">
            {aiModels.map(model => (
              <div key={model.id} className={`model-card ${model.status}`}>
                <div className="model-header">
                  <div className="model-icon">{getModelTypeIcon(model.type)}</div>
                  <div className="model-info">
                    <h3>{model.name}</h3>
                    <p className="model-description">{model.description}</p>
                  </div>
                  <div className="model-status">
                    <span 
                      className="status-badge"
                      style={{ color: getStatusColor(model.status) }}
                    >
                      {model.status === 'active' ? '运行中' : 
                       model.status === 'training' ? '训练中' : '已停止'}
                    </span>
                  </div>
                </div>
                
                <div className="model-metrics">
                  <div className="metric">
                    <span className="metric-label">准确率</span>
                    <span className="metric-value">{model.accuracy}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">最后更新</span>
                    <span className="metric-value">{model.lastUpdated}</span>
                  </div>
                </div>
                
                <div className="model-actions">
                  <button 
                    className="action-btn primary"
                    onClick={() => handleModelSelect(model.id)}
                  >
                    选择
                  </button>
                  <button 
                    className="action-btn secondary"
                    onClick={() => runPrediction(model.id)}
                  >
                    预测
                  </button>
                  <button 
                    className="action-btn warning"
                    onClick={() => startTraining(model.id)}
                    disabled={isTraining}
                  >
                    {isTraining ? '训练中...' : '训练'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 模型性能监控 */}
        {selectedModel && (
          <div className="performance-section">
            <h2>模型性能监控</h2>
            <div className="performance-grid">
              {Object.entries(modelPerformance[selectedModel] || {}).map(([key, value]) => (
                <div key={key} className="performance-card">
                  <div className="performance-label">
                    {key === 'accuracy' ? '准确率' :
                     key === 'precision' ? '精确率' :
                     key === 'recall' ? '召回率' :
                     key === 'f1Score' ? 'F1分数' :
                     key === 'auc' ? 'AUC' :
                     key === 'latency' ? '延迟(ms)' :
                     key === 'throughput' ? '吞吐量/小时' : key}
                  </div>
                  <div className="performance-value">
                    {typeof value === 'number' ? 
                      (key === 'auc' ? value.toFixed(3) : 
                       key === 'latency' ? value : 
                       key === 'throughput' ? value.toLocaleString() : 
                       value.toFixed(1)) : value}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 训练数据管理 */}
        <div className="training-data-section">
          <h2>训练数据管理</h2>
          <div className="data-table">
            <div className="table-header">
              <div className="table-cell">数据集</div>
              <div className="table-cell">大小</div>
              <div className="table-cell">质量</div>
              <div className="table-cell">最后使用</div>
              <div className="table-cell">状态</div>
              <div className="table-cell">操作</div>
            </div>
            {trainingData.map(data => (
              <div key={data.id} className="table-row">
                <div className="table-cell">
                  <span className="data-name">{data.dataset}</span>
                </div>
                <div className="table-cell">{data.size}</div>
                <div className="table-cell">
                  <span 
                    className="quality-badge"
                    style={{ color: getQualityColor(data.quality) }}
                  >
                    {data.quality === 'high' ? '高' :
                     data.quality === 'medium' ? '中' : '低'}
                  </span>
                </div>
                <div className="table-cell">{data.lastUsed}</div>
                <div className="table-cell">
                  <span 
                    className="status-badge"
                    style={{ color: getStatusColor(data.status) }}
                  >
                    {data.status === 'ready' ? '就绪' :
                     data.status === 'processing' ? '处理中' : '错误'}
                  </span>
                </div>
                <div className="table-cell">
                  <button className="action-btn small">使用</button>
                  <button className="action-btn small secondary">预览</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 预测结果 */}
        {predictionResults.length > 0 && (
          <div className="predictions-section">
            <h2>预测结果</h2>
            <div className="predictions-list">
              {predictionResults.map(result => (
                <div key={result.id} className="prediction-item">
                  <div className="prediction-input">{result.input}</div>
                  <div className="prediction-result">
                    <span className="prediction-label">预测:</span>
                    <span className="prediction-value">{result.prediction}</span>
                  </div>
                  <div className="prediction-confidence">
                    <span className="confidence-label">置信度:</span>
                    <span className="confidence-value">
                      {(result.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="prediction-time">{result.timestamp}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI配置 */}
        <div className="ai-config-section">
          <h2>AI配置</h2>
          <div className="config-grid">
            <div className="config-card">
              <h3>模型设置</h3>
              <div className="config-item">
                <label>默认模型</label>
                <select>
                  <option>风险评估模型 v2.0</option>
                  <option>信用评分模型 v1.0</option>
                  <option>欺诈检测模型 v3.0</option>
                </select>
              </div>
              <div className="config-item">
                <label>置信度阈值</label>
                <input type="range" min="0.5" max="1" step="0.05" defaultValue="0.8" />
                <span className="threshold-value">0.8</span>
              </div>
            </div>
            
            <div className="config-card">
              <h3>性能设置</h3>
              <div className="config-item">
                <label>批处理大小</label>
                <input type="number" defaultValue="32" min="1" max="128" />
              </div>
              <div className="config-item">
                <label>最大并发数</label>
                <input type="number" defaultValue="10" min="1" max="50" />
              </div>
            </div>
            
            <div className="config-card">
              <h3>监控设置</h3>
              <div className="config-item">
                <label>
                  <input type="checkbox" defaultChecked />
                  启用性能监控
                </label>
              </div>
              <div className="config-item">
                <label>
                  <input type="checkbox" defaultChecked />
                  启用异常告警
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AI模型训练监控 */}
      <div className="ai-section">
        <h2>🤖 AI模型训练监控</h2>
        <div className="training-monitor">
          <div className="training-status">
            <h3>训练状态</h3>
            <div className="status-indicator">
              <div className={`status-dot ${modelTraining.isTraining ? 'training' : 'idle'}`}></div>
              <span>{modelTraining.isTraining ? '训练中' : '空闲'}</span>
            </div>
          </div>
          
          {modelTraining.isTraining && (
            <div className="training-progress">
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${modelTraining.progress}%` }}
                ></div>
              </div>
              <div className="progress-info">
                <span>进度: {modelTraining.progress}%</span>
                <span>轮次: {modelTraining.currentEpoch}/{modelTraining.totalEpochs}</span>
                <span>损失: {modelTraining.loss.toFixed(4)}</span>
                <span>准确率: {(modelTraining.accuracy * 100).toFixed(2)}%</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* AI洞察分析 */}
      <div className="ai-section">
        <h2>💡 AI洞察分析</h2>
        <div className="insights-grid">
          <div className="insight-card">
            <h3>模型性能趋势</h3>
            <div className="trend-chart">
              <div className="chart-placeholder">
                <p>准确率持续提升，建议继续使用当前模型</p>
                <div className="trend-indicator up">↗ +2.3%</div>
              </div>
            </div>
          </div>
          
          <div className="insight-card">
            <h3>特征重要性</h3>
            <div className="feature-importance">
              <div className="feature-item">
                <span className="feature-name">信用历史</span>
                <div className="importance-bar">
                  <div className="importance-fill" style={{ width: '85%' }}></div>
                </div>
                <span className="importance-value">85%</span>
              </div>
              <div className="feature-item">
                <span className="feature-name">收入水平</span>
                <div className="importance-bar">
                  <div className="importance-fill" style={{ width: '72%' }}></div>
                </div>
                <span className="importance-value">72%</span>
              </div>
              <div className="feature-item">
                <span className="feature-name">债务比率</span>
                <div className="importance-bar">
                  <div className="importance-fill" style={{ width: '68%' }}></div>
                </div>
                <span className="importance-value">68%</span>
              </div>
            </div>
          </div>
          
          <div className="insight-card">
            <h3>模型比较</h3>
            <div className="model-comparison">
              <div className="comparison-item">
                <span className="model-name">风险评估 v2.0</span>
                <div className="comparison-metrics">
                  <span>准确率: 94.2%</span>
                  <span>速度: 120ms</span>
                  <span>内存: 2.1GB</span>
                </div>
              </div>
              <div className="comparison-item">
                <span className="model-name">信用评分 v1.0</span>
                <div className="comparison-metrics">
                  <span>准确率: 91.5%</span>
                  <span>速度: 80ms</span>
                  <span>内存: 1.2GB</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AI聊天机器人管理 */}
      <div className="ai-section">
        <h2>💬 AI聊天机器人管理</h2>
        <div className="chatbot-management">
          <div className="chatbot-status">
            <div className="status-card">
              <h3>运行状态</h3>
              <div className="status-indicator">
                <div className={`status-dot ${aiChatbot.isEnabled ? 'active' : 'inactive'}`}></div>
                <span>{aiChatbot.isEnabled ? '运行中' : '已停止'}</span>
              </div>
            </div>
            
            <div className="status-card">
              <h3>性能指标</h3>
              <div className="metrics-grid">
                <div className="metric">
                  <span className="metric-label">平均响应时间</span>
                  <span className="metric-value">{aiChatbot.responseTime}ms</span>
                </div>
                <div className="metric">
                  <span className="metric-label">用户满意度</span>
                  <span className="metric-value">{aiChatbot.satisfaction}%</span>
                </div>
                <div className="metric">
                  <span className="metric-label">总查询数</span>
                  <span className="metric-value">{aiChatbot.totalQueries.toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="chatbot-controls">
            <button 
              className={`btn ${aiChatbot.isEnabled ? 'btn-danger' : 'btn-success'}`}
              onClick={() => setAiChatbot(prev => ({ ...prev, isEnabled: !prev.isEnabled }))}
            >
              {aiChatbot.isEnabled ? '停止机器人' : '启动机器人'}
            </button>
            <button className="btn btn-outline">配置对话流程</button>
            <button className="btn btn-outline">查看对话日志</button>
            <button className="btn btn-outline">训练新对话</button>
          </div>
        </div>
      </div>

      {/* 模型部署管理 */}
      <div className="ai-section">
        <h2>🚀 模型部署管理</h2>
        <div className="deployment-management">
          <div className="deployment-status">
            <h3>部署状态</h3>
            <div className="status-indicator">
              <div className={`status-dot ${modelDeployment.deploymentStatus}`}></div>
              <span>
                {modelDeployment.deploymentStatus === 'idle' ? '空闲' :
                 modelDeployment.deploymentStatus === 'deploying' ? '部署中' :
                 modelDeployment.deploymentStatus === 'deployed' ? '已部署' : '部署失败'}
              </span>
            </div>
            
            {modelDeployment.isDeploying && (
              <div className="deployment-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${modelDeployment.deploymentProgress}%` }}
                  ></div>
                </div>
                <span>部署进度: {modelDeployment.deploymentProgress}%</span>
              </div>
            )}
          </div>
          
          <div className="deployment-actions">
            <button 
              className="btn btn-primary"
              onClick={() => {
                setModelDeployment(prev => ({ 
                  ...prev, 
                  isDeploying: true, 
                  deploymentStatus: 'deploying',
                  deploymentProgress: 0
                }));
                
                // 模拟部署过程
                const interval = setInterval(() => {
                  setModelDeployment(prev => {
                    const newProgress = prev.deploymentProgress + 10;
                    if (newProgress >= 100) {
                      clearInterval(interval);
                      return {
                        ...prev,
                        isDeploying: false,
                        deploymentStatus: 'deployed',
                        deploymentProgress: 100
                      };
                    }
                    return { ...prev, deploymentProgress: newProgress };
                  });
                }, 500);
              }}
              disabled={modelDeployment.isDeploying}
            >
              {modelDeployment.isDeploying ? '部署中...' : '部署模型'}
            </button>
            <button className="btn btn-outline">回滚版本</button>
            <button className="btn btn-outline">查看部署日志</button>
          </div>
        </div>
      </div>

      {/* AI实验管理 */}
      <div className="ai-section">
        <h2>🧪 AI实验管理</h2>
        <div className="experiment-management">
          <div className="experiment-list">
            <h3>进行中的实验</h3>
            <div className="experiment-cards">
              <div className="experiment-card">
                <h4>新风险评估算法</h4>
                <p>测试基于Transformer的风险评估模型</p>
                <div className="experiment-metrics">
                  <span>准确率: 95.2%</span>
                  <span>运行时间: 3天</span>
                  <span>状态: 进行中</span>
                </div>
                <div className="experiment-actions">
                  <button className="btn btn-sm btn-outline">查看详情</button>
                  <button className="btn btn-sm btn-danger">停止实验</button>
                </div>
              </div>
              
              <div className="experiment-card">
                <h4>多模态特征融合</h4>
                <p>结合文本和数值特征进行风险评估</p>
                <div className="experiment-metrics">
                  <span>准确率: 93.8%</span>
                  <span>运行时间: 1天</span>
                  <span>状态: 已完成</span>
                </div>
                <div className="experiment-actions">
                  <button className="btn btn-sm btn-outline">查看结果</button>
                  <button className="btn btn-sm btn-primary">应用到生产</button>
                </div>
              </div>
            </div>
          </div>
          
          <div className="experiment-creation">
            <h3>创建新实验</h3>
            <div className="creation-form">
              <div className="form-group">
                <label>实验名称</label>
                <input type="text" placeholder="输入实验名称" />
              </div>
              <div className="form-group">
                <label>实验类型</label>
                <select>
                  <option>风险评估</option>
                  <option>信用评分</option>
                  <option>欺诈检测</option>
                  <option>用户推荐</option>
                </select>
              </div>
              <div className="form-group">
                <label>算法选择</label>
                <select>
                  <option>Random Forest</option>
                  <option>XGBoost</option>
                  <option>Neural Network</option>
                  <option>Transformer</option>
                </select>
              </div>
              <button className="btn btn-primary">创建实验</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIEnhancements;
