import requests
import os

from flask import session, jsonify

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")  # 设置环境变量，安全
def ask_ai(prompt):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "qwen-7b-chat",
        "input": {
            "prompt": prompt
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return result.get("output", {}).get("text", "AI 无法回答")
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "未登录"}), 401
        return f(*args, **kwargs)
    return decorated_function
# 文件：backend/utils.py

import json

# 读取 JSON 文件
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # 如果文件不存在，返回空列表
    except json.JSONDecodeError:
        return []  # 如果文件无法解析为 JSON 格式，返回空列表
    except Exception as e:
        print(f"读取 JSON 文件时发生错误: {e}")
        return []

# 保存数据到 JSON 文件
def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"保存数据到 JSON 文件时发生错误: {e}")
