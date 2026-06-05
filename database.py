# 从 sqlalchemy 导入 create_engine
from sqlalchemy import create_engine
# 从 sqlalchemy.orm 导入 sessionmaker 和 declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base
# 数据库地址 = sqlite 文件 ./blog.db
sqlite_db = "sqlite:///./blog.db"
# 创建引擎 engine （注意 connect_args 参数）
engine = create_engine(sqlite_db,connect_args={"check_same_thread":False})
# 创建模型基类 Base
Base = declarative_base()
# 创建会话工厂 SessionLocal （autocommit=False, autoflush=False, 绑定 engine）
sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# 定义 get_db 函数
def get_db():
#   创建 db 会话
	db = sessionlocal()
#   try yield db
	try:
		yield db
#   finally 关闭 db
	finally:
		db.close()
