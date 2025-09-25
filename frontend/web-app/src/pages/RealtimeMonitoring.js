import React, { useState, useEffect } from 'react';
import Charts from '../components/Charts';
import './RealtimeMonitoring.css';

function RealtimeMonitoring() {
  const [systemStats, setSystemStats] = useState({
    totalLoans: 0,
    activeLoans: 0,
    totalAmount: 0,
    avgRiskScore: 0,
    successRate: 0,
    processingTime: 0
  });

  const [recentActivities, setRecentActivities] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState({
    riskDistribution: [],
    loanTrend: [],
    riskScoreDistribution: [],
    industryRisk: []
  });

  useEffect(() => {
    // 初始化图表数据
    setChartData({
      riskDistribution: [
        { level: '低风险', count: 45, percentage: 36 },
        { level: '中风险', count: 35, percentage: 28 },
        { level: '高风险', count: 45, percentage: 36 }
      ],
      loanTrend: [
        { month: '1月', total: 120, approved: 100, rejected: 20 },
        { month: '2月', total: 135, approved: 115, rejected: 20 },
        { month: '3月', total: 150, approved: 125, rejected: 25 },
        { month: '4月', total: 140, approved: 120, rejected: 20 },
        { month: '5月', total: 160, approved: 135, rejected: 25 },
        { month: '6月', total: 180, approved: 150, rejected: 30 }
      ],
      riskScoreDistribution: [
        { range: '0-20', count: 15 },
        { range: '21-40', count: 35 },
        { range: '41-60', count: 25 },
        { range: '61-80', count: 20 },
        { range: '81-100', count: 5 }
      ],
      industryRisk: [
        { name: '科技行业', risks: [85, 70, 60, 75, 80] },
        { name: '制造业', risks: [70, 80, 75, 85, 70] },
        { name: '零售业', risks: [60, 85, 80, 70, 75] },
        { name: '服务业', risks: [75, 75, 70, 80, 85] },
        { name: '建筑业', risks: [65, 90, 85, 90, 80] }
      ]
    });

    // 模拟实时数据更新
    const interval = setInterval(() => {
      setSystemStats(prev => ({
        totalLoans: prev.totalLoans + Math.floor(Math.random() * 3),
        activeLoans: Math.floor(Math.random() * 50) + 20,
        totalAmount: prev.totalAmount + Math.floor(Math.random() * 1000),
        avgRiskScore: Math.floor(Math.random() * 40) + 30,
        successRate: Math.floor(Math.random() * 20) + 80,
        processingTime: Math.floor(Math.random() * 5) + 2
      }));

      // 添加新的活动记录
      const activities = [
        '新贷款申请已提交',
        '风险评估完成',
        '匹配算法运行中',
        '贷款审批通过',
        '资金已发放',
        '还款提醒发送',
        '系统健康检查完成'
      ];

      const newActivity = {
        id: Date.now(),
        message: activities[Math.floor(Math.random() * activities.length)],
        timestamp: new Date().toLocaleTimeString(),
        type: Math.random() > 0.7 ? 'warning' : 'info'
      };

      setRecentActivities(prev => [newActivity, ...prev.slice(0, 9)]);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // 模拟警报
    const alertMessages = [
      '高风险贷款申请需要人工审核',
      '系统负载过高，建议扩容',
      '数据库连接异常',
      'AI模型准确率下降',
      '网络延迟增加'
    ];

    if (Math.random() > 0.8) {
      const newAlert = {
        id: Date.now(),
        message: alertMessages[Math.floor(Math.random() * alertMessages.length)],
        timestamp: new Date().toLocaleTimeString(),
        level: Math.random() > 0.5 ? 'high' : 'medium'
      };
      setAlerts(prev => [newAlert, ...prev.slice(0, 4)]);
    }
  }, [systemStats]);

  const getStatusColor = (value, type) => {
    switch (type) {
      case 'risk':
        if (value < 40) return '#4ecdc4';
        if (value < 70) return '#feca57';
        return '#ff6b6b';
      case 'success':
        if (value > 90) return '#4ecdc4';
        if (value > 80) return '#feca57';
        return '#ff6b6b';
      case 'time':
        if (value < 3) return '#4ecdc4';
        if (value < 5) return '#feca57';
        return '#ff6b6b';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className="realtime-monitoring">
      <div className="container">
        <h1>实时监控</h1>
        <p className="subtitle">全流程实时监控和管理</p>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>总贷款数</h3>
              <div className="stat-value">{systemStats.totalLoans.toLocaleString()}</div>
              <div className="stat-trend">+12% 本月</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔄</div>
            <div className="stat-content">
              <h3>活跃贷款</h3>
              <div className="stat-value">{systemStats.activeLoans}</div>
              <div className="stat-trend">实时更新</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">💰</div>
            <div className="stat-content">
              <h3>总金额</h3>
              <div className="stat-value">¥{systemStats.totalAmount.toLocaleString()}万</div>
              <div className="stat-trend">+8% 本月</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3>平均风险评分</h3>
              <div 
                className="stat-value"
                style={{ color: getStatusColor(systemStats.avgRiskScore, 'risk') }}
              >
                {systemStats.avgRiskScore}
              </div>
              <div className="stat-trend">风险可控</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>成功率</h3>
              <div 
                className="stat-value"
                style={{ color: getStatusColor(systemStats.successRate, 'success') }}
              >
                {systemStats.successRate}%
              </div>
              <div className="stat-trend">表现优秀</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-content">
              <h3>处理时间</h3>
              <div 
                className="stat-value"
                style={{ color: getStatusColor(systemStats.processingTime, 'time') }}
              >
                {systemStats.processingTime}s
              </div>
              <div className="stat-trend">响应迅速</div>
            </div>
          </div>
        </div>

        <div className="monitoring-sections">
          <div className="section">
            <h2>系统活动</h2>
            <div className="activity-list">
              {recentActivities.map(activity => (
                <div key={activity.id} className={`activity-item ${activity.type}`}>
                  <div className="activity-time">{activity.timestamp}</div>
                  <div className="activity-message">{activity.message}</div>
                  <div className={`activity-indicator ${activity.type}`}></div>
                </div>
              ))}
            </div>
          </div>

          <div className="section">
            <h2>系统警报</h2>
            <div className="alerts-list">
              {alerts.length > 0 ? (
                alerts.map(alert => (
                  <div key={alert.id} className={`alert-item ${alert.level}`}>
                    <div className="alert-time">{alert.timestamp}</div>
                    <div className="alert-message">{alert.message}</div>
                    <div className={`alert-level ${alert.level}`}>
                      {alert.level === 'high' ? '高' : '中'}
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-alerts">
                  <div className="no-alerts-icon">✅</div>
                  <p>系统运行正常，无警报</p>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="system-health">
          <h2>系统健康状态</h2>
          <div className="health-grid">
            <div className="health-item">
              <div className="health-label">API网关</div>
              <div className="health-status online">在线</div>
            </div>
            <div className="health-item">
              <div className="health-label">AI服务</div>
              <div className="health-status online">在线</div>
            </div>
            <div className="health-item">
              <div className="health-label">数据库</div>
              <div className="health-status online">在线</div>
            </div>
            <div className="health-item">
              <div className="health-label">缓存服务</div>
              <div className="health-status online">在线</div>
            </div>
            <div className="health-item">
              <div className="health-label">消息队列</div>
              <div className="health-status warning">维护中</div>
            </div>
            <div className="health-item">
              <div className="health-label">监控系统</div>
              <div className="health-status offline">离线</div>
            </div>
          </div>
        </div>

        {/* 数据可视化图表 */}
        <div className="charts-section">
          <h2>数据可视化分析</h2>
          <div className="charts-grid">
            <div className="chart-card">
              <Charts.RiskDistribution data={chartData.riskDistribution} />
            </div>
            <div className="chart-card">
              <Charts.LoanTrend data={chartData.loanTrend} />
            </div>
            <div className="chart-card">
              <Charts.RiskScoreDistribution data={chartData.riskScoreDistribution} />
            </div>
            <div className="chart-card">
              <Charts.IndustryRiskRadar data={chartData.industryRisk} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RealtimeMonitoring;
