const fetch = require('node-fetch');

async function testAPI() {
  try {
    console.log('Testing API call...');
    const response = await fetch('http://ai-loan-ai-service:8000/api/v1/chat/session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: '2',
        chatbot_role: 'general'
      })
    });
    
    console.log('Response status:', response.status);
    const data = await response.json();
    console.log('Response data:', data);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

testAPI();
