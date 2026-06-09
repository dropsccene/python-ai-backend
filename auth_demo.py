import bcrypt
import jwt
import datetime
import secrets

pwd = "hello123"

hashed = bcrypt.hashpw(pwd.encode(),bcrypt.gensalt())
print(hashed)
print(bcrypt.checkpw(pwd.encode(),hashed))
print(bcrypt.checkpw("wrong_password".encode(),hashed))

SECRET = secrets.token_hex(32)
payload = {"user_id":42,"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)}
token = jwt.encode(payload,SECRET,algorithm="HS256")
print(jwt.decode(token,SECRET,algorithms=["HS256"]))

def hash_password(plain:str)->str:
	pwd = bcrypt.hashpw(plain.encode(),bcrypt.gensalt())
	return pwd.decode()

def create_token(user_id:int)->str:
	payload = {"user_id":user_id,"exp":datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes= 15)}
	return jwt.encode(payload,SECRET,algorithm="HS256")

print(hash_password("python2024"))
print(hash_password("python2024"))
