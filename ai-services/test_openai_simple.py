import aiohttp
import asyncio
import os

async def test_openai():
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {api_key[:20]}...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 10
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.openai.com/v1/chat/completions', 
                                  headers=headers, 
                                  json=payload, 
                                  timeout=30) as response:
                print(f'Status: {response.status}')
                text = await response.text()
                print(f'Response: {text}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_openai())
