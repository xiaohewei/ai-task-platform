"""
app/models.py —— 数据模型层
=============================
这个文件只管一件事：定义表结构。

以前所有 class Student(Base) 都塞在 main.py 里，
现在全搬到这里。以后要改表结构，只改这一个文件。
"""

from app.db import Base
from sqlalchemy import Column, Integer, String


class Student(Base):
    """
    Student 类 = 数据库里的 students 表

    __tablename__ = 表名
    Column() = 字段定义
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)    # 主键，自增
    name = Column(String, nullable=False)     # 不能为空
    age = Column(Integer, default=18)         # 默认值 18

    def __repr__(self):
        return f"<Student id={self.id} name='{self.name}' age={self.age}>"


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subject = Column(String)

    def __repr__(self):
        return f"<Teacher id={self.id} name='{self.name}' subject='{self.subject}'>"
