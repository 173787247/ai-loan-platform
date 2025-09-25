import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import { useNotification } from '../components/NotificationSystem';
import Auth from '../components/Auth';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useUser();
  const { showSuccess } = useNotification();

  // 如果已经登录，重定向到首页
  React.useEffect(() => {
    if (isAuthenticated()) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = (user) => {
    showSuccess(`欢迎回来，${user.fullName}！`);
    navigate('/');
  };

  const handleRegister = (user) => {
    showSuccess(`注册成功，欢迎 ${user.fullName}！`);
    navigate('/');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>AI助贷招标平台</h1>
          <p>智能金融科技解决方案</p>
        </div>
        
        <Auth 
          onLogin={handleLogin}
          onRegister={handleRegister}
        />
      </div>
    </div>
  );
};

export default Login;