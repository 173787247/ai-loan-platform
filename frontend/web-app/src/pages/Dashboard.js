import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalLoans: 0,
    approvedLoans: 0,
    pendingLoans: 0,
    totalAmount: 0,
    riskScore: 0
  });

  const [chartData, setChartData] = useState({
    loanTrends: [],
    riskDistribution: [],
    userGrowth: []
  });

  useEffect(() => {
    // 模拟数据加载
    const mockStats = {
      totalUsers: 1250,
      totalLoans: 890,
      approvedLoans: 650,
      pendingLoans: 240,
      totalAmount: 125000000,
      riskScore: 75
    };
    setStats(mockStats);

    const mockChartData = {
      loanTrends: [
        { month: '1月', applications: 120, approved: 95 },
        { month: '2月', applications: 135, approved: 110 },
        { month: '3月', applications: 150, approved: 125 },
        { month: '4月', applications: 165, approved: 140 },
        { month: '5月', applications: 180, approved: 155 },
        { month: '6月', applications: 200, approved: 170 }
      ],
      riskDistribution: [
        { level: '低风险', count: 450, percentage: 50 },
        { level: '中风险', count: 300, percentage: 33.3 },
        { level: '高风险', count: 150, percentage: 16.7 }
      ],
      userGrowth: [
        { month: '1月', users: 800 },
        { month: '2月', users: 920 },
        { month: '3月', users: 1050 },
        { month: '4月', users: 1180 },
        { month: '5月', users: 1200 },
        { month: '6月', users: 1250 }
      ]
    };
    setChartData(mockChartData);
  }, []);

  const formatNumber = (num) => {
    if (num >= 100000000) {
      return (num / 100000000).toFixed(1) + '亿';
    } else if (num >= 10000) {
      return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
  };

  const StatCard = ({ title, value, icon, color, trend }) => (
    <div className="stat-card">
      <div className="stat-icon" style={{ backgroundColor: color }}>
        {icon}
      </div>
      <div className="stat-content">
        <h3>{title}</h3>
        <p className="stat-value">{value}</p>
        {trend && (
          <span className={`stat-trend ${trend > 0 ? 'positive' : 'negative'}`}>
            {trend > 0 ? '↗' : '↘'} {Math.abs(trend)}%
          </span>
        )}
      </div>
    </div>
  );

  const ChartCard = ({ title, children, className = '' }) => (
    <div className={`chart-card ${className}`}>
      <h3>{title}</h3>
      <div className="chart-content">
        {children}
      </div>
    </div>
  );

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>📊 智能仪表板</h1>
        <p>实时监控系统运行状态和业务数据</p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="总用户数"
          value={stats.totalUsers.toLocaleString()}
          icon="👥"
          color="#007bff"
          trend={5.2}
        />
        <StatCard
          title="总贷款数"
          value={stats.totalLoans.toLocaleString()}
          icon="💰"
          color="#28a745"
          trend={12.8}
        />
        <StatCard
          title="已批准"
          value={stats.approvedLoans.toLocaleString()}
          icon="✅"
          color="#17a2b8"
          trend={8.5}
        />
        <StatCard
          title="待审核"
          value={stats.pendingLoans.toLocaleString()}
          icon="⏳"
          color="#ffc107"
          trend={-2.1}
        />
        <StatCard
          title="总金额"
          value={formatNumber(stats.totalAmount)}
          icon="💎"
          color="#6f42c1"
          trend={15.3}
        />
        <StatCard
          title="风险评分"
          value={stats.riskScore + '%'}
          icon="🛡️"
          color="#dc3545"
          trend={-3.2}
        />
      </div>

      <div className="charts-grid">
        <ChartCard title="贷款趋势分析" className="trend-chart">
          <div className="trend-chart-container">
            {chartData.loanTrends.map((item, index) => (
              <div key={index} className="trend-item">
                <div className="trend-month">{item.month}</div>
                <div className="trend-bars">
                  <div className="trend-bar applications">
                    <div 
                      className="bar-fill" 
                      style={{ height: `${(item.applications / 200) * 100}%` }}
                    ></div>
                    <span className="bar-label">申请: {item.applications}</span>
                  </div>
                  <div className="trend-bar approved">
                    <div 
                      className="bar-fill" 
                      style={{ height: `${(item.approved / 200) * 100}%` }}
                    ></div>
                    <span className="bar-label">批准: {item.approved}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </ChartCard>

        <ChartCard title="风险分布" className="risk-chart">
          <div className="risk-distribution">
            {chartData.riskDistribution.map((item, index) => (
              <div key={index} className="risk-item">
                <div className="risk-level">{item.level}</div>
                <div className="risk-bar">
                  <div 
                    className="risk-fill" 
                    style={{ 
                      width: `${item.percentage}%`,
                      backgroundColor: index === 0 ? '#28a745' : index === 1 ? '#ffc107' : '#dc3545'
                    }}
                  ></div>
                </div>
                <div className="risk-stats">
                  <span className="risk-count">{item.count}</span>
                  <span className="risk-percentage">{item.percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </ChartCard>

        <ChartCard title="用户增长" className="growth-chart">
          <div className="growth-chart-container">
            {chartData.userGrowth.map((item, index) => (
              <div key={index} className="growth-item">
                <div className="growth-month">{item.month}</div>
                <div className="growth-bar">
                  <div 
                    className="growth-fill" 
                    style={{ height: `${(item.users / 1250) * 100}%` }}
                  ></div>
                </div>
                <div className="growth-value">{item.users}</div>
              </div>
            ))}
          </div>
        </ChartCard>

        <ChartCard title="系统状态" className="system-status">
          <div className="status-grid">
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>前端服务</span>
            </div>
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>AI服务</span>
            </div>
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>数据库</span>
            </div>
            <div className="status-item">
              <div className="status-indicator warning"></div>
              <span>微服务</span>
            </div>
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>网关</span>
            </div>
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>缓存</span>
            </div>
          </div>
        </ChartCard>
      </div>
    </div>
  );
};

export default Dashboard;
