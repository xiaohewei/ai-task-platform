"""
Day 2 - FastAPI 深入
今天学：路径参数 → 查询参数 → Pydantic 模型 + POST
"""

from fastapi import FastAPI

app = FastAPI()


# ============================================================
# 第一部分：路径参数（Path Parameter）
# ============================================================

# 假数据库 —— 一个字典，key 是学号，value 是学生信息
# 回忆 Day1 的字典：{键: 值, 键: 值}
students_db = {
    1: {"name": "张三", "age": 20, "major": "计算机科学"},
    2: {"name": "李四", "age": 21, "major": "软件工程"},
    3: {"name": "王五", "age": 19, "major": "人工智能"},
}


@app.get("/students/{student_id}")
async def get_student(student_id: int):
    """
    路径参数：URL 里的 {student_id} 是变量，不是固定文字。
    访问 /students/1  → student_id=1 → 返回张三
    访问 /students/2  → student_id=2 → 返回李四

    :int 的意思：告诉 FastAPI 自动把 URL 里的字符串 "1" 转成整数 1
    """
    if student_id not in students_db:
        return {"error": f"找不到学号为 {student_id} 的学生"}

    return {"学号": student_id, "信息": students_db[student_id]}
