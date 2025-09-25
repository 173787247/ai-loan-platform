// 详细测试API调用
const API_BASE_URL = 'http://host.docker.internal:8000/api/v1';

async function testCreateChatSession() {
  try {
    console.log('=== 测试创建聊天会话 ===');
    console.log('API Base URL:', API_BASE_URL);
    
    const requestBody = {
      user_id: 'test_user',
      chatbot_role: 'general'
    };
    
    console.log('请求体:', JSON.stringify(requestBody, null, 2));
    
    const response = await fetch(`${API_BASE_URL}/chat/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });
    
    console.log('响应状态:', response.status);
    console.log('响应头:', Object.fromEntries(response.headers.entries()));
    
    const responseText = await response.text();
    console.log('响应内容:', responseText);
    
    if (response.ok) {
      const data = JSON.parse(responseText);
      console.log('✅ 创建聊天会话成功:', data);
    } else {
      console.log('❌ 创建聊天会话失败:', responseText);
    }
  } catch (error) {
    console.error('❌ 请求失败:', error);
  }
}

// 运行测试
testCreateChatSession();
