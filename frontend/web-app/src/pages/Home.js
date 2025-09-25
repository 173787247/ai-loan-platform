import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import { useNotification } from '../components/NotificationSystem';
import './Home.css';

function Home() {
  const { isAuthenticated, user } = useUser();
  const { showSuccess } = useNotification();
  const [marketData, setMarketData] = useState(null);
  const [newsData, setNewsData] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());

  // 模拟市场数据
  const generateMarketData = () => ({
    totalLoans: Math.floor(Math.random() * 10000) + 50000,
    activeUsers: Math.floor(Math.random() * 5000) + 15000,
    successRate: (Math.random() * 20 + 80).toFixed(1),
    avgInterestRate: (Math.random() * 3 + 5).toFixed(2),
    marketTrend: Math.random() > 0.5 ? 'up' : 'down',
    trendPercentage: (Math.random() * 5 + 1).toFixed(1)
  });

  // 模拟新闻数据
  const generateNewsData = () => [
    {
      id: 1,
      title: '央行发布最新货币政策，支持小微企业融资',
      summary: '央行宣布降准0.5个百分点，释放流动性约1万亿元',
      time: '2小时前',
      category: '政策',
      importance: 'high'
    },
    {
      id: 2,
      title: 'AI技术在金融风控领域应用取得新突破',
      summary: '新算法将风险评估准确率提升至95%以上',
      time: '4小时前',
      category: '科技',
      importance: 'medium'
    },
    {
      id: 3,
      title: '区块链技术在供应链金融中的创新应用',
      summary: '多家银行联合推出基于区块链的供应链金融产品',
      time: '6小时前',
      category: '创新',
      importance: 'medium'
    }
  ];

  // 模拟用户统计数据
  const generateUserStats = (userType) => {
    if (!userType) return null;
    
    const baseStats = {
      borrower: {
        totalApplications: Math.floor(Math.random() * 10) + 5,
        approvedLoans: Math.floor(Math.random() * 8) + 3,
        totalAmount: Math.floor(Math.random() * 5000000) + 1000000,
        creditScore: Math.floor(Math.random() * 100) + 600
      },
      lender: {
        totalInvestments: Math.floor(Math.random() * 20) + 10,
        activeLoans: Math.floor(Math.random() * 15) + 5,
        totalReturn: Math.floor(Math.random() * 1000000) + 500000,
        avgReturnRate: (Math.random() * 5 + 8).toFixed(2)
      },
      admin: {
        totalUsers: Math.floor(Math.random() * 1000) + 5000,
        systemUptime: '99.9%',
        totalTransactions: Math.floor(Math.random() * 10000) + 50000,
        riskAlerts: Math.floor(Math.random() * 10) + 2
      }
    };
    
    return baseStats[userType] || null;
  };

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setMarketData(generateMarketData());
        setNewsData(generateNewsData());
        if (isAuthenticated()) {
          setUserStats(generateUserStats(user?.userType));
        }
      } catch (error) {
        console.error('加载数据失败:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();

    // 更新时间
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, [isAuthenticated, user]);

  const getPersonalizedRecommendations = () => {
    if (!isAuthenticated() || !user) return [];
    
    const recommendations = {
      borrower: [
        { title: '提升信用评分', description: '完善个人信息可提升信用评分', action: '完善资料', link: '/profile' },
        { title: '申请快速贷款', description: '基于您的信用状况，推荐快速审批产品', action: '立即申请', link: '/auto-matching' },
        { title: '查看贷款历史', description: '查看您的贷款申请记录和状态', action: '查看详情', link: '/dashboard' }
      ],
      lender: [
        { title: '投资机会推荐', description: '基于风险偏好，为您推荐优质投资项目', action: '查看机会', link: '/auto-matching' },
        { title: '投资组合分析', description: '分析您的投资组合表现和风险', action: '查看分析', link: '/analytics' },
        { title: '市场趋势报告', description: '获取最新的市场趋势和投资建议', action: '查看报告', link: '/reports' }
      ],
      admin: [
        { title: '系统监控', description: '查看系统运行状态和性能指标', action: '进入监控', link: '/monitoring' },
        { title: '用户管理', description: '管理用户账户和权限设置', action: '管理用户', link: '/dashboard' },
        { title: '风险预警', description: '查看当前风险预警和处理建议', action: '查看预警', link: '/risk-management' }
      ]
    };
    
    return recommendations[user.userType] || [];
  };

  const getQuickActions = () => {
    if (!isAuthenticated()) return [];
    
    const actions = {
      borrower: [
        { name: '申请贷款', icon: '💰', link: '/auto-matching', color: '#4CAF50' },
        { name: '风险评估', icon: '🔍', link: '/risk-assessment', color: '#2196F3' },
        { name: '我的贷款', icon: '📋', link: '/dashboard', color: '#FF9800' }
      ],
      lender: [
        { name: '投资机会', icon: '📈', link: '/auto-matching', color: '#4CAF50' },
        { name: '投资组合', icon: '💼', link: '/dashboard', color: '#2196F3' },
        { name: '风险分析', icon: '⚠️', link: '/analytics', color: '#FF9800' }
      ],
      admin: [
        { name: '系统监控', icon: '📊', link: '/monitoring', color: '#4CAF50' },
        { name: '用户管理', icon: '👥', link: '/dashboard', color: '#2196F3' },
        { name: '数据分析', icon: '📈', link: '/analytics', color: '#FF9800' }
      ]
    };
    
    return actions[user?.userType] || [];
  };

  return (
    <div className="home">
      <header className="home-header">
        <div className="header-content">
          <h1>AI助贷招标平台</h1>
          <p>智能金融科技解决方案</p>
          <div className="current-time">
            {currentTime.toLocaleString('zh-CN', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit'
            })}
          </div>
        </div>

        {/* 市场数据概览 */}
        {marketData && (
          <div className="market-overview">
            <h3>📊 市场概览</h3>
            <div className="market-stats">
              <div className="stat-item">
                <span className="stat-value">{marketData.totalLoans.toLocaleString()}</span>
                <span className="stat-label">累计贷款</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{marketData.activeUsers.toLocaleString()}</span>
                <span className="stat-label">活跃用户</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{marketData.successRate}%</span>
                <span className="stat-label">成功率</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{marketData.avgInterestRate}%</span>
                <span className="stat-label">平均利率</span>
                <span className={`trend ${marketData.marketTrend}`}>
                  {marketData.marketTrend === 'up' ? '↗' : '↘'} {marketData.trendPercentage}%
                </span>
              </div>
            </div>
          </div>
        )}

        <div className="cta-section">
          {isAuthenticated() ? (
            <div className="welcome-message">
              <h2>欢迎回来，{user?.username}！</h2>
              <p>您当前身份：{user?.userType === 'admin' ? '管理员' : user?.userType === 'borrower' ? '借款方' : '放贷方'}</p>
              
              {/* 用户统计信息 */}
              {userStats && (
                <div className="user-stats">
                  <h4>您的数据概览</h4>
                  <div className="stats-grid">
                    {Object.entries(userStats).map(([key, value]) => (
                      <div key={key} className="user-stat">
                        <span className="user-stat-value">{value}</span>
                        <span className="user-stat-label">
                          {key === 'totalApplications' ? '申请次数' :
                           key === 'approvedLoans' ? '获批贷款' :
                           key === 'totalAmount' ? '总金额' :
                           key === 'creditScore' ? '信用评分' :
                           key === 'totalInvestments' ? '投资次数' :
                           key === 'activeLoans' ? '活跃投资' :
                           key === 'totalReturn' ? '总收益' :
                           key === 'avgReturnRate' ? '平均收益率' :
                           key === 'totalUsers' ? '用户总数' :
                           key === 'systemUptime' ? '系统可用率' :
                           key === 'totalTransactions' ? '交易总数' :
                           key === 'riskAlerts' ? '风险预警' : key}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 个性化推荐 */}
              <div className="personalized-recommendations">
                <h4>💡 为您推荐</h4>
                <div className="recommendations-grid">
                  {getPersonalizedRecommendations().map((rec, index) => (
                    <div key={index} className="recommendation-card">
                      <h5>{rec.title}</h5>
                      <p>{rec.description}</p>
                      <Link to={rec.link} className="btn btn-sm btn-outline">
                        {rec.action}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>

              {/* 快速操作 */}
              <div className="quick-actions">
                <h4>⚡ 快速操作</h4>
                <div className="actions-grid">
                  {getQuickActions().map((action, index) => (
                    <Link key={index} to={action.link} className="action-card" style={{ '--action-color': action.color }}>
                      <div className="action-icon">{action.icon}</div>
                      <span className="action-name">{action.name}</span>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="login-prompt">
              <h2>开始您的智能助贷之旅</h2>
              <p>请先登录或注册账户以使用完整功能</p>
              <Link to="/login" className="btn btn-primary">
                立即登录
              </Link>
            </div>
          )}
        </div>

        {/* 功能卡片 */}
        <div className="features">
          <Link to="/risk-assessment" className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>智能风险评估</h3>
            <p>基于AI的贷款风险评估系统</p>
            <div className="feature-arrow">→</div>
          </Link>
          <Link to="/auto-matching" className="feature-card">
            <div className="feature-icon">🤝</div>
            <h3>自动化匹配</h3>
            <p>智能匹配借贷双方需求</p>
            <div className="feature-arrow">→</div>
          </Link>
          <Link to="/monitoring" className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>实时监控</h3>
            <p>全流程实时监控和管理</p>
            <div className="feature-arrow">→</div>
          </Link>
          <Link to="/analytics" className="feature-card">
            <div className="feature-icon">📈</div>
            <h3>数据分析</h3>
            <p>深度数据分析和智能洞察</p>
            <div className="feature-arrow">→</div>
          </Link>
        </div>

        {/* 最新资讯 */}
        {newsData.length > 0 && (
          <div className="news-section">
            <h3>📰 最新资讯</h3>
            <div className="news-grid">
              {newsData.map(news => (
                <div key={news.id} className={`news-card ${news.importance}`}>
                  <div className="news-header">
                    <span className="news-category">{news.category}</span>
                    <span className="news-time">{news.time}</span>
                  </div>
                  <h4 className="news-title">{news.title}</h4>
                  <p className="news-summary">{news.summary}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default Home;
