@app.get("/items/{item_id}")
def read_item(item_id:int):
    if item_id <= 0:
        raise HTTPException(status_code = 400, detail = "Invalid item ID")
    return {"item_id": item_id}

@app.get("/articles/top")
def top_articles(db : Session = Depends(get_db)):
	articles  = db.query(Article).order_by(Article.id.desc()).limit(5).all()
	if not articles:
		raise HTTPException(status_code = 404 , detail = "No articles found")
	return articles


enrollments Table(
    student_id Integer ForeignKey("students.student_id"),
    course_id Integer ForeignKey("courses.course_id"),
    PrimaryKeyConstraint(student_id, course_id)
) 

class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
class Course(Base):
    __tablename__= "courses"
    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    students = relationship("Student", secondary=student_courses, back_populates="courses")


def collect_items(name:str,*args,**kwargs):
	print(name)
	for arg in args:
		print(arg)
	if kwargs.get('tags') is None:
		print("no tags")
	else:
		print(kwargs.get('tags'))
