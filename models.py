from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship,Session
from sqlalchemy import event

engine = create_engine("sqlite:///test.db")
@event.listens_for(engine,"connect")
def enable_foreign_keys(dbapi_connection,connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key = True)
    name = Column(String,nullable=False)
    articles = relationship("Article",back_populates = "author")


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer,primary_key = True)
    title = Column(String,nullable = False)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    author = relationship("User",back_populates="articles")


Base.metadata.create_all(engine)

if __name__ == "__main__":
    print(Base.metadata.tables.keys())
