// 安全工具函数

// XSS防护
export const xssProtection = {
  // 转义HTML字符
  escapeHtml: (text) => {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;',
      '/': '&#x2F;'
    };
    return text.replace(/[&<>"'/]/g, (s) => map[s]);
  },

  // 清理用户输入
  sanitizeInput: (input) => {
    if (typeof input !== 'string') return input;
    return input
      .trim()
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
      .replace(/javascript:/gi, '')
      .replace(/on\w+\s*=/gi, '');
  },

  // 验证HTML内容
  validateHtml: (html) => {
    const allowedTags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li'];
    const allowedAttributes = ['class', 'id'];
    
    const temp = document.createElement('div');
    temp.innerHTML = html;
    
    const allElements = temp.querySelectorAll('*');
    for (let element of allElements) {
      if (!allowedTags.includes(element.tagName.toLowerCase())) {
        return false;
      }
      
      for (let attr of element.attributes) {
        if (!allowedAttributes.includes(attr.name)) {
          return false;
        }
      }
    }
    
    return true;
  }
};

// CSRF防护
export const csrfProtection = {
  // 生成CSRF令牌
  generateToken: () => {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
  },

  // 验证CSRF令牌
  validateToken: (token) => {
    const storedToken = localStorage.getItem('csrf_token');
    return storedToken && storedToken === token;
  },

  // 设置CSRF令牌
  setToken: (token) => {
    localStorage.setItem('csrf_token', token);
  },

  // 获取CSRF令牌
  getToken: () => {
    return localStorage.getItem('csrf_token');
  }
};

// 输入验证
export const inputValidation = {
  // 验证邮箱
  validateEmail: (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // 验证密码强度
  validatePassword: (password) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    return {
      isValid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar,
      strength: {
        length: password.length >= minLength,
        upperCase: hasUpperCase,
        lowerCase: hasLowerCase,
        numbers: hasNumbers,
        specialChar: hasSpecialChar
      }
    };
  },

  // 验证用户名
  validateUsername: (username) => {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    return usernameRegex.test(username);
  },

  // 验证手机号
  validatePhone: (phone) => {
    const phoneRegex = /^1[3-9]\d{9}$/;
    return phoneRegex.test(phone);
  },

  // 验证身份证号
  validateIdCard: (idCard) => {
    const idCardRegex = /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/;
    return idCardRegex.test(idCard);
  },

  // 验证URL
  validateUrl: (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  },

  // 验证数字范围
  validateNumberRange: (number, min, max) => {
    const num = Number(number);
    return !isNaN(num) && num >= min && num <= max;
  }
};

// 数据加密
export const dataEncryption = {
  // 简单的Base64编码（不用于敏感数据）
  encode: (data) => {
    return btoa(JSON.stringify(data));
  },

  // Base64解码
  decode: (encodedData) => {
    try {
      return JSON.parse(atob(encodedData));
    } catch {
      return null;
    }
  },

  // 生成随机字符串
  generateRandomString: (length = 32) => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  },

  // 简单的哈希函数（不用于密码）
  simpleHash: (str) => {
    let hash = 0;
    if (str.length === 0) return hash;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转换为32位整数
    }
    return hash.toString();
  }
};

// 会话管理
export const sessionManagement = {
  // 设置会话数据
  setSession: (key, value, expiresIn = 3600000) => { // 默认1小时
    const sessionData = {
      value,
      expires: Date.now() + expiresIn
    };
    sessionStorage.setItem(key, JSON.stringify(sessionData));
  },

  // 获取会话数据
  getSession: (key) => {
    const sessionData = sessionStorage.getItem(key);
    if (!sessionData) return null;
    
    const parsed = JSON.parse(sessionData);
    if (Date.now() > parsed.expires) {
      sessionStorage.removeItem(key);
      return null;
    }
    
    return parsed.value;
  },

  // 清除会话数据
  clearSession: (key) => {
    sessionStorage.removeItem(key);
  },

  // 清除所有会话数据
  clearAllSessions: () => {
    sessionStorage.clear();
  },

  // 检查会话是否有效
  isSessionValid: (key) => {
    const sessionData = sessionStorage.getItem(key);
    if (!sessionData) return false;
    
    const parsed = JSON.parse(sessionData);
    return Date.now() <= parsed.expires;
  }
};

// 权限控制
export const permissionControl = {
  // 检查用户权限
  hasPermission: (user, permission) => {
    if (!user || !user.permissions) return false;
    return user.permissions.includes('all') || user.permissions.includes(permission);
  },

  // 检查用户角色
  hasRole: (user, role) => {
    if (!user || !user.userType) return false;
    return user.userType === role;
  },

  // 检查管理员权限
  isAdmin: (user) => {
    return this.hasRole(user, 'admin');
  },

  // 检查借款方权限
  isBorrower: (user) => {
    return this.hasRole(user, 'borrower');
  },

  // 检查放贷方权限
  isLender: (user) => {
    return this.hasRole(user, 'lender');
  }
};

// 安全配置
export const securityConfig = {
  // 密码策略
  passwordPolicy: {
    minLength: 8,
    requireUpperCase: true,
    requireLowerCase: true,
    requireNumbers: true,
    requireSpecialChars: true,
    maxAttempts: 5,
    lockoutDuration: 300000 // 5分钟
  },

  // 会话配置
  sessionConfig: {
    maxAge: 3600000, // 1小时
    secure: true,
    httpOnly: true,
    sameSite: 'strict'
  },

  // 请求配置
  requestConfig: {
    timeout: 30000, // 30秒
    retryAttempts: 3,
    retryDelay: 1000 // 1秒
  }
};

// 安全监控
export const securityMonitoring = {
  // 记录安全事件
  logSecurityEvent: (event, details = {}) => {
    const logEntry = {
      timestamp: new Date().toISOString(),
      event,
      details,
      userAgent: navigator.userAgent,
      url: window.location.href
    };
    
    console.warn('安全事件:', logEntry);
    
    // 这里可以发送到安全监控服务
    // sendToSecurityService(logEntry);
  },

  // 检测异常行为
  detectAnomaly: (user, action) => {
    const suspiciousPatterns = [
      'rapid_requests', // 快速请求
      'unusual_location', // 异常位置
      'failed_logins', // 登录失败
      'privilege_escalation' // 权限提升
    ];
    
    // 简单的异常检测逻辑
    // 实际应用中需要更复杂的算法
    return false;
  },

  // 监控API调用
  monitorApiCalls: (url, method, response) => {
    if (response.status >= 400) {
      this.logSecurityEvent('api_error', {
        url,
        method,
        status: response.status
      });
    }
  }
};

export default {
  xssProtection,
  csrfProtection,
  inputValidation,
  dataEncryption,
  sessionManagement,
  permissionControl,
  securityConfig,
  securityMonitoring
};
