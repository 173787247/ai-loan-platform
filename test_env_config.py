#!/usr/bin/env python3
"""
环境变量配置测试脚本

@author AI Loan Platform Team
@version 1.0.0
"""

import os
import sys
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

def load_environment():
    """加载环境变量"""
    print("🔧 加载环境变量...")
    
    # 尝试加载.env文件
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ 成功加载 .env 文件")
    else:
        print("⚠️  未找到 .env 文件，使用系统环境变量")
    
    return True

def check_llm_providers():
    """检查LLM提供商配置"""
    print("\n🤖 检查LLM提供商配置...")
    
    providers = {
        "OpenAI": {
            "key": os.getenv("OPENAI_API_KEY"),
            "url": os.getenv("OPENAI_BASE_URL"),
            "model": os.getenv("OPENAI_MODEL")
        },
        "DeepSeek": {
            "key": os.getenv("DEEPSEEK_API_KEY"),
            "url": os.getenv("DEEPSEEK_BASE_URL"),
            "model": os.getenv("DEEPSEEK_MODEL")
        },
        "通义千问": {
            "key": os.getenv("QWEN_API_KEY"),
            "url": os.getenv("QWEN_BASE_URL"),
            "model": os.getenv("QWEN_MODEL")
        },
        "智谱AI": {
            "key": os.getenv("ZHIPU_API_KEY"),
            "url": os.getenv("ZHIPU_BASE_URL"),
            "model": os.getenv("ZHIPU_MODEL")
        },
        "百度文心一言": {
            "key": os.getenv("BAIDU_API_KEY"),
            "secret": os.getenv("BAIDU_SECRET_KEY"),
            "url": os.getenv("BAIDU_BASE_URL"),
            "model": os.getenv("BAIDU_MODEL")
        },
        "月之暗面": {
            "key": os.getenv("KIMI_API_KEY"),
            "url": os.getenv("KIMI_BASE_URL"),
            "model": os.getenv("KIMI_MODEL")
        }
    }
    
    configured_providers = []
    
    for name, config in providers.items():
        if name == "百度文心一言":
            # 百度需要API Key和Secret Key
            if config["key"] and config["secret"]:
                configured_providers.append(name)
                print(f"✅ {name}: 已配置")
            else:
                print(f"❌ {name}: 未配置 (需要API Key和Secret Key)")
        else:
            if config["key"]:
                configured_providers.append(name)
                print(f"✅ {name}: 已配置")
            else:
                print(f"❌ {name}: 未配置")
    
    print(f"\n📊 已配置的提供商数量: {len(configured_providers)}")
    print(f"📋 已配置的提供商: {', '.join(configured_providers)}")
    
    return configured_providers

def check_default_provider():
    """检查默认提供商设置"""
    print("\n⚙️  检查默认提供商设置...")
    
    default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "deepseek")
    print(f"🔧 默认提供商: {default_provider}")
    
    # 检查默认提供商是否已配置
    if default_provider == "deepseek" and os.getenv("DEEPSEEK_API_KEY"):
        print("✅ 默认提供商已正确配置")
        return True
    elif default_provider == "openai" and os.getenv("OPENAI_API_KEY"):
        print("✅ 默认提供商已正确配置")
        return True
    elif default_provider == "qwen" and os.getenv("QWEN_API_KEY"):
        print("✅ 默认提供商已正确配置")
        return True
    elif default_provider == "zhipu" and os.getenv("ZHIPU_API_KEY"):
        print("✅ 默认提供商已正确配置")
        return True
    elif default_provider == "baidu" and os.getenv("BAIDU_API_KEY") and os.getenv("BAIDU_SECRET_KEY"):
        print("✅ 默认提供商已正确配置")
        return True
    elif default_provider == "kimi" and os.getenv("KIMI_API_KEY"):
        print("✅ 默认提供商已正确配置")
        return True
    else:
        print("⚠️  默认提供商未正确配置，将使用模拟回复")
        return False

