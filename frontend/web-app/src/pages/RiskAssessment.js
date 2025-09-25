import React, { useState } from 'react';
import './RiskAssessment.css';

function RiskAssessment() {
  const [formData, setFormData] = useState({
    companyName: '',
    annualRevenue: '',
    loanAmount: '',
    loanTerm: '',
    industry: '',
    businessAge: ''
  });

  const [creditData, setCreditData] = useState({
    creditScore: null,
    creditLevel: '',
    isQuerying: false,
    queryError: null
  });

  const [assessmentResult, setAssessmentResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // 查询信用评分
  const queryCreditScore = async () => {
    if (!formData.companyName.trim()) {
      alert('请先输入企业名称');
      return;
    }

    setCreditData(prev => ({ ...prev, isQuerying: true, queryError: null }));

    try {
      // 调用真实的征信API
      const response = await fetch('http://localhost:8000/api/v1/credit/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_name: formData.companyName,
          provider: 'jingdong' // 默认使用京东万象
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setCreditData({
          creditScore: result.data.credit_score,
          creditLevel: result.data.credit_level,
          creditSource: result.data.credit_source,
          queryTime: result.data.query_time,
          isMock: result.data.is_mock,
          isQuerying: false,
          queryError: null
        });
      } else {
        throw new Error(result.message || '征信查询失败');
      }
    } catch (error) {
      console.error('征信查询失败:', error);
      setCreditData(prev => ({
        ...prev,
        isQuerying: false,
        queryError: '征信查询失败，请重试'
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 检查是否已查询信用评分
    if (!creditData.creditScore) {
      alert('请先查询企业信用评分');
      return;
    }
    
    setIsLoading(true);
    
    // 模拟AI风险评估API调用
    setTimeout(() => {
      // 基于输入数据计算风险评分
      let riskScore = 0;
      const factors = [];
      
      // 信用评分影响 (300-850分) - FICO标准
      const creditScore = creditData.creditScore;
      if (creditScore >= 800) {
        riskScore += 5;  // 优秀信用，风险很低
        factors.push('企业信用记录优秀');
      } else if (creditScore >= 740) {
        riskScore += 10; // 很好信用，风险很低
        factors.push('企业信用记录很好');
      } else if (creditScore >= 670) {
        riskScore += 20; // 良好信用，风险较低
        factors.push('企业信用记录良好');
      } else if (creditScore >= 580) {
        riskScore += 40; // 一般信用，风险中等
        factors.push('企业信用记录一般');
      } else {
        riskScore += 70; // 很差信用，风险很高
        factors.push('企业信用记录很差');
      }
      
      // 年收入影响 - 行业标准
      const annualRevenue = parseInt(formData.annualRevenue);
      if (annualRevenue >= 10000) {
        riskScore += 5;  // 高收入，风险很低
        factors.push('年收入稳定增长');
      } else if (annualRevenue >= 5000) {
        riskScore += 10; // 较高收入，风险较低
        factors.push('年收入稳定');
      } else if (annualRevenue >= 1000) {
        riskScore += 20; // 中等收入，风险中等
        factors.push('年收入一般');
      } else {
        riskScore += 40; // 低收入，风险较高
        factors.push('年收入较低');
      }
      
      // 贷款金额与年收入比例 - 行业标准
      const loanAmount = parseInt(formData.loanAmount);
      const loanToRevenueRatio = loanAmount / annualRevenue;
      if (loanToRevenueRatio <= 0.1) {
        riskScore += 5;  // 比例很低，风险很低
        factors.push('贷款金额合理');
      } else if (loanToRevenueRatio <= 0.3) {
        riskScore += 15; // 比例适中，风险较低
        factors.push('贷款金额适中');
      } else if (loanToRevenueRatio <= 0.5) {
        riskScore += 30; // 比例偏高，风险中等
        factors.push('贷款金额偏高');
      } else {
        riskScore += 50; // 比例过高，风险较高
        factors.push('贷款金额过高');
      }
      
      // 经营年限影响 - 行业标准
      const businessAge = parseInt(formData.businessAge);
      if (businessAge >= 15) {
        riskScore += 5;  // 经营年限很长，风险很低
        factors.push('经营年限充足');
      } else if (businessAge >= 10) {
        riskScore += 10; // 经营年限较长，风险较低
        factors.push('经营年限良好');
      } else if (businessAge >= 5) {
        riskScore += 20; // 经营年限适中，风险中等
        factors.push('经营年限适中');
      } else if (businessAge >= 3) {
        riskScore += 35; // 经营年限较短，风险较高
        factors.push('经营年限较短');
      } else {
        riskScore += 50; // 经营年限很短，风险很高
        factors.push('经营年限很短');
      }
      
      // 行业风险评估 - 行业标准
      const industry = formData.industry;
      if (['technology', 'finance', 'healthcare'].includes(industry)) {
        riskScore += 5;  // 朝阳行业，风险很低
        factors.push('行业前景良好');
      } else if (['manufacturing', 'retail', 'service'].includes(industry)) {
        riskScore += 15; // 传统行业，风险较低
        factors.push('行业前景一般');
      } else if (['construction', 'agriculture'].includes(industry)) {
        riskScore += 25; // 周期性行业，风险中等
        factors.push('行业风险中等');
      } else {
        riskScore += 35; // 其他行业，风险较高
        factors.push('行业风险较高');
      }
      
      // 确保风险评分在0-100范围内
      riskScore = Math.min(Math.max(riskScore, 0), 100);
      
      // 风险等级判断 - 行业标准 (分数越高风险越高)
      const riskLevel = riskScore <= 30 ? '低风险' : 
                       riskScore <= 60 ? '中风险' : 
                       riskScore <= 80 ? '高风险' : '极高风险';
      
      // 贷款建议 - 行业标准
      const recommendation = riskScore <= 30 ? '建议批准贷款' : 
                           riskScore <= 60 ? '建议进一步审核' : 
                           riskScore <= 80 ? '建议拒绝贷款' : '强烈建议拒绝贷款';
      
      setAssessmentResult({
        riskScore,
        riskLevel,
        recommendation,
        factors
      });
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="risk-assessment">
      <div className="container">
        <h1>智能风险评估</h1>
        <p className="subtitle">基于AI的贷款风险评估系统</p>
        
        <div className="assessment-form">
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label>企业名称</label>
                <input
                  type="text"
                  name="companyName"
                  value={formData.companyName}
                  onChange={handleInputChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>年收入 (万元)</label>
                <input
                  type="number"
                  name="annualRevenue"
                  value={formData.annualRevenue}
                  onChange={handleInputChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>企业信用评分</label>
                <div className="credit-query-section">
                  {creditData.creditScore ? (
                    <div className="credit-result">
                      <div className="credit-info">
                        <div className="credit-score-display">
                          <span className="score">{creditData.creditScore}</span>
                          <span className="level">({creditData.creditLevel})</span>
                        </div>
                        <div className="credit-details">
                          <div className="credit-source">
                            <strong>数据来源：</strong>{creditData.creditSource}
                            {creditData.isMock && <span className="mock-badge"> (模拟数据)</span>}
                          </div>
                          <div className="query-time">
                            <strong>查询时间：</strong>{creditData.queryTime}
                          </div>
                        </div>
                      </div>
                      <button 
                        type="button" 
                        onClick={queryCreditScore}
                        className="btn-refresh"
                        disabled={creditData.isQuerying}
                      >
                        {creditData.isQuerying ? '查询中...' : '重新查询'}
                      </button>
                    </div>
                  ) : (
                    <div className="credit-query">
                      <button 
                        type="button" 
                        onClick={queryCreditScore}
                        className="btn-query"
                        disabled={creditData.isQuerying}
                      >
                        {creditData.isQuerying ? '正在查询征信...' : '查询企业信用评分'}
                      </button>
                      {creditData.queryError && (
                        <div className="error-message">{creditData.queryError}</div>
                      )}
                    </div>
                  )}
                </div>
                <small className="form-hint">
                  <strong>演示模式：</strong>当前显示的是模拟数据，实际部署时需要接入真实的征信API
                  <br />
                  <strong>真实征信API：</strong>央行征信中心、百行征信、芝麻信用、腾讯征信等
                </small>
              </div>
              
              <div className="form-group">
                <label>贷款金额 (万元)</label>
                <input
                  type="number"
                  name="loanAmount"
                  value={formData.loanAmount}
                  onChange={handleInputChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>贷款期限 (月)</label>
                <select
                  name="loanTerm"
                  value={formData.loanTerm}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">请选择</option>
                  <option value="6">6个月</option>
                  <option value="12">12个月</option>
                  <option value="24">24个月</option>
                  <option value="36">36个月</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>所属行业</label>
                <select
                  name="industry"
                  value={formData.industry}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">请选择</option>
                  <option value="manufacturing">制造业</option>
                  <option value="technology">科技行业</option>
                  <option value="retail">零售业</option>
                  <option value="service">服务业</option>
                  <option value="construction">建筑业</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>经营年限</label>
                <input
                  type="number"
                  name="businessAge"
                  value={formData.businessAge}
                  onChange={handleInputChange}
                  min="1"
                  required
                />
              </div>
            </div>
            
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? 'AI分析中...' : '开始风险评估'}
            </button>
          </form>
        </div>
        
        {assessmentResult && (
          <div className="assessment-result">
            <h2>风险评估结果</h2>
            <div className="result-card">
              <div className="risk-score">
                <div className="score-circle">
                  <span className="score">{assessmentResult.riskScore}</span>
                  <span className="score-label">风险评分</span>
                </div>
                <div className="risk-level">
                  <h3>风险等级: {assessmentResult.riskLevel}</h3>
                  <p>{assessmentResult.recommendation}</p>
                </div>
              </div>
              
              <div className="risk-factors">
                <h4>关键风险因素</h4>
                <ul>
                  {assessmentResult.factors.map((factor, index) => (
                    <li key={index}>{factor}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RiskAssessment;
