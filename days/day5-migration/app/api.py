"""
app/api.py —— 路由层
=====================
这个文件只管一件事：定义所有的接口（GET/POST/PUT/DELETE）。

每个函数 = 一个接口 = 一个 URL 地址。
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db

# APIRouter = "路由组"
# 可以把多个接口分成一组，挂载到 FastAPI 主应用上
router = APIRouter()


# ============================================================
# POST /students —— 新增学生
# ============================================================
@router.post("/students", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    客户端发一个 JSON：
      {"name": "张三", "age": 20}

    FastAPI：
    1. 用 StudentCreate 校验 JSON
    2. 通过 Depends(get_db) 拿一个 session
    3. 执行函数体：insert 到数据库
    4. 返回学生数据（id 是自动生成的）
    """
    # 把校验通过的数据转成数据库对象
    db_student = models.Student(
        name=student.name,
        age=student.age,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)  # 刷新——拿到数据库自动生成的 id
    return db_student       # FastAPI 自动把它转成 StudentOut JSON


# ============================================================
# GET /students —— 查所有学生
# ============================================================
@router.get("/students", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students  # 返回列表，每个元素自动转成 StudentOut JSON


# ============================================================
# GET /students/{student_id} —— 按 ID 查一个学生
# ============================================================
@router.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return db.get(models.Student, student_id)  # 直接返回，没找到返回 None


# ============================================================
# PUT /students/{student_id} —— 更新学生
# ============================================================
@router.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,       # 只填想改的字段
    db: Session = Depends(get_db),
):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        return None

    # 只更新用户填了的字段
    if student.name is not None:
        db_student.name = student.name
    if student.age is not None:
        db_student.age = student.age

    db.commit()
    db.refresh(db_student)
    return db_student


# ============================================================
# DELETE /students/{student_id} —— 删除学生
# ============================================================
@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        return {"error": f"找不到 id 为 {student_id} 的学生"}

    db.delete(db_student)
    db.commit()
    return {"message": f"已删除 {db_student.name}"}
