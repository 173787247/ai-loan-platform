import React, { useState, useEffect } from 'react';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    totalLoans: 0,
    totalAmount: 0,
    activeLoans: 0,
    pendingLoans: 0,
    approvedLoans: 0,
    rejectedLoans: 0,
    totalUsers: 0,
    newUsers: 0,
    avgRiskScore: 0,
    successRate: 0
  });

  const [recentLoans, setRecentLoans] = useState([]);
  const [systemHealth, setSystemHealth] = useState({});

  useEffect(() => {
    // 模拟数据加载
    const loadDashboardData = () => {
      setStats({
        totalLoans: 1247,
        totalAmount: 156800,
        activeLoans: 89,
        pendingLoans: 23,
        approvedLoans: 1156,
        rejectedLoans: 68,
        totalUsers: 456,
        newUsers: 12,
        avgRiskScore: 45,
        successRate: 94.5
      });

      setRecentLoans([
        {
          id: 1,
          company: '北京科技有限公司',
          amount: 500,
          status: 'approved',
          riskScore: 35,
          date: '2025-09-21'
        },
        {
          id: 2,
          company: '上海制造有限公司',
          amount: 1000,
          status: 'pending',
          riskScore: 65,
          date: '2025-09-21'
        },
        {
          id: 3,
          company: '深圳贸易公司',
          amount: 300,
          status: 'rejected',
          riskScore: 85,
          date: '2025-09-20'
        },
        {
          id: 4,
          company: '广州服务公司',
          amount: 800,
          status: 'approved',
          riskScore: 40,
          date: '2025-09-20'
        }
      ]);

      setSystemHealth({
        apiGateway: 'online',
        aiService: 'online',
        database: 'online',
        cache: 'online',
        messageQueue: 'warning',
        monitoring: 'offline'
      });
    };

    loadDashboardData();
    
    // 模拟实时数据更新
    const interval = setInterval(() => {
      setStats(prev => ({
        ...prev,
        activeLoans: prev.activeLoans + Math.floor(Math.random() * 3) - 1,
        newUsers: prev.newUsers + Math.floor(Math.random() * 2)
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved': return 'status-approved';
      case 'pending': return 'status-pending';
      case 'rejected': return 'status-rejected';
      default: return '';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'approved': return '已批准';
      case 'pending': return '待审核';
      case 'rejected': return '已拒绝';
      default: return status;
    }
  };

  const getHealthStatus = (status) => {
    switch (status) {
      case 'online': return { text: '在线', class: 'health-online' };
      case 'warning': return { text: '警告', class: 'health-warning' };
      case 'offline': return { text: '离线', class: 'health-offline' };
      default: return { text: '未知', class: 'health-unknown' };
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>仪表盘</h1>
        <p>AI助贷招标平台实时数据概览</p>
      </div>

      {/* 统计卡片 */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>总贷款数</h3>
            <div className="stat-value">{stats.totalLoans.toLocaleString()}</div>
            <div className="stat-change positive">+12% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💵</div>
          <div className="stat-content">
            <h3>总金额</h3>
            <div className="stat-value">¥{stats.totalAmount.toLocaleString()}万</div>
            <div className="stat-change positive">+8% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔄</div>
          <div className="stat-content">
            <h3>活跃贷款</h3>
            <div className="stat-value">{stats.activeLoans}</div>
            <div className="stat-change">实时更新</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <h3>待审核</h3>
            <div className="stat-value">{stats.pendingLoans}</div>
            <div className="stat-change">需要处理</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>已批准</h3>
            <div className="stat-value">{stats.approvedLoans}</div>
            <div className="stat-change positive">+15% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">❌</div>
          <div className="stat-content">
            <h3>已拒绝</h3>
            <div className="stat-value">{stats.rejectedLoans}</div>
            <div className="stat-change negative">-5% 本月</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>总用户数</h3>
            <div className="stat-value">{stats.totalUsers}</div>
            <div className="stat-change positive">+{stats.newUsers} 今日</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>平均风险评分</h3>
            <div className="stat-value">{stats.avgRiskScore}</div>
            <div className="stat-change">风险可控</div>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        {/* 最近贷款申请 */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">最近贷款申请</h2>
            <button className="btn btn-primary">查看全部</button>
          </div>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>申请ID</th>
                  <th>企业名称</th>
                  <th>贷款金额</th>
                  <th>风险评分</th>
                  <th>状态</th>
                  <th>申请日期</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {recentLoans.map(loan => (
                  <tr key={loan.id}>
                    <td>#{loan.id}</td>
                    <td>{loan.company}</td>
                    <td>¥{loan.amount}万</td>
                    <td>
                      <span className={`risk-score ${loan.riskScore < 40 ? 'low' : loan.riskScore < 70 ? 'medium' : 'high'}`}>
                        {loan.riskScore}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${getStatusColor(loan.status)}`}>
                        {getStatusText(loan.status)}
                      </span>
                    </td>
                    <td>{loan.date}</td>
                    <td>
                      <button className="btn btn-primary" style={{ padding: '5px 10px', fontSize: '0.8rem' }}>
                        查看详情
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 系统健康状态 */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">系统健康状态</h2>
            <span className="last-update">最后更新: {new Date().toLocaleTimeString()}</span>
          </div>
          <div className="health-grid">
            {Object.entries(systemHealth).map(([service, status]) => {
              const health = getHealthStatus(status);
              return (
                <div key={service} className="health-item">
                  <div className="health-service">
                    <span className="service-name">{service}</span>
                    <span className={`health-status ${health.class}`}>
                      {health.text}
                    </span>
                  </div>
                  <div className="health-indicator">
                    <div className={`indicator-dot ${health.class}`}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
