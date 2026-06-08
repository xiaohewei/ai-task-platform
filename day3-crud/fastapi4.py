import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
                )
"""    )
    conn.commit()
    conn.close()

init_db()
print("数据库建立成功！")
class StudentCreate(BaseModel):
    name: str
    age: int


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None


@app.post("/students")
async def create_student(student: StudentCreate):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (student.name, student.age)
    )
    conn.commit()

    new_id = cur.lastrowid
    conn.close()

    return {"message": "新增成功!", "id": new_id, "name": student.name, "age": student.age}

@app.get("/students")
async def list_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({"id": row[0],"name": row[1],"age": row[2]})
    return {"count": len(result), "students": result}

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {"error": f"找不到 id 为 {student_id} 的学生"}

    return {"id": row[0], "name": row[1], "age": row[2]}
    




# ============================================================
# PUT /students/{student_id} — 更新某个学生（Update）
# ============================================================
@app.put("/students/{student_id}")
async def update_student(student_id: int, student: StudentUpdate):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    # 只更新用户填了的字段，没填的保持原值
    if student.name is not None:
        cur.execute(
            "UPDATE students SET name = ? WHERE id = ?",
            (student.name, student_id)
        )
    if student.age is not None:
        cur.execute(
            "UPDATE students SET age = ? WHERE id = ?",
            (student.age, student_id)
        )

    conn.commit()
    conn.close()

    return {"message": f"学号为 {student_id} 的学生更新成功！"}


# ============================================================
# DELETE /students/{student_id} — 删除某个学生（Delete）
# ============================================================
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return {"message": f"学号为 {student_id} 的学生已删除！"}