def test_ai_service():
    """测试AI服务连接"""
    print("\n🔗 测试AI服务连接...")
    
    try:
        # 测试AI服务健康检查
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI服务健康检查通过")
        else:
            print(f"⚠️  AI服务健康检查失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到AI服务: {e}")
        return False
    
    try:
        # 测试LLM提供商列表
        response = requests.get("http://localhost:8000/api/v1/llm/providers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                providers = data["data"]["available_providers"]
                print(f"✅ 获取到 {len(providers)} 个可用提供商: {', '.join(providers)}")
                return True
            else:
                print(f"❌ 获取提供商列表失败: {data.get('message')}")
                return False
        else:
            print(f"❌ 获取提供商列表失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法获取提供商列表: {e}")
        return False

def test_llm_provider(provider_name):
    """测试特定LLM提供商"""
    print(f"\n🧪 测试 {provider_name} 提供商...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/llm/test",
            json={
                "provider": provider_name,
                "message": "你好，请简单介绍一下你自己"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                result = data["data"]
                print(f"✅ {provider_name} 测试成功")
                print(f"📝 回复: {result.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ {provider_name} 测试失败: {data.get('message')}")
                return False
        else:
            print(f"❌ {provider_name} 测试失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {provider_name} 测试失败: {e}")
        return False

def test_chatbot():
    """测试AI智能客服"""
    print("\n💬 测试AI智能客服...")
    
    try:
        # 创建会话
        response = requests.post(
            "http://localhost:8000/api/v1/chat/session",
            json={
                "user_id": "test_user",
                "chatbot_role": "general"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                session_id = data["data"]["session_id"]
                print(f"✅ 会话创建成功: {session_id}")
                
                # 发送测试消息
                response = requests.post(
                    "http://localhost:8000/api/v1/chat/message",
                    json={
                        "session_id": session_id,
                        "message": "你好，我想了解贷款产品",
                        "user_info": {
                            "user_id": "test_user",
                            "username": "测试用户",
                            "role": "borrower"
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        ai_response = data["data"]["response"]
                        print(f"✅ 智能客服测试成功")
                        print(f"🤖 AI回复: {ai_response[:100]}...")
                        return True
                    else:
                        print(f"❌ 智能客服测试失败: {data.get('message')}")
                        return False
                else:
                    print(f"❌ 发送消息失败: HTTP {response.status_code}")
                    return False
            else:
                print(f"❌ 创建会话失败: {data.get('message')}")
                return False
        else:
            print(f"❌ 创建会话失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 智能客服测试失败: {e}")
        return False

def generate_report():
    """生成测试报告"""
    print("\n📊 生成测试报告...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "environment_check": {
            "env_file_loaded": os.path.exists('.env'),
            "default_provider": os.getenv("DEFAULT_LLM_PROVIDER", "deepseek"),
            "configured_providers": check_llm_providers()
        },
        "ai_service_status": test_ai_service(),
        "chatbot_status": test_chatbot()
    }
    
    # 保存报告
    with open("env_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ 测试报告已保存到 env_test_report.json")
    
    return report

def main():
    """主函数"""
    print("🚀 开始环境变量配置测试")
    print("=" * 50)
    
    # 1. 加载环境变量
    load_environment()
    
    # 2. 检查LLM提供商配置
    configured_providers = check_llm_providers()
    
    # 3. 检查默认提供商
    default_ok = check_default_provider()
    
    # 4. 测试AI服务
    ai_service_ok = test_ai_service()
    
    # 5. 测试智能客服
    chatbot_ok = test_chatbot()
    
    # 6. 如果有配置的提供商，测试它们
    if configured_providers and ai_service_ok:
        print("\n🧪 测试已配置的LLM提供商...")
        for provider in configured_providers:
            provider_map = {
                "OpenAI": "openai",
                "DeepSeek": "deepseek",
                "通义千问": "qwen",
                "智谱AI": "zhipu",
                "百度文心一言": "baidu",
                "月之暗面": "kimi"
            }
            test_llm_provider(provider_map.get(provider, provider.lower()))
    
    # 7. 生成报告
    report = generate_report()
    
    # 8. 总结
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    print(f"  环境变量加载: {'✅' if os.path.exists('.env') else '❌'}")
    print(f"  已配置提供商: {len(configured_providers)} 个")
    print(f"  默认提供商: {'✅' if default_ok else '❌'}")
    print(f"  AI服务连接: {'✅' if ai_service_ok else '❌'}")
    print(f"  智能客服: {'✅' if chatbot_ok else '❌'}")
    
    if all([default_ok, ai_service_ok, chatbot_ok]):
        print("\n🎉 所有测试通过！AI智能客服系统已准备就绪！")
    else:
        print("\n⚠️  部分测试失败，请检查配置并重试。")
    
    print("\n📚 更多帮助请查看 ENV_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
