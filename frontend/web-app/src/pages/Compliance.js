import React from 'react';
import './Compliance.css';

const Compliance = () => (
  <div className="compliance-container">
    <div className="compliance-header">
      <h1>📋 合规管理</h1>
      <p>合规检查和政策管理</p>
    </div>
    <div className="compliance-grid">
      <div className="compliance-card">
        <h3>数据保护</h3>
        <div className="compliance-status compliant">合规</div>
      </div>
      <div className="compliance-card">
        <h3>金融监管</h3>
        <div className="compliance-status compliant">合规</div>
      </div>
      <div className="compliance-card">
        <h3>审计要求</h3>
        <div className="compliance-status pending">待审核</div>
      </div>
    </div>
  </div>
);

export default Compliance;
