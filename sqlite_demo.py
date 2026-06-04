import sqlite3
# 连接到SQLite数据库
conn = sqlite3.connect('test.db')
# 创建一个Cursor对象来执行SQL语句
cursor = conn.cursor()
def print_result(result):
    for row in result:
        print(row)

# 执行sql语句
# 创建表
cursor.execute("create table if not exists users( id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL)")
cursor.execute("create table if not exists articles(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,user_id INTEGER NOT NULL,FOREIGN KEY (user_id) REFERENCES users(id))")

# 插入数据
cursor.execute("INSERT INTO users (name) VALUES (?)", ("张三",))
cursor.execute("INSERT INTO users (name) VALUES (?)", ("李四",))
cursor.execute("INSERT INTO users (name) VALUES (?)", ("王五",))
cursor.execute("INSERT INTO articles (title, user_id) VALUES (?, ?)", ("我的第一篇文章", 1))
cursor.execute("INSERT INTO articles (title, user_id) VALUES (?, ?)", ("学习SQL", 1))
cursor.execute("INSERT INTO articles (title, user_id) VALUES (?, ?)", ("Python 教程", 2))
cursor.execute("INSERT INTO articles (title, user_id) VALUES (?, ?)", ("数据库设计", 2))
cursor.execute("INSERT INTO articles (title, user_id) VALUES (?, ?)", ("周末计划", 3))

# 查询数据
cursor.execute("SELECT * FROM users")
print_result(cursor.fetchall())
cursor.execute("SELECT * FROM articles")
print_result(cursor.fetchall())


# 查询用户和他们的文章
cursor.execute("SELECT * FROM articles WHERE user_id = 1")
print_result(cursor.fetchall())

# 更新数据
cursor.execute("UPDATE articles SET title = ? WHERE id = ?", ("更新周末计划", 5))
cursor.execute("SELECT * FROM articles WHERE id = 5")
print_result(cursor.fetchall())

# 联表查“文章标题 + 作者名”
cursor.execute("SELECT articles.title, users.name FROM articles JOIN users ON articles.user_id = users.id")
print_result(cursor.fetchall())

# 统计每个用户的文章数量
cursor.execute("SELECT users.name, COUNT(articles.id) AS article_count FROM users LEFT JOIN articles ON users.id = articles.user_id GROUP BY users.id")
print_result(cursor.fetchall())
# 提交事务
conn.commit()
# 关闭连接
conn.close()