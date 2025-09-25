import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import './ProtectedRoute.css';

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { isAuthenticated, isAdmin, isLoading } = useUser();

  // 显示加载状态
  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>加载中...</p>
      </div>
    );
  }

  // 检查是否已登录
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  // 检查管理员权限
  if (adminOnly && !isAdmin()) {
    return (
      <div className="access-denied">
        <h2>访问被拒绝</h2>
        <p>您没有权限访问此页面。此页面仅限管理员使用。</p>
        <button 
          className="back-btn"
          onClick={() => window.history.back()}
        >
          返回上一页
        </button>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;