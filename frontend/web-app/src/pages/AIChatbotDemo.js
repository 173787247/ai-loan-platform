import React, { useState, useEffect, useRef } from 'react';
import { useUser } from '../contexts/UserContext';
import aiService from '../services/AIService';
import './AIChatbotDemo.css';

const AIChatbotDemo = () => {
  const { user } = useUser();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentSession, setCurrentSession] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // 滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 初始化欢迎消息
  useEffect(() => {
    if (user && messages.length === 0) {
      const welcomeMessage = {
        id: 'welcome',
        role: 'assistant',
        content: `您好！我是AI智能客服，很高兴为您服务。我可以帮助您：\n\n• 解答贷款相关问题\n• 推荐合适的银行产品\n• 进行风险评估\n• 提供专业建议\n\n请告诉我您需要什么帮助？`,
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
    }
  }, [user, messages.length]);

  // 创建新会话
  const createNewSession = async () => {
    try {
      console.log('创建新会话，用户ID:', user?.id);
      const response = await aiService.createChatSession(user?.id || 'anonymous', 'general');
      console.log('会话创建响应:', response);
      
      if (response.success && response.data?.session_id) {
        const sessionId = response.data.session_id;
        localStorage.setItem('chatSessionId', sessionId);
        setCurrentSession(sessionId);
        console.log('新会话创建成功，ID:', sessionId);
        return sessionId;
      } else {
        throw new Error('会话创建失败：响应格式错误');
      }
    } catch (error) {
      console.error('创建会话失败:', error);
      throw error;
    }
  };

  // 发送消息
  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      // 获取或创建会话ID
      let sessionId = currentSession || localStorage.getItem('chatSessionId');
      
      if (!sessionId || sessionId === 'undefined' || sessionId === 'null') {
        console.log('没有有效会话ID，创建新会话');
        sessionId = await createNewSession();
      } else {
        console.log('使用现有会话ID:', sessionId);
      }

      // 发送消息到AI服务
      console.log('发送消息到AI服务，会话ID:', sessionId);
      const response = await aiService.sendChatMessage(sessionId, userMessage.content, {
        user_id: user?.id || 'anonymous',
        username: user?.username || '用户'
      });

      console.log('AI服务响应:', response);

      // 处理AI回复
      if (response.success && response.data) {
        const aiMessage = {
          id: `ai_${Date.now()}`,
          role: 'assistant',
          content: response.data.response || response.data.message || '抱歉，我无法处理您的问题。',
          timestamp: new Date().toISOString()
        };
        
        console.log('AI回复内容:', aiMessage.content);
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error(response.message || 'AI服务响应格式错误');
      }

    } catch (error) {
      console.error('发送消息失败:', error);
      console.error('错误详情:', error.message);
      
      const errorMessage = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: `抱歉，发送消息时出现错误：${error.message}`,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // 处理回车键发送
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 清空对话
  const clearChat = () => {
    setMessages([]);
    setCurrentSession(null);
    localStorage.removeItem('chatSessionId');
    setError(null);
  };

  // 搜索知识库
  const searchKnowledge = async (query) => {
    try {
      const response = await aiService.searchKnowledge(query);
      return response.data?.results || [];
    } catch (error) {
      console.error('搜索知识库失败:', error);
      return [];
    }
  };

  // 渲染消息
  const renderMessage = (message, index) => {
    if (!message || typeof message !== 'object') {
      console.warn('无效的消息对象:', message);
      return null;
    }

    const isUser = message.role === 'user';
    const messageId = message.id || `msg_${index}`;

    return (
      <div key={messageId} className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
        <div className="message-content">
          <div className="message-text">
            {message.content}
          </div>
          <div className="message-time">
            {formatTime(message.timestamp)}
          </div>
        </div>
      </div>
    );
  };

  // 格式化时间
  const formatTime = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      console.error('时间格式化失败:', error);
      return '';
    }
  };

  if (!user) {
    return (
      <div className="ai-chatbot-demo">
        <div className="login-prompt">
          <h2>请先登录</h2>
          <p>您需要登录后才能使用AI智能客服功能。</p>
        </div>
      </div>
    );
  }

  return (
    <div className="ai-chatbot-demo">
      <div className="demo-content">
        {/* 左侧控制面板 */}
        <div className="control-panel">
          <h3>客服设置</h3>
          
          <div className="session-controls">
            <div className="session-status">
              {currentSession ? `会话已连接` : `未连接会话`}
            </div>
          </div>

          <div className="role-selector">
            <label>选择客服角色</label>
            <select>
              <option value="general">通用客服</option>
              <option value="loan_specialist">贷款专家</option>
              <option value="risk_analyst">风险分析师</option>
              <option value="technical_support">技术支持</option>
            </select>
          </div>

          <div className="preset-questions">
            <h4>预设问题</h4>
            <div className="question-list">
              <button 
                className="question-btn"
                onClick={() => setInputMessage("我想了解贷款产品")}
              >
                我想了解贷款产品
              </button>
              <button 
                className="question-btn"
                onClick={() => setInputMessage("个人信用贷款的利率是多少?")}
              >
                个人信用贷款的利率是多少?
              </button>
              <button 
                className="question-btn"
                onClick={() => setInputMessage("申请贷款需要什么条件?")}
              >
                申请贷款需要什么条件?
              </button>
              <button 
                className="question-btn"
                onClick={() => setInputMessage("如何申请贷款?")}
              >
                如何申请贷款?
              </button>
            </div>
          </div>
        </div>

        {/* 中间聊天区域 */}
        <div className="chat-container">
          <div className="chat-header">
            <h2>通用客服</h2>
            <button onClick={clearChat} className="clear-btn">
              清空对话
            </button>
          </div>

          <div className="messages-container">
            {messages.map((message, index) => renderMessage(message, index))}
            {isLoading && (
              <div className="message ai-message">
                <div className="message-content">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    正在思考中...
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <div className="input-wrapper">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="请输入您的问题..."
                disabled={isLoading}
                rows="3"
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="send-btn"
              >
                {isLoading ? '发送中...' : '发送'}
              </button>
            </div>
          </div>
        </div>

        {/* 右侧对话记录 */}
        <div className="chat-history">
          <h3>对话记录</h3>
          <div className="history-list">
            {messages.length === 0 ? (
              <div className="empty-history">
                <p>暂无对话记录</p>
                <button onClick={() => setInputMessage("开始与AI客服对话")}>
                  开始与AI客服对话
                </button>
              </div>
            ) : (
              <div className="history-items">
                {messages.map((message, index) => (
                  <div key={message.id || index} className="history-item">
                    <div className="history-role">
                      {message.role === 'user' ? '用户' : 'AI客服'}
                    </div>
                    <div className="history-content">
                      {message.content.substring(0, 50)}...
                    </div>
                    <div className="history-time">
                      {formatTime(message.timestamp)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <span>错误：{error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}
    </div>
  );
};

export default AIChatbotDemo;