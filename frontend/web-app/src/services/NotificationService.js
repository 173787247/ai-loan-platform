// 通知服务 - 支持多种通知方式
class NotificationService {
  constructor() {
    this.emailConfig = {
      apiKey: process.env.REACT_APP_EMAIL_API_KEY || 'demo-key',
      fromEmail: process.env.REACT_APP_FROM_EMAIL || 'noreply@ai-loan-platform.com'
    };
    
    this.smsConfig = {
      apiKey: process.env.REACT_APP_SMS_API_KEY || 'demo-key',
      fromNumber: process.env.REACT_APP_SMS_FROM || '+1234567890'
    };
    
    this.pushConfig = {
      vapidKey: process.env.REACT_APP_VAPID_KEY || 'demo-vapid-key',
      serverKey: process.env.REACT_APP_SERVER_KEY || 'demo-server-key'
    };
    
    this.isPushSupported = 'Notification' in window && 'serviceWorker' in navigator;
    this.pushSubscription = null;
  }

  // 初始化推送通知
  async initializePush() {
    if (!this.isPushSupported) {
      console.warn('推送通知不支持此浏览器');
      return false;
    }

    try {
      // 请求通知权限
      const permission = await Notification.requestPermission();
      if (permission !== 'granted') {
        console.warn('用户拒绝了通知权限');
        return false;
      }

      // 注册Service Worker
      const registration = await navigator.serviceWorker.register('/sw.js');
      
      // 获取推送订阅
      this.pushSubscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(this.pushConfig.vapidKey)
      });

      console.log('推送通知初始化成功');
      return true;
    } catch (error) {
      console.error('推送通知初始化失败:', error);
      return false;
    }
  }

  // 发送邮件通知
  async sendEmail(to, subject, content, options = {}) {
    try {
      // 模拟API调用
      const response = await fetch('/api/notifications/email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.emailConfig.apiKey}`
        },
        body: JSON.stringify({
          to,
          subject,
          content,
          from: this.emailConfig.fromEmail,
          ...options
        })
      });

      if (!response.ok) {
        throw new Error(`邮件发送失败: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('邮件发送成功:', result);
      return { success: true, messageId: result.messageId };
    } catch (error) {
      console.error('邮件发送失败:', error);
      return { success: false, error: error.message };
    }
  }

  // 发送短信通知
  async sendSMS(to, message, options = {}) {
    try {
      // 模拟API调用
      const response = await fetch('/api/notifications/sms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.smsConfig.apiKey}`
        },
        body: JSON.stringify({
          to,
          message,
          from: this.smsConfig.fromNumber,
          ...options
        })
      });

      if (!response.ok) {
        throw new Error(`短信发送失败: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('短信发送成功:', result);
      return { success: true, messageId: result.messageId };
    } catch (error) {
      console.error('短信发送失败:', error);
      return { success: false, error: error.message };
    }
  }

  // 发送推送通知
  async sendPush(title, body, options = {}) {
    if (!this.pushSubscription) {
      console.warn('推送订阅未初始化');
      return { success: false, error: '推送订阅未初始化' };
    }

    try {
      const response = await fetch('/api/notifications/push', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.pushConfig.serverKey}`
        },
        body: JSON.stringify({
          subscription: this.pushSubscription,
          title,
          body,
          ...options
        })
      });

      if (!response.ok) {
        throw new Error(`推送发送失败: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('推送发送成功:', result);
      return { success: true, messageId: result.messageId };
    } catch (error) {
      console.error('推送发送失败:', error);
      return { success: false, error: error.message };
    }
  }

  // 发送多渠道通知
  async sendMultiChannel(recipient, title, message, channels = ['email', 'sms', 'push']) {
    const results = {};

    for (const channel of channels) {
      switch (channel) {
        case 'email':
          results.email = await this.sendEmail(
            recipient.email, 
            title, 
            message,
            { recipientName: recipient.name }
          );
          break;
        case 'sms':
          results.sms = await this.sendSMS(
            recipient.phone, 
            `${title}: ${message}`
          );
          break;
        case 'push':
          results.push = await this.sendPush(title, message);
          break;
        default:
          console.warn(`不支持的通知渠道: ${channel}`);
      }
    }

    return results;
  }

  // 发送贷款申请通知
  async sendLoanApplicationNotification(borrower, loanData) {
    const title = '贷款申请提交成功';
    const message = `您的贷款申请已提交，申请金额：${loanData.amount}元，我们将在1-3个工作日内处理。`;

    return await this.sendMultiChannel(borrower, title, message, ['email', 'sms', 'push']);
  }

  // 发送风险评估通知
  async sendRiskAssessmentNotification(borrower, riskData) {
    const title = '风险评估完成';
    const message = `您的风险评估已完成，风险等级：${riskData.level}，评分：${riskData.score}分。`;

    return await this.sendMultiChannel(borrower, title, message, ['email', 'push']);
  }

  // 发送匹配结果通知
  async sendMatchingNotification(borrower, matchingResults) {
    const title = '智能匹配完成';
    const message = `为您找到${matchingResults.length}个匹配的贷款产品，请查看详情。`;

    return await this.sendMultiChannel(borrower, title, message, ['email', 'push']);
  }

  // 发送系统通知
  async sendSystemNotification(recipient, type, data) {
    const notifications = {
      'loan_approved': {
        title: '贷款申请已批准',
        message: `恭喜！您的贷款申请已获得批准，放款金额：${data.amount}元。`
      },
      'loan_rejected': {
        title: '贷款申请未通过',
        message: `很抱歉，您的贷款申请未通过审核。原因：${data.reason}。`
      },
      'payment_due': {
        title: '还款提醒',
        message: `您的还款日期即将到来，请及时还款。金额：${data.amount}元。`
      },
      'system_maintenance': {
        title: '系统维护通知',
        message: `系统将于${data.time}进行维护，预计持续${data.duration}。`
      }
    };

    const notification = notifications[type];
    if (!notification) {
      throw new Error(`未知的通知类型: ${type}`);
    }

    return await this.sendMultiChannel(recipient, notification.title, notification.message);
  }

  // 工具方法：转换VAPID密钥
  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  // 获取通知历史
  async getNotificationHistory(userId, limit = 50) {
    try {
      const response = await fetch(`/api/notifications/history/${userId}?limit=${limit}`);
      if (!response.ok) {
        throw new Error('获取通知历史失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取通知历史失败:', error);
      return [];
    }
  }

  // 标记通知为已读
  async markAsRead(notificationId) {
    try {
      const response = await fetch(`/api/notifications/${notificationId}/read`, {
        method: 'PUT'
      });
      return response.ok;
    } catch (error) {
      console.error('标记通知已读失败:', error);
      return false;
    }
  }
}

// 创建单例实例
const notificationService = new NotificationService();

export default notificationService;
