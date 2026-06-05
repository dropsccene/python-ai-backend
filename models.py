from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key = True)
    username = Column(String,nullable=False)
    articles = relationship("Article",back_populates = "author")
    email = Column(String,unique=True,nullable=False)

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer,primary_key = True)
    title = Column(String,nullable = False)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    author = relationship("User",back_populates="articles")
    content = Column(String,nullable=False)