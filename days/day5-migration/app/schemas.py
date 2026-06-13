"""
app/schemas.py —— 请求/响应校验层
====================================
这个文件只管一件事：定义"客户端发给我的数据应该长什么样"。

和 models.py 的区别：
- models.py = 数据库表（持久化存的）
- schemas.py = 请求/响应格式（网络传的）

为什么分两个？
- 有些字段数据库才需要（比如 id 是自动生成的）
- 有些字段前端才需要（比如确认密码，数据库不存）
"""

from pydantic import BaseModel


# 新增学生时的请求格式
class StudentCreate(BaseModel):
    name: str
    age: int


# 更新学生时的请求格式
# 字段都设为可选（= None），只更新用户填了的字段
class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None


# 查询所有学生时的响应格式
class StudentOut(BaseModel):
    id: int
    name: str
    age: int

    # 这行让 Pydantic 能从数据库对象自动转
    class Config:
        from_attributes = True
