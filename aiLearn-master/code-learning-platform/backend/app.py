from datetime import datetime
from flask import Flask, session, jsonify, request, send_from_directory, redirect, render_template
from flask_cors import CORS
import os
import json

from database import init_db, get_users, add_user, delete_user, assign_homework, get_submissions, submit_feedback
from auth import auth_bp
from ai import ai_bp
from student import student_bp
from teacher import teacher_bp
from admin import admin_bp
from utils import login_required, ask_ai

# 创建 Flask 应用
app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = 'your-secret-key'
CORS(app)
init_db()
feedback_file_path = os.path.join(os.path.dirname(__file__), 'data', 'feedbacks.json')
submissions_file_path = os.path.join(os.path.dirname(__file__), 'data', 'submissions.json')
homework_file_path = os.path.join(os.path.dirname(__file__), 'data', 'homework.json')
user_file_path = os.path.join(os.path.dirname(__file__), 'data', 'users.json')

# --------------------基础通用配置----------------------

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(app.static_folder, '404-ink.html'), 404

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')), filename)

@app.route('/')
def index():
    return redirect("/login.html")

@app.route('/api/status')
@login_required
def status():
    return jsonify({"message": "AI 编程平台后端启动成功"})

# --------------------身份登录与登出----------------------

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    with open(user_file_path, 'r', encoding='utf-8') as f:
        users = json.load(f)

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

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "已退出登录"})

# --------------------AI 问答----------------------

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = ask_ai(user_input)
    return jsonify({"response": response})

# --------------------课程与资料----------------------

@app.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    if session['role'] == 'student':
        return jsonify({"error": "学生无权访问课程管理"}), 403

    courses = [
        {"id": 1, "title": "Python 入门", "description": "基础语法与编程"},
        {"id": 2, "title": "数据结构与算法", "description": "常用数据结构与算法"},
        {"id": 3, "title": "Web 开发", "description": "Flask 与前端开发"}
    ]
    return jsonify(courses)

@app.route('/api/course-content/<filename>')
@login_required
def get_course_file(filename):
    course_path = os.path.join(os.getcwd(), '../frontend/dara')
    return send_from_directory(course_path, filename)

# --------------------学生作业提交----------------------

@app.route('/api/student/submit_assignment', methods=['POST'])
def submit_assignment():
    data = request.get_json()
    assignment_id = data.get('assignment_id')
    solution = data.get('solution')
    student = session.get('username')

    try:
        with open(submissions_file_path, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        submissions = []

    submissions.append({
        "assignment_id": int(assignment_id),
        "student": student,
        "solution": solution,
        "score": None,
        "feedback": None
    })

    with open(submissions_file_path, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, indent=2)

    return jsonify({"message": "作业提交成功！"})

@app.route('/api/assignments', methods=['GET'])
@login_required
def get_assignments():
    assignments = [
        {"id": 1, "title": "作业 1", "description": "基础编程作业"},
        {"id": 2, "title": "作业 2", "description": "数据结构作业"}
    ]
    return jsonify(assignments)

@app.route('/student/homework')
def student_homework():
    homework_list = []
    try:
        with open(homework_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                homework = json.loads(line.strip())
                homework_list.append(homework)
    except FileNotFoundError:
        print("homework.json 文件未找到")
    except json.JSONDecodeError as e:
        print(f"JSON 解码错误：{e}")

    return render_template('student_submit.html', homework_list=homework_list)

# --------------------教师作业发布与批改----------------------

@app.route('/assign_homework', methods=['POST'])
def assign_homework_route():
    data = request.get_json()
    title = data.get('homework_title')
    description = data.get('homework_description')

    if not title or not description:
        return jsonify({"error": "作业标题和描述不能为空"}), 400

    with open(homework_file_path, 'a', encoding='utf-8') as f:
        homework = {
            'title': title,
            'description': description,
            'assigned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(homework, f)
        f.write('\n')

    return jsonify({"message": "作业布置成功"}), 200

@app.route('/api/teacher/submissions', methods=['GET'])
def get_submissions_route():
    try:
        with open(submissions_file_path, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        submissions = []

    if not submissions:
        return jsonify({"error": "没有提交的作业"}), 404

    return jsonify(submissions)

@app.route('/api/teacher/feedback/<int:id>', methods=['POST'])
def submit_homework_feedback(id):
    data = request.get_json()
    feedback = data.get('feedback')

    if not feedback:
        return jsonify({"error": "反馈不能为空"}), 400

    submit_feedback(id, feedback)
    return jsonify({"message": "反馈提交成功"})

# --------------------管理员接口----------------------

@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    users = get_users()
    return jsonify(users)

@app.route('/api/admin/add_user', methods=['POST'])
def add_new_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"error": "用户名、密码和角色不能为空"}), 400

    result = add_user(username, password, role)
    return jsonify({"message": result})

@app.route('/api/admin/delete_user/<username>', methods=['DELETE'])
def delete_existing_user(username):
    result = delete_user(username)
    return jsonify({"message": result})

@app.route('/api/users')
def get_users_by_role():
    role = request.args.get('role')
    if not role:
        return jsonify({"error": "需要角色参数"}), 400

    from database import get_user_by_role
    users = get_user_by_role(role)
    return jsonify([{"id": u[0], "username": u[1]} for u in users])

# --------------------蓝图注册----------------------

app.register_blueprint(auth_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(admin_bp)

# --------------------启动----------------------

if __name__ == '__main__':
    app.run(debug=True)
