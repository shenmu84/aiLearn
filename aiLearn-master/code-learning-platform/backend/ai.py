from flask import Blueprint, request, session, jsonify
from utils import ask_ai

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/chat', methods=['POST'])
def chat():
    if 'username' not in session:
        return jsonify({"error": "未登录"}), 401

    data = request.get_json()
    response = ask_ai(data.get("message", ""))
    return jsonify({"response": response})
