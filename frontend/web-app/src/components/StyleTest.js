import React from 'react';
import './StyleTest.css';

const StyleTest = () => {
  return (
    <div className="style-test">
      <h1>样式测试页面</h1>
      
      <div className="test-section">
        <h2>导航栏样式测试</h2>
        <div className="user-navbar-test">
          <div className="navbar-container-test">
            <div className="navbar-logo-test">
              <span className="logo-icon-test">🏦</span>
              <span className="logo-text-test">测试Logo</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="test-section">
        <h2>内联样式测试</h2>
        <div style={{
          background: 'red',
          color: 'white',
          padding: '20px',
          fontSize: '24px',
          fontWeight: 'bold'
        }}>
          这是内联样式测试 - 如果看到红色背景，说明React正常工作
        </div>
      </div>
      
      <div className="test-section">
        <h2>CSS类测试</h2>
        <div className="css-test">
          这是CSS类测试 - 如果看到蓝色背景，说明CSS文件正常工作
        </div>
      </div>
    </div>
  );
};

export default StyleTest;
