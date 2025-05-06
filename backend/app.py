import hashlib

import pymysql
from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from flask_cors import CORS
from flask_caching import Cache

app = Flask(__name__)
# 使用内存缓存
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60  # 缓存默认时间，单位秒
cache = Cache(app)
CORS(app)  # 允许前端跨域访问

# neo4j
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "your_own_password"))

# 配置 MySQL 连接
db = pymysql.connect(
    host='localhost',
    user='root',
    password='your_own_password',
    database='cultural_relics',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


# 加密函数
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# 获取neo4j数据
def fetch_graph_data(keyword=None):
    with driver.session() as session:
        if keyword:
            query = """
            MATCH (n)
            WHERE any(prop IN keys(n) WHERE toString(n[prop]) CONTAINS $keyword)
            OPTIONAL MATCH (n)-[r]->(m)
            RETURN n, r, m
            limit 25
            """
            result = session.run(query, keyword=keyword)
        else:
            result = session.run("""
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, r, m
                limit 25
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


# 可缓存的函数（关键字参数必须参与 key 生成）
@cache.memoize(timeout=120)  # 设置缓存 2 分钟
def fetch_graph_data_cached(keyword=None):
    return fetch_graph_data(keyword)


# 知识图谱可视化
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


# 历史时间线
@app.route('/timeline-data')
def get_timeline_data():
    cursor = db.cursor()
    sql = """
        SELECT cr.name, cr.type, cr.description, cr.size, cr.matrials, 
        cr.dynasty, cr.likes_count, cr.views_count, cr.author, cr.entry_time, ri.image_url, m.museum_name
        FROM cultural_relic cr
        join museum m on cr.museum_id = m.museum_id
        LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id AND ri.status = 1
        WHERE cr.entry_time IS NOT NULL
        ORDER BY cr.entry_time ASC;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    events = []
    for row in rows:
        entry_year = row['entry_time']
        # 清洗作者字段
        if row['author'] != '不明':
            row['author'] = row['author'][row['author'].find('：') + 1:]
        events.append({
            'name': row['name'],
            'description': row['description'] or '',
            'year': entry_year,
            'image': row['image_url'],  # None 表示没有图片
            'museum': row['museum_name'],
            'type': row['type'],
            'dynasty': row['dynasty'],
            'likes_count': row['likes_count'],
            'views_count': row['views_count'],
            'size': row['size'],
            'matrials': row['matrials'],
            'author': row['author'],
        })

    return jsonify(events)


@app.route('/search')
def search_artifacts():
    query = request.args.get('q', '').strip()

    sql = """
            SELECT cr.relic_id, cr.name, cr.type, cr.description, cr.size, cr.matrials, 
                   cr.dynasty, cr.likes_count, cr.views_count, cr.author, cr.entry_time, 
                   ri.image_url, m.museum_name
            FROM cultural_relic cr
            JOIN museum m ON cr.museum_id = m.museum_id
            LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id AND ri.status = 1
            WHERE cr.entry_time IS NOT NULL
        """

    # 动态拼接关键词搜索条件
    if query:
        sql += " AND cr.description LIKE %s"

    try:
        with db.cursor() as cursor:
            if query:
                cursor.execute(sql, ('%' + query + '%',))
            else:
                cursor.execute(sql)
            rows = cursor.fetchall()

        # 构造前端需要的数据格式
        results = []
        for row in rows:
            results.append({
                "id": row['relic_id'],
                "type": row['type'],
                "title": row['name'],
                "date": row['entry_time'],
                "image": row['image_url'],
                "description": row['description'],
                "size": row['size'],
                "matrials": row['matrials'],
                "dynasty": row['dynasty'],
                "likes_count": row['likes_count'],
                "views_count": row['views_count'],
                "author": row['author'],
                "museum": row['museum_name'],
            })

        return jsonify({"results": results})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error"}), 500

    finally:
        if 'db' in locals():
            db.close()


if __name__ == "__main__":
    app.run(debug=True)
