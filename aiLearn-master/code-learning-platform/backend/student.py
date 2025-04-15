import os
import json
from flask import Blueprint, request, session, jsonify
from functools import wraps
from database import save_student_submission, get_student_grades

student_bp = Blueprint('student', __name__)

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "未登录"}), 401
        return f(*args, **kwargs)
    return wrapper
homework_file_path = os.path.join(os.path.dirname(__file__), 'data', 'homework.json')
feedback_file_path = os.path.join(os.path.dirname(__file__), 'data', 'feedbacks.json')
submissions_file_path = os.path.join(os.path.dirname(__file__), 'data', 'submissions.json')

print("jia"+homework_file_path)
# 获取作业列表
@student_bp.route('/api/student/homeworks', methods=['GET'])
@login_required
def get_student_homeworks():
    # 使用相对路径


    try:
        if not os.path.exists(homework_file_path):
            with open(homework_file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return jsonify({"message": "暂时没有作业，等待教师发布作业"}), 200

        with open(homework_file_path, 'r', encoding='utf-8') as f:
            try:
                homework_list = json.load(f)
            except json.JSONDecodeError as e:
                return jsonify({"error": f"JSON 解析错误: {str(e)}"}), 400

        if not homework_list:
            return jsonify({"message": "暂时没有作业，等待教师发布作业"}), 200

        return jsonify(homework_list), 200

    except Exception as e:
        return jsonify({"error": f"发生错误: {str(e)}"}), 500

# 提交作业
@student_bp.route('/api/student/submit_assignment', methods=['POST'])
@login_required
def submit_assignment():
    data = request.get_json()
    assignment_id = data.get('assignment_id')
    solution = data.get('solution')
    student = session.get('username')

    if not assignment_id or not solution:
        return jsonify({"error": "作业编号和答案不能为空"}), 400

    save_student_submission(student, assignment_id, solution)
    return jsonify({"message": "提交成功，等待老师评分"})

# 查看成绩
@student_bp.route('/api/student/grades', methods=['GET'])
@login_required
def get_grades():
    student = session.get('username')

    # 使用相对路径

    # 从 feedbacks.json 中筛选该学生的成绩
    with open(feedback_file_path, "r", encoding="utf-8") as f:
        feedbacks = json.load(f)

    # 加上学生提交的 solution 内容（从 submissions.json 取）
    with open(submissions_file_path, "r", encoding="utf-8") as f:
        submissions = json.load(f)

    result = []
    for fb in feedbacks:
        if fb["student"] == student:
            solution_text = ""
            for sub in submissions:
                if sub["assignment_id"] == fb["assignment_id"] and sub["student"] == student:
                    solution_text = sub["solution"]
                    break
            result.append({
                "assignment_id": fb["assignment_id"],
                "solution": solution_text,
                "feedback": fb.get("feedback", ""),
                "grade": fb.get("grade", "")
            })

    return jsonify(result)
