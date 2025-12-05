from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from datetime import datetime

# --- 数据库配置和初始化 ---
DATABASE = 'data.db'
app = Flask(__name__)

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 允许通过列名访问数据
    return conn

def init_db():
    """初始化数据库，创建用户表"""
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                realname TEXT NOT NULL,
                position TEXT NOT NULL,
                dob TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )'''
        )

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clicktime TEXT UNIQUE NOT NULL
            )'''
        )

        conn.commit()
        conn.close()
        print("数据库初始化完成：data.db")

# 在应用启动时初始化数据库
with app.app_context():
    init_db()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET'])
def register_html():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():
    """处理用户注册请求"""
    username = request.form.get("username")
    password = request.form.get("password")
    realname = request.form.get("realname")
    position = request.form.get("position")
    dob = request.form.get("dob")
    phone = request.form.get("phone")
    email = request.form.get("email")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password, realname, position, dob, phone,email) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, password, realname, position, dob, phone, email)
        )
        conn.commit()
        
        user_info = {
            'username': username,
            'realname': realname,
            'position': position,
        }

        return render_template('success.html', user_info=user_info)
        
    except sqlite3.IntegrityError:
        # 捕获 UNIQUE 约束错误 (即 username 已存在)
        return jsonify({"message": "账户名称已存在，请更换"}), 409 # 409 Conflict
    except Exception as e:
        print(e)
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    """处理用户登录请求"""
    username = request.form.get("username")
    password = request.form.get("password")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询用户
    user = cursor.execute("SELECT username, password, realname, position FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user is None:
        # 账户不存在
        return render_template('fail.html')

    if user['password'] == password:
        # 将 sqlite3.Row 对象转换为字典，方便模板使用
        user_info = {
            'username': user['username'],
            'realname': user['realname'],
            'position': user['position']
        }
        
        # 使用 render_template 渲染成功页面，并传入 user_info 字典
        return render_template('success.html', user_info=user_info)
    
    else:
        # 密码错误
        return render_template('fail.html')
    

@app.route('/click', methods=['GET'])
def click():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO clicks (clicktime) VALUES (?)",
            (now,)
        )
        conn.commit()
        
    except Exception as e:
        print(e)
    finally:
        conn.close() 

    return "click"
        

# 运行应用
if __name__ == '__main__':    
    app.run(host="0.0.0.0", port=10001, debug=True)