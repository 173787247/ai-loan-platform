import React, { useState, useEffect } from 'react';
import { useNotification } from './NotificationSystem';
import './IntegrationAPIs.css';

const IntegrationAPIs = () => {
  const [integrations, setIntegrations] = useState([]);
  const [selectedIntegration, setSelectedIntegration] = useState(null);
  const [isConfiguring, setIsConfiguring] = useState(false);
  const [configData, setConfigData] = useState({});
  const [apiKeys, setApiKeys] = useState({});
  const [testResults, setTestResults] = useState({});
  const { showSuccess, showError, showInfo } = useNotification();

  useEffect(() => {
    loadIntegrations();
    loadApiKeys();
  }, []);

  const loadIntegrations = async () => {
    try {
      // 模拟第三方集成数据
      const mockIntegrations = [
        {
          id: 1,
          name: '征信系统集成',
          provider: '中国人民银行征信中心',
          type: 'credit_check',
          status: 'active',
          description: '集成央行征信系统，获取个人和企业信用报告',
          endpoints: [
            { name: '个人征信查询', url: '/api/credit/personal', method: 'POST' },
            { name: '企业征信查询', url: '/api/credit/enterprise', method: 'POST' },
            { name: '征信状态检查', url: '/api/credit/status', method: 'GET' }
          ],
          rateLimit: { requests: 1000, period: 'hour' },
          lastSync: '2025-09-21 14:30:00',
          successRate: 99.2,
          responseTime: 1200
        },
        {
          id: 2,
          name: '银行账户验证',
          provider: '银联数据',
          type: 'bank_verification',
          status: 'active',
          description: '验证银行账户真实性和余额信息',
          endpoints: [
            { name: '账户验证', url: '/api/bank/verify', method: 'POST' },
            { name: '余额查询', url: '/api/bank/balance', method: 'POST' },
            { name: '交易记录', url: '/api/bank/transactions', method: 'GET' }
          ],
          rateLimit: { requests: 500, period: 'hour' },
          lastSync: '2025-09-21 14:25:00',
          successRate: 98.8,
          responseTime: 800
        },
        {
          id: 3,
          name: '身份认证服务',
          provider: '公安部身份认证',
          type: 'identity_verification',
          status: 'active',
          description: '身份证信息真实性验证和人脸识别',
          endpoints: [
            { name: '身份证验证', url: '/api/identity/idcard', method: 'POST' },
            { name: '人脸识别', url: '/api/identity/face', method: 'POST' },
            { name: '活体检测', url: '/api/identity/liveness', method: 'POST' }
          ],
          rateLimit: { requests: 2000, period: 'hour' },
          lastSync: '2025-09-21 14:20:00',
          successRate: 99.5,
          responseTime: 600
        },
        {
          id: 4,
          name: '短信通知服务',
          provider: '阿里云通信',
          type: 'sms_notification',
          status: 'active',
          description: '发送验证码、通知和营销短信',
          endpoints: [
            { name: '发送短信', url: '/api/sms/send', method: 'POST' },
            { name: '短信状态', url: '/api/sms/status', method: 'GET' },
            { name: '模板管理', url: '/api/sms/templates', method: 'GET' }
          ],
          rateLimit: { requests: 10000, period: 'hour' },
          lastSync: '2025-09-21 14:15:00',
          successRate: 99.8,
          responseTime: 300
        },
        {
          id: 5,
          name: '支付网关',
          provider: '支付宝开放平台',
          type: 'payment_gateway',
          status: 'inactive',
          description: '集成支付宝支付功能',
          endpoints: [
            { name: '创建支付', url: '/api/payment/create', method: 'POST' },
            { name: '支付查询', url: '/api/payment/query', method: 'GET' },
            { name: '退款处理', url: '/api/payment/refund', method: 'POST' }
          ],
          rateLimit: { requests: 5000, period: 'hour' },
          lastSync: null,
          successRate: 0,
          responseTime: 0
        },
        {
          id: 6,
          name: '风控数据源',
          provider: '百融云创',
          type: 'risk_control',
          status: 'active',
          description: '提供反欺诈和风险评估数据',
          endpoints: [
            { name: '反欺诈检测', url: '/api/risk/fraud', method: 'POST' },
            { name: '风险评分', url: '/api/risk/score', method: 'POST' },
            { name: '黑名单查询', url: '/api/risk/blacklist', method: 'GET' }
          ],
          rateLimit: { requests: 800, period: 'hour' },
          lastSync: '2025-09-21 14:10:00',
          successRate: 97.5,
          responseTime: 1500
        }
      ];
      setIntegrations(mockIntegrations);
    } catch (error) {
      showError('加载集成服务失败');
    }
  };

  const loadApiKeys = () => {
    // 模拟API密钥数据
    const mockApiKeys = {
      1: { key: 'pbccrc_****_****_****', secret: 'secret_****_****' },
      2: { key: 'unionpay_****_****', secret: 'secret_****_****' },
      3: { key: 'mps_****_****_****', secret: 'secret_****_****' },
      4: { key: 'aliyun_****_****', secret: 'secret_****_****' },
      5: { key: 'alipay_****_****', secret: 'secret_****_****' },
      6: { key: 'bairong_****_****', secret: 'secret_****_****' }
    };
    setApiKeys(mockApiKeys);
  };

  const handleConfigureIntegration = (integration) => {
    setSelectedIntegration(integration);
    setConfigData({
      apiKey: apiKeys[integration.id]?.key || '',
      apiSecret: apiKeys[integration.id]?.secret || '',
      baseUrl: integration.baseUrl || '',
      timeout: integration.timeout || 30000,
      retryCount: integration.retryCount || 3,
      enableLogging: integration.enableLogging || true
    });
    setIsConfiguring(true);
  };

  const handleSaveConfiguration = () => {
    if (!configData.apiKey || !configData.apiSecret) {
      showError('请填写API密钥和密钥');
      return;
    }

    // 更新集成配置
    const updatedIntegrations = integrations.map(integration => 
      integration.id === selectedIntegration.id 
        ? { ...integration, ...configData, status: 'active' }
        : integration
    );
    setIntegrations(updatedIntegrations);

    // 更新API密钥
    setApiKeys(prev => ({
      ...prev,
      [selectedIntegration.id]: {
        key: configData.apiKey,
        secret: configData.apiSecret
      }
    }));

    showSuccess('集成配置保存成功');
    setIsConfiguring(false);
  };

  const handleTestIntegration = async (integration) => {
    showInfo('正在测试集成连接...');
    
    try {
      // 模拟API测试
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const testResult = {
        success: Math.random() > 0.1, // 90%成功率
        responseTime: Math.floor(Math.random() * 1000) + 500,
        error: Math.random() > 0.9 ? '连接超时' : null,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setTestResults(prev => ({
        ...prev,
        [integration.id]: testResult
      }));

      if (testResult.success) {
        showSuccess('集成测试成功');
      } else {
        showError(`集成测试失败: ${testResult.error}`);
      }
    } catch (error) {
      showError('集成测试失败');
    }
  };

  const handleToggleIntegration = (integrationId) => {
    const updatedIntegrations = integrations.map(integration => 
      integration.id === integrationId 
        ? { ...integration, status: integration.status === 'active' ? 'inactive' : 'active' }
        : integration
    );
    setIntegrations(updatedIntegrations);
    
    const integration = integrations.find(i => i.id === integrationId);
    showInfo(`集成服务已${integration.status === 'active' ? '停用' : '启用'}`);
  };

  const handleSyncData = async (integration) => {
    showInfo('正在同步数据...');
    
    try {
      // 模拟数据同步
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const updatedIntegrations = integrations.map(i => 
        i.id === integration.id 
          ? { ...i, lastSync: new Date().toLocaleString() }
          : i
      );
      setIntegrations(updatedIntegrations);
      
      showSuccess('数据同步完成');
    } catch (error) {
      showError('数据同步失败');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#28a745';
      case 'inactive': return '#6c757d';
      case 'error': return '#dc3545';
      case 'pending': return '#ffc107';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return '运行中';
      case 'inactive': return '已停用';
      case 'error': return '错误';
      case 'pending': return '待配置';
      default: return '未知';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'credit_check': return '📊';
      case 'bank_verification': return '🏦';
      case 'identity_verification': return '🆔';
      case 'sms_notification': return '📱';
      case 'payment_gateway': return '💳';
      case 'risk_control': return '🛡️';
      default: return '🔗';
    }
  };

  return (
    <div className="integration-apis">
      <div className="integration-header">
        <h1>第三方集成API管理</h1>
        <p>管理和配置第三方服务集成，确保数据安全和系统稳定</p>
        
        <div className="integration-stats">
          <div className="stat-card">
            <div className="stat-icon">🔗</div>
            <div className="stat-content">
              <h3>{integrations.length}</h3>
              <p>集成服务</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>{integrations.filter(i => i.status === 'active').length}</h3>
              <p>运行中</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3>99.2%</h3>
              <p>平均成功率</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <h3>850ms</h3>
              <p>平均响应时间</p>
            </div>
          </div>
        </div>
      </div>

      <div className="integration-content">
        <div className="integrations-grid">
          {integrations.map(integration => (
            <div key={integration.id} className="integration-card">
              <div className="card-header">
                <div className="integration-info">
                  <div className="integration-icon">
                    {getTypeIcon(integration.type)}
                  </div>
                  <div className="integration-details">
                    <h3>{integration.name}</h3>
                    <p className="provider">{integration.provider}</p>
                    <span 
                      className="status-badge"
                      style={{ color: getStatusColor(integration.status) }}
                    >
                      {getStatusText(integration.status)}
                    </span>
                  </div>
                </div>
                <div className="card-actions">
                  <button 
                    className="action-btn test"
                    onClick={() => handleTestIntegration(integration)}
                    title="测试连接"
                  >
                    🧪
                  </button>
                  <button 
                    className="action-btn sync"
                    onClick={() => handleSyncData(integration)}
                    title="同步数据"
                  >
                    🔄
                  </button>
                  <button 
                    className="action-btn config"
                    onClick={() => handleConfigureIntegration(integration)}
                    title="配置"
                  >
                    ⚙️
                  </button>
                  <button 
                    className="action-btn toggle"
                    onClick={() => handleToggleIntegration(integration.id)}
                    title={integration.status === 'active' ? '停用' : '启用'}
                  >
                    {integration.status === 'active' ? '⏸️' : '▶️'}
                  </button>
                </div>
              </div>

              <div className="card-content">
                <p className="description">{integration.description}</p>
                
                <div className="endpoints">
                  <h4>API端点:</h4>
                  <div className="endpoint-list">
                    {integration.endpoints.map((endpoint, index) => (
                      <div key={index} className="endpoint-item">
                        <span className="method">{endpoint.method}</span>
                        <span className="url">{endpoint.url}</span>
                        <span className="name">{endpoint.name}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="integration-metrics">
                  <div className="metric">
                    <span className="metric-label">成功率:</span>
                    <span className="metric-value">{integration.successRate}%</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">响应时间:</span>
                    <span className="metric-value">{integration.responseTime}ms</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">限流:</span>
                    <span className="metric-value">
                      {integration.rateLimit.requests}/{integration.rateLimit.period}
                    </span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">最后同步:</span>
                    <span className="metric-value">
                      {integration.lastSync || '未同步'}
                    </span>
                  </div>
                </div>

                {testResults[integration.id] && (
                  <div className="test-result">
                    <h4>测试结果:</h4>
                    <div className={`result ${testResults[integration.id].success ? 'success' : 'error'}`}>
                      <span className="result-icon">
                        {testResults[integration.id].success ? '✅' : '❌'}
                      </span>
                      <span className="result-text">
                        {testResults[integration.id].success 
                          ? `连接成功 (${testResults[integration.id].responseTime}ms)`
                          : `连接失败: ${testResults[integration.id].error}`
                        }
                      </span>
                      <span className="result-time">
                        {testResults[integration.id].timestamp}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 配置对话框 */}
      {isConfiguring && (
        <div className="config-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>配置 {selectedIntegration?.name}</h2>
              <button 
                className="close-btn"
                onClick={() => setIsConfiguring(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="form-group">
                <label>API密钥</label>
                <input
                  type="text"
                  value={configData.apiKey}
                  onChange={(e) => setConfigData({...configData, apiKey: e.target.value})}
                  placeholder="输入API密钥"
                />
              </div>
              
              <div className="form-group">
                <label>API密钥</label>
                <input
                  type="password"
                  value={configData.apiSecret}
                  onChange={(e) => setConfigData({...configData, apiSecret: e.target.value})}
                  placeholder="输入API密钥"
                />
              </div>
              
              <div className="form-group">
                <label>基础URL</label>
                <input
                  type="url"
                  value={configData.baseUrl}
                  onChange={(e) => setConfigData({...configData, baseUrl: e.target.value})}
                  placeholder="https://api.example.com"
                />
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label>超时时间 (ms)</label>
                  <input
                    type="number"
                    value={configData.timeout}
                    onChange={(e) => setConfigData({...configData, timeout: parseInt(e.target.value)})}
                    min="1000"
                    max="60000"
                  />
                </div>
                
                <div className="form-group">
                  <label>重试次数</label>
                  <input
                    type="number"
                    value={configData.retryCount}
                    onChange={(e) => setConfigData({...configData, retryCount: parseInt(e.target.value)})}
                    min="0"
                    max="10"
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={configData.enableLogging}
                    onChange={(e) => setConfigData({...configData, enableLogging: e.target.checked})}
                  />
                  启用日志记录
                </label>
              </div>
            </div>
            
            <div className="modal-footer">
              <button 
                className="btn-cancel"
                onClick={() => setIsConfiguring(false)}
              >
                取消
              </button>
              <button 
                className="btn-save"
                onClick={handleSaveConfiguration}
              >
                保存配置
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IntegrationAPIs;
