from flask import Flask, render_template, request, jsonify
import psycopg2 as db
import hashlib

# #创建哈希
# def hash_password(password):
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     return hashed_password

#验证哈希
def verify_password(input_password, hashed_password):
    input_hashed_password = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hashed_password == hashed_password

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")
    # return "Hello , my new app!"


@app.route("/login")
def login():
    return render_template("login.html")

# 连接 MySQL 数据库
server_params = {
    'dbname': 'mondial',
    'host': 'db.doc.ic.ac.uk',
    'port': '5432',
    'user': 'nl1023',
    'password': 'lab',
    'client_encoding': 'utf-8'
}

conn = db.connect(**server_params)

# 创建游标对象
cursor = db.cursor()

# 处理登录请求
@app.route("/login", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("keyword")

    # 查询数据库中是否存在该用户
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and verify_password(password,user[2]):  
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

