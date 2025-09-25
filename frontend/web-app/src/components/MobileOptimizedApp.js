import React, { useState, useEffect } from 'react';
import { useUser } from '../contexts/UserContext';
import { useEnhancedNotification } from './EnhancedNotificationSystem';
import './MobileOptimizedApp.css';

const MobileOptimizedApp = ({ children }) => {
  const { user, isAuthenticated } = useUser();
  const { isPushEnabled, updateUserPreferences } = useEnhancedNotification();
  const [isMobile, setIsMobile] = useState(false);
  const [isPWAInstalled, setIsPWAInstalled] = useState(false);
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [deviceOrientation, setDeviceOrientation] = useState('portrait');
  const [touchGestures, setTouchGestures] = useState({
    swipeUp: 0,
    swipeDown: 0,
    swipeLeft: 0,
    swipeRight: 0
  });
  const [performanceMetrics, setPerformanceMetrics] = useState({
    loadTime: 0,
    memoryUsage: 0,
    batteryLevel: 100
  });

  // 检测移动设备
  useEffect(() => {
    const checkMobile = () => {
      const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      const isSmallScreen = window.innerWidth <= 768;
      setIsMobile(isMobileDevice || isSmallScreen);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // 检测PWA安装状态
  useEffect(() => {
    const checkPWAInstall = () => {
      // 检查是否在独立模式下运行
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const isIOSStandalone = window.navigator.standalone === true;
      setIsPWAInstalled(isStandalone || isIOSStandalone);
    };

    checkPWAInstall();
  }, []);

  // 监听PWA安装提示
  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowInstallPrompt(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    return () => window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
  }, []);

  // 安装PWA
  const handleInstallPWA = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      console.log(`PWA安装结果: ${outcome}`);
      setDeferredPrompt(null);
      setShowInstallPrompt(false);
    }
  };

  // 关闭安装提示
  const handleCloseInstallPrompt = () => {
    setShowInstallPrompt(false);
  };

  // 请求通知权限
  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        updateUserPreferences({ push: true });
      }
    }
  };

  // 添加触摸手势支持
  useEffect(() => {
    if (!isMobile) return;

    let startY = 0;
    let startX = 0;

    const handleTouchStart = (e) => {
      startY = e.touches[0].clientY;
      startX = e.touches[0].clientX;
    };

    const handleTouchEnd = (e) => {
      const endY = e.changedTouches[0].clientY;
      const endX = e.changedTouches[0].clientX;
      const diffY = startY - endY;
      const diffX = startX - endX;

      // 检测滑动方向
      if (Math.abs(diffY) > Math.abs(diffX)) {
        if (diffY > 50) {
          // 向上滑动 - 可以用于刷新
          console.log('向上滑动');
        } else if (diffY < -50) {
          // 向下滑动 - 可以用于显示更多内容
          console.log('向下滑动');
        }
      } else {
        if (diffX > 50) {
          // 向左滑动 - 可以用于导航
          console.log('向左滑动');
        } else if (diffX < -50) {
          // 向右滑动 - 可以用于返回
          console.log('向右滑动');
        }
      }
    };

    document.addEventListener('touchstart', handleTouchStart, { passive: true });
    document.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      document.removeEventListener('touchstart', handleTouchStart);
      document.removeEventListener('touchend', handleTouchEnd);
    };
  }, [isMobile]);

  return (
    <div className={`mobile-optimized-app ${isMobile ? 'mobile' : 'desktop'}`}>
      {/* PWA安装提示 */}
      {showInstallPrompt && !isPWAInstalled && (
        <div className="pwa-install-prompt">
          <div className="install-prompt-content">
            <div className="install-prompt-icon">📱</div>
            <div className="install-prompt-text">
              <h3>安装应用</h3>
              <p>将AI助贷平台添加到主屏幕，获得更好的体验</p>
            </div>
            <div className="install-prompt-actions">
              <button 
                className="install-btn"
                onClick={handleInstallPWA}
              >
                安装
              </button>
              <button 
                className="close-btn"
                onClick={handleCloseInstallPrompt}
              >
                ×
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 移动端底部导航 */}
      {isMobile && isAuthenticated() && (
        <MobileBottomNavigation />
      )}

      {/* 移动端顶部状态栏 */}
      {isMobile && (
        <MobileStatusBar />
      )}

      {/* 主要内容 */}
      <div className="mobile-main-content">
        {children}
      </div>

      {/* 移动端浮动操作按钮 */}
      {isMobile && isAuthenticated() && (
        <MobileFloatingActionButton />
      )}

      {/* 移动端键盘适配 */}
      {isMobile && (
        <div className="mobile-keyboard-spacer" />
      )}
    </div>
  );
};

