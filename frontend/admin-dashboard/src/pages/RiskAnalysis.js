import React, { useState, useEffect } from 'react';
import './RiskAnalysis.css';

function RiskAnalysis() {
  const [riskData, setRiskData] = useState({
    distribution: [],
    trends: [],
    factors: [],
    alerts: []
  });

  useEffect(() => {
    // 模拟风险分析数据
    setRiskData({
      distribution: [
        { level: '低风险', count: 45, percentage: 36 },
        { level: '中风险', count: 35, percentage: 28 },
        { level: '高风险', count: 45, percentage: 36 }
      ],
      trends: [
        { month: '1月', low: 40, medium: 30, high: 30 },
        { month: '2月', low: 42, medium: 28, high: 30 },
        { month: '3月', low: 38, medium: 32, high: 30 },
        { month: '4月', low: 35, medium: 35, high: 30 },
        { month: '5月', low: 32, medium: 38, high: 30 },
        { month: '6月', low: 36, medium: 28, high: 36 }
      ],
      factors: [
        { name: '信用评分', impact: 85, trend: 'up' },
        { name: '年收入', impact: 78, trend: 'up' },
        { name: '行业风险', impact: 65, trend: 'down' },
        { name: '经营年限', impact: 72, trend: 'up' },
        { name: '资产负债率', impact: 68, trend: 'down' }
      ],
      alerts: [
        { id: 1, type: 'high', message: '高风险贷款申请增加', count: 5, time: '2小时前' },
        { id: 2, type: 'medium', message: '信用评分异常波动', count: 3, time: '4小时前' },
        { id: 3, type: 'low', message: '系统性能正常', count: 0, time: '6小时前' }
      ]
    });
  }, []);

  const getAlertColor = (type) => {
    switch (type) {
      case 'high': return 'alert-high';
      case 'medium': return 'alert-medium';
      case 'low': return 'alert-low';
      default: return '';
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'high': return '🔴';
      case 'medium': return '🟡';
      case 'low': return '🟢';
      default: return '⚪';
    }
  };

  const getTrendIcon = (trend) => {
    return trend === 'up' ? '📈' : '📉';
  };

  return (
    <div className="risk-analysis">
      <div className="page-header">
        <h1>风险分析</h1>
        <p>AI驱动的风险分析和预警系统</p>
      </div>

      {/* 风险分布概览 */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>总评估数</h3>
            <div className="stat-value">1,247</div>
            <div className="stat-change positive">+12% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>高风险比例</h3>
            <div className="stat-value">36%</div>
            <div className="stat-change negative">+3% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>低风险比例</h3>
            <div className="stat-value">36%</div>
            <div className="stat-change positive">+2% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>平均风险评分</h3>
            <div className="stat-value">52</div>
            <div className="stat-change">稳定</div>
          </div>
        </div>
      </div>

      <div className="analysis-content">
        {/* 风险分布图表 */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">风险等级分布</h2>
            <button className="btn btn-primary">导出报告</button>
          </div>
          <div className="chart-container">
            <div className="risk-distribution">
              {riskData.distribution.map((item, index) => (
                <div key={index} className="distribution-item">
                  <div className="distribution-bar">
                    <div 
                      className={`bar ${item.level === '低风险' ? 'low' : item.level === '中风险' ? 'medium' : 'high'}`}
                      style={{ height: `${item.percentage}%` }}
                    ></div>
                  </div>
                  <div className="distribution-info">
                    <div className="distribution-label">{item.level}</div>
                    <div className="distribution-count">{item.count}个</div>
                    <div className="distribution-percentage">{item.percentage}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 风险趋势 */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">风险趋势分析</h2>
            <div className="time-range">
              <select>
                <option>最近6个月</option>
                <option>最近1年</option>
                <option>最近2年</option>
              </select>
            </div>
          </div>
          <div className="trend-chart">
            <div className="trend-lines">
              <div className="trend-line low">
                <div className="line-label">低风险</div>
                <div className="line-path"></div>
              </div>
              <div className="trend-line medium">
                <div className="line-label">中风险</div>
                <div className="line-path"></div>
              </div>
              <div className="trend-line high">
                <div className="line-label">高风险</div>
                <div className="line-path"></div>
              </div>
            </div>
            <div className="trend-months">
              {riskData.trends.map((trend, index) => (
                <div key={index} className="trend-month">
                  <div className="month-label">{trend.month}</div>
                  <div className="month-bars">
                    <div className="month-bar low" style={{ height: `${trend.low}%` }}></div>
                    <div className="month-bar medium" style={{ height: `${trend.medium}%` }}></div>
                    <div className="month-bar high" style={{ height: `${trend.high}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 风险因素分析 */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">关键风险因素</h2>
            <button className="btn btn-primary">更新模型</button>
          </div>
          <div className="factors-list">
            {riskData.factors.map((factor, index) => (
              <div key={index} className="factor-item">
                <div className="factor-info">
                  <div className="factor-name">{factor.name}</div>
                  <div className="factor-impact">影响度: {factor.impact}%</div>
                </div>
                <div className="factor-visual">
                  <div className="impact-bar">
                    <div 
                      className="impact-fill"
                      style={{ width: `${factor.impact}%` }}
                    ></div>
                  </div>
                  <div className="factor-trend">
                    <span className="trend-icon">{getTrendIcon(factor.trend)}</span>
                    <span className="trend-text">
                      {factor.trend === 'up' ? '上升' : '下降'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 风险预警 */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">风险预警</h2>
            <span className="alert-count">共 {riskData.alerts.length} 条预警</span>
          </div>
          <div className="alerts-list">
            {riskData.alerts.map(alert => (
              <div key={alert.id} className={`alert-item ${getAlertColor(alert.type)}`}>
                <div className="alert-icon">{getAlertIcon(alert.type)}</div>
                <div className="alert-content">
                  <div className="alert-message">{alert.message}</div>
                  <div className="alert-meta">
                    <span className="alert-count">影响 {alert.count} 个申请</span>
                    <span className="alert-time">{alert.time}</span>
                  </div>
                </div>
                <div className="alert-actions">
                  <button className="btn btn-primary">查看详情</button>
                  <button className="btn btn-warning">处理</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default RiskAnalysis;
