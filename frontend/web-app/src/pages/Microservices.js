import React from 'react';
import './Microservices.css';

const Microservices = () => (
  <div className="microservices-container">
    <div className="microservices-header">
      <h1>🏗️ 微服务架构</h1>
      <p>服务监控和架构管理</p>
    </div>
    <div className="services-grid">
      <div className="service-card">
        <h3>用户服务</h3>
        <span className="status online">运行中</span>
      </div>
      <div className="service-card">
        <h3>贷款服务</h3>
        <span className="status online">运行中</span>
      </div>
      <div className="service-card">
        <h3>风险服务</h3>
        <span className="status offline">离线</span>
      </div>
      <div className="service-card">
        <h3>匹配服务</h3>
        <span className="status online">运行中</span>
      </div>
    </div>
  </div>
);

export default Microservices;
