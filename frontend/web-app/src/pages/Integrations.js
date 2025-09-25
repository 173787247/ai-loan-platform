import React from 'react';
import './Integrations.css';

const Integrations = () => (
  <div className="integrations-container">
    <div className="integrations-header">
      <h1>🔗 集成管理</h1>
      <p>第三方服务集成和API管理</p>
    </div>
    <div className="integrations-grid">
      <div className="integration-card">
        <h3>🏦 银行API</h3>
        <p>与各大银行系统集成</p>
        <span className="status active">已连接</span>
      </div>
      <div className="integration-card">
        <h3>📊 数据分析</h3>
        <p>第三方数据分析服务</p>
        <span className="status active">已连接</span>
      </div>
      <div className="integration-card">
        <h3>🔐 身份验证</h3>
        <p>第三方身份验证服务</p>
        <span className="status pending">连接中</span>
      </div>
    </div>
  </div>
);

export default Integrations;
