import aiohttp
import asyncio
import os

async def test_openai():
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key length: {len(api_key) if api_key else 0}")
    print(f"API Key starts with: {api_key[:20] if api_key else 'None'}")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 10
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.openai.com/v1/chat/completions', 
                              headers=headers, 
                              json=payload, 
                              timeout=30) as response:
            print(f'Status: {response.status}')
            text = await response.text()
            print(f'Response: {text}')

if __name__ == "__main__":
    asyncio.run(test_openai())
