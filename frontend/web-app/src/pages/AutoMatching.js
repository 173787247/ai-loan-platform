import React, { useState, useEffect } from 'react';
import './AutoMatching.css';

function AutoMatching() {
  const [borrowers, setBorrowers] = useState([]);
  const [lenders, setLenders] = useState([]);
  const [matches, setMatches] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // 模拟数据
  useEffect(() => {
    const mockBorrowers = [
      {
        id: 1,
        name: '北京科技有限公司',
        amount: 500,
        term: 24,
        rate: 8.5,
        risk: '低',
        industry: '科技'
      },
      {
        id: 2,
        name: '上海制造有限公司',
        amount: 1000,
        term: 36,
        rate: 9.2,
        risk: '中',
        industry: '制造业'
      },
      {
        id: 3,
        name: '深圳贸易公司',
        amount: 300,
        term: 12,
        rate: 7.8,
        risk: '低',
        industry: '贸易'
      }
    ];

    const mockLenders = [
      {
        id: 1,
        name: '招商银行',
        availableAmount: 2000,
        minRate: 7.0,
        maxTerm: 36,
        riskPreference: '低'
      },
      {
        id: 2,
        name: '建设银行',
        availableAmount: 1500,
        minRate: 8.0,
        maxTerm: 24,
        riskPreference: '中'
      },
      {
        id: 3,
        name: '工商银行',
        availableAmount: 3000,
        minRate: 6.5,
        maxTerm: 48,
        riskPreference: '低'
      }
    ];

    setBorrowers(mockBorrowers);
    setLenders(mockLenders);
  }, []);

  const runMatching = async () => {
    setIsLoading(true);
    
    // 模拟AI匹配算法
    setTimeout(() => {
      const mockMatches = [
        {
          id: 1,
          borrower: borrowers[0],
          lender: lenders[0],
          matchScore: 95,
          suggestedRate: 8.0,
          status: '推荐'
        },
        {
          id: 2,
          borrower: borrowers[1],
          lender: lenders[2],
          matchScore: 88,
          suggestedRate: 8.5,
          status: '推荐'
        },
        {
          id: 3,
          borrower: borrowers[2],
          lender: lenders[1],
          matchScore: 82,
          suggestedRate: 8.2,
          status: '备选'
        }
      ];
      
      setMatches(mockMatches);
      setIsLoading(false);
    }, 2000);
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case '低': return '#4ecdc4';
      case '中': return '#feca57';
      case '高': return '#ff6b6b';
      default: return '#95a5a6';
    }
  };

  const getMatchColor = (score) => {
    if (score >= 90) return '#4ecdc4';
    if (score >= 80) return '#feca57';
    return '#ff6b6b';
  };

  return (
    <div className="auto-matching">
      <div className="container">
        <h1>自动化匹配</h1>
        <p className="subtitle">智能匹配借贷双方需求</p>
        
        <div className="matching-controls">
          <button 
            className="match-btn" 
            onClick={runMatching}
            disabled={isLoading}
          >
            {isLoading ? 'AI匹配中...' : '开始智能匹配'}
          </button>
        </div>

        <div className="data-sections">
          <div className="section">
            <h2>借款方</h2>
            <div className="data-grid">
              {borrowers.map(borrower => (
                <div key={borrower.id} className="data-card">
                  <h3>{borrower.name}</h3>
                  <div className="data-row">
                    <span>贷款金额:</span>
                    <span>{borrower.amount}万元</span>
                  </div>
                  <div className="data-row">
                    <span>期限:</span>
                    <span>{borrower.term}个月</span>
                  </div>
                  <div className="data-row">
                    <span>期望利率:</span>
                    <span>{borrower.rate}%</span>
                  </div>
                  <div className="data-row">
                    <span>风险等级:</span>
                    <span 
                      className="risk-badge"
                      style={{ backgroundColor: getRiskColor(borrower.risk) }}
                    >
                      {borrower.risk}风险
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="section">
            <h2>放贷方</h2>
            <div className="data-grid">
              {lenders.map(lender => (
                <div key={lender.id} className="data-card">
                  <h3>{lender.name}</h3>
                  <div className="data-row">
                    <span>可用资金:</span>
                    <span>{lender.availableAmount}万元</span>
                  </div>
                  <div className="data-row">
                    <span>最低利率:</span>
                    <span>{lender.minRate}%</span>
                  </div>
                  <div className="data-row">
                    <span>最长期限:</span>
                    <span>{lender.maxTerm}个月</span>
                  </div>
                  <div className="data-row">
                    <span>风险偏好:</span>
                    <span 
                      className="risk-badge"
                      style={{ backgroundColor: getRiskColor(lender.riskPreference) }}
                    >
                      {lender.riskPreference}风险
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {matches.length > 0 && (
          <div className="matches-section">
            <h2>匹配结果</h2>
            <div className="matches-grid">
              {matches.map(match => (
                <div key={match.id} className="match-card">
                  <div className="match-header">
                    <h3>匹配 #{match.id}</h3>
                    <div 
                      className="match-score"
                      style={{ backgroundColor: getMatchColor(match.matchScore) }}
                    >
                      {match.matchScore}分
                    </div>
                  </div>
                  
                  <div className="match-content">
                    <div className="match-parties">
                      <div className="party">
                        <h4>借款方</h4>
                        <p>{match.borrower.name}</p>
                        <p>{match.borrower.amount}万元 / {match.borrower.term}个月</p>
                      </div>
                      
                      <div className="match-arrow">↔</div>
                      
                      <div className="party">
                        <h4>放贷方</h4>
                        <p>{match.lender.name}</p>
                        <p>可用: {match.lender.availableAmount}万元</p>
                      </div>
                    </div>
                    
                    <div className="match-details">
                      <div className="detail-row">
                        <span>建议利率:</span>
                        <span className="rate">{match.suggestedRate}%</span>
                      </div>
                      <div className="detail-row">
                        <span>匹配状态:</span>
                        <span className={`status ${match.status.toLowerCase()}`}>
                          {match.status}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AutoMatching;
