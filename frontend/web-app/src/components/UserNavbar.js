import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import { useNotification } from './NotificationSystem';
import './UserNavbar.css';

const UserNavbar = () => {
  const { user, isAuthenticated, logout, isAdmin } = useUser();
  const { showSuccess } = useNotification();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    showSuccess('已成功登出');
    navigate('/');
    setIsMenuOpen(false);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="user-navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          <span className="logo-icon">🏦</span>
          <span className="logo-text">AI助贷招标平台</span>
        </Link>

        <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
          {/* 第一排菜单 */}
          <div className="navbar-row">
            <Link to="/" className="navbar-link" onClick={closeMenu}>
              首页
            </Link>
            
            <Link to="/risk-assessment" className="navbar-link" onClick={closeMenu}>
              风险评估
            </Link>
            <Link to="/auto-matching" className="navbar-link" onClick={closeMenu}>
              智能匹配
            </Link>
            <Link to="/realtime-monitoring" className="navbar-link" onClick={closeMenu}>
              实时监控
            </Link>
            <Link to="/notifications" className="navbar-link" onClick={closeMenu}>
              通知中心
            </Link>
            <Link to="/dashboard" className="navbar-link" onClick={closeMenu}>
              智能仪表板
            </Link>
            <Link to="/analytics" className="navbar-link" onClick={closeMenu}>
              数据分析
            </Link>
            <Link to="/reports" className="navbar-link" onClick={closeMenu}>
              报表中心
            </Link>
          </div>
          
          {/* 第二排菜单 */}
          <div className="navbar-row">
            <Link to="/ai-enhancements" className="navbar-link" onClick={closeMenu}>
              AI增强
            </Link>
            <Link to="/workflow" className="navbar-link" onClick={closeMenu}>
              工作流
            </Link>
            <Link to="/integrations" className="navbar-link" onClick={closeMenu}>
              集成管理
            </Link>
            <Link to="/microservices" className="navbar-link" onClick={closeMenu}>
              微服务架构
            </Link>
            <Link to="/risk-management" className="navbar-link" onClick={closeMenu}>
              风险管理
            </Link>
            <Link to="/compliance" className="navbar-link" onClick={closeMenu}>
              合规管理
            </Link>
            <Link to="/ai-chatbot-demo" className="navbar-link" onClick={closeMenu}>
              🤖 AI智能客服
            </Link>
          </div>
        </div>

        <div className="navbar-user">
          {isAuthenticated() ? (
            <div className="user-menu">
              <div className="user-info">
                <span className="user-avatar">{user?.avatar || '👤'}</span>
                <span className="user-name">{user?.fullName || user?.username}</span>
                <span className="user-type">{user?.userType === 'admin' ? '管理员' : 
                                           user?.userType === 'borrower' ? '借款方' : '放贷方'}</span>
              </div>
              <button className="logout-btn" onClick={handleLogout}>
                登出
              </button>
            </div>
          ) : (
            <Link to="/login" className="login-btn">
              登录
            </Link>
          )}
        </div>

        <button className="menu-toggle" onClick={toggleMenu}>
          <span className="hamburger"></span>
          <span className="hamburger"></span>
          <span className="hamburger"></span>
        </button>
      </div>
    </nav>
  );
};

export default UserNavbar;