import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import Charts from './Charts';
import './AdvancedRiskManagement.css';

const AdvancedRiskManagement = () => {
  const [riskData, setRiskData] = useState({});
  const [riskRules, setRiskRules] = useState([]);
  const [riskAlerts, setRiskAlerts] = useState([]);
  const [riskModels, setRiskModels] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadRiskData();
    loadRiskRules();
    loadRiskAlerts();
    loadRiskModels();
  }, []);

  const loadRiskData = async () => {
    try {
      // 模拟风险数据
      const mockData = {
        overallRisk: 65.5,
        riskTrend: 'stable',
        totalApplications: 1250,
        highRiskApplications: 89,
        mediumRiskApplications: 456,
        lowRiskApplications: 705,
        riskDistribution: [
          { level: '低风险', count: 705, percentage: 56.4, color: '#28a745' },
          { level: '中风险', count: 456, percentage: 36.5, color: '#ffc107' },
          { level: '高风险', count: 89, percentage: 7.1, color: '#dc3545' }
        ],
        riskFactors: [
          { factor: '信用历史', weight: 0.3, score: 70, trend: 'up' },
          { factor: '收入稳定性', weight: 0.25, score: 65, trend: 'stable' },
          { factor: '负债比例', weight: 0.2, score: 60, trend: 'down' },
          { factor: '行业风险', weight: 0.15, score: 75, trend: 'up' },
          { factor: '担保情况', weight: 0.1, score: 80, trend: 'stable' }
        ],
        monthlyTrend: Array.from({ length: 12 }, (_, i) => ({
          month: `2025-${String(i + 1).padStart(2, '0')}`,
          riskScore: Math.floor(Math.random() * 20) + 60,
          applications: Math.floor(Math.random() * 200) + 100,
          approvals: Math.floor(Math.random() * 150) + 80
        }))
      };
      setRiskData(mockData);
    } catch (error) {
      showError('加载风险数据失败');
    }
  };

  const loadRiskRules = async () => {
    try {
      // 模拟风险规则数据
      const mockRules = [
        {
          id: 1,
          name: '信用评分规则',
          description: '基于信用历史的评分规则',
          status: 'active',
          priority: 'high',
          conditions: [
            { field: 'credit_score', operator: '<', value: 600, action: 'reject' },
            { field: 'credit_score', operator: '>=', value: 600, action: 'approve' },
            { field: 'credit_score', operator: '>=', value: 750, action: 'fast_track' }
          ],
          lastModified: '2025-09-21 10:00:00',
          hitCount: 1250
        },
        {
          id: 2,
          name: '收入验证规则',
          description: '验证申请人收入真实性',
          status: 'active',
          priority: 'high',
          conditions: [
            { field: 'income_ratio', operator: '<', value: 0.3, action: 'approve' },
            { field: 'income_ratio', operator: '>=', value: 0.3, action: 'review' },
            { field: 'income_ratio', operator: '>=', value: 0.5, action: 'reject' }
          ],
          lastModified: '2025-09-20 15:30:00',
          hitCount: 980
        },
        {
          id: 3,
          name: '行业风险规则',
          description: '特定行业的风险控制规则',
          status: 'active',
          priority: 'medium',
          conditions: [
            { field: 'industry', operator: '==', value: 'construction', action: 'review' },
            { field: 'industry', operator: '==', value: 'gaming', action: 'reject' },
            { field: 'industry', operator: '==', value: 'technology', action: 'approve' }
          ],
          lastModified: '2025-09-19 09:15:00',
          hitCount: 456
        },
        {
          id: 4,
          name: '地域风险规则',
          description: '基于地理位置的风险控制',
          status: 'inactive',
          priority: 'low',
          conditions: [
            { field: 'region', operator: '==', value: 'high_risk_area', action: 'review' },
            { field: 'region', operator: '==', value: 'low_risk_area', action: 'approve' }
          ],
          lastModified: '2025-09-18 14:20:00',
          hitCount: 234
        }
      ];
      setRiskRules(mockRules);
    } catch (error) {
      showError('加载风险规则失败');
    }
  };

  const loadRiskAlerts = async () => {
    try {
      // 模拟风险告警数据
      const mockAlerts = [
        {
          id: 1,
          type: 'high_risk',
          title: '高风险申请激增',
          description: '过去24小时内高风险申请数量增加了150%',
          severity: 'high',
          timestamp: '2025-09-21 14:30:00',
          status: 'active',
          affectedApplications: 25
        },
        {
          id: 2,
          type: 'rule_violation',
          title: '规则命中率异常',
          description: '信用评分规则的命中率下降到85%',
          severity: 'medium',
          timestamp: '2025-09-21 13:45:00',
          status: 'active',
          affectedApplications: 12
        },
        {
          id: 3,
          type: 'model_drift',
          title: '模型漂移检测',
          description: '风险评估模型出现轻微漂移',
          severity: 'low',
          timestamp: '2025-09-21 12:00:00',
          status: 'resolved',
          affectedApplications: 0
        },
        {
          id: 4,
          type: 'fraud_detection',
          title: '疑似欺诈申请',
          description: '检测到3个疑似欺诈的贷款申请',
          severity: 'high',
          timestamp: '2025-09-21 11:15:00',
          status: 'investigating',
          affectedApplications: 3
        }
      ];
      setRiskAlerts(mockAlerts);
    } catch (error) {
      showError('加载风险告警失败');
    }
  };

  const loadRiskModels = async () => {
    try {
      // 模拟风险模型数据
      const mockModels = [
        {
          id: 1,
          name: '信用评分模型',
          version: 'v2.1.0',
          status: 'active',
          accuracy: 94.2,
          precision: 92.5,
          recall: 89.8,
          f1Score: 91.1,
          lastTrained: '2025-09-20 10:00:00',
          trainingDataSize: 50000,
          features: ['credit_history', 'income', 'debt_ratio', 'employment_length'],
          performance: {
            accuracy: 94.2,
            precision: 92.5,
            recall: 89.8,
            f1Score: 91.1,
            auc: 0.95
          }
        },
        {
          id: 2,
          name: '欺诈检测模型',
          version: 'v1.8.3',
          status: 'active',
          accuracy: 96.8,
          precision: 95.2,
          recall: 93.5,
          f1Score: 94.3,
          lastTrained: '2025-09-19 15:30:00',
          trainingDataSize: 25000,
          features: ['device_fingerprint', 'behavior_pattern', 'ip_location', 'document_verification'],
          performance: {
            accuracy: 96.8,
            precision: 95.2,
            recall: 93.5,
            f1Score: 94.3,
            auc: 0.97
          }
        },
        {
          id: 3,
          name: '收入预测模型',
          version: 'v1.5.2',
          status: 'training',
          accuracy: 0,
          precision: 0,
          recall: 0,
          f1Score: 0,
          lastTrained: null,
          trainingDataSize: 30000,
          features: ['employment_history', 'education', 'industry', 'location'],
          performance: {
            accuracy: 0,
            precision: 0,
            recall: 0,
            f1Score: 0,
            auc: 0
          }
        }
      ];
      setRiskModels(mockModels);
    } catch (error) {
      showError('加载风险模型失败');
    }
  };

  const handleRunRiskAnalysis = async () => {
    setIsAnalyzing(true);
    showInfo('正在执行风险分析...');
    
    try {
      // 模拟风险分析
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // 更新风险数据
      setRiskData(prev => ({
        ...prev,
        overallRisk: Math.floor(Math.random() * 20) + 60,
        totalApplications: prev.totalApplications + Math.floor(Math.random() * 50)
      }));
      
      showSuccess('风险分析完成');
    } catch (error) {
      showError('风险分析失败');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleUpdateRiskRule = async (ruleId, updates) => {
    showInfo('正在更新风险规则...');
    
    try {
      // 模拟规则更新
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const updatedRules = riskRules.map(rule => 
        rule.id === ruleId 
          ? { ...rule, ...updates, lastModified: new Date().toLocaleString() }
          : rule
      );
      setRiskRules(updatedRules);
      
      showSuccess('风险规则更新成功');
    } catch (error) {
      showError('风险规则更新失败');
    }
  };

  const handleTrainModel = async (modelId) => {
    showInfo('正在训练风险模型...');
    
    try {
      // 模拟模型训练
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      const updatedModels = riskModels.map(model => 
        model.id === modelId 
          ? { 
              ...model, 
              status: 'active',
              lastTrained: new Date().toLocaleString(),
              accuracy: Math.random() * 10 + 90,
              precision: Math.random() * 10 + 90,
              recall: Math.random() * 10 + 90,
              f1Score: Math.random() * 10 + 90
            }
          : model
      );
      setRiskModels(updatedModels);
      
      showSuccess('风险模型训练完成');
    } catch (error) {
      showError('风险模型训练失败');
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return '#dc3545';
      case 'medium': return '#ffc107';
      case 'low': return '#17a2b8';
      default: return '#6c757d';
    }
  };

  const getSeverityText = (severity) => {
    switch (severity) {
      case 'high': return '高';
      case 'medium': return '中';
      case 'low': return '低';
      default: return '未知';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#28a745';
      case 'inactive': return '#6c757d';
      case 'training': return '#ffc107';
      case 'resolved': return '#17a2b8';
      case 'investigating': return '#fd7e14';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return '活跃';
      case 'inactive': return '停用';
      case 'training': return '训练中';
      case 'resolved': return '已解决';
      case 'investigating': return '调查中';
      default: return '未知';
    }
  };

  return (
    <div className="advanced-risk-management">
      <div className="risk-header">
        <h1>高级风险管理</h1>
        <p>智能风险识别、评估和控制，保障平台安全运营</p>
        
        <div className="risk-stats">
          <div className="stat-card">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3>{riskData.overallRisk}%</h3>
              <p>整体风险评分</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>{riskData.totalApplications?.toLocaleString()}</h3>
              <p>总申请数</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔴</div>
            <div className="stat-content">
              <h3>{riskData.highRiskApplications}</h3>
              <p>高风险申请</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🟡</div>
            <div className="stat-content">
              <h3>{riskData.mediumRiskApplications}</h3>
              <p>中风险申请</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🟢</div>
            <div className="stat-content">
              <h3>{riskData.lowRiskApplications}</h3>
              <p>低风险申请</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3>{riskData.riskTrend}</h3>
              <p>风险趋势</p>
            </div>
          </div>
        </div>
      </div>

      <div className="risk-content">
        <div className="content-grid">
          {/* 风险概览 */}
          <div className="risk-overview-section">
            <h2>风险概览</h2>
            <div className="overview-cards">
              <div className="overview-card">
                <h3>风险分布</h3>
                <div className="risk-distribution">
                  {riskData.riskDistribution?.map((item, index) => (
                    <div key={index} className="distribution-item">
                      <div className="distribution-bar">
                        <div 
                          className="distribution-fill"
                          style={{ 
                            width: `${item.percentage}%`,
                            backgroundColor: item.color
                          }}
                        ></div>
                      </div>
                      <div className="distribution-info">
                        <span className="distribution-label">{item.level}</span>
                        <span className="distribution-value">{item.count} ({item.percentage}%)</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="overview-card">
                <h3>风险因子</h3>
                <div className="risk-factors">
                  {riskData.riskFactors?.map((factor, index) => (
                    <div key={index} className="factor-item">
                      <div className="factor-header">
                        <span className="factor-name">{factor.factor}</span>
                        <span className="factor-weight">权重: {factor.weight}</span>
                      </div>
                      <div className="factor-score">
                        <div className="score-bar">
                          <div 
                            className="score-fill"
                            style={{ width: `${factor.score}%` }}
                          ></div>
                        </div>
                        <span className="score-value">{factor.score}分</span>
                        <span className={`trend ${factor.trend}`}>
                          {factor.trend === 'up' ? '↗️' : factor.trend === 'down' ? '↘️' : '→'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* 风险规则 */}
          <div className="risk-rules-section">
            <h2>风险规则</h2>
            <div className="rules-list">
              {riskRules.map(rule => (
                <div key={rule.id} className="rule-card">
                  <div className="rule-header">
                    <div className="rule-info">
                      <h3>{rule.name}</h3>
                      <p>{rule.description}</p>
                      <div className="rule-meta">
                        <span className={`priority ${rule.priority}`}>
                          优先级: {rule.priority}
                        </span>
                        <span className={`status ${rule.status}`}>
                          {getStatusText(rule.status)}
                        </span>
                        <span className="hit-count">
                          命中: {rule.hitCount}
                        </span>
                      </div>
                    </div>
                    <div className="rule-actions">
                      <button 
                        className="action-btn edit"
                        onClick={() => handleUpdateRiskRule(rule.id, {})}
                      >
                        编辑
                      </button>
                      <button 
                        className="action-btn toggle"
                        onClick={() => handleUpdateRiskRule(rule.id, { 
                          status: rule.status === 'active' ? 'inactive' : 'active' 
                        })}
                      >
                        {rule.status === 'active' ? '停用' : '启用'}
                      </button>
                    </div>
                  </div>
                  
                  <div className="rule-conditions">
                    <h4>规则条件:</h4>
                    <div className="conditions-list">
                      {rule.conditions.map((condition, index) => (
                        <div key={index} className="condition-item">
                          <span className="field">{condition.field}</span>
                          <span className="operator">{condition.operator}</span>
                          <span className="value">{condition.value}</span>
                          <span className="action">{condition.action}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 风险告警 */}
          <div className="risk-alerts-section">
            <h2>风险告警</h2>
            <div className="alerts-list">
              {riskAlerts.map(alert => (
                <div key={alert.id} className={`alert-card ${alert.severity}`}>
                  <div className="alert-header">
                    <div className="alert-info">
                      <h3>{alert.title}</h3>
                      <p>{alert.description}</p>
                      <div className="alert-meta">
                        <span className={`severity ${alert.severity}`}>
                          严重程度: {getSeverityText(alert.severity)}
                        </span>
                        <span className={`status ${alert.status}`}>
                          {getStatusText(alert.status)}
                        </span>
                        <span className="affected">
                          影响申请: {alert.affectedApplications}
                        </span>
                      </div>
                    </div>
                    <div className="alert-actions">
                      <button className="action-btn resolve">解决</button>
                      <button className="action-btn investigate">调查</button>
                    </div>
                  </div>
                  <div className="alert-time">
                    {alert.timestamp}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 风险模型 */}
          <div className="risk-models-section">
            <h2>风险模型</h2>
            <div className="models-list">
              {riskModels.map(model => (
                <div key={model.id} className="model-card">
                  <div className="model-header">
                    <div className="model-info">
                      <h3>{model.name}</h3>
                      <p>版本: {model.version}</p>
                      <div className="model-meta">
                        <span className={`status ${model.status}`}>
                          {getStatusText(model.status)}
                        </span>
                        <span className="training-data">
                          训练数据: {model.trainingDataSize.toLocaleString()}
                        </span>
                        <span className="last-trained">
                          最后训练: {model.lastTrained || '未训练'}
                        </span>
                      </div>
                    </div>
                    <div className="model-actions">
                      <button 
                        className="action-btn train"
                        onClick={() => handleTrainModel(model.id)}
                        disabled={model.status === 'training'}
                      >
                        {model.status === 'training' ? '训练中...' : '训练模型'}
                      </button>
                      <button className="action-btn evaluate">评估</button>
                      <button className="action-btn deploy">部署</button>
                    </div>
                  </div>
                  
                  <div className="model-performance">
                    <h4>模型性能:</h4>
                    <div className="performance-metrics">
                      <div className="metric">
                        <span className="metric-label">准确率:</span>
                        <span className="metric-value">{model.accuracy.toFixed(1)}%</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">精确率:</span>
                        <span className="metric-value">{model.precision.toFixed(1)}%</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">召回率:</span>
                        <span className="metric-value">{model.recall.toFixed(1)}%</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">F1分数:</span>
                        <span className="metric-value">{model.f1Score.toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="model-features">
                    <h4>特征变量:</h4>
                    <div className="features-list">
                      {model.features.map((feature, index) => (
                        <span key={index} className="feature-tag">
                          {feature}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="risk-actions">
          <button 
            className="action-btn analyze"
            onClick={handleRunRiskAnalysis}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? '分析中...' : '🔍 执行风险分析'}
          </button>
          <button className="action-btn report">📊 生成风险报告</button>
          <button className="action-btn export">📤 导出风险数据</button>
        </div>
      </div>
    </div>
  );
};

export default AdvancedRiskManagement;
