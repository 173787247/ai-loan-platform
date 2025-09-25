import React, { useState, useEffect } from 'react';
import './Analytics.css';

const Analytics = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [selectedMetric, setSelectedMetric] = useState('loans');
  const [analyticsData, setAnalyticsData] = useState({
    loanAnalytics: [],
    userAnalytics: [],
    riskAnalytics: [],
    performanceMetrics: {}
  });

  useEffect(() => {
    // 模拟数据分析
    const mockData = {
      loanAnalytics: [
        { period: '2025-01', applications: 120, approved: 95, rejected: 25, amount: 5000000 },
        { period: '2025-02', applications: 135, approved: 110, rejected: 25, amount: 5500000 },
        { period: '2025-03', applications: 150, approved: 125, rejected: 25, amount: 6000000 },
        { period: '2025-04', applications: 165, approved: 140, rejected: 25, amount: 6500000 },
        { period: '2025-05', applications: 180, approved: 155, rejected: 25, amount: 7000000 },
        { period: '2025-06', applications: 200, approved: 170, rejected: 30, amount: 7500000 }
      ],
      userAnalytics: [
        { period: '2025-01', newUsers: 80, activeUsers: 200, totalUsers: 800 },
        { period: '2025-02', newUsers: 90, activeUsers: 220, totalUsers: 890 },
        { period: '2025-03', newUsers: 100, activeUsers: 250, totalUsers: 990 },
        { period: '2025-04', newUsers: 110, activeUsers: 280, totalUsers: 1100 },
        { period: '2025-05', newUsers: 120, activeUsers: 300, totalUsers: 1220 },
        { period: '2025-06', newUsers: 130, activeUsers: 320, totalUsers: 1350 }
      ],
      riskAnalytics: [
        { category: '信用评分', low: 450, medium: 300, high: 150 },
        { category: '收入水平', low: 380, medium: 350, high: 170 },
        { category: '负债比例', low: 420, medium: 320, high: 158 },
        { category: '经营年限', low: 200, medium: 400, high: 300 }
      ],
      performanceMetrics: {
        approvalRate: 85.5,
        averageProcessingTime: 2.3,
        customerSatisfaction: 4.2,
        riskScore: 72.8
      }
    };
    setAnalyticsData(mockData);
  }, []);

  const formatNumber = (num) => {
    if (num >= 100000000) {
      return (num / 100000000).toFixed(1) + '亿';
    } else if (num >= 10000) {
      return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
  };

  const MetricCard = ({ title, value, icon, color, trend, subtitle }) => (
    <div className="metric-card">
      <div className="metric-icon" style={{ backgroundColor: color }}>
        {icon}
      </div>
      <div className="metric-content">
        <h3>{title}</h3>
        <p className="metric-value">{value}</p>
        {subtitle && <p className="metric-subtitle">{subtitle}</p>}
        {trend && (
          <span className={`metric-trend ${trend > 0 ? 'positive' : 'negative'}`}>
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
    <div className="analytics-container">
      <div className="analytics-header">
        <h1>📊 数据分析中心</h1>
        <p>深度分析业务数据，洞察市场趋势</p>
        <div className="analytics-controls">
          <select 
            value={selectedPeriod} 
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="period-selector"
          >
            <option value="week">最近一周</option>
            <option value="month">最近一月</option>
            <option value="quarter">最近一季</option>
            <option value="year">最近一年</option>
          </select>
          <select 
            value={selectedMetric} 
            onChange={(e) => setSelectedMetric(e.target.value)}
            className="metric-selector"
          >
            <option value="loans">贷款数据</option>
            <option value="users">用户数据</option>
            <option value="risk">风险数据</option>
            <option value="performance">性能数据</option>
          </select>
        </div>
      </div>

      <div className="metrics-grid">
        <MetricCard
          title="批准率"
          value={analyticsData.performanceMetrics.approvalRate + '%'}
          icon="✅"
          color="#28a745"
          trend={5.2}
          subtitle="较上月提升"
        />
        <MetricCard
          title="平均处理时间"
          value={analyticsData.performanceMetrics.averageProcessingTime + '天'}
          icon="⏱️"
          color="#17a2b8"
          trend={-12.5}
          subtitle="较上月缩短"
        />
        <MetricCard
          title="客户满意度"
          value={analyticsData.performanceMetrics.customerSatisfaction + '/5.0'}
          icon="😊"
          color="#ffc107"
          trend={8.3}
          subtitle="用户评价"
        />
        <MetricCard
          title="风险评分"
          value={analyticsData.performanceMetrics.riskScore + '/100'}
          icon="🛡️"
          color="#dc3545"
          trend={-3.1}
          subtitle="风险控制"
        />
      </div>

      <div className="charts-section">
        <div className="charts-grid">
          <ChartCard title="贷款申请趋势" className="trend-chart">
            <div className="trend-chart-container">
              {analyticsData.loanAnalytics.map((item, index) => (
                <div key={index} className="trend-item">
                  <div className="trend-period">{item.period}</div>
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
                    <div className="trend-bar rejected">
                      <div 
                        className="bar-fill" 
                        style={{ height: `${(item.rejected / 200) * 100}%` }}
                      ></div>
                      <span className="bar-label">拒绝: {item.rejected}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </ChartCard>

          <ChartCard title="用户增长分析" className="user-chart">
            <div className="user-chart-container">
              {analyticsData.userAnalytics.map((item, index) => (
                <div key={index} className="user-item">
                  <div className="user-period">{item.period}</div>
                  <div className="user-bars">
                    <div className="user-bar new-users">
                      <div 
                        className="bar-fill" 
                        style={{ height: `${(item.newUsers / 130) * 100}%` }}
                      ></div>
                      <span className="bar-label">新用户: {item.newUsers}</span>
                    </div>
                    <div className="user-bar active-users">
                      <div 
                        className="bar-fill" 
                        style={{ height: `${(item.activeUsers / 320) * 100}%` }}
                      ></div>
                      <span className="bar-label">活跃: {item.activeUsers}</span>
                    </div>
                    <div className="user-bar total-users">
                      <div 
                        className="bar-fill" 
                        style={{ height: `${(item.totalUsers / 1350) * 100}%` }}
                      ></div>
                      <span className="bar-label">总计: {item.totalUsers}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </ChartCard>

          <ChartCard title="风险分布分析" className="risk-chart">
            <div className="risk-distribution">
              {analyticsData.riskAnalytics.map((item, index) => (
                <div key={index} className="risk-category">
                  <div className="risk-category-name">{item.category}</div>
                  <div className="risk-levels">
                    <div className="risk-level low">
                      <span className="level-label">低风险</span>
                      <div className="level-bar">
                        <div 
                          className="level-fill" 
                          style={{ width: `${(item.low / 500) * 100}%` }}
                        ></div>
                        <span className="level-count">{item.low}</span>
                      </div>
                    </div>
                    <div className="risk-level medium">
                      <span className="level-label">中风险</span>
                      <div className="level-bar">
                        <div 
                          className="level-fill" 
                          style={{ width: `${(item.medium / 500) * 100}%` }}
                        ></div>
                        <span className="level-count">{item.medium}</span>
                      </div>
                    </div>
                    <div className="risk-level high">
                      <span className="level-label">高风险</span>
                      <div className="level-bar">
                        <div 
                          className="level-fill" 
                          style={{ width: `${(item.high / 500) * 100}%` }}
                        ></div>
                        <span className="level-count">{item.high}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </ChartCard>

          <ChartCard title="数据导出工具" className="export-tools">
            <div className="export-options">
              <div className="export-option">
                <h4>📊 报表导出</h4>
                <p>导出详细的数据分析报表</p>
                <button className="export-btn">导出Excel</button>
                <button className="export-btn">导出PDF</button>
              </div>
              <div className="export-option">
                <h4>📈 图表导出</h4>
                <p>导出高质量的分析图表</p>
                <button className="export-btn">导出PNG</button>
                <button className="export-btn">导出SVG</button>
              </div>
              <div className="export-option">
                <h4>📋 原始数据</h4>
                <p>导出原始数据用于进一步分析</p>
                <button className="export-btn">导出CSV</button>
                <button className="export-btn">导出JSON</button>
              </div>
            </div>
          </ChartCard>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
