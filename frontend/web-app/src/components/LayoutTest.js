import React from 'react';
import './LayoutTest.css';

const LayoutTest = () => {
  return (
    <div className="layout-test">
      <div className="test-header">
        <h1>布局测试页面</h1>
        <p>这个页面用于测试首页布局是否正确显示</p>
      </div>
      
      <div className="test-content">
        <div className="test-section">
          <h2>测试区域 1</h2>
          <p>这是第一个测试区域，用于验证内容是否正确显示。</p>
        </div>
        
        <div className="test-section">
          <h2>测试区域 2</h2>
          <p>这是第二个测试区域，用于验证布局是否完整。</p>
        </div>
        
        <div className="test-section">
          <h2>测试区域 3</h2>
          <p>这是第三个测试区域，用于验证响应式设计。</p>
        </div>
      </div>
      
      <div className="test-footer">
        <p>布局测试完成 - 如果能看到这个页面，说明布局修复成功！</p>
      </div>
    </div>
  );
};

export default LayoutTest;
