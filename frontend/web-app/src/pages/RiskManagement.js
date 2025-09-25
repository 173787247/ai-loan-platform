import React from 'react';
import './RiskManagement.css';

const RiskManagement = () => (
  <div className="risk-management-container">
    <div className="risk-management-header">
      <h1>🛡️ 风险管理</h1>
      <p>风险识别、评估和预警系统</p>
    </div>
    <div className="risk-grid">
      <div className="risk-card">
        <h3>信用风险</h3>
        <div className="risk-level high">高风险</div>
      </div>
      <div className="risk-card">
        <h3>市场风险</h3>
        <div className="risk-level medium">中风险</div>
      </div>
      <div className="risk-card">
        <h3>操作风险</h3>
        <div className="risk-level low">低风险</div>
      </div>
    </div>
  </div>
);

export default RiskManagement;
