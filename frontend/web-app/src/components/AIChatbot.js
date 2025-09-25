import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useUser } from '../contexts/UserContext';
import { useNotification } from './NotificationSystem';
import FileUpload from './FileUpload';
import aiService from '../services/AIService';
import './AIChatbot.css';

const AIChatbot = () => {
  const { user } = useUser();
  const { showSuccess, showError } = useNotification();
  
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [chatbotRole, setChatbotRole] = useState('general');
  const [showFileUpload, setShowFileUpload] = useState(false);
  
  const messagesEndRef = useRef(null);

  // 聊天机器人角色选项
  const chatbotRoles = [
    { value: 'general', label: '通用客服', icon: '🤖' },
    { value: 'loan_specialist', label: '贷款专家', icon: '💰' },
    { value: 'risk_analyst', label: '风险分析师', icon: '📊' },
    { value: 'technical_support', label: '技术支持', icon: '🔧' }
  ];

  // 创建会话
  const createSession = useCallback(async () => {
    if (!user || !user.id) {
      console.log('用户未登录，无法创建会话');
      return;
    }
    
    try {
      console.log('开始创建聊天会话...', { userId: user.id, chatbotRole });
      setIsLoading(true);
      
      const response = await aiService.createChatSession(String(user.id), chatbotRole);
      console.log('API响应:', response);
      
      if (response.success) {
        console.log('会话创建成功:', response.data);
        setSessionId(response.data.session_id);
        setChatbotRole(response.data.chatbot_role);
        
        // 添加欢迎消息
        const welcomeMessages = {
          general: '👋 您好！我是AI智能客服，很高兴为您服务！请问有什么可以帮助您的吗？',
          loan_specialist: '💰 您好！我是贷款专家，专门为您提供贷款产品咨询和建议。请告诉我您的贷款需求！',
          risk_analyst: '📊 您好！我是风险分析师，可以为您解释风险评估和信用评分相关问题。',
          technical_support: '🔧 您好！我是技术支持，可以帮助您解决平台使用中的技术问题。'
        };
        
        const welcomeMessage = {
          id: 'welcome',
          role: 'assistant',
          content: welcomeMessages[chatbotRole] || welcomeMessages.general,
          timestamp: new Date().toISOString(),
          isWelcome: true
        };
        setMessages([welcomeMessage]);
        
        showSuccess('AI智能客服已就绪');
      } else {
        console.error('API返回失败:', response);
        throw new Error(response.message || '创建会话失败');
      }
    } catch (error) {
      console.error('创建会话失败:', error);
      showError('创建聊天会话失败');
    } finally {
      setIsLoading(false);
    }
  }, [user, chatbotRole, showError, showSuccess]);

  // 用户登录后自动创建会话
  useEffect(() => {
    if (user && !sessionId) {
      console.log('用户已登录，开始创建聊天会话...', { user: user.id, username: user.username });
      createSession();
    }
  }, [user, sessionId, createSession]);


  // 聊天窗口打开时自动创建会话
  useEffect(() => {
    console.log('聊天窗口状态检查:', { 
      isOpen, 
      user: !!user, 
      sessionId, 
      userId: user?.id,
      username: user?.username,
      userType: user?.userType
    });
    if (isOpen && user && !sessionId) {
      console.log('聊天窗口已打开，开始创建聊天会话...', { user: user.id, username: user.username });
      createSession();
    } else if (isOpen && !user) {
      console.log('用户未登录，无法创建会话');
    } else if (isOpen && sessionId) {
      console.log('会话已存在，无需创建');
    }
  }, [isOpen, user, sessionId, createSession]);

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 发送消息
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !sessionId || isLoading) return;

    const userMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await aiService.sendChatMessage(sessionId, inputMessage, {
        user_id: String(user.id),
        user_role: user.role,
        username: user.username
      });

      if (response.success) {
        const aiMessage = {
          id: `ai_${Date.now()}`,
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toISOString(),
          metadata: response.data.metadata
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error(response.message || '发送消息失败');
      }
    } catch (error) {
      console.error('发送消息失败:', error);
      showError('发送消息失败，请重试');
      
      const errorMessage = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: '抱歉，我暂时无法处理您的请求，请稍后再试。',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // 处理文件上传
  const handleFileUpload = (files) => {
    const fileNames = files.map(file => file.name).join(', ');
    const uploadMessage = `📎 我已上传了以下文件：${fileNames}\n\n请帮我分析这些贷款申请材料。`;
    
    setMessages(prev => [...prev, {
      id: `user_${Date.now()}`,
      role: 'user',
      content: uploadMessage,
      timestamp: new Date().toISOString()
    }]);

    // 自动发送消息给AI
    setTimeout(() => {
      setInputMessage(uploadMessage);
      handleSendMessage();
    }, 500);
  };

  // 处理回车键
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // 切换角色
  const handleRoleChange = async (newRole) => {
    if (newRole === chatbotRole) return;
    
    setChatbotRole(newRole);
    setMessages([]);
    setSessionId(null);
    
    // 创建新会话
    await createSession();
  };

  // 清空聊天
  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    createSession();
  };

  // 格式化时间
  const formatTime = (timestamp) =>
    new Date(timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });

  // 渲染消息
  const renderMessage = (message, index) => {
    const isUser = message.role === 'user';
    const isError = message.isError;
    
    return (
      <div 
        key={message.id || index} 
        className={`chat-message ${isUser ? 'user' : 'assistant'} ${isError ? 'error' : ''}`}
      >
        <div className="message-bubble">
          <div className="message-header">
            <span className="message-role">
              {isUser ? user?.username || '您' : 'AI客服'}
            </span>
            <span className="message-time">
              {formatTime(message.timestamp)}
            </span>
          </div>
          
          <div className="message-text">
            {message.content}
          </div>
          
          {message.metadata?.knowledge_used && (
            <div className="knowledge-used">
              <small>💡 基于知识库信息回答</small>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="ai-chatbot">
      {/* 聊天窗口 */}
      <div className={`chat-window ${isOpen ? 'open' : ''}`}>
        <div className="chat-header">
          <div className="chat-title">
            <span className="chatbot-icon">
              {chatbotRoles.find(r => r.value === chatbotRole)?.icon || '🤖'}
            </span>
            <span>AI智能客服</span>
          </div>
          
          <div className="chat-controls">
            <select
              value={chatbotRole}
              onChange={(e) => handleRoleChange(e.target.value)}
              className="role-selector"
              disabled={isLoading}
            >
              {chatbotRoles.map(role => (
                <option key={role.value} value={role.value}>
                  {role.icon} {role.label}
                </option>
              ))}
            </select>
            <button onClick={clearChat} className="clear-chat-button" title="清空聊天">
              <span role="img" aria-label="clear">🗑️</span>
            </button>
            <button onClick={() => setIsOpen(false)} className="close-chat-button" title="关闭">
              ✖️
            </button>
          </div>
        </div>

        <div className="chat-messages">
          {messages.length === 0 && !isLoading && (
            <div className="empty-chat-message">
              <span role="img" aria-label="robot">🤖</span>
              <p>开始与AI客服对话吧!</p>
              <p>选择一个角色开始您的咨询。</p>
            </div>
          )}
          {messages.map(renderMessage)}
          {isLoading && (
            <div className="chat-message assistant typing">
              <div className="message-bubble">
                <div className="message-text">AI正在思考...</div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <div className="input-toolbar">
            <button 
              className="file-upload-btn"
              onClick={() => setShowFileUpload(true)}
              disabled={!user}
              title="上传文件"
            >
              📎
            </button>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={user ? "输入您的问题..." : "请先登录以使用AI客服"}
              disabled={!user}
              style={{
                flex: 1,
                border: '1px solid #ddd',
                borderRadius: '20px',
                padding: '8px 16px',
                fontSize: '14px',
                outline: 'none',
                backgroundColor: user ? 'white' : '#f8f9fa',
                cursor: user ? 'text' : 'not-allowed'
              }}
            />
            <button 
              onClick={handleSendMessage} 
              disabled={isLoading || !inputMessage.trim()}
              style={{
                background: (isLoading || !inputMessage.trim()) ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '20px',
                padding: '8px 16px',
                cursor: (isLoading || !inputMessage.trim()) ? 'not-allowed' : 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
                minWidth: '60px',
                height: '36px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              {isLoading ? '发送中...' : '发送'}
            </button>
          </div>
        </div>
      </div>

      {/* 聊天按钮 */}
      <button
        className={`chat-toggle ${isOpen ? 'active' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        title="AI智能客服"
      >
        <span className="chatbot-icon">🤖</span>
        {!sessionId && <span className="notification-badge">!</span>}
      </button>

      {/* 文件上传组件 */}
      <FileUpload
        isVisible={showFileUpload}
        onFileUpload={handleFileUpload}
        onClose={() => setShowFileUpload(false)}
      />
    </div>
  );
};

export default AIChatbot;
