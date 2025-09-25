import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import notificationService from '../services/NotificationService';
import './EnhancedNotificationSystem.css';

const EnhancedNotificationContext = createContext();

export const EnhancedNotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [notificationHistory, setNotificationHistory] = useState([]);
  const [isPushEnabled, setIsPushEnabled] = useState(false);
  const [userPreferences, setUserPreferences] = useState({
    email: true,
    sms: false,
    push: true,
    inApp: true
  });

  // 初始化推送通知
  useEffect(() => {
    const initPush = async () => {
      const enabled = await notificationService.initializePush();
      setIsPushEnabled(enabled);
    };
    initPush();
  }, []);

  // 添加通知
  const addNotification = useCallback((notification) => {
    const id = Date.now() + Math.random();
    const newNotification = {
      id,
      type: 'info',
      duration: 5000,
      timestamp: new Date().toISOString(),
      read: false,
      ...notification
    };

    setNotifications(prev => [...prev, newNotification]);
    setNotificationHistory(prev => [newNotification, ...prev]);

    // 自动移除通知
    if (newNotification.duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, newNotification.duration);
    }

    return id;
  }, []);

  // 移除通知
  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  // 标记为已读
  const markAsRead = useCallback(async (id) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === id ? { ...notification, read: true } : notification
      )
    );
    setNotificationHistory(prev => 
      prev.map(notification => 
        notification.id === id ? { ...notification, read: true } : notification
      )
    );
    
    // 同步到服务器
    await notificationService.markAsRead(id);
  }, []);

  // 清空所有通知
  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  // 发送多渠道通知
  const sendMultiChannelNotification = useCallback(async (recipient, title, message, channels = null) => {
    const channelsToUse = channels || Object.keys(userPreferences).filter(key => userPreferences[key]);
    
    try {
      const results = await notificationService.sendMultiChannel(recipient, title, message, channelsToUse);
      
      // 添加应用内通知
      if (userPreferences.inApp) {
        addNotification({
          type: 'info',
          title: '多渠道通知已发送',
          message: `已通过 ${channelsToUse.join(', ')} 发送通知`,
          duration: 3000
        });
      }
      
      return results;
    } catch (error) {
      addNotification({
        type: 'error',
        title: '通知发送失败',
        message: error.message,
        duration: 5000
      });
      return { success: false, error: error.message };
    }
  }, [userPreferences, addNotification]);

  // 发送贷款申请通知
  const sendLoanApplicationNotification = useCallback(async (borrower, loanData) => {
    try {
      const results = await notificationService.sendLoanApplicationNotification(borrower, loanData);
      
      addNotification({
        type: 'success',
        title: '贷款申请已提交',
        message: `申请金额：${loanData.amount}元`,
        duration: 5000
      });
      
      return results;
    } catch (error) {
      addNotification({
        type: 'error',
        title: '通知发送失败',
        message: error.message,
        duration: 5000
      });
      return { success: false, error: error.message };
    }
  }, [addNotification]);

  // 发送风险评估通知
  const sendRiskAssessmentNotification = useCallback(async (borrower, riskData) => {
    try {
      const results = await notificationService.sendRiskAssessmentNotification(borrower, riskData);
      
      addNotification({
        type: 'info',
        title: '风险评估完成',
        message: `风险等级：${riskData.level}，评分：${riskData.score}分`,
        duration: 5000
      });
      
      return results;
    } catch (error) {
      addNotification({
        type: 'error',
        title: '通知发送失败',
        message: error.message,
        duration: 5000
      });
      return { success: false, error: error.message };
    }
  }, [addNotification]);

  // 发送匹配结果通知
  const sendMatchingNotification = useCallback(async (borrower, matchingResults) => {
    try {
      const results = await notificationService.sendMatchingNotification(borrower, matchingResults);
      
      addNotification({
        type: 'success',
        title: '智能匹配完成',
        message: `找到${matchingResults.length}个匹配产品`,
        duration: 5000
      });
      
      return results;
    } catch (error) {
      addNotification({
        type: 'error',
        title: '通知发送失败',
        message: error.message,
        duration: 5000
      });
      return { success: false, error: error.message };
    }
  }, [addNotification]);

  // 发送系统通知
  const sendSystemNotification = useCallback(async (recipient, type, data) => {
    try {
      const results = await notificationService.sendSystemNotification(recipient, type, data);
      
      addNotification({
        type: 'info',
        title: '系统通知已发送',
        message: `已向 ${recipient.name || recipient.email} 发送通知`,
        duration: 3000
      });
      
      return results;
    } catch (error) {
      addNotification({
        type: 'error',
        title: '系统通知发送失败',
        message: error.message,
        duration: 5000
      });
      return { success: false, error: error.message };
    }
  }, [addNotification]);

  // 更新用户偏好
  const updateUserPreferences = useCallback((preferences) => {
    setUserPreferences(prev => ({ ...prev, ...preferences }));
    localStorage.setItem('notificationPreferences', JSON.stringify({ ...userPreferences, ...preferences }));
  }, [userPreferences]);

  // 加载用户偏好
  useEffect(() => {
    const savedPreferences = localStorage.getItem('notificationPreferences');
    if (savedPreferences) {
      try {
        setUserPreferences(JSON.parse(savedPreferences));
      } catch (error) {
        console.error('加载通知偏好失败:', error);
      }
    }
  }, []);

  // 加载通知历史
  const loadNotificationHistory = useCallback(async (userId) => {
    try {
      const history = await notificationService.getNotificationHistory(userId);
      setNotificationHistory(history);
    } catch (error) {
      console.error('加载通知历史失败:', error);
    }
  }, []);

  const value = {
    notifications,
    notificationHistory,
    isPushEnabled,
    userPreferences,
    addNotification,
    removeNotification,
    markAsRead,
    clearAll,
    sendMultiChannelNotification,
    sendLoanApplicationNotification,
    sendRiskAssessmentNotification,
    sendMatchingNotification,
    sendSystemNotification,
    updateUserPreferences,
    loadNotificationHistory
  };

  return (
    <EnhancedNotificationContext.Provider value={value}>
      {children}
      <EnhancedNotificationContainer />
    </EnhancedNotificationContext.Provider>
  );
};