// 移动端底部导航组件
const MobileBottomNavigation = () => {
  const [activeTab, setActiveTab] = useState('home');

  const tabs = [
    { id: 'home', label: '首页', icon: '🏠', path: '/' },
    { id: 'risk', label: '风险评估', icon: '📊', path: '/risk-assessment' },
    { id: 'matching', label: '智能匹配', icon: '🔍', path: '/auto-matching' },
    { id: 'monitoring', label: '监控', icon: '📈', path: '/monitoring' },
    { id: 'profile', label: '我的', icon: '👤', path: '/profile' }
  ];

  const handleTabClick = (tab) => {
    setActiveTab(tab.id);
    // 这里可以添加路由导航逻辑
    console.log(`切换到: ${tab.label}`);
  };

  return (
    <div className="mobile-bottom-navigation">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => handleTabClick(tab)}
        >
          <div className="nav-icon">{tab.icon}</div>
          <div className="nav-label">{tab.label}</div>
        </button>
      ))}
    </div>
  );
};

// 移动端状态栏组件
const MobileStatusBar = () => {
  const [batteryLevel, setBatteryLevel] = useState(100);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    // 监听网络状态
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // 监听电池状态（如果支持）
    if ('getBattery' in navigator) {
      navigator.getBattery().then(battery => {
        setBatteryLevel(Math.round(battery.level * 100));
        
        battery.addEventListener('levelchange', () => {
          setBatteryLevel(Math.round(battery.level * 100));
        });
      });
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <div className="mobile-status-bar">
      <div className="status-left">
        <span className="time">{new Date().toLocaleTimeString('zh-CN', { 
          hour: '2-digit', 
          minute: '2-digit' 
        })}</span>
      </div>
      <div className="status-center">
        <span className={`network-status ${isOnline ? 'online' : 'offline'}`}>
          {isOnline ? '📶' : '📵'}
        </span>
      </div>
      <div className="status-right">
        <span className="battery-level">
          🔋{batteryLevel}%
        </span>
      </div>
    </div>
  );
};

// 移动端浮动操作按钮
const MobileFloatingActionButton = () => {
  const [isExpanded, setIsExpanded] = useState(false);

  const quickActions = [
    { id: 'new-loan', label: '新贷款', icon: '➕', action: () => console.log('新贷款') },
    { id: 'risk-check', label: '风险检查', icon: '🔍', action: () => console.log('风险检查') },
    { id: 'contact', label: '联系客服', icon: '💬', action: () => console.log('联系客服') },
    { id: 'help', label: '帮助', icon: '❓', action: () => console.log('帮助') }
  ];

  return (
    <div className="mobile-fab-container">
      {isExpanded && (
        <div className="fab-actions">
          {quickActions.map(action => (
            <button
              key={action.id}
              className="fab-action"
              onClick={action.action}
            >
              <span className="fab-action-icon">{action.icon}</span>
              <span className="fab-action-label">{action.label}</span>
            </button>
          ))}
        </div>
      )}
      <button
        className={`mobile-fab ${isExpanded ? 'expanded' : ''}`}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="fab-icon">{isExpanded ? '✕' : '⚡'}</span>
      </button>
    </div>
  );
};

// 移动端性能监控组件
const MobilePerformanceMonitor = ({ metrics }) => {
  const [isVisible, setIsVisible] = useState(false);

  if (!isVisible) {
    return (
      <button 
        className="performance-toggle"
        onClick={() => setIsVisible(true)}
      >
        📊
      </button>
    );
  }

  return (
    <div className="performance-monitor">
      <div className="performance-header">
        <h4>性能监控</h4>
        <button onClick={() => setIsVisible(false)}>×</button>
      </div>
      <div className="performance-metrics">
        <div className="metric-item">
          <span className="metric-label">加载时间</span>
          <span className="metric-value">{metrics.loadTime}ms</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">内存使用</span>
          <span className="metric-value">{metrics.memoryUsage}MB</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">电池电量</span>
          <span className="metric-value">{metrics.batteryLevel}%</span>
        </div>
      </div>
    </div>
  );
};

// 移动端手势识别组件
const MobileGestureRecognizer = ({ onGesture }) => {
  const [gestureHistory, setGestureHistory] = useState([]);

  useEffect(() => {
    let startX = 0;
    let startY = 0;
    let startTime = 0;

    const handleTouchStart = (e) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      startTime = Date.now();
    };

    const handleTouchEnd = (e) => {
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      const endTime = Date.now();
      
      const deltaX = endX - startX;
      const deltaY = endY - startY;
      const deltaTime = endTime - startTime;
      
      const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      const velocity = distance / deltaTime;
      
      if (velocity > 0.5) { // 快速滑动
        if (Math.abs(deltaX) > Math.abs(deltaY)) {
          // 水平滑动
          if (deltaX > 0) {
            onGesture('swipeRight');
          } else {
            onGesture('swipeLeft');
          }
        } else {
          // 垂直滑动
          if (deltaY > 0) {
            onGesture('swipeDown');
          } else {
            onGesture('swipeUp');
          }
        }
      }
    };

    document.addEventListener('touchstart', handleTouchStart, { passive: true });
    document.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      document.removeEventListener('touchstart', handleTouchStart);
      document.removeEventListener('touchend', handleTouchEnd);
    };
  }, [onGesture]);

  return null;
};

