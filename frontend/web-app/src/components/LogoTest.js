import React from 'react';
import './LogoTest.css';

const LogoTest = () => {
  return (
    <div className="logo-test">
      <div className="test-container">
        <h1>Logo显示测试</h1>
        
        <div className="test-section">
          <h2>桌面端Logo测试</h2>
          <div className="navbar-logo desktop">
            <span className="logo-icon">🏦</span>
            <span className="logo-text">AI助贷平台</span>
          </div>
        </div>
        
        <div className="test-section">
          <h2>平板端Logo测试 (768px以下)</h2>
          <div className="navbar-logo tablet">
            <span className="logo-icon">🏦</span>
            <span className="logo-text">AI助贷平台</span>
          </div>
        </div>
        
        <div className="test-section">
          <h2>手机端Logo测试 (480px以下)</h2>
          <div className="navbar-logo mobile">
            <span className="logo-icon">🏦</span>
            <span className="logo-text">AI助贷平台</span>
          </div>
        </div>
        
        <div className="test-section">
          <h2>原始Logo测试</h2>
          <div className="navbar-logo original">
            <span className="logo-icon">🏦</span>
            <span className="logo-text">AI助贷招标平台</span>
          </div>
        </div>
        
        <div className="test-instructions">
          <h3>测试说明：</h3>
          <ul>
            <li>检查"AI助贷平台"是否完整显示</li>
            <li>检查在不同屏幕尺寸下是否正常</li>
            <li>检查文字是否被截断</li>
            <li>检查图标和文字的对齐</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LogoTest;
