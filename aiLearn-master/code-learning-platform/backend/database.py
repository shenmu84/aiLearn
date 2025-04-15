# backend/database.py
import sqlite3
import os

from flask import json

# SQLite 数据库文件
DB_FILE = 'db.sqlite3'
# 初始化数据库（如果数据库文件不存在，创建表）
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # 创建 users 表，确保包含 password 列
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )''')

        # 创建其他表
        c.execute('''CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course TEXT,
                content TEXT,
                feedback TEXT,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )''')

        # 插入默认用户
        if not os.path.exists(DB_FILE):
            default_students = [
                ("student01", "123456", "student"),
                ("student02", "123456", "student"),
                ("student03", "123456", "student"),
                ("teacher1", "123456", "teacher"),
                ("admin1", "123456", "admin")
            ]
            for u, p, r in default_students:
                try:
                    c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (u, p, r))
                except sqlite3.IntegrityError:
                    pass  # 用户已存在跳过
            conn.commit()
        conn.close()

# 获取用户列表
def add_user(username, password, role, approved=False):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT,
                approved BOOLEAN DEFAULT 0
            )
        ''')
        cursor.execute('''
            INSERT INTO users (username, password, role, approved) VALUES (?, ?, ?, ?)
        ''', (username, password, role, int(approved)))
        conn.commit()
        return "用户添加成功"
    except sqlite3.IntegrityError:
        return "用户名已存在"
    finally:
        conn.close()
# 获取所有用户
def get_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# 按角色获取用户
def get_user_by_role(role):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE role=?", (role,))
    users = c.fetchall()
    conn.close()
    return users

# 添加用户
def add_user(username, password, role, approved=False):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT,
                approved BOOLEAN DEFAULT 0
            )
        ''')
        cursor.execute('''
            INSERT INTO users (username, password, role, approved) VALUES (?, ?, ?, ?)
        ''', (username, password, role, int(approved)))
        conn.commit()
        return "用户添加成功"
    except sqlite3.IntegrityError:
        return "用户名已存在"
    finally:
        conn.close()
def get_user_id_by_username(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# 删除用户
def delete_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()
def save_student_submission(student, assignment_id, solution):
    if not os.path.exists('data/submissions.json'):
        with open('data/submissions.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

    with open('data/submissions.json', 'r', encoding='utf-8') as f:
        submissions = json.load(f)

    submissions.append({
        "student": student,
        "assignment_id": assignment_id,
        "solution": solution,
        "grade": None,
        "feedback": ""
    })

    with open('data/submissions.json', 'w', encoding='utf-8') as f:
        json.dump(submissions, f)


def get_student_grades(student):
    if not os.path.exists('data/submissions.json'):
        return []

    with open('data/submissions.json', 'r', encoding='utf-8') as f:
        submissions = json.load(f)

    return [s for s in submissions if s["student"] == student]

# 布置作业
def assign_homework(student_id, course, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO assignments (student_id, course, content, feedback) VALUES (?, ?, ?, ?)",
              (student_id, course, content, ""))
    conn.commit()
    conn.close()

# 获取作业提交
def get_submissions():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT a.id, u.username AS student, a.course, a.content, a.feedback
                 FROM assignments a
                 JOIN users u ON a.student_id = u.id''')
    submissions = c.fetchall()
    conn.close()
    return submissions

# 提交反馈
def submit_feedback(assignment_id, feedback):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE assignments SET feedback=? WHERE id=?", (feedback, assignment_id))
    conn.commit()
    conn.close()
