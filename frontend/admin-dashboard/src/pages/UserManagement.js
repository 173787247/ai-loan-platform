import React, { useState, useEffect } from 'react';
import './UserManagement.css';

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [filters, setFilters] = useState({
    role: 'all',
    status: 'all',
    search: ''
  });

  useEffect(() => {
    const mockUsers = [
      {
        id: 1,
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '138****1234',
        role: 'borrower',
        company: '北京科技有限公司',
        status: 'active',
        registerDate: '2025-09-15',
        lastLogin: '2025-09-21',
        totalLoans: 3,
        approvedLoans: 2
      },
      {
        id: 2,
        name: '李四',
        email: 'lisi@example.com',
        phone: '139****5678',
        role: 'lender',
        company: '招商银行',
        status: 'active',
        registerDate: '2025-09-10',
        lastLogin: '2025-09-21',
        totalLoans: 0,
        approvedLoans: 0
      },
      {
        id: 3,
        name: '王五',
        email: 'wangwu@example.com',
        phone: '137****9012',
        role: 'borrower',
        company: '上海制造有限公司',
        status: 'inactive',
        registerDate: '2025-09-08',
        lastLogin: '2025-09-18',
        totalLoans: 1,
        approvedLoans: 0
      },
      {
        id: 4,
        name: '赵六',
        email: 'zhaoliu@example.com',
        phone: '136****3456',
        role: 'admin',
        company: '系统管理员',
        status: 'active',
        registerDate: '2025-09-01',
        lastLogin: '2025-09-21',
        totalLoans: 0,
        approvedLoans: 0
      }
    ];

    setUsers(mockUsers);
  }, []);

  const filteredUsers = users.filter(user => {
    if (filters.role !== 'all' && user.role !== filters.role) return false;
    if (filters.status !== 'all' && user.status !== filters.status) return false;
    if (filters.search && !user.name.toLowerCase().includes(filters.search.toLowerCase()) && 
        !user.email.toLowerCase().includes(filters.search.toLowerCase()) &&
        !user.company.toLowerCase().includes(filters.search.toLowerCase())) return false;
    return true;
  });

  const getRoleText = (role) => {
    switch (role) {
      case 'borrower': return '借款方';
      case 'lender': return '放贷方';
      case 'admin': return '管理员';
      default: return role;
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'borrower': return 'role-borrower';
      case 'lender': return 'role-lender';
      case 'admin': return 'role-admin';
      default: return '';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'status-active';
      case 'inactive': return 'status-inactive';
      default: return '';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return '活跃';
      case 'inactive': return '非活跃';
      default: return status;
    }
  };

  return (
    <div className="user-management">
      <div className="page-header">
        <h1>用户管理</h1>
        <p>管理系统用户和权限</p>
      </div>

      {/* 筛选器 */}
      <div className="card">
        <div className="filters">
          <div className="filter-group">
            <label>角色筛选</label>
            <select 
              value={filters.role} 
              onChange={(e) => setFilters(prev => ({ ...prev, role: e.target.value }))}
            >
              <option value="all">全部角色</option>
              <option value="borrower">借款方</option>
              <option value="lender">放贷方</option>
              <option value="admin">管理员</option>
            </select>
          </div>

          <div className="filter-group">
            <label>状态筛选</label>
            <select 
              value={filters.status} 
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            >
              <option value="all">全部状态</option>
              <option value="active">活跃</option>
              <option value="inactive">非活跃</option>
            </select>
          </div>

          <div className="filter-group search-group">
            <label>搜索</label>
            <input
              type="text"
              placeholder="搜索姓名、邮箱或公司..."
              value={filters.search}
              onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
            />
          </div>

          <button className="btn btn-primary">导出用户</button>
        </div>
      </div>

      {/* 用户列表 */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">用户列表</h2>
          <div className="card-actions">
            <span className="total-count">共 {filteredUsers.length} 个用户</span>
            <button className="btn btn-success">添加用户</button>
          </div>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>用户ID</th>
                <th>用户信息</th>
                <th>角色</th>
                <th>公司</th>
                <th>状态</th>
                <th>贷款记录</th>
                <th>注册日期</th>
                <th>最后登录</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map(user => (
                <tr key={user.id}>
                  <td>#{user.id}</td>
                  <td>
                    <div className="user-info">
                      <div className="user-name">{user.name}</div>
                      <div className="user-email">{user.email}</div>
                      <div className="user-phone">{user.phone}</div>
                    </div>
                  </td>
                  <td>
                    <span className={`role-badge ${getRoleColor(user.role)}`}>
                      {getRoleText(user.role)}
                    </span>
                  </td>
                  <td>{user.company}</td>
                  <td>
                    <span className={`status-badge ${getStatusColor(user.status)}`}>
                      {getStatusText(user.status)}
                    </span>
                  </td>
                  <td>
                    <div className="loan-stats">
                      <div className="stat-item">
                        <span className="stat-label">总申请:</span>
                        <span className="stat-value">{user.totalLoans}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">已批准:</span>
                        <span className="stat-value">{user.approvedLoans}</span>
                      </div>
                    </div>
                  </td>
                  <td>{user.registerDate}</td>
                  <td>{user.lastLogin}</td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn btn-primary">查看详情</button>
                      <button className="btn btn-warning">编辑</button>
                      <button className="btn btn-danger">禁用</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default UserManagement;
