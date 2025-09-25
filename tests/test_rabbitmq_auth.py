#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RabbitMQ认证测试脚本
测试RabbitMQ连接和认证配置
"""

import pika
import json
import time
from datetime import datetime

def test_rabbitmq_connection():
    """测试RabbitMQ连接和认证"""
    print("🔍 测试RabbitMQ连接和认证...")
    
    try:
        # 使用正确的认证信息
        credentials = pika.PlainCredentials('admin', 'admin123')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                virtual_host='/',
                credentials=credentials
            )
        )
        
        channel = connection.channel()
        
        # 测试发送消息
        test_message = {
            "test": "RabbitMQ认证测试",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        channel.basic_publish(
            exchange='',
            routing_key='test_queue',
            body=json.dumps(test_message, ensure_ascii=False)
        )
        
        print("✅ RabbitMQ连接成功，认证通过")
        print(f"✅ 消息发送成功: {test_message}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ RabbitMQ连接失败: {e}")
        return False

def test_rabbitmq_management():
    """测试RabbitMQ管理界面"""
    print("\n🔍 测试RabbitMQ管理界面...")
    
    try:
        import requests
        
        # 测试管理界面访问
        response = requests.get(
            'http://localhost:15672/api/overview',
            auth=('admin', 'admin123'),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ RabbitMQ管理界面访问成功")
            print(f"✅ 集群名称: {data.get('cluster_name', 'N/A')}")
            print(f"✅ 版本: {data.get('rabbitmq_version', 'N/A')}")
            return True
        else:
            print(f"❌ 管理界面访问失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 管理界面测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 RabbitMQ认证配置测试")
    print("=" * 50)
    
    # 测试连接
    connection_ok = test_rabbitmq_connection()
    
    # 测试管理界面
    management_ok = test_rabbitmq_management()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"   {'✅' if connection_ok else '❌'} RabbitMQ连接: {'通过' if connection_ok else '失败'}")
    print(f"   {'✅' if management_ok else '❌'} 管理界面: {'通过' if management_ok else '失败'}")
    
    if connection_ok and management_ok:
        print("\n🎉 RabbitMQ认证配置正常！")
        return True
    else:
        print("\n⚠️ RabbitMQ认证配置需要修复")
        return False

if __name__ == "__main__":
    main()
