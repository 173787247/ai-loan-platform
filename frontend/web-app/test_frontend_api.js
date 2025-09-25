// 测试前端API调用
const API_BASE_URL = 'http://host.docker.internal:8000/api/v1';

async function testCreateChatSession() {
  try {
    console.log('测试创建聊天会话...');
    console.log('API Base URL:', API_BASE_URL);
    
    const response = await fetch(`${API_BASE_URL}/chat/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 'test_user',
        chatbot_role: 'general'
      })
    });
    
    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);
    
    const data = await response.json();
    console.log('Response data:', data);
    
    if (response.ok) {
      console.log('✅ 创建聊天会话成功');
    } else {
      console.log('❌ 创建聊天会话失败:', data);
    }
  } catch (error) {
    console.error('❌ 请求失败:', error);
  }
}

// 运行测试
testCreateChatSession();
