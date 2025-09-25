import React, { useState } from 'react';
import { useUser } from '../contexts/UserContext';
import { useNotification } from './NotificationSystem';
import { testAccounts, quickLoginAccounts } from '../data/testAccounts';
import './Auth.css';

const Auth = ({ onLogin, onRegister }) => {
  const { login, register, isLoading } = useUser();
  const { showSuccess, showError } = useNotification();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    userType: 'borrower' // borrower, lender, admin
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // 清除错误信息
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      if (isLogin) {
        // 登录逻辑
        const result = await login(formData.username, formData.password);
        if (result.success) {
          showSuccess(`欢迎回来，${result.user.fullName}！`);
          if (onLogin) {
            onLogin(result.user);
          }
        } else {
          setError(result.error);
          showError(result.error);
        }
      } else {
        // 注册逻辑
        if (formData.password !== formData.confirmPassword) {
          const errorMsg = '密码确认不匹配';
          setError(errorMsg);
          showError(errorMsg);
          return;
        }
        
        if (formData.password.length < 6) {
          const errorMsg = '密码长度至少6位';
          setError(errorMsg);
          showError(errorMsg);
          return;
        }
        
        const result = await register({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          userType: formData.userType,
          fullName: formData.username
        });
        
        if (result.success) {
          showSuccess(`注册成功，欢迎 ${result.user.fullName}！`);
          if (onRegister) {
            onRegister(result.user);
          }
        } else {
          setError(result.error);
          showError(result.error);
        }
      }
    } catch (error) {
      const errorMsg = '操作失败，请重试';
      setError(errorMsg);
      showError(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      userType: 'borrower'
    });
    setError('');
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>{isLogin ? '登录' : '注册'}</h1>
          <p>{isLogin ? '欢迎回来！' : '创建新账户'}</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">用户名</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="请输入用户名"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">邮箱</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="请输入邮箱地址"
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">密码</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="请输入密码"
            />
          </div>

          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="confirmPassword">确认密码</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  placeholder="请再次输入密码"
                />
              </div>

              <div className="form-group">
                <label htmlFor="userType">用户类型</label>
                <select
                  id="userType"
                  name="userType"
                  value={formData.userType}
                  onChange={handleChange}
                  required
                >
                  <option value="borrower">借款方</option>
                  <option value="lender">放贷方</option>
                  <option value="admin">管理员</option>
                </select>
              </div>
            </>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="auth-submit-btn"
            disabled={isSubmitting || isLoading}
          >
            {isSubmitting || isLoading ? '处理中...' : (isLogin ? '登录' : '注册')}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            {isLogin ? '还没有账户？' : '已有账户？'}
            <button 
              type="button" 
              className="switch-mode-btn"
              onClick={switchMode}
            >
              {isLogin ? '立即注册' : '立即登录'}
            </button>
          </p>
        </div>

        {isLogin && (
          <div className="test-accounts">
            <h3>测试账号</h3>
            <div className="account-list">
              {quickLoginAccounts.map((account, index) => (
                <div key={index} className="account-item">
                  <div className="account-info">
                    <strong>{account.username}</strong> <span className="password">/{account.password}</span>
                    <span className="account-type">{account.type}</span>
                  </div>
                  <div className="account-desc">{account.description}</div>
                </div>
              ))}
            </div>
            <p className="test-note">
              💡 提示：您可以使用上述任意测试账号登录，或注册新账号
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Auth;
