import os

from flask import Blueprint, request, jsonify, session
from utils import load_json, save_json
from database import add_user

auth_bp = Blueprint('auth', __name__)
import_file_path = os.path.join(os.path.dirname(__file__), 'import_users.py')

def save_to_json(user_data):
    users = load_json(import_file_path)
    for user in users:
        if user['username'] == user_data['username']:
            return False
    users.append(user_data)
    save_json(import_file_path, users)
    return True

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"success": False, "message": "缺少必要信息"}), 400

    user = {
        "username": username,
        "password": password,
        "role": role,
        "approved": False
    }

    json_success = save_to_json(user)
    db_message = add_user(username, password, role, approved=False)

    if db_message != "用户添加成功":
        return jsonify({"success": False, "message": db_message}), 400

    return jsonify({"success": True, "message": "注册成功，等待管理员审核"})


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_json(import_file_path)

    for user in users:
        if user['username'] == username and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return jsonify({
                "message": "登录成功",
                "role": user['role'],
                "redirect": f"/{user['role']}-dashboard.html"
            })

    return jsonify({"error": "用户名或密码错误"}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "已退出登录"})
