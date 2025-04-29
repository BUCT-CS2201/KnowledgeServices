# 🌠KnowledgeServices—海外文物知识服务子系统

### 🙋‍♀️Who we are?

- BUCT计科2201海外文物知识服务子系统小组
- 成员：高洁、梅宸倩、陈嘉欣、杨蕊菡、杨心怡、崔文悦

### 🛩️Where are we going?

- 编写Web端程序，使用知识图谱构建子系统获取的数据，实现数据浏览、查询、可视化等服务。

### 🔬Which tech do we use?

- 前端：Vue
- 后端：Python（Flask）

### 🏘️How to build?

> 在本地环境上试运行（部署后删除）
>
> - 创建数据库、导入表文件
> - 更改backend\app.py中的数据库账号密码
>
> ```bash
> # neo4j
> driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "your_own_password"))# change to your own name and password
> 
> # MySQL
> db = pymysql.connect(
>     host='localhost',
>     user='root',
>     password='your_own_password',# change to your own name and password
>     database='cultural_relics',
>     charset='utf8mb4'
> )
> ```

 - 后端环境搭建（使用conda进行环境管理）：

   ```bash
   conda create -n KnowledgeServices310 python=3.10 -y
   conda activate KnowledgeServices310
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

- 前端环境搭建

  ```bash
  cd frontend
  npm install
  npm run serve
  ```

