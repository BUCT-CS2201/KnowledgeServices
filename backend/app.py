import hashlib
import os
from datetime import datetime
from io import BytesIO

import pymysql
from flask import Flask, jsonify, request, g
from neo4j import GraphDatabase
from flask_cors import CORS
from flask_caching import Cache
from PIL import Image

app = Flask(__name__)

# 使用内存缓存
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60  # 缓存默认时间，单位秒
cache = Cache(app)
CORS(app, supports_credentials=True, origins=['http://localhost:8080'])  # 允许前端跨域访问

# neo4j
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "your_own_password"))


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host='localhost',
            user='root',
            password='your_own_password',
            database='cultural_relics',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


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
            limit 300
            """
            result = session.run(query, keyword=keyword)
        else:
            result = session.run("""
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, r, m
                limit 300
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


# 获取知识图谱数据（含缓存）
@cache.memoize(timeout=120)  # 设置缓存 2 分钟
def fetch_graph_data_cached(keyword=None):
    return fetch_graph_data(keyword)


# 知识图谱可视化
@app.route("/graph-data")
def graph_data():
    keyword = request.args.get("keyword", default=None)
    return jsonify(fetch_graph_data(keyword))


# 搜索自动填充
@app.route('/search-suggestions')
def search_suggestions():
    conn = get_db()
    cursor = conn.cursor()

    # 获取各维度建议词
    suggestions = {
        '朝代': [],
        '材料': [],
        '博物馆': [],
        '类型': [],
        '名称': [],
        '作者': []
    }

    # 查询各维度数据
    cursor.execute("SELECT DISTINCT dynasty FROM cultural_relic WHERE dynasty IS NOT NULL")
    suggestions['朝代'] = [row['dynasty'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT matrials FROM cultural_relic WHERE matrials IS NOT NULL")
    suggestions['材料'] = [row['matrials'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT museum_name FROM museum")
    suggestions['博物馆'] = [row['museum_name'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT type FROM cultural_relic WHERE type IS NOT NULL")
    suggestions['类型'] = [row['type'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT name FROM cultural_relic WHERE name IS NOT NULL")
    suggestions['名称'] = [row['name'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT author FROM cultural_relic WHERE author IS NOT NULL")
    suggestions['作者'] = [row['author'] for row in cursor.fetchall()]

    return jsonify(suggestions)


# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')
    hashed_password = hash_password(password)

    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE phone_number = %s"
    cursor.execute(sql, (phone_number))
    result = cursor.fetchone()
    if result is None:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 401
    if result['password'] == hashed_password:
        return jsonify(
            {'status': 'success', 'message': '登录成功', 'username': result['name'], 'user_id': result['user_id']})
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

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE phone_number = %s", (phone_number,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': '此手机号已注册'}), 400

    cursor.execute("INSERT INTO user (name, password, id_number, phone_number) VALUES (%s, %s, %s, %s)",
                   (username, hashed_password, id_number, phone_number))
    conn.commit()
    return jsonify({'status': 'success', 'message': '注册成功'})


# 历史时间线
@app.route('/timeline-data')
def get_timeline_data():
    conn = get_db()
    cursor = conn.cursor()
    sql = """
        SELECT cr.name, cr.type, cr.description, cr.size, cr.matrials, 
        cr.dynasty, cr.likes_count, cr.views_count, cr.author, cr.entry_time, ri.img_url, m.museum_name
        FROM cultural_relic cr
        join museum m on cr.museum_id = m.museum_id
        LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id
        WHERE cr.entry_time IS NOT NULL
        ORDER BY cr.entry_time ASC
        LIMIT 300
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
            'image': row['img_url'],  # None 表示没有图片
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


# 大页面搜索
@app.route('/search')
def search_artifacts():
    sort_dict = {
        '时间：新-旧': ' ORDER BY cr.entry_time DESC',
        '时间：旧-新': ' ORDER BY cr.entry_time ASC',
        '名称：A-Z': ' ORDER BY cr.name ASC',
        '名称：Z-A': ' ORDER BY cr.name DESC'
    }

    condition_dict = {
        '作者': 'author',
        '标题': 'name',
        '描述': 'description',
        '类型': 'type',
        '朝代': 'dynasty',
        '材料': 'matrials',
        '尺寸': 'size',
    }

    popular_dict = {
        '仰韶文化': ('cr.dynasty LIKE %s', '%仰韶文化%'),
        '作者不详': ('cr.author = %s', '不明'),
        '纸本水墨': ('cr.description LIKE %s', '%纸本水墨%'),
        '山水': ('cr.description LIKE %s', '%山水%'),
        '含视频': ('rv.video_url IS NOT NULL', None)
    }

    # 获取参数
    query = request.args.get('q', '').strip()
    sort = request.args.get('sort', '').strip()
    condition = request.args.get('condition', '').strip()
    popular = request.args.getlist('popular')
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    start = (page - 1) * page_size
    end = start + page_size

    # 高级搜索字段
    author = request.args.get('author')
    name = request.args.get('name')
    museum = request.args.get('museum')
    dynasty = request.args.get('dynasty')
    matrials = request.args.get('matrials')
    after = request.args.get('after')
    before = request.args.get('before')
    type_ = request.args.get('type')

    sql = """
        SELECT cr.relic_id, cr.name, cr.type, cr.description, cr.size, cr.matrials,
               cr.dynasty, cr.likes_count, cr.views_count, cr.author, cr.entry_time,
               ri.img_url, m.museum_name, rv.video_url
        FROM cultural_relic cr
        JOIN museum m ON cr.museum_id = m.museum_id
        LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id
        LEFT JOIN relic_video rv ON cr.relic_id = rv.relic_id AND rv.is_official = 1 AND rv.status = 1
    """

    where_clauses = []
    params = []

    # 模糊搜索
    if query and condition:
        where_clauses.append(f"cr.{condition_dict[condition]} LIKE %s")
        params.append(f"%{query}%")
    elif query:
        like_fields = ['cr.name', 'cr.description', 'cr.size', 'cr.matrials',
                       'cr.dynasty', 'cr.author', 'cr.entry_time', 'm.museum_name']
        or_conditions = " OR ".join([f"{field} LIKE %s" for field in like_fields])
        where_clauses.append(f"({or_conditions})")
        params.extend([f"%{query}%"] * len(like_fields))

    # 高级搜索字段拼接
    if author:
        where_clauses.append("cr.author LIKE %s")
        params.append(f"%{author}%")

    if name:
        where_clauses.append("cr.name LIKE %s")
        params.append(f"%{name}%")

    if museum:
        where_clauses.append("m.museum_name LIKE %s")
        params.append(f"%{museum}%")

    if dynasty:
        where_clauses.append("cr.dynasty LIKE %s")
        params.append(f"%{dynasty}%")

    if matrials:
        where_clauses.append("cr.matrials LIKE %s")
        params.append(f"%{matrials}%")

    if type_:
        where_clauses.append("cr.type LIKE %s")
        params.append(f"%{type_}%")

    # 时间范围筛选
    if after and before:
        where_clauses.append("cr.entry_time BETWEEN %s AND %s")
        params.extend([after, before])
    elif after:
        where_clauses.append("cr.entry_time >= %s")
        params.append(after)
    elif before:
        where_clauses.append("cr.entry_time <= %s")
        params.append(before)

    # popular 标签
    for item in popular:
        if item in popular_dict:
            condition_sql, value = popular_dict[item]
            where_clauses.append(condition_sql)
            if value is not None:
                params.append(value)

    # 拼接 WHERE 子句
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    # 排序
    if sort in sort_dict:
        sql += sort_dict[sort]

    # 分页
    sql += " limit %s offset %s"
    params.extend([page_size, start])

    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                "id": row['relic_id'],
                "type": row['type'],
                "name": row['name'],
                "date": row['entry_time'],
                "image": row['img_url'],
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
            conn.close()


# 文物详情
@app.route('/api/detail_inform', methods=['GET'])
def get_inform():
    relic_id = request.args.get('relic_id')

    if not relic_id:
        return jsonify({'status': 'error', 'message': 'relic_id is required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        # 获取文物有关视频
        sql = "SELECT * FROM relic_video where relic_id=%s LIMIT 4"
        cursor.execute(sql, (relic_id,))
        videoData = cursor.fetchall()
        # 获取文物的图片URL
        sql = "SELECT * FROM relic_image WHERE relic_id = %s"
        cursor.execute(sql, (relic_id,))
        result_img = cursor.fetchone()
        img_url = result_img['img_url'] if result_img else None

        # 获取文物的详细信息
        sql = "SELECT * FROM cultural_relic WHERE relic_id = %s"
        cursor.execute(sql, (relic_id,))
        result = cursor.fetchone()
        museum_id = result['museum_id']
        sql = "SELECT * FROM museum WHERE museum_id = %s"
        cursor.execute(sql, (museum_id,))
        museum = cursor.fetchone()

        if not result:
            return jsonify({'status': 'error', 'message': 'No relic found with this ID'}), 404

        name = result['name']
        author = result['author']
        dynasty = result['dynasty']

        # 获取相关的文物数据并排除当前文物
        sql = "SELECT * FROM cultural_relic WHERE name LIKE %s AND relic_id != %s LIMIT 4"
        cursor.execute(sql, ('%' + name + '%', relic_id))
        namelist = cursor.fetchall()

        sql = "SELECT * FROM cultural_relic WHERE author LIKE %s AND relic_id != %s LIMIT 4"
        cursor.execute(sql, ('%' + author + '%', relic_id))
        authorlist = cursor.fetchall()

        sql = "SELECT * FROM cultural_relic WHERE dynasty LIKE %s AND relic_id != %s LIMIT 4"
        cursor.execute(sql, ('%' + dynasty + '%', relic_id))
        dynastylist = cursor.fetchall()

        sql = "SELECT ri.relic_id,ri.img_url,er.author,er.dynasty FROM relic_image ri JOIN cultural_relic er ON ri.relic_id=er.relic_id ORDER BY RAND() LIMIT 4"
        cursor.execute(sql)
        rand_list = cursor.fetchall()

        # 合并所有的 relic_id
        all_relic_ids = [relic['relic_id'] for relic in namelist] + [relic['relic_id'] for relic in authorlist] + [
            relic['relic_id'] for relic in dynastylist]

        # 查询所有相关 relic_id 对应的图片 URL
        img_urls_dict = {}
        if all_relic_ids:
            sql = "SELECT relic_id, img_url FROM relic_image WHERE relic_id IN (%s)" % ','.join(
                ['%s'] * len(all_relic_ids))
            cursor.execute(sql, tuple(all_relic_ids))
            img_urls = cursor.fetchall()

            # 将 img_url 按照 relic_id 存储到字典中
            for img in img_urls:
                img_urls_dict[img['relic_id']] = img['img_url']

        # 合并文物信息和图片
        def combine_list_with_images(relic_list):
            combined_list = []
            for relic in relic_list:
                relic_id = relic['relic_id']
                img_url = img_urls_dict.get(relic_id, None)
                combined_list.append({
                    'relic_id': relic_id,
                    'name': relic['name'],
                    'author': relic['author'],
                    'dynasty': relic['dynasty'],
                    'description': relic['description'],
                    'img_url': img_url,
                })
            return combined_list

        # 合并 namelist、authorlist 和 dynastylist 数据
        combined_namelist = combine_list_with_images(namelist)
        combined_authorlist = combine_list_with_images(authorlist)
        combined_dynastylist = combine_list_with_images(dynastylist)

        return jsonify({
            'status': 'success',
            'img_url': img_url,
            'relic_id': relic_id,
            'relic_inform': result,
            'namelist': combined_namelist,
            'authorlist': combined_authorlist,
            'dynastylist': combined_dynastylist,
            'rand_list': rand_list,
            'museum': museum,
            'video_data': videoData
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'db' in locals():
            cursor.close()


# 提交浏览记录(并更新用户浏览记录表)
@app.route('/api/put_view/<relic_id>', methods=['PUT'])
def get_view(relic_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'views_count is required'}), 400

    views_count = data['views_count']
    user_id = data['user_id']

    conn = get_db()
    cursor = conn.cursor()
    sql = "UPDATE cultural_relic SET views_count=%s  WHERE relic_id = %s"
    cursor.execute(sql, (views_count, relic_id,))

    # 先查询是否已有浏览记录
    sql_check_history = """
            SELECT id FROM user_browsing_history 
            WHERE user_id = %s AND relic_id = %s
        """
    cursor.execute(sql_check_history, (user_id, relic_id))
    result = cursor.fetchone()

    if result:
        # 更新浏览时间
        sql_update_history = """
                UPDATE user_browsing_history 
                SET browse_time = %s 
                WHERE id = %s
            """
        cursor.execute(sql_update_history, (datetime.now(), result['id']))
    else:
        # 插入新的浏览记录
        sql_insert_history = """
                INSERT INTO user_browsing_history (user_id, relic_id, browse_time) 
                VALUES (%s, %s, %s)
            """
        cursor.execute(sql_insert_history, (user_id, relic_id, datetime.now()))

    conn.commit()

    return jsonify({'status': 'success', 'message': '提交浏览成功'})


# 点赞记录
@app.route('/api/put_like/<relic_id>', methods=['PUT'])
def get_like(relic_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'like_count is required'}), 400
    likes_count = data['likes_count']
    conn = get_db()
    cursor = conn.cursor()
    # 提交点赞
    sql = "UPDATE cultural_relic SET likes_count=%s  WHERE relic_id = %s"
    cursor.execute(sql, (likes_count, relic_id,))
    user_id = data['user_id']
    islike = data['islike']
    if islike:
        sql = "DELETE FROM relic_like where relic_id=%s and user_id=%s"
        cursor.execute(sql, (relic_id, user_id))
    else:
        sql = "INSERT INTO relic_like(user_id,relic_id) VALUES (%s,%s)"
        cursor.execute(sql, (user_id, relic_id))
    # 提交收藏

    conn.commit()
    return jsonify({'status': 'success', 'message': '提交收藏成功'})


# 获得点赞记录
@app.route('/api/get_thumsbup', methods=['GET'])
def get_thumbsup():
    relic_id = request.args.get('relic_id')
    user_id = request.args.get('user_id')
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * from relic_like where relic_id=%s and user_id=%s"
    cursor.execute(sql, (relic_id, user_id))
    islike = cursor.fetchone()
    sql = "SELECT * from user_favorite where relic_id=%s and user_id=%s"
    cursor.execute(sql, (relic_id, user_id))
    isfav = cursor.fetchone()
    return jsonify({"islike": islike, 'isfav': isfav})


# 获得收藏记录
@app.route('/api/put_Fav/<int:fav_id>', methods=['PUT'])
def get_fav(fav_id):
    data = request.get_json()
    museum_id = data['museum_id']
    relic_id = fav_id
    is_fav = data['is_fav']
    user_id = data['user_id']
    conn = get_db()
    cursor = conn.cursor()
    if is_fav:
        sql = "DELETE FROM user_favorite where relic_id=%s and user_id=%s"
        cursor.execute(sql, (relic_id, user_id,))
    else:
        sql = "INSERT INTO user_favorite(user_id,relic_id,museum_id,favorite_type) VALUES (%s,%s,%s,1)"
        cursor.execute(sql, (user_id, relic_id, museum_id))

    conn.commit()
    return jsonify('提交成功')


# 个人信息展示
@app.route('/user_info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    conn = get_db()
    cursor = conn.cursor()

    # 获取用户信息
    cursor.execute("""
        SELECT user_id, phone_number, id_number, name, description, gender, age,
               address, wechat, qq
        FROM user WHERE user_id=%s
    """, (user_id,))
    user_info = cursor.fetchone()
    if not user_info:
        return jsonify({"error": "User not found"}), 404

    # 查询收藏、点赞、评论的文物ID
    cursor.execute("SELECT relic_id FROM user_favorite WHERE user_id=%s AND favorite_type=1",
                   (user_id,))
    favorite_ids = [row['relic_id'] for row in cursor.fetchall()]

    cursor.execute("SELECT relic_id FROM relic_like WHERE user_id=%s", (user_id,))
    like_ids = [row['relic_id'] for row in cursor.fetchall()]

    cursor.execute(
        "SELECT DISTINCT relic_id FROM relic_comment WHERE user_id=%s AND is_deleted=0",
        (user_id,))
    comment_ids = [row['relic_id'] for row in cursor.fetchall()]

    cursor.execute("select relic_id FROM user_browsing_history WHERE user_id=%s", (user_id,))
    browsing_history_ids = [row['relic_id'] for row in cursor.fetchall()]

    # 合并所有文物ID用于批量查询文物信息
    all_ids = set(favorite_ids + like_ids + comment_ids + browsing_history_ids)
    relic_details = {}
    if all_ids:
        format_strings = ','.join(['%s'] * len(all_ids))
        cursor.execute(f"""
            SELECT cr.relic_id, cr.name, cr.type, cr.matrials,
               cr.dynasty, cr.author, cr.entry_time,
               ri.img_url, m.museum_name
        FROM cultural_relic cr
        JOIN museum m ON cr.museum_id = m.museum_id
        LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id
        WHERE cr.relic_id IN ({format_strings})
        """, tuple(all_ids))  # 参数传两遍，一次用于子查询，一次用于主查询

        for row in cursor.fetchall():
            relic_details[row['relic_id']] = row

    # 整理每一类的文物详细信息列表
    favorites = [relic_details[rid] for rid in favorite_ids if rid in relic_details]
    likes = [relic_details[rid] for rid in like_ids if rid in relic_details]
    comments = [relic_details[rid] for rid in comment_ids if rid in relic_details]
    browsing_history = [relic_details[rid] for rid in browsing_history_ids if rid in relic_details]

    result = {
        "user_info": user_info,
        "favorites": favorites,
        "likes": likes,
        "comments": comments,
        "browsing_history": browsing_history
    }

    return jsonify(result)


# 头像上传
@app.route('/upload_avatar/<int:user_id>', methods=['POST'])
def upload_avatar(user_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # 头像保存目录
        avatar_dir = os.path.join('static', 'avatar')
        os.makedirs(avatar_dir, exist_ok=True)

        # 将图片转换为PNG并保存
        image = Image.open(file.stream)
        image = image.convert('RGBA')  # 转为支持透明通道的PNG格式
        save_path = os.path.join(avatar_dir, f'{user_id}.png')
        image.save(save_path, 'PNG')

        return jsonify({'message': 'Upload successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 修改密码
@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    user_id = data.get('user_id')
    new_password = data.get('new_password')

    if not user_id or not new_password:
        return jsonify({'status': 'error', 'message': '缺少必要参数'}), 400

    hashed_password = hash_password(new_password)

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_password, user_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': '用户不存在或密码未更新'}), 404

        return jsonify({'status': 'success', 'message': '密码修改成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': '服务器错误: ' + str(e)}), 500


# 编辑用户信息
@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'status': 'error', 'message': '缺少用户ID'}), 400

    name = data.get('name')
    description = data.get('description')
    gender = data.get('gender')
    address = data.get('address')
    age = data.get('age')
    wechat = data.get('wechat')
    qq = data.get('qq')

    if not name:
        return jsonify({'status': 'error', 'message': '用户名不能为空'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user
            SET name = %s,
                description = %s,
                gender = %s,
                address = %s,
                age = %s,
                wechat = %s,
                qq = %s
            WHERE user_id = %s
        """, (name, description, gender, address, age, wechat, qq, user_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': '用户未找到或信息未变动'}), 404

        return jsonify({'status': 'success', 'message': '用户信息更新成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': '数据库错误: ' + str(e)}), 500


# 用户评论
@app.route('/user/comment', methods=['POST'])
def upload_comment():
    relic_id = request.form.get('relic_id')  # 前端需传文物ID
    user_id = request.form.get('user_id')  # 前端需传用户ID
    text = request.form.get('text')
    files = request.files.getlist('images')

    if not relic_id or not user_id:
        return jsonify({'status': 'error', 'message': '缺少 relic_id 或 user_id'}), 400

    try:
        conn = get_db()
        with conn.cursor() as cursor:
            # 1. 插入评论内容
            insert_comment = """
                    INSERT INTO relic_comment (relic_id, user_id, content)
                    VALUES (%s, %s, %s)
                """
            cursor.execute(insert_comment, (relic_id, user_id, text))
            comment_id = cursor.lastrowid

            saved_image_urls = []

            for file in files:
                if file:
                    # 将原图转为 PNG 格式（使用 PIL）
                    img = Image.open(file.stream).convert("RGBA")
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")
                    buffer.seek(0)

                    # 插入图片记录（先不保存路径）
                    insert_image = """
                            INSERT INTO user_image (image_suffix, user_id, comment_id)
                            VALUES (%s, %s, %s)
                        """
                    cursor.execute(insert_image, ('.png', user_id, comment_id))
                    image_id = cursor.lastrowid

                    # 保存 PNG 文件
                    filename = f"{image_id}.png"
                    dir = os.path.join('static', 'comment_image')
                    filepath = os.path.join(dir, filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'wb') as f:
                        f.write(buffer.read())

                    image_url = f"/static/comment_image/{filename}"
                    saved_image_urls.append(image_url)

            conn.commit()

        return jsonify({
            'status': 'success',
            'message': '评论提交成功',
            'comment_id': comment_id,
            'images': saved_image_urls
        })

    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# 获取评论
@app.route('/get/comments', methods=['GET'])
def get_comments():
    relic_id = request.args.get('relic_id')

    conn = get_db()
    with conn.cursor() as cursor:
        # 获取主评论
        cursor.execute("""
            SELECT c.comment_id, c.user_id, c.content, c.update_time, u.name, c.reply_count
            FROM relic_comment c
            JOIN user u ON c.user_id = u.user_id
            WHERE c.relic_id = %s AND c.is_deleted = 0 AND c.status = 1 AND c.parent_id IS NULL
            ORDER BY c.create_time DESC
        """, (relic_id,))
        top_comments = cursor.fetchall()

        # 获取子评论
        cursor.execute("""
            SELECT c.comment_id, c.parent_id, c.user_id, c.content, c.update_time, u.name
            FROM relic_comment c
            JOIN user u ON c.user_id = u.user_id
            WHERE c.relic_id = %s AND c.is_deleted = 0 AND c.status = 1 AND c.parent_id IS NOT NULL
            ORDER BY c.create_time ASC
        """, (relic_id,))
        child_comments = cursor.fetchall()

        # 获取图片（只针对主评论）
        cursor.execute("""
            SELECT comment_id, image_id, image_suffix
            FROM user_image
            WHERE status = 1
        """)
        image_rows = cursor.fetchall()

    # 构建主评论字典
    comment_map = {}
    for c in top_comments:
        comment_map[c['comment_id']] = {
            'comment_id': c['comment_id'],
            'user_id': c['user_id'],
            'content': c['content'],
            'update_time': c['update_time'],
            'name': c['name'],
            'reply_count': c['reply_count'],
            'images': [],
            'children': []
        }

    # 添加图片（只挂主评论）
    for img in image_rows:
        comment_id = img['comment_id']
        if comment_id in comment_map:
            url = f"http://localhost:5000/static/comment_image/{img['image_id']}.png"
            comment_map[comment_id]['images'].append(url)

    # 添加子评论
    print(child_comments)
    for reply in child_comments:
        parent_id = reply['parent_id']
        sub_comment = {
            'comment_id': reply['comment_id'],
            'user_id': reply['user_id'],
            'content': reply['content'],
            'update_time': reply['update_time'],
            'name': reply['name']
        }
        if parent_id in comment_map:
            comment_map[parent_id]['children'].append(sub_comment)
        else:
            # 若主评论不存在（例如被删了），可选：创建临时挂载点或跳过
            print(f"⚠️ 无效 parent_id={parent_id}，跳过该子评论。")

    # 返回按时间排序的主评论列表
    sorted_comments = sorted(comment_map.values(), key=lambda x: x['update_time'], reverse=True)

    return jsonify(sorted_comments)


# 回复评论
@app.route('/user/reply', methods=['POST'])
def user_reply():
    data = request.get_json()
    parent_id = data.get('parent_id')
    user_id = data.get('user_id')
    content = data.get('content')

    if not parent_id or not user_id or not content:
        return jsonify({'status': 'error', 'message': '缺少必要字段'}), 400

    try:
        conn = get_db()
        with conn.cursor() as cursor:
            # 插入子评论
            cursor.execute("""
                INSERT INTO relic_comment (parent_id, user_id, relic_id, content)
                SELECT %s, %s, relic_id, %s FROM relic_comment WHERE comment_id = %s
            """, (parent_id, user_id, content, parent_id))

            # 更新主评论的回复计数
            cursor.execute("""
                UPDATE relic_comment SET reply_count = reply_count + 1
                WHERE comment_id = %s
            """, (parent_id,))

        conn.commit()
        return jsonify({'status': 'success', 'message': '回复成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
