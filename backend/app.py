import hashlib

import pymysql
from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问

# neo4j
# driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "your_own_password"))
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "password"))

# 配置 MySQL 连接
db = pymysql.connect(
    host='localhost',
    user='root',
    # password='your_own_password',
    password='password',
    database='cultural_relics',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


# 加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:32]


# 获取neo4j数据
def fetch_graph_data(keyword=None):
    with driver.session() as session:
        if keyword:
            query = """
            MATCH (n)
            WHERE any(prop IN keys(n) WHERE toString(n[prop]) CONTAINS $keyword)
            OPTIONAL MATCH (n)-[r]->(m)
            RETURN n, r, m
            """
            result = session.run(query, keyword=keyword)
        else:
            result = session.run("""
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, r, m
            """)
        nodes = {}
        links = []
        for record in result:
            n, m, r = record["n"], record["m"], record["r"]
            if n.element_id not in nodes:
                props = dict(n.items())
                nodes[n.element_id] = {
                    "id": n.element_id,
                    "label": list(n.labels)[0] if n.labels else "Node",
                    "name": props.get("name", "未命名"),
                    "properties": props
                }
            if r is not None and m is not None:
                if m.element_id not in nodes:
                    props = dict(m.items())
                    nodes[m.element_id] = {
                        "id": m.element_id,
                        "label": list(m.labels)[0] if m.labels else "Node",
                        "name": props.get("name", "未命名"),
                        "properties": props
                    }
                links.append({
                    "source": n.element_id,
                    "target": m.element_id,
                    "type": r.type,
                    "label": r.type
                })
        return {"nodes": list(nodes.values()), "links": links}


@app.route("/graph-data")
def graph_data():
    keyword = request.args.get("keyword", default=None)
    return jsonify(fetch_graph_data(keyword))


# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')
    hashed_password = hash_password(password)

    cursor = db.cursor()
    sql = "SELECT * FROM user WHERE phone_number = %s"
    cursor.execute(sql, (phone_number))
    result = cursor.fetchone()
    if result is None:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 401
    if result['password'] == hashed_password:
        return jsonify({'status': 'success', 'message': '登录成功', 'username': result['name']})
    else:
        return jsonify({'status': 'error', 'message': '密码错误'}), 401


# 注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    id_number = data.get('id_number')
    phone_number = data.get('phone_number')
    hashed_password = hash_password(password)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE phone_number = %s", (phone_number,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': '此手机号已注册'}), 400

    cursor.execute("INSERT INTO user (name, password, id_number, phone_number) VALUES (%s, %s, %s, %s)",
                   (username, hashed_password, id_number, phone_number))
    db.commit()
    return jsonify({'status': 'success', 'message': '注册成功'})


@app.route('/timeline-data')
def get_timeline_data():
    cursor = db.cursor()
    sql = """
        SELECT name, description, entry_time, dynasty
        FROM cultural_relic
        WHERE entry_time IS NOT NULL
        ORDER BY entry_time ASC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    # 构建时间线事件数据
    events = []
    for row in rows:
        entry_year = row['entry_time']
        events.append({
            'name': row['name'],
            'description': row['description'] or '',
            'year': entry_year,
            # 可扩展字段：media, dynasty, etc.
        })

    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)
