import React, { useState, useEffect, useCallback } from 'react';
import { useUser } from '../contexts/UserContext';
import { useNotification } from './NotificationSystem';
import './AdvancedAnalytics.css';

const AdvancedAnalytics = () => {
  const { user, isAdmin, isBorrower, isLender } = useUser();
  const { showSuccess, showError, showInfo } = useNotification();
  
  // 权限检查
  const canViewAnalytics = () => {
    if (isAdmin()) return true;
    if (isBorrower() && user?.permissions?.includes('view_my_analytics')) return true;
    if (isLender() && user?.permissions?.includes('view_market_analytics')) return true;
    return false;
  };
  
  const [analyticsData, setAnalyticsData] = useState(null);
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d');
  const [selectedMetric, setSelectedMetric] = useState('overview');
  const [isLoading, setIsLoading] = useState(false);
  const [predictions, setPredictions] = useState(null);
  const [realTimeData, setRealTimeData] = useState(null);
  const [exportFormat, setExportFormat] = useState('pdf');
  const [customDateRange, setCustomDateRange] = useState({
    start: '',
    end: ''
  });
  const [selectedChart, setSelectedChart] = useState('overview');
  const [chartFilters, setChartFilters] = useState({
    userType: 'all',
    riskLevel: 'all',
    amountRange: 'all',
    region: 'all'
  });
  const [drillDownData, setDrillDownData] = useState(null);
  const [comparisonMode, setComparisonMode] = useState(false);
  const [comparisonData, setComparisonData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [dashboardLayout, setDashboardLayout] = useState('grid');
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(30);

  // 生成更丰富的模拟数据
  const generateAnalyticsData = useCallback((timeRange) => {
    const now = new Date();
    const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
    const data = [];

    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      data.push({
        date: date.toISOString().split('T')[0],
        loanApplications: Math.floor(Math.random() * 50) + 20,
        approvedLoans: Math.floor(Math.random() * 30) + 15,
        rejectedLoans: Math.floor(Math.random() * 20) + 5,
        totalAmount: Math.floor(Math.random() * 1000000) + 500000,
        averageRiskScore: Math.floor(Math.random() * 40) + 60,
        userRegistrations: Math.floor(Math.random() * 20) + 10,
        activeUsers: Math.floor(Math.random() * 100) + 200,
        conversionRate: Math.random() * 20 + 10,
        averageLoanAmount: Math.floor(Math.random() * 500000) + 200000,
        riskDistribution: {
          low: Math.floor(Math.random() * 30) + 40,
          medium: Math.floor(Math.random() * 30) + 30,
          high: Math.floor(Math.random() * 20) + 10
        },
        geographicData: {
          '北京': Math.floor(Math.random() * 100) + 50,
          '上海': Math.floor(Math.random() * 80) + 40,
          '广州': Math.floor(Math.random() * 60) + 30,
          '深圳': Math.floor(Math.random() * 70) + 35,
          '其他': Math.floor(Math.random() * 200) + 100
        }
      });
    }

    return data;
  }, []);

  // 生成AI预测数据
  const generatePredictions = useCallback(() => {
    return {
      nextWeek: {
        loanApplications: Math.floor(Math.random() * 100) + 150,
        approvedLoans: Math.floor(Math.random() * 60) + 80,
        totalAmount: Math.floor(Math.random() * 2000000) + 1500000,
        confidence: Math.floor(Math.random() * 20) + 75,
        riskTrend: 'stable'
      },
      nextMonth: {
        loanApplications: Math.floor(Math.random() * 400) + 600,
        approvedLoans: Math.floor(Math.random() * 250) + 350,
        totalAmount: Math.floor(Math.random() * 8000000) + 6000000,
        confidence: Math.floor(Math.random() * 15) + 70,
        riskTrend: 'improving'
      },
      riskTrends: {
        low: Math.floor(Math.random() * 20) + 30,
        medium: Math.floor(Math.random() * 30) + 40,
        high: Math.floor(Math.random() * 20) + 20
      },
      marketInsights: [
        '预计下周贷款申请量将增长15%',
        '风险评分模型准确率提升至92%',
        '用户转化率有望突破25%',
        '建议增加对中小企业的关注'
      ]
    };
  }, []);

  // 生成实时数据
  const generateRealTimeData = useCallback(() => {
    return {
      currentUsers: Math.floor(Math.random() * 50) + 100,
      activeLoans: Math.floor(Math.random() * 200) + 500,
      pendingApplications: Math.floor(Math.random() * 30) + 20,
      systemHealth: Math.floor(Math.random() * 20) + 80,
      recentActivities: [
        { time: '2分钟前', action: '新用户注册', user: '张***', amount: null },
        { time: '5分钟前', action: '贷款申请', user: '李***', amount: 500000 },
        { time: '8分钟前', action: '贷款批准', user: '王***', amount: 300000 },
        { time: '12分钟前', action: '风险评估', user: '赵***', amount: null }
      ]
    };
  }, []);

  // 加载分析数据
  const loadAnalyticsData = useCallback(async () => {
    setIsLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const data = generateAnalyticsData(selectedTimeRange);
      const predictions = generatePredictions();
      const realTime = generateRealTimeData();
      
      setAnalyticsData(data);
      setPredictions(predictions);
      setRealTimeData(realTime);
      
      showSuccess(`已加载${selectedTimeRange}的分析数据`);
    } catch (error) {
      showError('无法加载分析数据，请重试');
    } finally {
      setIsLoading(false);
    }
  }, [selectedTimeRange, generateAnalyticsData, generatePredictions, generateRealTimeData, showSuccess, showError]);

  // 初始加载数据
  useEffect(() => {
    loadAnalyticsData();
  }, [loadAnalyticsData]);

  // 计算统计数据
  const calculateStats = (data) => {
    if (!data || data.length === 0) return null;

    const total = data.reduce((acc, item) => ({
      loanApplications: acc.loanApplications + item.loanApplications,
      approvedLoans: acc.approvedLoans + item.approvedLoans,
      rejectedLoans: acc.rejectedLoans + item.rejectedLoans,
      totalAmount: acc.totalAmount + item.totalAmount,
      userRegistrations: acc.userRegistrations + item.userRegistrations
    }), {
      loanApplications: 0,
      approvedLoans: 0,
      rejectedLoans: 0,
      totalAmount: 0,
      userRegistrations: 0
    });

    const averageRiskScore = data.reduce((acc, item) => acc + item.averageRiskScore, 0) / data.length;
    const approvalRate = (total.approvedLoans / total.loanApplications) * 100;
    const averageConversionRate = data.reduce((acc, item) => acc + item.conversionRate, 0) / data.length;
    const averageLoanAmount = data.reduce((acc, item) => acc + item.averageLoanAmount, 0) / data.length;

    return {
      ...total,
      averageRiskScore: Math.round(averageRiskScore),
      approvalRate: Math.round(approvalRate * 100) / 100,
      averageConversionRate: Math.round(averageConversionRate * 100) / 100,
      averageLoanAmount: Math.round(averageLoanAmount)
    };
  };

  const stats = analyticsData ? calculateStats(analyticsData) : null;

  // 导出数据
  const handleExport = (format) => {
    showInfo(`正在导出${format.toUpperCase()}格式的数据...`);
    // 这里可以添加实际的导出逻辑
  };

  // 刷新数据
  const handleRefresh = () => {
    loadAnalyticsData();
  };

  // 权限检查
  if (!canViewAnalytics()) {
    return (
      <div className="advanced-analytics">
        <div className="access-denied">
          <h2>🚫 访问受限</h2>
          <p>您没有权限访问此数据分析页面。</p>
          <div className="permission-info">
            <h3>权限说明：</h3>
            <ul>
              <li><strong>管理员</strong>：可访问所有分析数据</li>
              <li><strong>借款方</strong>：可查看个人相关分析数据</li>
              <li><strong>放贷方</strong>：可查看市场分析数据</li>
            </ul>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => window.history.back()}
          >
            返回上一页
          </button>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="advanced-analytics">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>正在加载分析数据...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="advanced-analytics">
      {/* 页面头部 */}
      <div className="analytics-header">
        <div className="header-content">
          <h1>📊 高级数据分析</h1>
          <p>实时监控业务指标，AI驱动的智能分析</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn btn-secondary" 
            onClick={handleRefresh}
            disabled={isLoading}
          >
            🔄 刷新数据
          </button>
          <select 
            value={exportFormat} 
            onChange={(e) => setExportFormat(e.target.value)}
            className="export-select"
          >
            <option value="pdf">导出PDF</option>
            <option value="excel">导出Excel</option>
            <option value="csv">导出CSV</option>
          </select>
          <button 
            className="btn btn-primary" 
            onClick={() => handleExport(exportFormat)}
          >
            📥 导出报告
          </button>
        </div>
      </div>

      {/* 时间范围选择 */}
      <div className="time-range-selector">
        <div className="selector-group">
          <label>时间范围：</label>
          <div className="time-buttons">
            {['7d', '30d', '90d'].map(range => (
              <button
                key={range}
                className={`time-btn ${selectedTimeRange === range ? 'active' : ''}`}
                onClick={() => setSelectedTimeRange(range)}
              >
                {range === '7d' ? '最近7天' : range === '30d' ? '最近30天' : '最近90天'}
              </button>
            ))}
          </div>
        </div>
        <div className="custom-date-range">
          <label>自定义范围：</label>
          <input
            type="date"
            value={customDateRange.start}
            onChange={(e) => setCustomDateRange(prev => ({ ...prev, start: e.target.value }))}
            className="date-input"
          />
          <span>至</span>
          <input
            type="date"
            value={customDateRange.end}
            onChange={(e) => setCustomDateRange(prev => ({ ...prev, end: e.target.value }))}
            className="date-input"
          />
        </div>
      </div>

      {/* 指标选择 */}
      <div className="metric-selector">
        <label>分析维度：</label>
        <div className="metric-buttons">
          {[
            { key: 'overview', label: '总览', icon: '📈' },
            { key: 'loans', label: '贷款分析', icon: '💰' },
            { key: 'users', label: '用户分析', icon: '👥' },
            { key: 'risk', label: '风险分析', icon: '⚠️' },
            { key: 'predictions', label: 'AI预测', icon: '🔮' },
            { key: 'realtime', label: '实时监控', icon: '⚡' }
          ].map(metric => (
            <button
              key={metric.key}
              className={`metric-btn ${selectedMetric === metric.key ? 'active' : ''}`}
              onClick={() => setSelectedMetric(metric.key)}
            >
              <span className="metric-icon">{metric.icon}</span>
              {metric.label}
            </button>
          ))}
        </div>
      </div>

      {/* 高级控制面板 */}
      <div className="advanced-controls">
        <div className="control-panel">
          <div className="panel-section">
            <h4>📊 图表控制</h4>
            <div className="chart-controls">
              <select 
                value={selectedChart} 
                onChange={(e) => setSelectedChart(e.target.value)}
              >
                <option value="overview">概览图表</option>
                <option value="loans">贷款分析</option>
                <option value="users">用户分析</option>
                <option value="risk">风险分析</option>
                <option value="predictions">预测分析</option>
              </select>
              
              <div className="layout-controls">
                <button 
                  className={`btn btn-sm ${dashboardLayout === 'grid' ? 'btn-primary' : 'btn-outline'}`}
                  onClick={() => setDashboardLayout('grid')}
                >
                  ⊞ 网格布局
                </button>
                <button 
                  className={`btn btn-sm ${dashboardLayout === 'list' ? 'btn-primary' : 'btn-outline'}`}
                  onClick={() => setDashboardLayout('list')}
                >
                  ☰ 列表布局
                </button>
              </div>
            </div>
          </div>

          <div className="panel-section">
            <h4>🔄 自动刷新</h4>
            <div className="refresh-controls">
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                />
                启用自动刷新
              </label>
              {autoRefresh && (
                <select 
                  value={refreshInterval}
                  onChange={(e) => setRefreshInterval(Number(e.target.value))}
                >
                  <option value={10}>10秒</option>
                  <option value={30}>30秒</option>
                  <option value={60}>1分钟</option>
                  <option value={300}>5分钟</option>
                </select>
              )}
            </div>
          </div>

          <div className="panel-section">
            <h4>🔍 高级功能</h4>
            <div className="feature-controls">
              <button 
                className="btn btn-outline"
                onClick={() => setComparisonMode(!comparisonMode)}
              >
                {comparisonMode ? '关闭比较' : '开启比较'}
              </button>
              <button 
                className="btn btn-outline"
                onClick={() => setDrillDownData({
                  title: '贷款趋势分析',
                  stats: [
                    { label: '总申请数', value: '1,234' },
                    { label: '通过率', value: '85.6%' },
                    { label: '平均金额', value: '¥456,789' }
                  ],
                  chartData: { /* 图表数据 */ },
                  tableData: [
                    { time: '2024-01-01', value: '100', change: 5.2 },
                    { time: '2024-01-02', value: '105', change: -2.1 }
                  ]
                })}
              >
                数据钻取
              </button>
            </div>
          </div>
        </div>

        {/* 高级过滤器 */}
        <AdvancedFilters 
          filters={chartFilters}
          onFilterChange={(key, value) => setChartFilters(prev => ({ ...prev, [key]: value }))}
          onReset={() => setChartFilters({
            userType: 'all',
            riskLevel: 'all',
            amountRange: 'all',
            region: 'all'
          })}
        />

        {/* 智能预警 */}
        <SmartAlerts 
          alerts={alerts}
          onDismiss={(id) => setAlerts(prev => prev.filter(alert => alert.id !== id))}
          onConfigure={() => showInfo('预警配置功能开发中...')}
        />

        {/* 收藏夹 */}
        <FavoritesPanel 
          favorites={favorites}
          onRemove={(id) => setFavorites(prev => prev.filter(fav => fav.id !== id))}
          onAdd={() => setFavorites(prev => [...prev, {
            id: Date.now(),
            title: '新收藏图表',
            description: '用户自定义收藏'
          }])}
        />

        {/* 导出面板 */}
        <ExportPanel 
          onExport={handleExport}
          format={exportFormat}
          onFormatChange={setExportFormat}
        />
      </div>

      {/* 关键指标卡片 */}
      {stats && (
        <div className="metrics-grid">
          <MetricCard
            title="贷款申请"
            value={stats.loanApplications}
            change="+12.5%"
            trend="up"
            icon="📈"
            color="#4CAF50"
          />
          <MetricCard
            title="批准率"
            value={`${stats.approvalRate}%`}
            change="+2.3%"
            trend="up"
            icon="✅"
            color="#2196F3"
          />
          <MetricCard
            title="总金额"
            value={`¥${(stats.totalAmount / 10000).toFixed(1)}万`}
            change="+8.7%"
            trend="up"
            icon="💰"
            color="#FF9800"
          />
          <MetricCard
            title="平均风险评分"
            value={stats.averageRiskScore}
            change="-1.2"
            trend="down"
            icon="🎯"
            color="#9C27B0"
          />
          <MetricCard
            title="转化率"
            value={`${stats.averageConversionRate}%`}
            change="+3.1%"
            trend="up"
            icon="🔄"
            color="#00BCD4"
          />
          <MetricCard
            title="平均贷款金额"
            value={`¥${(stats.averageLoanAmount / 10000).toFixed(1)}万`}
            change="+5.2%"
            trend="up"
            icon="💳"
            color="#795548"
          />
        </div>
      )}

      {/* 图表区域 */}
      <div className="charts-section">
        {selectedMetric === 'overview' && (
          <OverviewCharts data={analyticsData} />
        )}
        {selectedMetric === 'loans' && (
          <LoanAnalysisCharts data={analyticsData} />
        )}
        {selectedMetric === 'users' && (
          <UserAnalysisCharts data={analyticsData} />
        )}
        {selectedMetric === 'risk' && (
          <RiskAnalysisCharts data={analyticsData} />
        )}
        {selectedMetric === 'predictions' && (
          <PredictionCharts predictions={predictions} />
        )}
        {selectedMetric === 'realtime' && (
          <RealTimeCharts realTimeData={realTimeData} />
        )}
      </div>

      {/* AI洞察 */}
      {analyticsData && (
        <AIInsights data={analyticsData} stats={stats} predictions={predictions} />
      )}

      {/* 数据钻取模态框 */}
      {drillDownData && (
        <DataDrillDown 
          data={drillDownData}
          onClose={() => setDrillDownData(null)}
          onBack={() => setDrillDownData(null)}
        />
      )}

      {/* 比较模式模态框 */}
      {comparisonMode && (
        <ComparisonMode 
          data={comparisonData}
          onClose={() => setComparisonMode(false)}
          onAddComparison={(type) => {
            setComparisonData({
              type,
              currentData: analyticsData,
              comparisonData: generateAnalyticsData(selectedTimeRange)
            });
          }}
        />
      )}
    </div>
  );
};

