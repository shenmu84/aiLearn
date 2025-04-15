# ✅ 整合版 admin.py

from flask import Blueprint, request, session, jsonify
from utils import load_json, save_json

admin_bp = Blueprint('admin', __name__)
# ✅ 权限检查装饰器
def admin_required(func):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({"error": "权限不足"}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
# 获取所有用户（真实数据）
@admin_bp.route('/api/admin/users', methods=['GET'])
@admin_required
def get_users():
    if session.get('role') != 'admin':
        return jsonify({"error": "权限不足"}), 403

    users = load_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json')
    return jsonify(users)

# 审核用户
@admin_bp.route('/api/admin/approve', methods=['POST'])
@admin_required
def approve_user():
    if session.get('role') != 'admin':
        return jsonify({"error": "权限不足"}), 403

    data = request.json
    users = load_json('D:\\learn\\Program\\python\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json')
    for user in users:
        if user['username'] == data['username']:
            user['approved'] = True
            break
    save_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json', users)
    return jsonify({'success': True})

# 设置用户角色
@admin_bp.route('/api/admin/set_role', methods=['POST'])
@admin_required
def set_role():
    if session.get('role') != 'admin':
        return jsonify({"error": "权限不足"}), 403

    data = request.json
    users = load_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json')
    for user in users:
        if user['username'] == data['username']:
            user['role'] = data['role']
            break
    save_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json', users)
    return jsonify({'success': True})
# ✅ 删除用户
@admin_bp.route('/api/admin/delete_user', methods=['POST'])
@admin_required
def delete_user():
    data = request.json
    username_to_delete = data.get('username')

    users = load_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json')
    users = [user for user in users if user['username'] != username_to_delete]
    save_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json', users)
    return jsonify({'success': True, 'message': f'{username_to_delete} 已删除'})

# ✅ 获取单个用户详情
@admin_bp.route('/api/admin/user/<username>', methods=['GET'])
@admin_required
def get_user(username):
    users = load_json('D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json')
    for user in users:
        if user['username'] == username:
            return jsonify(user)
    return jsonify({"error": "用户不存在"}), 404
# 示例设置接口（可选保留）
@admin_bp.route('/api/admin/settings', methods=['POST'])
@admin_required
def set_settings():
    if session.get('role') != 'admin':
        return jsonify({"error": "权限不足"}), 403

    data = request.get_json()
    return jsonify({"message": "设置已更新", "settings": data})
