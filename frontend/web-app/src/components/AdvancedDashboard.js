import React, { useState, useEffect } from 'react';
import { useUser } from '../contexts/UserContext';
import { useNotification } from './NotificationSystem';
import Charts from './Charts';
import './AdvancedDashboard.css';

const AdvancedDashboard = () => {
  const { user, isAdmin, isBorrower, isLender } = useUser();
  const { showInfo, showSuccess } = useNotification();
  const [dashboardData, setDashboardData] = useState({
    kpis: {},
    charts: {},
    alerts: [],
    recentActivities: [],
    systemHealth: {},
    marketTrends: {},
    userInsights: {}
  });
  const [selectedTimeframe, setSelectedTimeframe] = useState('7days');
  const [isLoading, setIsLoading] = useState(false);
  const [widgets, setWidgets] = useState([]);
  const [customizable, setCustomizable] = useState(false);

  useEffect(() => {
    loadDashboardData();
    loadUserWidgets();
  }, [selectedTimeframe, user]);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const data = {
        kpis: generateKPIs(),
        charts: generateChartData(),
        alerts: generateAlerts(),
        recentActivities: generateRecentActivities(),
        systemHealth: generateSystemHealth(),
        marketTrends: generateMarketTrends(),
        userInsights: generateUserInsights()
      };
      
      setDashboardData(data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadUserWidgets = () => {
    // 根据用户角色加载不同的组件
    const baseWidgets = [
      { id: 'kpi-overview', type: 'kpi', title: '关键指标概览', size: 'large' },
      { id: 'loan-trend', type: 'chart', title: '贷款趋势', size: 'medium' },
      { id: 'risk-distribution', type: 'chart', title: '风险分布', size: 'medium' },
      { id: 'recent-activities', type: 'activity', title: '最近活动', size: 'small' },
      { id: 'system-health', type: 'health', title: '系统健康', size: 'small' }
    ];

    if (isAdmin()) {
      baseWidgets.push(
        { id: 'user-management', type: 'admin', title: '用户管理', size: 'medium' },
        { id: 'system-monitoring', type: 'monitor', title: '系统监控', size: 'large' },
        { id: 'ai-performance', type: 'ai', title: 'AI性能', size: 'medium' }
      );
    }

    if (isBorrower()) {
      baseWidgets.push(
        { id: 'my-loans', type: 'loans', title: '我的贷款', size: 'medium' },
        { id: 'credit-score', type: 'credit', title: '信用评分', size: 'small' },
        { id: 'recommendations', type: 'recommend', title: '推荐产品', size: 'small' }
      );
    }

    if (isLender()) {
      baseWidgets.push(
        { id: 'investment-portfolio', type: 'portfolio', title: '投资组合', size: 'medium' },
        { id: 'market-opportunities', type: 'opportunities', title: '市场机会', size: 'medium' },
        { id: 'risk-analysis', type: 'risk', title: '风险分析', size: 'small' }
      );
    }

    setWidgets(baseWidgets);
  };

  const generateKPIs = () => ({
    totalLoans: Math.floor(Math.random() * 1000) + 500,
    totalAmount: Math.floor(Math.random() * 100000000) + 50000000,
    successRate: (Math.random() * 20 + 80).toFixed(1),
    avgProcessingTime: (Math.random() * 2 + 1).toFixed(1),
    activeUsers: Math.floor(Math.random() * 100) + 50,
    systemUptime: (Math.random() * 5 + 95).toFixed(1),
    aiAccuracy: (Math.random() * 10 + 90).toFixed(1),
    customerSatisfaction: (Math.random() * 2 + 4).toFixed(1)
  });

  const generateChartData = () => ({
    loanTrend: Array.from({ length: 12 }, (_, i) => ({
      month: `2025-${String(i + 1).padStart(2, '0')}`,
      total: Math.floor(Math.random() * 100) + 50,
      approved: Math.floor(Math.random() * 80) + 40,
      rejected: Math.floor(Math.random() * 20) + 10
    })),
    riskDistribution: [
      { level: '低风险', count: Math.floor(Math.random() * 200) + 300 },
      { level: '中风险', count: Math.floor(Math.random() * 150) + 200 },
      { level: '高风险', count: Math.floor(Math.random() * 100) + 100 }
    ],
    industryAnalysis: [
      { name: '科技行业', risks: [85, 70, 60, 75, 80], loanCount: 120 },
      { name: '制造业', risks: [70, 80, 75, 85, 70], loanCount: 95 },
      { name: '零售业', risks: [60, 85, 80, 70, 75], loanCount: 80 },
      { name: '服务业', risks: [75, 75, 70, 80, 85], loanCount: 65 },
      { name: '建筑业', risks: [65, 90, 85, 90, 80], loanCount: 45 }
    ]
  });

  const generateAlerts = () => [
    {
      id: 1,
      type: 'warning',
      title: '系统负载较高',
      message: '当前系统负载达到85%，建议关注',
      timestamp: new Date().toLocaleTimeString(),
      severity: 'medium'
    },
    {
      id: 2,
      type: 'info',
      title: '新用户注册',
      message: '有5个新用户完成注册',
      timestamp: new Date().toLocaleTimeString(),
      severity: 'low'
    },
    {
      id: 3,
      type: 'success',
      title: '批量处理完成',
      message: '1000条贷款申请处理完成',
      timestamp: new Date().toLocaleTimeString(),
      severity: 'low'
    }
  ];

  const generateRecentActivities = () => [
    { id: 1, type: 'loan_approved', user: '张三', amount: 500000, time: '2分钟前' },
    { id: 2, type: 'user_login', user: '李四', amount: null, time: '5分钟前' },
    { id: 3, type: 'risk_assessment', user: '王五', amount: null, time: '8分钟前' },
    { id: 4, type: 'loan_rejected', user: '赵六', amount: 200000, time: '12分钟前' },
    { id: 5, type: 'system_backup', user: '系统', amount: null, time: '15分钟前' }
  ];

  const generateSystemHealth = () => ({
    cpu: Math.floor(Math.random() * 30) + 40,
    memory: Math.floor(Math.random() * 20) + 60,
    disk: Math.floor(Math.random() * 15) + 25,
    network: Math.floor(Math.random() * 10) + 5,
    database: Math.floor(Math.random() * 20) + 30,
    aiService: Math.floor(Math.random() * 25) + 35
  });

  const generateMarketTrends = () => ({
    interestRate: (Math.random() * 2 + 3).toFixed(2),
    marketVolatility: (Math.random() * 20 + 10).toFixed(1),
    creditDemand: Math.floor(Math.random() * 30) + 70,
    riskAppetite: Math.floor(Math.random() * 40) + 60
  });

  const generateUserInsights = () => ({
    loginFrequency: Math.floor(Math.random() * 10) + 5,
    avgSessionTime: Math.floor(Math.random() * 30) + 15,
    featureUsage: {
      riskAssessment: Math.floor(Math.random() * 20) + 80,
      loanApplication: Math.floor(Math.random() * 15) + 70,
      portfolioManagement: Math.floor(Math.random() * 25) + 60
    }
  });

  const handleTimeframeChange = (timeframe) => {
    setSelectedTimeframe(timeframe);
    showInfo(`时间范围已切换到${timeframe === '7days' ? '7天' : timeframe === '30days' ? '30天' : '90天'}`);
  };

  const handleWidgetCustomize = () => {
    setCustomizable(!customizable);
    showInfo(customizable ? '已退出自定义模式' : '已进入自定义模式');
  };

  const handleWidgetReorder = (dragIndex, hoverIndex) => {
    const newWidgets = [...widgets];
    const draggedWidget = newWidgets[dragIndex];
    newWidgets.splice(dragIndex, 1);
    newWidgets.splice(hoverIndex, 0, draggedWidget);
    setWidgets(newWidgets);
  };

  const renderWidget = (widget) => {
    switch (widget.type) {
      case 'kpi':
        return <KPICard key={widget.id} data={dashboardData.kpis} />;
      case 'chart':
        if (widget.id === 'loan-trend') {
          return <Charts.LoanTrend key={widget.id} data={dashboardData.charts.loanTrend} />;
        } else if (widget.id === 'risk-distribution') {
          return <Charts.RiskDistribution key={widget.id} data={dashboardData.charts.riskDistribution} />;
        }
        break;
      case 'activity':
        return <ActivityFeed key={widget.id} data={dashboardData.recentActivities} />;
      case 'health':
        return <SystemHealth key={widget.id} data={dashboardData.systemHealth} />;
      case 'admin':
        return <AdminPanel key={widget.id} />;
      case 'monitor':
        return <SystemMonitor key={widget.id} />;
      case 'ai':
        return <AIPerformance key={widget.id} />;
      case 'loans':
        return <MyLoans key={widget.id} />;
      case 'credit':
        return <CreditScore key={widget.id} />;
      case 'recommend':
        return <Recommendations key={widget.id} />;
      case 'portfolio':
        return <InvestmentPortfolio key={widget.id} />;
      case 'opportunities':
        return <MarketOpportunities key={widget.id} />;
      case 'risk':
        return <RiskAnalysis key={widget.id} />;
      default:
        return null;
    }
  };

  if (isLoading) {
    return (
      <div className="advanced-dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>正在加载仪表板数据...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="advanced-dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>智能仪表板</h1>
          <p>欢迎回来，{user?.fullName}！这里是您的专属数据中心</p>
        </div>
        
        <div className="dashboard-controls">
          <div className="control-group">
            <label>时间范围:</label>
            <select 
              value={selectedTimeframe} 
              onChange={(e) => handleTimeframeChange(e.target.value)}
            >
              <option value="7days">近7天</option>
              <option value="30days">近30天</option>
              <option value="90days">近90天</option>
            </select>
          </div>
          
          <button 
            className={`customize-btn ${customizable ? 'active' : ''}`}
            onClick={handleWidgetCustomize}
          >
            <span className="btn-icon">⚙️</span>
            {customizable ? '完成自定义' : '自定义布局'}
          </button>
          
          <button className="refresh-btn" onClick={loadDashboardData}>
            <span className="btn-icon">🔄</span>
            刷新数据
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="widgets-grid">
          {widgets.map((widget, index) => (
            <div 
              key={widget.id} 
              className={`widget widget-${widget.size} ${customizable ? 'customizable' : ''}`}
              draggable={customizable}
              onDragStart={(e) => e.dataTransfer.setData('text/plain', index)}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const dragIndex = parseInt(e.dataTransfer.getData('text/plain'));
                handleWidgetReorder(dragIndex, index);
              }}
            >
              <div className="widget-header">
                <h3>{widget.title}</h3>
                {customizable && (
                  <button className="remove-widget-btn">×</button>
                )}
              </div>
              <div className="widget-content">
                {renderWidget(widget)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// KPI卡片组件
const KPICard = ({ data }) => (
  <div className="kpi-grid">
    <div className="kpi-item">
      <div className="kpi-icon">💰</div>
      <div className="kpi-content">
        <h4>总贷款数</h4>
        <p className="kpi-value">{data.totalLoans.toLocaleString()}</p>
        <span className="kpi-trend positive">+12.5%</span>
      </div>
    </div>
    <div className="kpi-item">
      <div className="kpi-icon">📊</div>
      <div className="kpi-content">
        <h4>成功率</h4>
        <p className="kpi-value">{data.successRate}%</p>
        <span className="kpi-trend positive">+2.3%</span>
      </div>
    </div>
    <div className="kpi-item">
      <div className="kpi-icon">⏱️</div>
      <div className="kpi-content">
        <h4>处理时间</h4>
        <p className="kpi-value">{data.avgProcessingTime}天</p>
        <span className="kpi-trend negative">-0.5天</span>
      </div>
    </div>
    <div className="kpi-item">
      <div className="kpi-icon">👥</div>
      <div className="kpi-content">
        <h4>活跃用户</h4>
        <p className="kpi-value">{data.activeUsers}</p>
        <span className="kpi-trend positive">+8.2%</span>
      </div>
    </div>
  </div>
);

// 活动流组件
const ActivityFeed = ({ data }) => (
  <div className="activity-feed">
    {data.map(activity => (
      <div key={activity.id} className="activity-item">
        <div className="activity-icon">
          {activity.type === 'loan_approved' ? '✅' :
           activity.type === 'loan_rejected' ? '❌' :
           activity.type === 'user_login' ? '👤' :
           activity.type === 'risk_assessment' ? '🎯' : '⚙️'}
        </div>
        <div className="activity-content">
          <p className="activity-text">
            {activity.user} {activity.type === 'loan_approved' ? '的贷款已批准' :
                            activity.type === 'loan_rejected' ? '的贷款被拒绝' :
                            activity.type === 'user_login' ? '已登录' :
                            activity.type === 'risk_assessment' ? '完成风险评估' : '执行系统操作'}
            {activity.amount && ` (¥${(activity.amount / 10000).toFixed(0)}万)`}
          </p>
          <span className="activity-time">{activity.time}</span>
        </div>
      </div>
    ))}
  </div>
);

// 系统健康组件
const SystemHealth = ({ data }) => (
  <div className="system-health">
    {Object.entries(data).map(([key, value]) => (
      <div key={key} className="health-item">
        <div className="health-label">
          {key === 'cpu' ? 'CPU' :
           key === 'memory' ? '内存' :
           key === 'disk' ? '磁盘' :
           key === 'network' ? '网络' :
           key === 'database' ? '数据库' : 'AI服务'}
        </div>
        <div className="health-bar">
          <div 
            className="health-progress"
            style={{ 
              width: `${value}%`,
              backgroundColor: value > 80 ? '#dc3545' : value > 60 ? '#ffc107' : '#28a745'
            }}
          ></div>
        </div>
        <div className="health-value">{value}%</div>
      </div>
    ))}
  </div>
);

// 其他组件占位符
const AdminPanel = () => <div className="placeholder">管理员面板</div>;
const SystemMonitor = () => <div className="placeholder">系统监控</div>;
const AIPerformance = () => <div className="placeholder">AI性能</div>;
const MyLoans = () => <div className="placeholder">我的贷款</div>;
const CreditScore = () => <div className="placeholder">信用评分</div>;
const Recommendations = () => <div className="placeholder">推荐产品</div>;
const InvestmentPortfolio = () => <div className="placeholder">投资组合</div>;
const MarketOpportunities = () => <div className="placeholder">市场机会</div>;
const RiskAnalysis = () => <div className="placeholder">风险分析</div>;

export default AdvancedDashboard;
