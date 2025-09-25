// 测试API调用的简单脚本
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

async function testAPI() {
  try {
    console.log('Testing API with URL:', API_BASE_URL);
    
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
    
    return data;
  } catch (error) {
    console.error('API test failed:', error);
    return null;
  }
}

// 导出测试函数
window.testAPI = testAPI;
