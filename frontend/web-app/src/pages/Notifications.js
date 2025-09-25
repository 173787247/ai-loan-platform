import React, { useState, useEffect } from 'react';
import './Notifications.css';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // 模拟通知数据
    const mockNotifications = [
      {
        id: 1,
        type: 'info',
        title: '系统更新通知',
        message: '系统已更新到最新版本，新增了多项功能。',
        timestamp: '2025-09-24 10:30:00',
        read: false
      },
      {
        id: 2,
        type: 'warning',
        title: '风险评估提醒',
        message: '您的贷款申请风险评估已完成，请查看详情。',
        timestamp: '2025-09-24 09:15:00',
        read: true
      },
      {
        id: 3,
        type: 'success',
        title: '匹配成功',
        message: '已为您找到合适的贷款产品，请及时查看。',
        timestamp: '2025-09-24 08:45:00',
        read: false
      },
      {
        id: 4,
        type: 'error',
        title: '申请失败',
        message: '您的贷款申请未通过审核，请重新提交。',
        timestamp: '2025-09-23 16:20:00',
        read: true
      }
    ];
    setNotifications(mockNotifications);
  }, []);

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'info': return 'ℹ️';
      case 'warning': return '⚠️';
      case 'success': return '✅';
      case 'error': return '❌';
      default: return '📢';
    }
  };

  const getNotificationClass = (type) => {
    switch (type) {
      case 'info': return 'notification-info';
      case 'warning': return 'notification-warning';
      case 'success': return 'notification-success';
      case 'error': return 'notification-error';
      default: return 'notification-default';
    }
  };

  const filteredNotifications = notifications.filter(notification => {
    if (filter === 'all') return true;
    if (filter === 'unread') return !notification.read;
    return notification.type === filter;
  });

  const markAsRead = (id) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === id 
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <div className="notifications-container">
      <div className="notifications-header">
        <h1>📢 通知中心</h1>
        <div className="notifications-actions">
          <div className="filter-buttons">
            <button 
              className={filter === 'all' ? 'active' : ''} 
              onClick={() => setFilter('all')}
            >
              全部 ({notifications.length})
            </button>
            <button 
              className={filter === 'unread' ? 'active' : ''} 
              onClick={() => setFilter('unread')}
            >
              未读 ({unreadCount})
            </button>
            <button 
              className={filter === 'info' ? 'active' : ''} 
              onClick={() => setFilter('info')}
            >
              信息
            </button>
            <button 
              className={filter === 'warning' ? 'active' : ''} 
              onClick={() => setFilter('warning')}
            >
              警告
            </button>
            <button 
              className={filter === 'success' ? 'active' : ''} 
              onClick={() => setFilter('success')}
            >
              成功
            </button>
            <button 
              className={filter === 'error' ? 'active' : ''} 
              onClick={() => setFilter('error')}
            >
              错误
            </button>
          </div>
          <button className="mark-all-read" onClick={markAllAsRead}>
            全部标记为已读
          </button>
        </div>
      </div>

      <div className="notifications-list">
        {filteredNotifications.length === 0 ? (
          <div className="no-notifications">
            <p>暂无通知</p>
          </div>
        ) : (
          filteredNotifications.map(notification => (
            <div 
              key={notification.id} 
              className={`notification-item ${getNotificationClass(notification.type)} ${notification.read ? 'read' : 'unread'}`}
              onClick={() => markAsRead(notification.id)}
            >
              <div className="notification-icon">
                {getNotificationIcon(notification.type)}
              </div>
              <div className="notification-content">
                <div className="notification-header">
                  <h3>{notification.title}</h3>
                  <span className="notification-time">{notification.timestamp}</span>
                </div>
                <p className="notification-message">{notification.message}</p>
              </div>
              {!notification.read && <div className="unread-indicator"></div>}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Notifications;
