from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from fastapi import FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Depends
engine = create_engine("sqlite:///school.db",echo = True)

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(engine)
app = FastAPI()
def get_db():
    session = Session(engine)   
    try:
        yield session          
    finally:
        session.close()          
class StudentCreate(BaseModel):
    name: str
    age: int

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None

# ============================================================
# 增 — Create
# ============================================================
@app.post("/students")
async def create_student(student: StudentCreate, sess = Depends(get_db)):
    s = Student(name=student.name, age=student.age)  # 创建 ORM 对象
    sess.add(s)          # 放进待保存区
    sess.commit()        # 写入数据库
    return {"id": s.id, "name": s.name}

# ============================================================
# 查全部 — Read All
# ============================================================
@app.get("/students")
async def list_students(sess = Depends(get_db)):
    students = sess.query(Student).all()   # 等价于 SELECT *
    result = []
    for s in students:
        result.append({"id": s.id, "name": s.name, "age": s.age})
    return {"count": len(result), "students": result}

# ============================================================
# 查一个 — Read One
# ============================================================
@app.get("/students/{student_id}")
async def get_student(student_id: int, sess = Depends(get_db)):
    s = sess.get(Student, student_id)   # 按主键查，比 filter 快
    if s is None:
        return {"error": f"找不到 id={student_id} 的学生"}
    return {"id": s.id, "name": s.name, "age": s.age}

# ============================================================
# 改 — Update
# ============================================================
@app.put("/students/{student_id}")
async def update_student(student_id: int, data: StudentUpdate, sess = Depends(get_db)):
    s = sess.get(Student, student_id)
    if s is None:
        return {"error": f"找不到 id={student_id} 的学生"}
    # 只改用户填了的字段，没填的不动
    if data.name is not None:
        s.name = data.name    # 直接改属性！
    if data.age is not None:
        s.age = data.age       # 直接改属性！
    sess.commit()              # 提交，数据库自动更新
    return {"message": f"id={student_id} 更新成功"}

# ============================================================
# 删 — Delete
# ============================================================
@app.delete("/students/{student_id}")
async def delete_student(student_id: int, sess = Depends(get_db)):
    s = sess.get(Student, student_id)
    if s is None:
        return {"error": f"找不到 id={student_id} 的学生"}
    sess.delete(s)      # 标记删除
    sess.commit()        # 真正从数据库删掉
    return {"message": f"id={student_id} 已删除"}