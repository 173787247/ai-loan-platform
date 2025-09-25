import React, { useState, useEffect } from 'react';
import './LoanManagement.css';

function LoanManagement() {
  const [loans, setLoans] = useState([]);
  const [filters, setFilters] = useState({
    status: 'all',
    riskLevel: 'all',
    amountRange: 'all'
  });
  const [selectedLoan, setSelectedLoan] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    // 模拟数据加载
    const mockLoans = [
      {
        id: 1,
        company: '北京科技有限公司',
        amount: 500,
        term: 24,
        rate: 8.5,
        riskScore: 35,
        status: 'approved',
        applicationDate: '2025-09-21',
        approvalDate: '2025-09-21',
        borrower: '张三',
        phone: '138****1234',
        industry: '科技'
      },
      {
        id: 2,
        company: '上海制造有限公司',
        amount: 1000,
        term: 36,
        rate: 9.2,
        riskScore: 65,
        status: 'pending',
        applicationDate: '2025-09-21',
        approvalDate: null,
        borrower: '李四',
        phone: '139****5678',
        industry: '制造业'
      },
      {
        id: 3,
        company: '深圳贸易公司',
        amount: 300,
        term: 12,
        rate: 7.8,
        riskScore: 85,
        status: 'rejected',
        applicationDate: '2025-09-20',
        approvalDate: '2025-09-20',
        borrower: '王五',
        phone: '137****9012',
        industry: '贸易'
      },
      {
        id: 4,
        company: '广州服务公司',
        amount: 800,
        term: 18,
        rate: 8.0,
        riskScore: 40,
        status: 'approved',
        applicationDate: '2025-09-20',
        approvalDate: '2025-09-20',
        borrower: '赵六',
        phone: '136****3456',
        industry: '服务业'
      },
      {
        id: 5,
        company: '杭州电商公司',
        amount: 1200,
        term: 30,
        rate: 9.5,
        riskScore: 70,
        status: 'pending',
        applicationDate: '2025-09-19',
        approvalDate: null,
        borrower: '孙七',
        phone: '135****7890',
        industry: '电商'
      }
    ];

    setLoans(mockLoans);
  }, []);

  const filteredLoans = loans.filter(loan => {
    if (filters.status !== 'all' && loan.status !== filters.status) return false;
    if (filters.riskLevel !== 'all') {
      const riskLevel = loan.riskScore < 40 ? 'low' : loan.riskScore < 70 ? 'medium' : 'high';
      if (riskLevel !== filters.riskLevel) return false;
    }
    if (filters.amountRange !== 'all') {
      const amount = loan.amount;
      switch (filters.amountRange) {
        case 'low': if (amount >= 500) return false; break;
        case 'medium': if (amount < 500 || amount >= 1000) return false; break;
        case 'high': if (amount < 1000) return false; break;
      }
    }
    return true;
  });

  const handleStatusChange = (loanId, newStatus) => {
    setLoans(prev => prev.map(loan => 
      loan.id === loanId 
        ? { ...loan, status: newStatus, approvalDate: newStatus !== 'pending' ? new Date().toISOString().split('T')[0] : null }
        : loan
    ));
  };

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

  const getRiskLevel = (score) => {
    if (score < 40) return { level: '低风险', class: 'risk-low' };
    if (score < 70) return { level: '中风险', class: 'risk-medium' };
    return { level: '高风险', class: 'risk-high' };
  };

  return (
    <div className="loan-management">
      <div className="page-header">
        <h1>贷款管理</h1>
        <p>管理所有贷款申请和审批流程</p>
      </div>

      {/* 筛选器 */}
      <div className="card">
        <div className="filters">
          <div className="filter-group">
            <label>状态筛选</label>
            <select 
              value={filters.status} 
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            >
              <option value="all">全部状态</option>
              <option value="pending">待审核</option>
              <option value="approved">已批准</option>
              <option value="rejected">已拒绝</option>
            </select>
          </div>

          <div className="filter-group">
            <label>风险等级</label>
            <select 
              value={filters.riskLevel} 
              onChange={(e) => setFilters(prev => ({ ...prev, riskLevel: e.target.value }))}
            >
              <option value="all">全部等级</option>
              <option value="low">低风险</option>
              <option value="medium">中风险</option>
              <option value="high">高风险</option>
            </select>
          </div>

          <div className="filter-group">
            <label>金额范围</label>
            <select 
              value={filters.amountRange} 
              onChange={(e) => setFilters(prev => ({ ...prev, amountRange: e.target.value }))}
            >
              <option value="all">全部金额</option>
              <option value="low">500万以下</option>
              <option value="medium">500-1000万</option>
              <option value="high">1000万以上</option>
            </select>
          </div>

          <button className="btn btn-primary">导出数据</button>
        </div>
      </div>

      {/* 贷款列表 */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">贷款申请列表</h2>
          <div className="card-actions">
            <span className="total-count">共 {filteredLoans.length} 条记录</span>
          </div>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>申请ID</th>
                <th>企业名称</th>
                <th>申请人</th>
                <th>贷款金额</th>
                <th>期限</th>
                <th>利率</th>
                <th>风险评分</th>
                <th>状态</th>
                <th>申请日期</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredLoans.map(loan => {
                const risk = getRiskLevel(loan.riskScore);
                return (
                  <tr key={loan.id}>
                    <td>#{loan.id}</td>
                    <td>
                      <div className="company-info">
                        <div className="company-name">{loan.company}</div>
                        <div className="company-industry">{loan.industry}</div>
                      </div>
                    </td>
                    <td>
                      <div className="borrower-info">
                        <div className="borrower-name">{loan.borrower}</div>
                        <div className="borrower-phone">{loan.phone}</div>
                      </div>
                    </td>
                    <td>¥{loan.amount}万</td>
                    <td>{loan.term}个月</td>
                    <td>{loan.rate}%</td>
                    <td>
                      <div className="risk-info">
                        <span className={`risk-score ${risk.class}`}>
                          {loan.riskScore}
                        </span>
                        <div className="risk-level">{risk.level}</div>
                      </div>
                    </td>
                    <td>
                      <span className={`status-badge ${getStatusColor(loan.status)}`}>
                        {getStatusText(loan.status)}
                      </span>
                    </td>
                    <td>{loan.applicationDate}</td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="btn btn-primary"
                          onClick={() => {
                            setSelectedLoan(loan);
                            setShowModal(true);
                          }}
                        >
                          查看详情
                        </button>
                        {loan.status === 'pending' && (
                          <>
                            <button 
                              className="btn btn-success"
                              onClick={() => handleStatusChange(loan.id, 'approved')}
                            >
                              批准
                            </button>
                            <button 
                              className="btn btn-danger"
                              onClick={() => handleStatusChange(loan.id, 'rejected')}
                            >
                              拒绝
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* 详情模态框 */}
      {showModal && selectedLoan && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>贷款申请详情 - #{selectedLoan.id}</h3>
              <button 
                className="modal-close"
                onClick={() => setShowModal(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="detail-grid">
                <div className="detail-item">
                  <label>企业名称</label>
                  <span>{selectedLoan.company}</span>
                </div>
                <div className="detail-item">
                  <label>申请人</label>
                  <span>{selectedLoan.borrower}</span>
                </div>
                <div className="detail-item">
                  <label>联系电话</label>
                  <span>{selectedLoan.phone}</span>
                </div>
                <div className="detail-item">
                  <label>所属行业</label>
                  <span>{selectedLoan.industry}</span>
                </div>
                <div className="detail-item">
                  <label>贷款金额</label>
                  <span>¥{selectedLoan.amount}万</span>
                </div>
                <div className="detail-item">
                  <label>贷款期限</label>
                  <span>{selectedLoan.term}个月</span>
                </div>
                <div className="detail-item">
                  <label>申请利率</label>
                  <span>{selectedLoan.rate}%</span>
                </div>
                <div className="detail-item">
                  <label>风险评分</label>
                  <span className={`risk-score ${getRiskLevel(selectedLoan.riskScore).class}`}>
                    {selectedLoan.riskScore}
                  </span>
                </div>
                <div className="detail-item">
                  <label>申请状态</label>
                  <span className={`status-badge ${getStatusColor(selectedLoan.status)}`}>
                    {getStatusText(selectedLoan.status)}
                  </span>
                </div>
                <div className="detail-item">
                  <label>申请日期</label>
                  <span>{selectedLoan.applicationDate}</span>
                </div>
                {selectedLoan.approvalDate && (
                  <div className="detail-item">
                    <label>审批日期</label>
                    <span>{selectedLoan.approvalDate}</span>
                  </div>
                )}
              </div>
            </div>
            <div className="modal-footer">
              <button 
                className="btn btn-primary"
                onClick={() => setShowModal(false)}
              >
                关闭
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default LoanManagement;
