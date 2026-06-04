from models import engine,Base,User,Article
from sqlalchemy.orm import Session

session = Session(engine)
session.add(User(name = "赵六"))
session.add(Article(title = "新名字",user_id = 1))
session.commit()

def print_query(results):
    for row in results:
        print(row)

print_query(session.query(User).all())

user=session.query(User).filter(User.id == 1).first()
print(user)

user.name = "新名字"
session.commit()
print(user)

articles = user.articles
for a in articles:
    print(a.title)


session.delete(user)
session.commit()
print(user)



