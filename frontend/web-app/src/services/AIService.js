/**
 * AI服务接口 - 简化版本
 */
class AIService {
  constructor() {
    this.baseURL = '/ai';
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    try {
      console.log(`发送API请求: ${url}`);
      
      // 添加超时控制
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30秒超时
      
      const response = await fetch(url, {
        ...config,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      console.log(`API响应状态: ${response.status}`);
      
      const data = await response.json();
      console.log(`API响应数据:`, data);
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }
      
      return data;
    } catch (error) {
      if (error.name === 'AbortError') {
        console.error(`API请求超时: ${endpoint}`);
        throw new Error('请求超时，请重试');
      }
      console.error(`API请求失败: ${endpoint}`, error);
      throw error;
    }
  }

  // 创建聊天会话
  async createChatSession(userId, chatbotRole = 'general') {
    return this.request('/api/v1/chat/session', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        chatbot_role: chatbotRole
      })
    });
  }

  // 发送聊天消息
  async sendChatMessage(sessionId, message, userInfo = null) {
    return this.request('/api/v1/chat/message', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
        user_info: userInfo
      })
    });
  }

  // 搜索知识库
  async searchKnowledge(query) {
    return this.request('/api/v1/rag/search', {
      method: 'POST',
      body: JSON.stringify({
        query: query,
        search_type: 'simple',
        max_results: 5
      })
    });
  }
}

export default new AIService();
