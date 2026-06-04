create table users(
    id INTEGER PRIMARY KeY AUTOINCREMENT,
    NAME TEXT NOT NULL
);

create table articles(
    id integer primary key autoincrement,
    title text not null,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name) VALUES ('张三');
INSERT INTO users (name) VALUES ('李四');
INSERT INTO users (name) VALUES ('王五');
INSERT INTO articles (title ,user_id) VALUES ('我的第一篇文章',1);
INSERT INTO articles (title ,user_id) VALUES ('学习SQL',1);
INSERT INTO articles (title ,user_id) VALUES ('Python 教程',2);
INSERT INTO articles (title ,user_id) VALUES ('数据库设计',2);
INSERT INTO articles (title ,user_id) VALUES ('周末计划',3);

-- 查询所有用户,所有文章
SELECT * FROM users;
SELECT * FROM articles;

-- 查询张三的文章
SELECT * FROM articles WHERE user_id = 1;

-- 修改一篇文章的标题
UPDATE articles  SET title = '更新周末计划' WHERE id = 5;

-- 联表查“文章标题 + 作者名”
SELECT articles.title,users.name 
FROM articles
JOIN users ON articles.user_id = users.id;

-- 统计每个用户有多少篇文章
SELECT users.name,COUNT(articles.id) AS article_count
FROM users
LEFT JOIN articles ON users.id = articles.user_id
GROUP BY users.id;
