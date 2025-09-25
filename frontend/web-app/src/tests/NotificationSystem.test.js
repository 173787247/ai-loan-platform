import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { NotificationProvider, useNotification } from '../components/NotificationSystem';

// 测试组件
const TestComponent = () => {
  const { showSuccess, showError, showWarning, showInfo } = useNotification();

  return (
    <div>
      <button onClick={() => showSuccess('成功消息')}>显示成功</button>
      <button onClick={() => showError('错误消息')}>显示错误</button>
      <button onClick={() => showWarning('警告消息')}>显示警告</button>
      <button onClick={() => showInfo('信息消息')}>显示信息</button>
    </div>
  );
};

describe('NotificationSystem', () => {
  test('renders notification provider', () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    expect(screen.getByText('显示成功')).toBeInTheDocument();
  });

  test('shows success notification', async () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    const successButton = screen.getByText('显示成功');
    fireEvent.click(successButton);
    
    await waitFor(() => {
      expect(screen.getByText('成功消息')).toBeInTheDocument();
    });
  });

  test('shows error notification', async () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    const errorButton = screen.getByText('显示错误');
    fireEvent.click(errorButton);
    
    await waitFor(() => {
      expect(screen.getByText('错误消息')).toBeInTheDocument();
    });
  });

  test('shows warning notification', async () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    const warningButton = screen.getByText('显示警告');
    fireEvent.click(warningButton);
    
    await waitFor(() => {
      expect(screen.getByText('警告消息')).toBeInTheDocument();
    });
  });

  test('shows info notification', async () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    const infoButton = screen.getByText('显示信息');
    fireEvent.click(infoButton);
    
    await waitFor(() => {
      expect(screen.getByText('信息消息')).toBeInTheDocument();
    });
  });

  test('allows manual notification removal', async () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    const successButton = screen.getByText('显示成功');
    fireEvent.click(successButton);
    
    await waitFor(() => {
      expect(screen.getByText('成功消息')).toBeInTheDocument();
    });
    
    const closeButton = screen.getByLabelText('关闭通知');
    fireEvent.click(closeButton);
    
    await waitFor(() => {
      expect(screen.queryByText('成功消息')).not.toBeInTheDocument();
    });
  });

  test('shows multiple notifications', async () => {
    render(
      <NotificationProvider>
        <TestComponent />
      </NotificationProvider>
    );
    
    const successButton = screen.getByText('显示成功');
    const errorButton = screen.getByText('显示错误');
    
    fireEvent.click(successButton);
    fireEvent.click(errorButton);
    
    await waitFor(() => {
      expect(screen.getByText('成功消息')).toBeInTheDocument();
      expect(screen.getByText('错误消息')).toBeInTheDocument();
    });
  });
});
