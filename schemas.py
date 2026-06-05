#  pydantic 导入 BaseModel
from pydantic import BaseModel
# 创建UserCreate模型，包含 username、email 的字符串类型
class UserCreate(BaseModel):
	username:str
	email:str
# 创建UserResponse 模型，包含id-整数类型、username、email-字符串类型
class UserResponse(BaseModel):
	id : int
	username:str
	email:str
    # UserResponse 配置 model_config = {“from_attributes”:True},让Pydantic 能从 SQLAlchemy ORM 对象自动读取属性
	model_config = {"from_attributes": True}
class ArticleCreate(BaseModel):
	title :str
	content : str
class ArticleResponse(BaseModel):
	id : int
	title : str
	content : str
	model_config = {"from_attributes" : True}
