import React, { createContext, useContext, useState, useCallback } from 'react';
import './NotificationSystem.css';

const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);

  const addNotification = useCallback((notification) => {
    const id = Date.now() + Math.random();
    const newNotification = {
      id,
      type: 'info',
      duration: 5000,
      ...notification
    };

    setNotifications(prev => [...prev, newNotification]);

    // 自动移除通知
    if (newNotification.duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, newNotification.duration);
    }

    return id;
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  const showSuccess = useCallback((message, options = {}) => {
    return addNotification({
      type: 'success',
      message,
      ...options
    });
  }, [addNotification]);

  const showError = useCallback((message, options = {}) => {
    return addNotification({
      type: 'error',
      message,
      duration: 8000, // 错误通知显示更长时间
      ...options
    });
  }, [addNotification]);

  const showWarning = useCallback((message, options = {}) => {
    return addNotification({
      type: 'warning',
      message,
      ...options
    });
  }, [addNotification]);

  const showInfo = useCallback((message, options = {}) => {
    return addNotification({
      type: 'info',
      message,
      ...options
    });
  }, [addNotification]);

  const value = {
    notifications,
    addNotification,
    removeNotification,
    clearAll,
    showSuccess,
    showError,
    showWarning,
    showInfo
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
      <NotificationContainer />
    </NotificationContext.Provider>
  );
};

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

const NotificationContainer = () => {
  const { notifications, removeNotification } = useNotification();

  return (
    <div className="notification-container">
      {notifications.map(notification => (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onRemove={removeNotification}
        />
      ))}
    </div>
  );
};

const NotificationItem = ({ notification, onRemove }) => {
  const { id, type, message, title, duration, persistent } = notification;

  const handleRemove = () => {
    onRemove(id);
  };

  const getIcon = () => {
    switch (type) {
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
      default:
        return 'ℹ️';
    }
  };

  return (
    <div className={`notification-item notification-${type}`}>
      <div className="notification-content">
        <div className="notification-icon">
          {getIcon()}
        </div>
        <div className="notification-text">
          {title && <div className="notification-title">{title}</div>}
          <div className="notification-message">{message}</div>
        </div>
        <button
          className="notification-close"
          onClick={handleRemove}
          aria-label="关闭通知"
        >
          ×
        </button>
      </div>
      {!persistent && duration > 0 && (
        <div className="notification-progress">
          <div
            className="notification-progress-bar"
            style={{
              animationDuration: `${duration}ms`
            }}
          />
        </div>
      )}
    </div>
  );
};

// 通知演示组件
export const NotificationDemo = () => {
  const { showSuccess, showError, showWarning, showInfo } = useNotification();

  const handleTestSuccess = () => {
    showSuccess('操作成功完成！', {
      title: '成功',
      duration: 3000
    });
  };

  const handleTestError = () => {
    showError('操作失败，请重试！', {
      title: '错误',
      duration: 0 // 不自动关闭
    });
  };

  const handleTestWarning = () => {
    showWarning('请注意相关风险！', {
      title: '警告',
      duration: 5000
    });
  };

  const handleTestInfo = () => {
    showInfo('这是一条信息通知', {
      title: '信息',
      duration: 4000
    });
  };

  return (
    <div className="notification-demo">
      <h2>通知系统演示</h2>
      <div className="demo-buttons">
        <button className="demo-btn success" onClick={handleTestSuccess}>
          成功通知
        </button>
        <button className="demo-btn error" onClick={handleTestError}>
          错误通知
        </button>
        <button className="demo-btn warning" onClick={handleTestWarning}>
          警告通知
        </button>
        <button className="demo-btn info" onClick={handleTestInfo}>
          信息通知
        </button>
      </div>
    </div>
  );
};

export default NotificationDemo;