// 指标卡片组件
const MetricCard = ({ title, value, change, trend, icon, color = '#2196F3' }) => {
  return (
    <div className="metric-card" style={{ borderLeftColor: color }}>
      <div className="metric-header">
        <div className="metric-icon" style={{ color }}>{icon}</div>
        <div className="metric-title">{title}</div>
      </div>
      <div className="metric-value" style={{ color }}>{value}</div>
      <div className={`metric-change ${trend}`}>
        <span className="change-icon">
          {trend === 'up' ? '↗' : '↘'}
        </span>
        {change}
      </div>
    </div>
  );
};

// 总览图表组件
const OverviewCharts = ({ data }) => {
  if (!data) return <div className="chart-placeholder">暂无数据</div>;

  return (
    <div className="overview-charts">
      <div className="chart-container">
        <h3>📈 业务趋势</h3>
        <div className="chart-content">
          <div className="trend-chart">
            {data.map((item, index) => (
              <div key={index} className="trend-bar">
                <div 
                  className="bar" 
                  style={{ height: `${(item.loanApplications / 50) * 100}%` }}
                ></div>
                <span className="bar-label">{item.date.split('-')[2]}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>💰 金额分布</h3>
        <div className="chart-content">
          <div className="amount-chart">
            {data.slice(-7).map((item, index) => (
              <div key={index} className="amount-item">
                <div className="amount-bar">
                  <div 
                    className="amount-fill" 
                    style={{ width: `${(item.totalAmount / 1000000) * 100}%` }}
                  ></div>
                </div>
                <span className="amount-value">¥{(item.totalAmount / 10000).toFixed(1)}万</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// 贷款分析图表组件
const LoanAnalysisCharts = ({ data }) => {
  if (!data) return <div className="chart-placeholder">暂无数据</div>;

  return (
    <div className="loan-charts">
      <div className="chart-container">
        <h3>📊 贷款申请趋势</h3>
        <div className="chart-content">
          <div className="loan-trend">
            {data.map((item, index) => (
              <div key={index} className="trend-item">
                <div className="trend-line">
                  <div className="approved" style={{ height: `${(item.approvedLoans / 30) * 100}%` }}></div>
                  <div className="rejected" style={{ height: `${(item.rejectedLoans / 20) * 100}%` }}></div>
                </div>
                <span className="date-label">{item.date.split('-')[1]}/{item.date.split('-')[2]}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>🎯 批准率分析</h3>
        <div className="chart-content">
          <div className="approval-rate">
            {data.slice(-7).map((item, index) => {
              const rate = (item.approvedLoans / item.loanApplications) * 100;
              return (
                <div key={index} className="rate-item">
                  <div className="rate-bar">
                    <div 
                      className="rate-fill" 
                      style={{ width: `${rate}%` }}
                    ></div>
                  </div>
                  <span className="rate-value">{rate.toFixed(1)}%</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

// 用户分析图表组件
const UserAnalysisCharts = ({ data }) => {
  if (!data) return <div className="chart-placeholder">暂无数据</div>;

  return (
    <div className="user-charts">
      <div className="chart-container">
        <h3>👥 用户增长趋势</h3>
        <div className="chart-content">
          <div className="user-growth">
            {data.map((item, index) => (
              <div key={index} className="growth-item">
                <div className="growth-bar">
                  <div 
                    className="growth-fill" 
                    style={{ height: `${(item.userRegistrations / 20) * 100}%` }}
                  ></div>
                </div>
                <span className="growth-value">{item.userRegistrations}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>🌍 地域分布</h3>
        <div className="chart-content">
          <div className="geographic-distribution">
            {data[0]?.geographicData && Object.entries(data[0].geographicData).map(([city, count]) => (
              <div key={city} className="geo-item">
                <span className="geo-city">{city}</span>
                <div className="geo-bar">
                  <div 
                    className="geo-fill" 
                    style={{ width: `${(count / 200) * 100}%` }}
                  ></div>
                </div>
                <span className="geo-count">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// 风险分析图表组件
const RiskAnalysisCharts = ({ data }) => {
  if (!data) return <div className="chart-placeholder">暂无数据</div>;

  return (
    <div className="risk-charts">
      <div className="chart-container">
        <h3>⚠️ 风险评分趋势</h3>
        <div className="chart-content">
          <div className="risk-trend">
            {data.map((item, index) => (
              <div key={index} className="risk-item">
                <div className="risk-score">
                  <div 
                    className="score-bar" 
                    style={{ 
                      height: `${item.averageRiskScore}%`,
                      backgroundColor: item.averageRiskScore > 70 ? '#f44336' : 
                                     item.averageRiskScore > 50 ? '#ff9800' : '#4caf50'
                    }}
                  ></div>
                </div>
                <span className="score-value">{item.averageRiskScore}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>📊 风险分布</h3>
        <div className="chart-content">
          <div className="risk-distribution">
            {data[0]?.riskDistribution && Object.entries(data[0].riskDistribution).map(([level, percentage]) => (
              <div key={level} className="risk-level">
                <div className="level-info">
                  <span className="level-name">{level}风险</span>
                  <span className="level-percentage">{percentage}%</span>
                </div>
                <div className="level-bar">
                  <div 
                    className="level-fill" 
                    style={{ 
                      width: `${percentage}%`,
                      backgroundColor: level === '低' ? '#4caf50' : 
                                     level === '中' ? '#ff9800' : '#f44336'
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// 预测图表组件
const PredictionCharts = ({ predictions }) => {
  if (!predictions) return <div className="chart-placeholder">暂无预测数据</div>;

  return (
    <div className="prediction-charts">
      <div className="chart-container">
        <h3>🔮 AI预测分析</h3>
        <div className="chart-content">
          <div className="prediction-overview">
            <div className="prediction-item">
              <h4>下周预测</h4>
              <div className="prediction-metrics">
                <div className="metric">
                  <span className="label">贷款申请:</span>
                  <span className="value">{predictions.nextWeek.loanApplications}</span>
                </div>
                <div className="metric">
                  <span className="label">批准数量:</span>
                  <span className="value">{predictions.nextWeek.approvedLoans}</span>
                </div>
                <div className="metric">
                  <span className="label">总金额:</span>
                  <span className="value">¥{(predictions.nextWeek.totalAmount / 10000).toFixed(1)}万</span>
                </div>
                <div className="metric">
                  <span className="label">置信度:</span>
                  <span className="value">{predictions.nextWeek.confidence}%</span>
                </div>
              </div>
            </div>
            
            <div className="prediction-item">
              <h4>下月预测</h4>
              <div className="prediction-metrics">
                <div className="metric">
                  <span className="label">贷款申请:</span>
                  <span className="value">{predictions.nextMonth.loanApplications}</span>
                </div>
                <div className="metric">
                  <span className="label">批准数量:</span>
                  <span className="value">{predictions.nextMonth.approvedLoans}</span>
                </div>
                <div className="metric">
                  <span className="label">总金额:</span>
                  <span className="value">¥{(predictions.nextMonth.totalAmount / 10000).toFixed(1)}万</span>
                </div>
                <div className="metric">
                  <span className="label">置信度:</span>
                  <span className="value">{predictions.nextMonth.confidence}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>💡 市场洞察</h3>
        <div className="chart-content">
          <div className="market-insights">
            {predictions.marketInsights.map((insight, index) => (
              <div key={index} className="insight-item">
                <span className="insight-icon">💡</span>
                <span className="insight-text">{insight}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// 实时监控图表组件
const RealTimeCharts = ({ realTimeData }) => {
  if (!realTimeData) return <div className="chart-placeholder">暂无实时数据</div>;

  return (
    <div className="realtime-charts">
      <div className="chart-container">
        <h3>⚡ 实时监控</h3>
        <div className="chart-content">
          <div className="realtime-metrics">
            <div className="realtime-item">
              <span className="realtime-label">当前在线用户</span>
              <span className="realtime-value">{realTimeData.currentUsers}</span>
            </div>
            <div className="realtime-item">
              <span className="realtime-label">活跃贷款</span>
              <span className="realtime-value">{realTimeData.activeLoans}</span>
            </div>
            <div className="realtime-item">
              <span className="realtime-label">待处理申请</span>
              <span className="realtime-value">{realTimeData.pendingApplications}</span>
            </div>
            <div className="realtime-item">
              <span className="realtime-label">系统健康度</span>
              <span className="realtime-value">{realTimeData.systemHealth}%</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>📋 最近活动</h3>
        <div className="chart-content">
          <div className="recent-activities">
            {realTimeData.recentActivities.map((activity, index) => (
              <div key={index} className="activity-item">
                <span className="activity-time">{activity.time}</span>
                <span className="activity-action">{activity.action}</span>
                <span className="activity-user">{activity.user}</span>
                {activity.amount && (
                  <span className="activity-amount">¥{(activity.amount / 10000).toFixed(1)}万</span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// 高级过滤器组件
const AdvancedFilters = ({ filters, onFilterChange, onReset }) => {
  return (
    <div className="advanced-filters">
      <h4>🔍 高级过滤器</h4>
      <div className="filter-grid">
        <div className="filter-group">
          <label>用户类型</label>
          <select 
            value={filters.userType} 
            onChange={(e) => onFilterChange('userType', e.target.value)}
          >
            <option value="all">全部</option>
            <option value="borrower">借款方</option>
            <option value="lender">放贷方</option>
            <option value="admin">管理员</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>风险等级</label>
          <select 
            value={filters.riskLevel} 
            onChange={(e) => onFilterChange('riskLevel', e.target.value)}
          >
            <option value="all">全部</option>
            <option value="low">低风险</option>
            <option value="medium">中风险</option>
            <option value="high">高风险</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>金额范围</label>
          <select 
            value={filters.amountRange} 
            onChange={(e) => onFilterChange('amountRange', e.target.value)}
          >
            <option value="all">全部</option>
            <option value="0-100000">0-10万</option>
            <option value="100000-500000">10-50万</option>
            <option value="500000-1000000">50-100万</option>
            <option value="1000000+">100万以上</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>地区</label>
          <select 
            value={filters.region} 
            onChange={(e) => onFilterChange('region', e.target.value)}
          >
            <option value="all">全部</option>
            <option value="beijing">北京</option>
            <option value="shanghai">上海</option>
            <option value="guangzhou">广州</option>
            <option value="shenzhen">深圳</option>
            <option value="other">其他</option>
          </select>
        </div>
      </div>
      
      <div className="filter-actions">
        <button className="btn btn-secondary" onClick={onReset}>
          重置过滤器
        </button>
        <button className="btn btn-primary">
          应用过滤器
        </button>
      </div>
    </div>
  );
};

// 数据钻取组件
const DataDrillDown = ({ data, onClose, onBack }) => {
  if (!data) return null;

  return (
    <div className="drill-down-modal">
      <div className="drill-down-content">
        <div className="drill-down-header">
          <h3>📊 数据钻取: {data.title}</h3>
          <div className="drill-down-actions">
            <button className="btn btn-secondary" onClick={onBack}>
              ← 返回
            </button>
            <button className="btn btn-danger" onClick={onClose}>
              ✕ 关闭
            </button>
          </div>
        </div>
        
        <div className="drill-down-body">
          <div className="drill-down-stats">
            {data.stats.map((stat, index) => (
              <div key={index} className="drill-stat">
                <span className="drill-stat-label">{stat.label}</span>
                <span className="drill-stat-value">{stat.value}</span>
              </div>
            ))}
          </div>
          
          <div className="drill-down-chart">
            <h4>详细趋势</h4>
            <div className="chart-placeholder">
              {/* 这里可以集成真实的图表库 */}
              <p>图表数据: {JSON.stringify(data.chartData, null, 2)}</p>
            </div>
          </div>
          
          <div className="drill-down-table">
            <h4>详细数据</h4>
            <table>
              <thead>
                <tr>
                  <th>时间</th>
                  <th>数值</th>
                  <th>变化</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {data.tableData.map((row, index) => (
                  <tr key={index}>
                    <td>{row.time}</td>
                    <td>{row.value}</td>
                    <td className={row.change > 0 ? 'positive' : 'negative'}>
                      {row.change > 0 ? '+' : ''}{row.change}%
                    </td>
                    <td>
                      <button className="btn btn-sm btn-outline">
                        查看详情
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

// 比较模式组件
const ComparisonMode = ({ data, onClose, onAddComparison }) => {
  return (
    <div className="comparison-mode">
      <div className="comparison-header">
        <h3>📈 数据比较模式</h3>
        <button className="btn btn-danger" onClick={onClose}>
          ✕ 关闭比较
        </button>
      </div>
      
      <div className="comparison-content">
        <div className="comparison-selector">
          <h4>选择比较数据</h4>
          <div className="comparison-options">
            <button className="btn btn-outline" onClick={() => onAddComparison('previous')}>
              与上期比较
            </button>
            <button className="btn btn-outline" onClick={() => onAddComparison('year')}>
              与去年同期比较
            </button>
            <button className="btn btn-outline" onClick={() => onAddComparison('custom')}>
              自定义比较
            </button>
          </div>
        </div>
        
        {data && (
          <div className="comparison-results">
            <h4>比较结果</h4>
            <div className="comparison-charts">
              <div className="comparison-chart">
                <h5>当前数据</h5>
                <div className="chart-placeholder">当前数据图表</div>
              </div>
              <div className="comparison-chart">
                <h5>对比数据</h5>
                <div className="chart-placeholder">对比数据图表</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// 智能预警组件
const SmartAlerts = ({ alerts, onDismiss, onConfigure }) => {
  return (
    <div className="smart-alerts">
      <div className="alerts-header">
        <h4>🚨 智能预警</h4>
        <button className="btn btn-sm btn-outline" onClick={onConfigure}>
          配置预警
        </button>
      </div>
      
      <div className="alerts-list">
        {alerts.length === 0 ? (
          <div className="no-alerts">
            <p>暂无预警信息</p>
          </div>
        ) : (
          alerts.map((alert, index) => (
            <div key={index} className={`alert-item ${alert.severity}`}>
              <div className="alert-icon">
                {alert.severity === 'high' ? '🔴' : 
                 alert.severity === 'medium' ? '🟡' : '🟢'}
              </div>
              <div className="alert-content">
                <h5>{alert.title}</h5>
                <p>{alert.message}</p>
                <span className="alert-time">{alert.time}</span>
              </div>
              <div className="alert-actions">
                <button className="btn btn-sm btn-outline">
                  查看详情
                </button>
                <button 
                  className="btn btn-sm btn-danger" 
                  onClick={() => onDismiss(alert.id)}
                >
                  忽略
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// 收藏夹组件
const FavoritesPanel = ({ favorites, onRemove, onAdd }) => {
  return (
    <div className="favorites-panel">
      <div className="favorites-header">
        <h4>⭐ 我的收藏</h4>
        <button className="btn btn-sm btn-primary" onClick={onAdd}>
          + 添加收藏
        </button>
      </div>
      
      <div className="favorites-list">
        {favorites.length === 0 ? (
          <div className="no-favorites">
            <p>暂无收藏的图表</p>
          </div>
        ) : (
          favorites.map((favorite, index) => (
            <div key={index} className="favorite-item">
              <div className="favorite-info">
                <h5>{favorite.title}</h5>
                <p>{favorite.description}</p>
              </div>
              <div className="favorite-actions">
                <button className="btn btn-sm btn-outline">
                  查看
                </button>
                <button 
                  className="btn btn-sm btn-danger" 
                  onClick={() => onRemove(favorite.id)}
                >
                  移除
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// 导出功能组件
const ExportPanel = ({ onExport, format, onFormatChange }) => {
  const exportOptions = [
    { value: 'pdf', label: 'PDF报告', icon: '📄' },
    { value: 'excel', label: 'Excel表格', icon: '📊' },
    { value: 'csv', label: 'CSV数据', icon: '📋' },
    { value: 'image', label: '图片', icon: '🖼️' }
  ];

  return (
    <div className="export-panel">
      <h4>📤 导出数据</h4>
      
      <div className="export-options">
        <div className="format-selector">
          <label>选择格式:</label>
          <div className="format-buttons">
            {exportOptions.map(option => (
              <button
                key={option.value}
                className={`format-btn ${format === option.value ? 'active' : ''}`}
                onClick={() => onFormatChange(option.value)}
              >
                <span className="format-icon">{option.icon}</span>
                <span className="format-label">{option.label}</span>
              </button>
            ))}
          </div>
        </div>
        
        <div className="export-actions">
          <button 
            className="btn btn-primary"
            onClick={() => onExport(format)}
          >
            导出 {exportOptions.find(o => o.value === format)?.label}
          </button>
        </div>
      </div>
    </div>
  );
};

// AI洞察组件
const AIInsights = ({ data, stats, predictions }) => {
  if (!data || !stats) return null;

  const insights = [
    {
      type: 'success',
      title: '业务增长良好',
      description: `贷款申请量较上周增长${Math.floor(Math.random() * 20) + 10}%，建议继续保持当前策略`,
      recommendation: '继续优化用户体验，提升转化率'
    },
    {
      type: 'warning',
      title: '风险评分偏高',
      description: `平均风险评分为${stats.averageRiskScore}，建议加强风险评估流程`,
      recommendation: '优化风险模型，增加更多评估维度'
    },
    {
      type: 'info',
      title: '用户活跃度提升',
      description: `用户注册量增长${Math.floor(Math.random() * 15) + 5}%，活跃用户数量稳定`,
      recommendation: '加强用户留存策略，提升用户粘性'
    }
  ];

  return (
    <div className="ai-insights">
      <h3>🤖 AI智能洞察</h3>
      <div className="insights-grid">
        {insights.map((insight, index) => (
          <div key={index} className={`insight-card ${insight.type}`}>
            <div className="insight-header">
              <span className="insight-icon">
                {insight.type === 'success' ? '✅' : 
                 insight.type === 'warning' ? '⚠️' : 'ℹ️'}
              </span>
              <h4>{insight.title}</h4>
            </div>
            <p className="insight-description">{insight.description}</p>
            <p className="insight-recommendation">
              <strong>建议:</strong> {insight.recommendation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdvancedAnalytics;