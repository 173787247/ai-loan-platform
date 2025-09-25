import React from 'react';
import { NotificationDemo } from '../components/NotificationSystem';
import './NotificationDemo.css';

const NotificationDemoPage = () => {
  return (
    <div className="notification-demo-page">
      <div className="container">
        <h1>通知系统演示</h1>
        <p className="description">
          体验不同类型的通知消息，包括成功、错误、警告和信息通知。
        </p>
        
        <div className="demo-section">
          <NotificationDemo />
        </div>

        <div className="features-section">
          <h2>通知系统特性</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>多种类型</h3>
              <p>支持成功、错误、警告和信息四种通知类型</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⏰</div>
              <h3>自动消失</h3>
              <p>可设置自动消失时间，或手动关闭</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>响应式设计</h3>
              <p>完美适配桌面端和移动端设备</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h3>美观界面</h3>
              <p>现代化的UI设计，提供良好的用户体验</p>
            </div>
          </div>
        </div>

        <div className="usage-section">
          <h2>使用方法</h2>
          <div className="code-example">
            <pre>
{`import { useNotification } from '../components/NotificationSystem';

const { showSuccess, showError, showWarning, showInfo } = useNotification();

// 显示成功通知
showSuccess('操作成功完成！');

// 显示错误通知
showError('操作失败，请重试！');

// 显示警告通知
showWarning('请注意相关风险！');

// 显示信息通知
showInfo('这是一条信息通知');`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotificationDemoPage;