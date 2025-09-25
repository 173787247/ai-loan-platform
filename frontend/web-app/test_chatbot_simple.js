// 简单的聊天机器人测试脚本
const testChatbot = async () => {
  const API_BASE_URL = 'http://ai-loan-ai-service:8000/api/v1';
  
  console.log('开始测试聊天机器人API...');
  
  try {
    // 测试健康检查
    console.log('1. 测试健康检查...');
    const healthResponse = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
    const healthData = await healthResponse.json();
    console.log('健康检查结果:', healthData);
    
    // 测试创建会话
    console.log('2. 测试创建会话...');
    const sessionResponse = await fetch(`${API_BASE_URL}/chat/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 'test_user',
        chatbot_role: 'general'
      })
    });
    
    console.log('会话创建响应状态:', sessionResponse.status);
    console.log('会话创建响应头:', Object.fromEntries(sessionResponse.headers.entries()));
    
    if (sessionResponse.ok) {
      const sessionData = await sessionResponse.json();
      console.log('会话创建成功:', sessionData);
      
      // 测试发送消息
      console.log('3. 测试发送消息...');
      const messageResponse = await fetch(`${API_BASE_URL}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionData.data.session_id,
          message: '你好',
          user_info: {
            user_id: 'test_user',
            user_role: 'borrower',
            username: 'test_user'
          }
        })
      });
      
      console.log('消息发送响应状态:', messageResponse.status);
      if (messageResponse.ok) {
        const messageData = await messageResponse.json();
        console.log('消息发送成功:', messageData);
      } else {
        const errorText = await messageResponse.text();
        console.log('消息发送失败:', errorText);
      }
    } else {
      const errorText = await sessionResponse.text();
      console.log('会话创建失败:', errorText);
    }
    
  } catch (error) {
    console.error('测试过程中出错:', error);
  }
};

// 运行测试
testChatbot();
