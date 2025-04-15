# backend/teacher.py
import os
import json
from datetime import datetime
from flask import Blueprint, session, jsonify, request
from database import assign_homework, get_submissions, submit_feedback

teacher_bp = Blueprint('teacher', __name__)
homework_file_path = os.path.join(os.path.dirname(__file__), 'data', 'homework.json')
feedback_file_path = os.path.join(os.path.dirname(__file__), 'data', 'feedbacks.json')
submissions_file_path = os.path.join(os.path.dirname(__file__), 'data', 'submissions.json')

# 获取课程列表
@teacher_bp.route('/api/teacher/courses', methods=['GET'])
def get_courses():
    if session.get('role') != 'teacher':
        return jsonify({"error": "权限不足"}), 403

    courses = [
        {"id": 1, "title": "Python 入门", "description": "基础语法与编程"},
        {"id": 2, "title": "算法课程", "description": "基础数据结构与算法"}
    ]
    return jsonify(courses)

# 发布作业
@teacher_bp.route('/api/teacher/assignments', methods=['POST'])
def assign_homework_api():
    print("省份是"+session.get('role'))
    if session.get('role') != 'teacher':
        return jsonify({"error": "权限不足"}), 403
    print("test")
    data = request.get_json()
    course = data.get("course")
    content = data.get("content")

    if not course or not content:
        return jsonify({"error": "课程和作业内容不能为空"}), 400

    try:
        with open(homework_file_path, 'r', encoding='utf-8') as f:
            homework_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        homework_list = []

    next_id = max((hw.get("id", 0) for hw in homework_list), default=0) + 1

    new_homework = {
        "id": next_id,
        "title": f"{course} 作业 {next_id}",
        "description": content,
        "assigned_date": datetime.now().strftime("%Y-%m-%d"),
        "course": course
    }

    homework_list.append(new_homework)

    with open(homework_file_path, 'w', encoding='utf-8') as f:
        json.dump(homework_list, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "作业已发布"})

# 获取提交列表
@teacher_bp.route('/api/teacher/submissions', methods=['GET'])
def get_submissions_api():
    if session.get('role') != 'teacher':
        return jsonify({"error": "权限不足"}), 403

    try:
        with open(submissions_file_path, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []

    return jsonify(submissions)

# 提交反馈与评分

# 文件路径：teacher.py

from flask import Blueprint, request, jsonify, session
import json
import os

teacher_bp = Blueprint("teacher", __name__)

# 统一使用绝对路径

@teacher_bp.route('/api/teacher/feedback', methods=['POST'])
def submit_feedback_api():
    if session.get('role') != 'teacher':
        return jsonify({"error": "权限不足"}), 403

    data = request.get_json()
    assignment_id = data.get("assignment_id")
    student = data.get("student")
    feedback = data.get("feedback")
    score = data.get("score")

    if not assignment_id or not student:
        return jsonify({"error": "缺少 assignment_id 或 student 字段"}), 400

    # 读取 feedbacks.json，处理空内容或不存在的情况
    feedbacks = []
    if os.path.exists(feedback_file_path):
        try:
            with open(feedback_file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    feedbacks = json.loads(content)
        except Exception as e:
            return jsonify({"error": f"读取反馈文件失败: {str(e)}"}), 500

    # 更新或添加记录
    found = False
    for item in feedbacks:
        if item["assignment_id"] == assignment_id and item["student"] == student:
            item["feedback"] = feedback
            item["grade"] = score
            found = True
            break

    if not found:
        feedbacks.append({
            "assignment_id": assignment_id,
            "student": student,
            "feedback": feedback,
            "grade": score
        })

    # 写入文件
    try:
        with open(feedback_file_path, "w", encoding="utf-8") as f:
            json.dump(feedbacks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({"error": f"写入反馈失败: {str(e)}"}), 500

    return jsonify({"message": "反馈提交成功"})

