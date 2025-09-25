// 性能优化工具函数

// 防抖函数
export const debounce = (func, wait, immediate = false) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      timeout = null;
      if (!immediate) func(...args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func(...args);
  };
};

// 节流函数
export const throttle = (func, limit) => {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// 图片懒加载
export const lazyLoadImages = () => {
  const images = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.remove('lazy');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach(img => imageObserver.observe(img));
};

// 虚拟滚动
export const virtualScroll = (container, items, itemHeight, renderItem) => {
  const containerHeight = container.clientHeight;
  const visibleItems = Math.ceil(containerHeight / itemHeight) + 1;
  const scrollTop = container.scrollTop;
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + visibleItems, items.length);

  const visibleItemsData = items.slice(startIndex, endIndex);
  const offsetY = startIndex * itemHeight;

  return {
    visibleItems: visibleItemsData,
    offsetY,
    totalHeight: items.length * itemHeight
  };
};

// 内存管理
export const memoryManager = {
  cache: new Map(),
  maxSize: 100,

  set(key, value) {
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  },

  get(key) {
    return this.cache.get(key);
  },

  clear() {
    this.cache.clear();
  },

  size() {
    return this.cache.size;
  }
};

// 请求缓存
export const requestCache = {
  cache: new Map(),
  pending: new Map(),

  async get(key, fetcher, ttl = 300000) { // 默认5分钟TTL
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < ttl) {
      return cached.data;
    }

    if (this.pending.has(key)) {
      return this.pending.get(key);
    }

    const promise = fetcher().then(data => {
      this.cache.set(key, {
        data,
        timestamp: Date.now()
      });
      this.pending.delete(key);
      return data;
    }).catch(error => {
      this.pending.delete(key);
      throw error;
    });

    this.pending.set(key, promise);
    return promise;
  },

  clear() {
    this.cache.clear();
    this.pending.clear();
  }
};

// 组件懒加载
export const lazyLoadComponent = (importFunc) => {
  return React.lazy(importFunc);
};

// 代码分割
export const codeSplit = {
  // 路由级别的代码分割
  routeSplit: (importFunc) => {
    return React.lazy(importFunc);
  },

  // 组件级别的代码分割
  componentSplit: (importFunc) => {
    return React.lazy(importFunc);
  }
};

// 性能监控
export const performanceMonitor = {
  // 测量函数执行时间
  measureTime: (name, func) => {
    const start = performance.now();
    const result = func();
    const end = performance.now();
    console.log(`${name} 执行时间: ${end - start}ms`);
    return result;
  },

  // 测量异步函数执行时间
  measureAsyncTime: async (name, func) => {
    const start = performance.now();
    const result = await func();
    const end = performance.now();
    console.log(`${name} 执行时间: ${end - start}ms`);
    return result;
  },

  // 监控内存使用
  monitorMemory: () => {
    if (performance.memory) {
      const memory = performance.memory;
      console.log('内存使用情况:', {
        used: Math.round(memory.usedJSHeapSize / 1024 / 1024) + 'MB',
        total: Math.round(memory.totalJSHeapSize / 1024 / 1024) + 'MB',
        limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024) + 'MB'
      });
    }
  },

  // 监控长任务
  observeLongTasks: (callback) => {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (entry.duration > 50) { // 超过50ms的任务
            callback(entry);
          }
        });
      });
      observer.observe({ entryTypes: ['longtask'] });
      return observer;
    }
  }
};

// 资源预加载
export const resourcePreloader = {
  // 预加载图片
  preloadImages: (urls) => {
    urls.forEach(url => {
      const img = new Image();
      img.src = url;
    });
  },

  // 预加载字体
  preloadFonts: (urls) => {
    urls.forEach(url => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = url;
      link.as = 'font';
      link.type = 'font/woff2';
      link.crossOrigin = 'anonymous';
      document.head.appendChild(link);
    });
  },

  // 预加载关键资源
  preloadCritical: (urls) => {
    urls.forEach(url => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = url;
      link.as = 'fetch';
      link.crossOrigin = 'anonymous';
      document.head.appendChild(link);
    });
  }
};

// 批量更新
export const batchUpdate = (updates) => {
  return new Promise((resolve) => {
    requestAnimationFrame(() => {
      updates.forEach(update => update());
      resolve();
    });
  });
};

// 优化重绘和回流
export const optimizeRendering = {
  // 批量DOM操作
  batchDOMUpdates: (updates) => {
    const fragment = document.createDocumentFragment();
    updates.forEach(update => update(fragment));
    document.body.appendChild(fragment);
  },

  // 使用transform代替position
  useTransform: (element, x, y) => {
    element.style.transform = `translate3d(${x}px, ${y}px, 0)`;
  },

  // 避免强制同步布局
  avoidForcedLayout: (callback) => {
    requestAnimationFrame(() => {
      callback();
    });
  }
};

export default {
  debounce,
  throttle,
  lazyLoadImages,
  virtualScroll,
  memoryManager,
  requestCache,
  lazyLoadComponent,
  codeSplit,
  performanceMonitor,
  resourcePreloader,
  batchUpdate,
  optimizeRendering
};
