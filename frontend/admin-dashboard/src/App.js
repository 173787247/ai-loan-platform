import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';
import Dashboard from './pages/Dashboard';
import LoanManagement from './pages/LoanManagement';
import UserManagement from './pages/UserManagement';
import RiskAnalysis from './pages/RiskAnalysis';
import SystemSettings from './pages/SystemSettings';

function App() {
  return (
    <Router>
      <div className="admin-app">
        <AdminLayout />
      </div>
    </Router>
  );
}

function AdminLayout() {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const menuItems = [
    { path: '/', label: '仪表盘', icon: '📊' },
    { path: '/loans', label: '贷款管理', icon: '💰' },
    { path: '/users', label: '用户管理', icon: '👥' },
    { path: '/risk', label: '风险分析', icon: '⚠️' },
    { path: '/settings', label: '系统设置', icon: '⚙️' }
  ];

  return (
    <div className="admin-layout">
      {/* 侧边栏 */}
      <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>AI助贷管理后台</h2>
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>
        
        <nav className="sidebar-nav">
          {menuItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>
      </div>

      {/* 主内容区 */}
      <div className="main-content">
        <header className="top-header">
          <div className="header-left">
            <h1>AI助贷招标平台 - 管理后台</h1>
          </div>
          <div className="header-right">
            <div className="user-info">
              <span className="user-name">管理员</span>
              <div className="user-avatar">👤</div>
            </div>
          </div>
        </header>

        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/loans" element={<LoanManagement />} />
            <Route path="/users" element={<UserManagement />} />
            <Route path="/risk" element={<RiskAnalysis />} />
            <Route path="/settings" element={<SystemSettings />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
