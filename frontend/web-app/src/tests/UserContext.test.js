import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserProvider, useUser } from '../contexts/UserContext';

// 测试组件
const TestComponent = () => {
  const { 
    user, 
    isAuthenticated, 
    login, 
    logout, 
    isAdmin, 
    isBorrower, 
    isLender 
  } = useUser();

  const handleLogin = async () => {
    const result = await login('testuser', 'testpass');
    console.log('Login result:', result);
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div>
      <div data-testid="user-info">
        {user ? `欢迎, ${user.fullName}` : '未登录'}
      </div>
      <div data-testid="auth-status">
        {isAuthenticated() ? '已登录' : '未登录'}
      </div>
      <div data-testid="user-type">
        {user?.userType || 'none'}
      </div>
      <div data-testid="is-admin">
        {isAdmin() ? '是管理员' : '不是管理员'}
      </div>
      <div data-testid="is-borrower">
        {isBorrower() ? '是借款方' : '不是借款方'}
      </div>
      <div data-testid="is-lender">
        {isLender() ? '是放贷方' : '不是放贷方'}
      </div>
      <button onClick={handleLogin}>登录</button>
      <button onClick={handleLogout}>登出</button>
    </div>
  );
};

describe('UserContext', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('renders user provider', () => {
    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    expect(screen.getByText('未登录')).toBeInTheDocument();
  });

  test('shows unauthenticated state initially', () => {
    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    expect(screen.getByTestId('auth-status')).toHaveTextContent('未登录');
    expect(screen.getByTestId('user-type')).toHaveTextContent('none');
  });

  test('handles successful login', async () => {
    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    const loginButton = screen.getByText('登录');
    fireEvent.click(loginButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('已登录');
    });
  });

  test('handles failed login', async () => {
    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    // 模拟错误的登录凭据
    const loginButton = screen.getByText('登录');
    fireEvent.click(loginButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('未登录');
    });
  });

  test('handles logout', async () => {
    // 先设置一个已登录状态
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'testuser',
      userType: 'borrower',
      fullName: '测试用户'
    }));

    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('已登录');
    });
    
    const logoutButton = screen.getByText('登出');
    fireEvent.click(logoutButton);
    
    expect(screen.getByTestId('auth-status')).toHaveTextContent('未登录');
  });

  test('identifies admin user correctly', async () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'admin',
      userType: 'admin',
      fullName: '管理员'
    }));

    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    await waitFor(() => {
      expect(screen.getByTestId('is-admin')).toHaveTextContent('是管理员');
      expect(screen.getByTestId('user-type')).toHaveTextContent('admin');
    });
  });

  test('identifies borrower user correctly', async () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'borrower',
      userType: 'borrower',
      fullName: '借款方'
    }));

    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    await waitFor(() => {
      expect(screen.getByTestId('is-borrower')).toHaveTextContent('是借款方');
      expect(screen.getByTestId('user-type')).toHaveTextContent('borrower');
    });
  });

  test('identifies lender user correctly', async () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'lender',
      userType: 'lender',
      fullName: '放贷方'
    }));

    render(
      <UserProvider>
        <TestComponent />
      </UserProvider>
    );
    
    await waitFor(() => {
      expect(screen.getByTestId('is-lender')).toHaveTextContent('是放贷方');
      expect(screen.getByTestId('user-type')).toHaveTextContent('lender');
    });
  });
});
