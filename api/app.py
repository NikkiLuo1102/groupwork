from flask import Flask, render_template, request, jsonify
import psycopg2 as db
import hashlib

# #创建哈希
# def hash_password(password):
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     return hashed_password

#验证哈希
# def verify_password(input_password, hashed_password):
#     input_hashed_password = hashlib.sha256(input_password.encode()).hexdigest()
#     return input_hashed_password == hashed_password

app = Flask(__name__)

# 连接 MySQL 数据库
def get_db_connection():
    server_params = {
        'dbname': 'nl1023',
        'host': 'db.doc.ic.ac.uk',
        'port': '5432',
        'user': 'nl1023',
        'password': 'aFZK-3CzFH*j3y',
        'client_encoding': 'utf-8'
    }
    return db.connect(**server_params)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


# 处理登录请求
@app.route("/login", methods=["POST"])
def submit():
    data = request.json  # 获取 JSON 数据

    # 获取用户名和密码
    username = data.get("username")
    password = data.get("password")

    # 连接数据库
    conn = get_db_connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 查询数据库中是否存在该用户
    query = "SELECT * FROM my_user WHERE name = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    print(password,user[6])
    if user and hashlib.md5(password.encode()).hexdigest()==user[6]:  
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