export const useEnhancedNotification = () => {
  const context = useContext(EnhancedNotificationContext);
  if (!context) {
    throw new Error('useEnhancedNotification must be used within an EnhancedNotificationProvider');
  }
  return context;
};

// 通知容器组件
const EnhancedNotificationContainer = () => {
  const { notifications, removeNotification, markAsRead } = useEnhancedNotification();

  return (
    <div className="enhanced-notification-container">
      {notifications.map(notification => (
        <EnhancedNotificationItem
          key={notification.id}
          notification={notification}
          onRemove={removeNotification}
          onMarkAsRead={markAsRead}
        />
      ))}
    </div>
  );
};

// 通知项组件
const EnhancedNotificationItem = ({ notification, onRemove, onMarkAsRead }) => {
  const { id, type, message, title, duration, persistent, read, timestamp } = notification;

  const handleRemove = () => {
    onRemove(id);
  };

  const handleMarkAsRead = () => {
    onMarkAsRead(id);
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

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`;
    return date.toLocaleDateString();
  };

  return (
    <div className={`enhanced-notification-item enhanced-notification-${type} ${read ? 'read' : 'unread'}`}>
      <div className="enhanced-notification-content">
        <div className="enhanced-notification-icon">
          {getIcon()}
        </div>
        <div className="enhanced-notification-text">
          {title && <div className="enhanced-notification-title">{title}</div>}
          <div className="enhanced-notification-message">{message}</div>
          <div className="enhanced-notification-time">{formatTime(timestamp)}</div>
        </div>
        <div className="enhanced-notification-actions">
          {!read && (
            <button
              className="enhanced-notification-mark-read"
              onClick={handleMarkAsRead}
              title="标记为已读"
            >
              ✓
            </button>
          )}
          <button
            className="enhanced-notification-close"
            onClick={handleRemove}
            title="关闭通知"
          >
            ×
          </button>
        </div>
      </div>
      {!persistent && duration > 0 && (
        <div className="enhanced-notification-progress">
          <div
            className="enhanced-notification-progress-bar"
            style={{
              animationDuration: `${duration}ms`
            }}
          />
        </div>
      )}
    </div>
  );
};

// 通知设置组件
export const NotificationSettings = () => {
  const { userPreferences, updateUserPreferences, isPushEnabled } = useEnhancedNotification();

  const handlePreferenceChange = (key, value) => {
    updateUserPreferences({ [key]: value });
  };

  return (
    <div className="notification-settings">
      <h3>通知设置</h3>
      <div className="preference-group">
        <label className="preference-item">
          <input
            type="checkbox"
            checked={userPreferences.email}
            onChange={(e) => handlePreferenceChange('email', e.target.checked)}
          />
          <span>邮件通知</span>
        </label>
        <label className="preference-item">
          <input
            type="checkbox"
            checked={userPreferences.sms}
            onChange={(e) => handlePreferenceChange('sms', e.target.checked)}
          />
          <span>短信通知</span>
        </label>
        <label className="preference-item">
          <input
            type="checkbox"
            checked={userPreferences.push && isPushEnabled}
            onChange={(e) => handlePreferenceChange('push', e.target.checked)}
            disabled={!isPushEnabled}
          />
          <span>推送通知 {!isPushEnabled && '(不支持)'}</span>
        </label>
        <label className="preference-item">
          <input
            type="checkbox"
            checked={userPreferences.inApp}
            onChange={(e) => handlePreferenceChange('inApp', e.target.checked)}
          />
          <span>应用内通知</span>
        </label>
      </div>
    </div>
  );
};

export default EnhancedNotificationProvider;
