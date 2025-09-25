import React, { useState, useEffect, useRef } from 'react';
import { useNotification } from './NotificationSystem';
import './RealTimeFeatures.css';

const RealTimeFeatures = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [realTimeData, setRealTimeData] = useState({
    activeUsers: 0,
    currentLoans: 0,
    systemLoad: 0,
    recentActivities: [],
    alerts: [],
    liveTransactions: []
  });
  const [selectedTimeframe, setSelectedTimeframe] = useState('1hour');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const { showInfo, showWarning, showError } = useNotification();
  const wsRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    initializeWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (autoRefresh) {
      startAutoRefresh();
    } else {
      stopAutoRefresh();
    }
    return () => stopAutoRefresh();
  }, [autoRefresh, selectedTimeframe]);

  const initializeWebSocket = () => {
    try {
      // 模拟WebSocket连接
      setIsConnected(true);
      showInfo('实时连接已建立');
      
      // 模拟实时数据更新
      startAutoRefresh();
    } catch (error) {
      console.error('WebSocket connection failed:', error);
      showError('实时连接失败，使用轮询模式');
      startAutoRefresh();
    }
  };

  const startAutoRefresh = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    const interval = setInterval(() => {
      updateRealTimeData();
    }, 2000); // 每2秒更新一次
    
    intervalRef.current = interval;
  };

  const stopAutoRefresh = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const updateRealTimeData = () => {
    setRealTimeData(prev => {
      const newData = { ...prev };
      
      // 模拟活跃用户数变化
      newData.activeUsers = Math.floor(Math.random() * 50) + 20;
      
      // 模拟当前贷款数变化
      newData.currentLoans = Math.floor(Math.random() * 30) + 10;
      
      // 模拟系统负载变化
      newData.systemLoad = Math.floor(Math.random() * 40) + 30;
      
      // 添加新的活动记录
      const activities = [
        '新用户注册',
        '贷款申请提交',
        '风险评估完成',
        '贷款审批通过',
        '用户登录',
        '文件上传完成',
        '系统健康检查',
        '数据备份完成'
      ];
      
      const newActivity = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        type: activities[Math.floor(Math.random() * activities.length)],
        user: `用户${Math.floor(Math.random() * 1000)}`,
        status: Math.random() > 0.1 ? 'success' : 'warning'
      };
      
      newData.recentActivities = [newActivity, ...prev.recentActivities.slice(0, 19)];
      
      // 模拟实时交易
      if (Math.random() > 0.7) {
        const newTransaction = {
          id: Date.now(),
          amount: Math.floor(Math.random() * 1000000) + 100000,
          type: Math.random() > 0.5 ? 'loan_approved' : 'loan_rejected',
          borrower: `借款人${Math.floor(Math.random() * 100)}`,
          timestamp: new Date().toLocaleTimeString()
        };
        
        newData.liveTransactions = [newTransaction, ...prev.liveTransactions.slice(0, 9)];
      }
      
      // 模拟系统警报
      if (Math.random() > 0.9) {
        const alerts = [
          '系统负载过高',
          '数据库连接异常',
          'AI服务响应缓慢',
          '内存使用率过高',
          '网络延迟增加'
        ];
        
        const newAlert = {
          id: Date.now(),
          type: 'warning',
          message: alerts[Math.floor(Math.random() * alerts.length)],
          timestamp: new Date().toLocaleTimeString(),
          severity: Math.random() > 0.5 ? 'high' : 'medium'
        };
        
        newData.alerts = [newAlert, ...prev.alerts.slice(0, 4)];
        showWarning(newAlert.message);
      }
      
      return newData;
    });
  };

  const handleTimeframeChange = (timeframe) => {
    setSelectedTimeframe(timeframe);
    showInfo(`时间范围已切换到${timeframe === '1hour' ? '1小时' : timeframe === '6hours' ? '6小时' : '24小时'}`);
  };

  const handleRefresh = () => {
    updateRealTimeData();
    showInfo('数据已刷新');
  };

  const clearAlerts = () => {
    setRealTimeData(prev => ({
      ...prev,
      alerts: []
    }));
    showInfo('警报已清除');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return '#28a745';
      case 'warning': return '#ffc107';
      case 'error': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return '#dc3545';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  return (
    <div className="realtime-features">
      <div className="realtime-header">
        <h1>实时监控中心</h1>
        <p>实时监控系统状态和业务数据</p>
        
        <div className="realtime-controls">
          <div className="control-group">
            <label>时间范围:</label>
            <select 
              value={selectedTimeframe} 
              onChange={(e) => handleTimeframeChange(e.target.value)}
            >
              <option value="1hour">近1小时</option>
              <option value="6hours">近6小时</option>
              <option value="24hours">近24小时</option>
            </select>
          </div>
          
          <div className="control-group">
            <label>
              <input 
                type="checkbox" 
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
              />
              自动刷新
            </label>
          </div>
          
          <button className="refresh-btn" onClick={handleRefresh}>
            <span className="refresh-icon">🔄</span>
            手动刷新
          </button>
        </div>
        
        <div className="connection-status">
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            <span className="status-dot"></span>
            {isConnected ? '已连接' : '连接断开'}
          </div>
        </div>
      </div>

      <div className="realtime-content">
        {/* 实时指标卡片 */}
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon">👥</div>
            <div className="metric-content">
              <h3>活跃用户</h3>
              <p className="metric-value">{realTimeData.activeUsers}</p>
              <div className="metric-trend">实时在线</div>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">💰</div>
            <div className="metric-content">
              <h3>当前贷款</h3>
              <p className="metric-value">{realTimeData.currentLoans}</p>
              <div className="metric-trend">处理中</div>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">⚡</div>
            <div className="metric-content">
              <h3>系统负载</h3>
              <p className="metric-value">{realTimeData.systemLoad}%</p>
              <div className={`metric-trend ${realTimeData.systemLoad > 80 ? 'warning' : 'normal'}`}>
                {realTimeData.systemLoad > 80 ? '负载较高' : '运行正常'}
              </div>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">🔔</div>
            <div className="metric-content">
              <h3>系统警报</h3>
              <p className="metric-value">{realTimeData.alerts.length}</p>
              <div className="metric-trend">
                {realTimeData.alerts.length > 0 ? '需要关注' : '运行正常'}
              </div>
            </div>
          </div>
        </div>

        {/* 实时活动流 */}
        <div className="activity-section">
          <div className="section-header">
            <h2>实时活动流</h2>
            <span className="activity-count">{realTimeData.recentActivities.length} 条记录</span>
          </div>
          
          <div className="activity-stream">
            {realTimeData.recentActivities.map(activity => (
              <div key={activity.id} className="activity-item">
                <div className="activity-time">{activity.timestamp}</div>
                <div className="activity-content">
                  <div className="activity-type">{activity.type}</div>
                  <div className="activity-user">{activity.user}</div>
                </div>
                <div 
                  className="activity-status"
                  style={{ color: getStatusColor(activity.status) }}
                >
                  {activity.status === 'success' ? '✓' : '⚠'}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 实时交易 */}
        <div className="transactions-section">
          <div className="section-header">
            <h2>实时交易</h2>
            <span className="transaction-count">{realTimeData.liveTransactions.length} 笔交易</span>
          </div>
          
          <div className="transactions-list">
            {realTimeData.liveTransactions.map(transaction => (
              <div key={transaction.id} className="transaction-item">
                <div className="transaction-time">{transaction.timestamp}</div>
                <div className="transaction-details">
                  <div className="transaction-amount">
                    ¥{(transaction.amount / 10000).toFixed(0)}万
                  </div>
                  <div className="transaction-borrower">{transaction.borrower}</div>
                </div>
                <div className={`transaction-type ${transaction.type}`}>
                  {transaction.type === 'loan_approved' ? '已批准' : '已拒绝'}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 系统警报 */}
        {realTimeData.alerts.length > 0 && (
          <div className="alerts-section">
            <div className="section-header">
              <h2>系统警报</h2>
              <button className="clear-alerts-btn" onClick={clearAlerts}>
                清除警报
              </button>
            </div>
            
            <div className="alerts-list">
              {realTimeData.alerts.map(alert => (
                <div key={alert.id} className={`alert-item ${alert.severity}`}>
                  <div className="alert-time">{alert.timestamp}</div>
                  <div className="alert-message">{alert.message}</div>
                  <div 
                    className="alert-severity"
                    style={{ color: getSeverityColor(alert.severity) }}
                  >
                    {alert.severity === 'high' ? '高' : alert.severity === 'medium' ? '中' : '低'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 系统状态 */}
        <div className="system-status">
          <h2>系统状态</h2>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">API网关</span>
              <span className="status-value online">在线</span>
            </div>
            <div className="status-item">
              <span className="status-label">用户服务</span>
              <span className="status-value online">在线</span>
            </div>
            <div className="status-item">
              <span className="status-label">AI服务</span>
              <span className="status-value online">在线</span>
            </div>
            <div className="status-item">
              <span className="status-label">数据库</span>
              <span className="status-value online">在线</span>
            </div>
            <div className="status-item">
              <span className="status-label">缓存服务</span>
              <span className="status-value online">在线</span>
            </div>
            <div className="status-item">
              <span className="status-label">消息队列</span>
              <span className="status-value online">在线</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeFeatures;
