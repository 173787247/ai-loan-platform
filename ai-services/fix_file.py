#!/usr/bin/env python3
import os

def fix_file():
    file_path = '/app/services/ai_chatbot.py'
    
    # 读取文件
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # 移除null字节
    clean_content = content.replace(b'\x00', b'')
    
    # 写回文件
    with open(file_path, 'wb') as f:
        f.write(clean_content)
    
    print(f"File {file_path} cleaned, removed {len(content) - len(clean_content)} null bytes")

if __name__ == "__main__":
    fix_file()
