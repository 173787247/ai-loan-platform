import React, { useState } from 'react';
import { useNotifications } from './NotificationSystem';
import './NotificationBell.css';

const NotificationBell = () => {
  const { notifications, unreadCount, markAllAsRead, clearAll } = useNotifications();
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleMarkAllRead = () => {
    markAllAsRead();
  };

  const handleClearAll = () => {
    clearAll();
    setIsOpen(false);
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
      case 'loan_approved':
        return '✅';
      case 'error':
      case 'loan_rejected':
        return '❌';
      case 'warning':
      case 'risk_alert':
        return '⚠️';
      case 'info':
      case 'system':
        return 'ℹ️';
      default:
        return '📢';
    }
  };

  const formatTime = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    return `${days}天前`;
  };

  return (
    <div className="notification-bell">
      <button 
        className="bell-button"
        onClick={toggleDropdown}
        aria-label="通知"
      >
        <span className="bell-icon">🔔</span>
        {unreadCount > 0 && (
          <span className="notification-badge">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="notification-dropdown">
          <div className="dropdown-header">
            <h3>通知中心</h3>
            <div className="header-actions">
              {unreadCount > 0 && (
                <button 
                  className="mark-read-btn"
                  onClick={handleMarkAllRead}
                >
                  全部已读
                </button>
              )}
              <button 
                className="clear-all-btn"
                onClick={handleClearAll}
              >
                清空
              </button>
            </div>
          </div>

          <div className="notification-list">
            {notifications.length === 0 ? (
              <div className="empty-notifications">
                <div className="empty-icon">📭</div>
                <p>暂无通知</p>
              </div>
            ) : (
              notifications.slice(0, 10).map(notification => (
                <div 
                  key={notification.id}
                  className={`notification-item ${notification.read ? 'read' : 'unread'}`}
                >
                  <div className="notification-icon">
                    {getNotificationIcon(notification.type)}
                  </div>
                  <div className="notification-content">
                    <div className="notification-title">
                      {notification.title}
                    </div>
                    <div className="notification-message">
                      {notification.message}
                    </div>
                    <div className="notification-time">
                      {formatTime(notification.timestamp)}
                    </div>
                  </div>
                  {!notification.read && (
                    <div className="unread-indicator"></div>
                  )}
                </div>
              ))
            )}
          </div>

          {notifications.length > 10 && (
            <div className="dropdown-footer">
              <button className="view-all-btn">
                查看全部通知
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