// 移动端离线模式组件
const MobileOfflineMode = ({ isOffline }) => {
  const [offlineData, setOfflineData] = useState([]);
  const [syncStatus, setSyncStatus] = useState('idle');

  useEffect(() => {
    if (isOffline) {
      // 加载离线数据
      const cachedData = localStorage.getItem('offlineData');
      if (cachedData) {
        setOfflineData(JSON.parse(cachedData));
      }
    } else {
      // 在线时同步数据
      setSyncStatus('syncing');
      setTimeout(() => {
        setSyncStatus('synced');
        setTimeout(() => setSyncStatus('idle'), 2000);
      }, 1000);
    }
  }, [isOffline]);

  if (!isOffline) {
    return (
      <div className="sync-status">
        {syncStatus === 'syncing' && <span>🔄 同步中...</span>}
        {syncStatus === 'synced' && <span>✅ 已同步</span>}
      </div>
    );
  }

  return (
    <div className="offline-mode">
      <div className="offline-indicator">
        <span>📵 离线模式</span>
        <span className="offline-data-count">{offlineData.length} 条缓存数据</span>
      </div>
    </div>
  );
};

// 移动端键盘适配组件
const MobileKeyboardAdapter = () => {
  const [keyboardHeight, setKeyboardHeight] = useState(0);
  const [isKeyboardVisible, setIsKeyboardVisible] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      const initialHeight = window.innerHeight;
      const currentHeight = window.innerHeight;
      const heightDiff = initialHeight - currentHeight;
      
      if (heightDiff > 150) { // 键盘高度阈值
        setKeyboardHeight(heightDiff);
        setIsKeyboardVisible(true);
      } else {
        setKeyboardHeight(0);
        setIsKeyboardVisible(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div 
      className="keyboard-spacer"
      style={{ height: `${keyboardHeight}px` }}
    />
  );
};

// 移动端主题切换组件
const MobileThemeSwitcher = () => {
  const [theme, setTheme] = useState('light');
  const [isAutoTheme, setIsAutoTheme] = useState(true);

  useEffect(() => {
    // 检测系统主题偏好
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleThemeChange = (e) => {
      if (isAutoTheme) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    };

    mediaQuery.addEventListener('change', handleThemeChange);
    handleThemeChange(mediaQuery);

    return () => mediaQuery.removeEventListener('change', handleThemeChange);
  }, [isAutoTheme]);

  const toggleTheme = () => {
    if (isAutoTheme) {
      setIsAutoTheme(false);
      setTheme(theme === 'light' ? 'dark' : 'light');
    } else {
      setTheme(theme === 'light' ? 'dark' : 'light');
    }
  };

  return (
    <div className="theme-switcher">
      <button 
        className={`theme-btn ${theme}`}
        onClick={toggleTheme}
      >
        {theme === 'light' ? '🌞' : '🌙'}
      </button>
      {isAutoTheme && <span className="auto-theme">自动</span>}
    </div>
  );
};

// 移动端网络状态组件
const MobileNetworkStatus = ({ isOnline }) => {
  const [connectionType, setConnectionType] = useState('unknown');
  const [connectionSpeed, setConnectionSpeed] = useState('unknown');

  useEffect(() => {
    if ('connection' in navigator) {
      const connection = navigator.connection;
      setConnectionType(connection.effectiveType || 'unknown');
      setConnectionSpeed(connection.downlink ? `${connection.downlink}Mbps` : 'unknown');
    }
  }, []);

  return (
    <div className={`network-status ${isOnline ? 'online' : 'offline'}`}>
      <span className="status-icon">
        {isOnline ? '📶' : '📵'}
      </span>
      {isOnline && (
        <span className="connection-info">
          {connectionType} • {connectionSpeed}
        </span>
      )}
    </div>
  );
};

// 移动端快捷操作面板
const MobileQuickActions = () => {
  const [isOpen, setIsOpen] = useState(false);

  const quickActions = [
    { id: 'scan', label: '扫码', icon: '📷', action: () => console.log('扫码') },
    { id: 'voice', label: '语音', icon: '🎤', action: () => console.log('语音') },
    { id: 'location', label: '定位', icon: '📍', action: () => console.log('定位') },
    { id: 'share', label: '分享', icon: '📤', action: () => console.log('分享') },
    { id: 'search', label: '搜索', icon: '🔍', action: () => console.log('搜索') },
    { id: 'settings', label: '设置', icon: '⚙️', action: () => console.log('设置') }
  ];

  return (
    <div className="quick-actions-panel">
      <button 
        className="quick-actions-toggle"
        onClick={() => setIsOpen(!isOpen)}
      >
        ⚡
      </button>
      
      {isOpen && (
        <div className="quick-actions-grid">
          {quickActions.map(action => (
            <button
              key={action.id}
              className="quick-action-btn"
              onClick={() => {
                action.action();
                setIsOpen(false);
              }}
            >
              <span className="action-icon">{action.icon}</span>
              <span className="action-label">{action.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default MobileOptimizedApp;
