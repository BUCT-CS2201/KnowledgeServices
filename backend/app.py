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
        return jsonify({'status': 'success', 'message': '登录成功', 'username': result['name'], 'user_id':result['user_id']})
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
        cr.dynasty, cr.likes_count, cr.views_count, cr.author, cr.entry_time, ri.img_url, m.museum_name
        FROM cultural_relic cr
        join museum m on cr.museum_id = m.museum_id
        LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id
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
        '时间：新-旧': 'order by entry_time desc',
        '时间：旧-新': 'order by entry_time asc',
        '名称：A-Z': 'order by name desc',
        '名称：Z-A': 'order by name asc'
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

    query = request.args.get('q', '').strip()
    sort = request.args.get('sort', '').strip()
    condition = request.args.get('condition', '').strip()
    popular = request.args.getlist('popular')

    sql = """
            SELECT cr.relic_id, cr.name, cr.type, cr.description, cr.size, cr.matrials, 
                   cr.dynasty, cr.likes_count, cr.views_count, cr.author, cr.entry_time, 
                   ri.img_url, m.museum_name
            FROM cultural_relic cr
            JOIN museum m ON cr.museum_id = m.museum_id
            LEFT JOIN relic_image ri ON cr.relic_id = ri.relic_id
        """

    # 动态拼接关键词搜索条件
    if query and condition:
        sql += " where cr." + condition_dict[condition] + " like %s"
    elif query:
        sql += (" where cr.name like %s or cr.description like %s or cr.size like %s or cr.matrials like"
                " or cr.dynasty like %s or cr.author like %s or cr.entry_time like %s or m.museum_name like %s")

    if sort:
        sql += sort_dict[sort]

    try:
        with db.cursor() as cursor:
            if query and condition:
                cursor.execute(sql, ('%' + query + '%',))
            elif query:
                cursor.execute(sql, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%',
                                     '%' + query + '%', '%' + query + '%', '%' + query + '%',))
            else:
                cursor.execute(sql)
            rows = cursor.fetchall()

        # 构造前端需要的数据格式
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

        # print(results)
        return jsonify({"results": results})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error"}), 500

    finally:
        if 'db' in locals():
            db.close()


# 页面图片
@app.route('/api/detail_inform', methods=['GET'])
def get_inform():
    relic_id = request.args.get('relic_id')

    if not relic_id:
        return jsonify({'status': 'error', 'message': 'relic_id is required'}), 400

    cursor = db.cursor()
    try:
        #获取文物有关视频
        sql="SELECT * FROM relic_video where relic_id=%s LIMIT 4"
        cursor.execute(sql,(relic_id,))
        videoData=cursor.fetchall()
        # 获取文物的图片URL
        sql = "SELECT * FROM relic_image WHERE relic_id = %s"
        cursor.execute(sql, (relic_id,))
        result_img = cursor.fetchone()
        img_url = result_img['img_url'] if result_img else None

        # 获取文物的详细信息
        sql = "SELECT * FROM cultural_relic WHERE relic_id = %s"
        cursor.execute(sql, (relic_id,))
        result = cursor.fetchone()
        museum_id=result['museum_id']
        print(museum_id)
        sql = "SELECT * FROM museum WHERE museum_id = %s"
        cursor.execute(sql, (museum_id,))
        museum = cursor.fetchone()
        print(museum)

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
            'museum':museum,
            'video_data':videoData
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'db' in locals():
            cursor.close()


# 提交浏览记录
@app.route('/api/put_view/<relic_id>', methods=['PUT'])
def get_view(relic_id):
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'status': 'error', 'message': 'views_count is required'}), 400
    views_count = data['views_count']
    cursor = db.cursor()
    sql = "UPDATE cultural_relic SET views_count=%s  WHERE relic_id = %s"
    cursor.execute(sql, (views_count, relic_id,))
    db.commit()
    return jsonify({'status': 'success', 'message': '提交浏览成功'})


# 点赞记录
@app.route('/api/put_like/<relic_id>', methods=['PUT'])
def get_like(relic_id):
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'status': 'error', 'message': 'like_count is required'}), 400
    likes_count = data['likes_count']
    cursor = db.cursor()
    #提交点赞
    sql = "UPDATE cultural_relic SET likes_count=%s  WHERE relic_id = %s"
    cursor.execute(sql, (likes_count,relic_id,))
    user_id=data['user_id']
    islike=data['islike']
    if islike:
        sql="INSERT INTO relic_like(user_id,relic_id) VALUES (%s,%s)"
        cursor.execute(sql,(user_id,relic_id))
    else:
        sql="DELETE FROM relic_like where relic_id=%s"
        cursor.execute(sql,(relic_id,))
    #提交收藏

    db.commit()
    return jsonify({'status': 'success', 'message': '提交收藏成功'})
#获得点赞记录
@app.route('/api/get_thumsbup',methods=['GET'])
def get_thumbsup():
    relic_id=request.args.get('relic_id')
    print(relic_id)
    cursor=db.cursor()
    sql="SELECT user_id from relic_like where relic_id=%s"
    cursor.execute(sql,(relic_id,))
    user_id=cursor.fetchone()
    sql="SELECT user_id from user_favorite where relic_id=%s"
    cursor.execute(sql,(relic_id,))
    user_favid=cursor.fetchone()
    print(user_id)
    return jsonify({"user_id": user_id,'user_favid':user_favid})
   
#获得收藏记录
@app.route('/api/put_Fav/<Fav_id>',methods=['PUT'])
def get_Fav(Fav_id):
    data=request.get_json()
    museum_id=data['museum_id']
    relic_id=Fav_id
    isFav=data['isFav']
    user_id=data['user_id']
    cursor=db.cursor()
    if isFav:
        sql="INSERT INTO user_favorite(user_id,relic_id,museum_id,favorite_type) VALUES (%s,%s,%s,1)"
        cursor.execute(sql,(user_id,relic_id,museum_id))
    else:
        sql="DELETE FROM user_favorite where relic_id=%s"
        cursor.execute(sql,(relic_id,))
    return jsonify('提交成功')

if __name__ == "__main__":
    app.run(debug=True)
