// Service Worker for Push Notifications
const CACHE_NAME = 'ai-loan-platform-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

// 安装事件
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: 缓存已打开');
        return cache.addAll(urlsToCache);
      })
  );
});

// 激活事件
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: 删除旧缓存', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// 拦截请求
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // 如果缓存中有，返回缓存
        if (response) {
          return response;
        }
        // 否则从网络获取
        return fetch(event.request);
      }
    )
  );
});

// 推送事件
self.addEventListener('push', (event) => {
  console.log('Service Worker: 收到推送消息', event);
  
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data = { title: '新通知', body: event.data.text() };
    }
  }
  
  const options = {
    body: data.body || '您有新的通知',
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: data.data || {},
    actions: data.actions || [
      {
        action: 'view',
        title: '查看',
        icon: '/icon-192x192.png'
      },
      {
        action: 'close',
        title: '关闭',
        icon: '/icon-192x192.png'
      }
    ],
    requireInteraction: data.requireInteraction || false,
    silent: data.silent || false,
    tag: data.tag || 'ai-loan-notification',
    renotify: data.renotify || false,
    timestamp: Date.now()
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'AI助贷平台', options)
  );
});

// 通知点击事件
self.addEventListener('notificationclick', (event) => {
  console.log('Service Worker: 通知被点击', event);
  
  event.notification.close();
  
  if (event.action === 'close') {
    return;
  }
  
  // 默认行为：打开应用
  const urlToOpen = event.notification.data?.url || '/';
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // 检查是否已经有窗口打开
        for (const client of clientList) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            client.focus();
            client.navigate(urlToOpen);
            return;
          }
        }
        
        // 如果没有窗口打开，打开新窗口
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});

// 通知关闭事件
self.addEventListener('notificationclose', (event) => {
  console.log('Service Worker: 通知被关闭', event);
  
  // 可以在这里发送分析数据
  if (event.notification.data?.analytics) {
    // 发送通知关闭事件到分析服务
    fetch('/api/analytics/notification-closed', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        notificationId: event.notification.data.notificationId,
        timestamp: Date.now(),
        action: 'close'
      })
    }).catch(err => console.log('分析数据发送失败:', err));
  }
});

// 后台同步事件
self.addEventListener('sync', (event) => {
  console.log('Service Worker: 后台同步', event);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

// 执行后台同步
async function doBackgroundSync() {
  try {
    // 同步离线数据
    const offlineData = await getOfflineData();
    if (offlineData.length > 0) {
      await syncOfflineData(offlineData);
    }
  } catch (error) {
    console.error('后台同步失败:', error);
  }
}

// 获取离线数据
async function getOfflineData() {
  try {
    const cache = await caches.open('offline-data');
    const requests = await cache.keys();
    const data = [];
    
    for (const request of requests) {
      const response = await cache.match(request);
      if (response) {
        const json = await response.json();
        data.push(json);
      }
    }
    
    return data;
  } catch (error) {
    console.error('获取离线数据失败:', error);
    return [];
  }
}

// 同步离线数据
async function syncOfflineData(data) {
  try {
    for (const item of data) {
      await fetch('/api/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
      });
    }
    
    // 清除已同步的数据
    const cache = await caches.open('offline-data');
    await cache.delete('/offline-data');
    
    console.log('离线数据同步完成');
  } catch (error) {
    console.error('同步离线数据失败:', error);
  }
}

// 消息事件（用于与主线程通信）
self.addEventListener('message', (event) => {
  console.log('Service Worker: 收到消息', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

// 错误处理
self.addEventListener('error', (event) => {
  console.error('Service Worker: 发生错误', event);
});

self.addEventListener('unhandledrejection', (event) => {
  console.error('Service Worker: 未处理的Promise拒绝', event);
});
