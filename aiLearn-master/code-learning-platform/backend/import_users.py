# import_users.py

import sqlite3
import json
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 执行 ALTER TABLE 添加新列（如果列不存在）
try:
    cursor.execute("ALTER TABLE users ADD COLUMN name TEXT;")
    print("成功添加 name 字段")
except sqlite3.OperationalError as e:
    print(f"操作失败：{e}")

# 提交更改并关闭连接
conn.commit()
conn.close()
DB_FILE = 'db.sqlite3'
JSON_FILE = 'D:\\learn\\Program\\python\\code\\code-learning-platform\\code-learning-platform\\backend\data\\users.json'  # 如果你存储在别处请修改路径

def create_users_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 创建 users 表（包含 approved 字段）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            approved BOOLEAN DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def import_users_from_json():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        users = json.load(f)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for user in users:
        username = user.get('username')
        password = user.get('password')
        role = user.get('role')

        if username and password and role:
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO users (username, password, role, approved) VALUES (?, ?, ?, ?)',
                    (username, password, role, 1)
                )
                print(f"✅ 导入用户：{username}")
            except Exception as e:
                print(f"❌ 插入用户 {username} 时出错：{e}")

    conn.commit()
    conn.close()
    print("🎉 用户导入完成！")

if __name__ == '__main__':
    create_users_table()
    import_users_from_json()
