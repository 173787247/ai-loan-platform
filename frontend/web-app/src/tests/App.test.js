import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { UserProvider } from '../contexts/UserContext';
import { NotificationProvider } from '../components/NotificationSystem';
import App from '../App';

// 测试包装器
const TestWrapper = ({ children }) => (
  <UserProvider>
    <NotificationProvider>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </NotificationProvider>
  </UserProvider>
);

describe('App Component', () => {
  test('renders home page by default', () => {
    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );
    
    expect(screen.getByText('AI助贷招标平台')).toBeInTheDocument();
  });

  test('navigates to login page', () => {
    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );
    
    const loginLink = screen.getByText('登录');
    fireEvent.click(loginLink);
    
    expect(screen.getByText('AI助贷招标平台')).toBeInTheDocument();
  });

  test('shows navigation menu for authenticated users', async () => {
    // 模拟已登录状态
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'testuser',
      userType: 'borrower',
      fullName: '测试用户'
    }));

    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('风险评估')).toBeInTheDocument();
      expect(screen.getByText('智能匹配')).toBeInTheDocument();
    });
  });
});

describe('Authentication Flow', () => {
  test('redirects unauthenticated users to login', () => {
    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );
    
    // 尝试访问受保护的路由
    window.history.pushState({}, 'Test page', '/risk-assessment');
    
    expect(screen.getByText('登录')).toBeInTheDocument();
  });

  test('allows access to protected routes for authenticated users', async () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'testuser',
      userType: 'borrower',
      fullName: '测试用户'
    }));

    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('测试用户')).toBeInTheDocument();
    });
  });
});

describe('Navigation', () => {
  test('renders all navigation links for admin users', async () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'admin',
      userType: 'admin',
      fullName: '管理员'
    }));

    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('实时监控')).toBeInTheDocument();
      expect(screen.getByText('AI增强')).toBeInTheDocument();
    });
  });

  test('hides admin-only links for non-admin users', async () => {
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: 'borrower',
      userType: 'borrower',
      fullName: '借款方'
    }));

    render(
      <TestWrapper>
        <App />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.queryByText('AI增强')).not.toBeInTheDocument();
    });
  });
});
