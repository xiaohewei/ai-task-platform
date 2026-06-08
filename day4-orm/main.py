"""
Day4 — SQLAlchemy ORM：用 Python 类操作数据库
================================================
今天的目标：再也不用拼 SQL 字符串，用 Python 类直接操作数据库。

核心概念：
- 一张表 = 一个 Python 类（class）
- 一行数据 = 一个 Python 对象（object）
- 一个字段 = 一个类属性（attribute）

比如 student.name = "张三" → 数据库自动更新 name 字段
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

# ============================================================
# 第一步：创建数据库引擎
# ============================================================
# create_engine() = "告诉 SQLAlchemy 数据库在哪"
# 参数是数据库 URL，格式：数据库类型:///文件路径
# echo=True = 把每条 SQL 打印到控制台，方便我们看它背后做了什么
engine = create_engine("sqlite:///school.db", echo=True)


# ============================================================
# 第二步：定义 Base 基类
# ============================================================
# DeclarativeBase = "声明式基类"
# 所有的表模型（Student、Teacher...）都继承它
# 继承 = "我爸有的能力我全都有"
class Base(DeclarativeBase):
    pass


# ============================================================
# 第三步：定义模型（Student 类 = students 表）
# ============================================================
class Student(Base):
    """
    这个 Python 类 = 数据库里的 students 表

    Column() = "这是表里的一个字段"
    - Integer = 整数类型
    - String = 字符串类型
    - primary_key=True = 主键（唯一标识，不能重复）
    """
    __tablename__ = "students"  # 表名（数据库里叫啥）

    id = Column(Integer, primary_key=True)   # id 字段：整数、主键
    name = Column(String)                     # name 字段：字符串
    age = Column(Integer)                     # age 字段：整数

    def __repr__(self):
        """打印对象时的显示格式，方便调试"""
        return f"<Student id={self.id} name='{self.name}' age={self.age}>"


# ============================================================
# 第四步：创建表
# ============================================================
# create_all() = "扫描所有继承 Base 的类，在数据库里建对应的表"
# 如果表已经存在，不会重复创建（不会覆盖数据）
Base.metadata.create_all(engine)
print("[OK] 表创建完成！")


# ============================================================
# 第五步：打开会话（Session = 数据库操作的"临时工作区"）
# ============================================================
# Session = 数据库连接 + 事务管理
# 类比：你打开一个 Word 文档开始编辑，Session 就是那个"编辑状态"
# 只有 commit() 之后，修改才真正写进数据库
session = Session(engine)


# ============================================================
# 第六步：增删改查（CRUD）—— 看好了，一行 SQL 都不用写
# ============================================================

print("\n=== 1. 新增（Create） ===")

# 之前：cur.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("张三", 20))
# 现在：直接创建 Python 对象
s1 = Student(name="张三", age=20)
s2 = Student(name="李四", age=21)
s3 = Student(name="王五", age=19)

session.add(s1)       # 逐个添加
session.add_all([s2, s3])  # 批量添加
session.commit()      # 提交！数据真正写入数据库

print("三个学生已添加")

# ============================================================
# 第七步：查询（Read）
# ============================================================

print("\n=== 2. 查询全部 ===")
# 之前：cur.execute("SELECT * FROM students")
# 现在：session.query(Student).all()
all_students = session.query(Student).all()
for s in all_students:
    print(f"  {s.id}: {s.name}, {s.age}岁")  # 直接 .name ！不用 row[1]！

print("\n=== 3. 条件查询 ===")
# 之前：cur.execute("SELECT * FROM students WHERE age >= ?", (20,))
# 现在：用 .filter()
adults = session.query(Student).filter(Student.age >= 20).all()
for s in adults:
    print(f"  {s.name} >= 20岁")

print("\n=== 4. 按主键查 ===")
# 之前：cur.execute("SELECT * FROM students WHERE id = ?", (1,))
# 现在：session.get(Student, 1)
student = session.get(Student, 1)
if student:
    print(f"  找到：{student.name}, {student.age}岁")
else:
    print("  没找到 id=1 的学生")

# ============================================================
# 第八步：更新（Update）
# ============================================================

print("\n=== 5. 更新 ===")
# 之前：cur.execute("UPDATE students SET age = ? WHERE id = ?", (22, 1))
# 现在：直接修改属性，然后 commit
student = session.get(Student, 1)
if student:
    student.age = 22          # 就这一行！
    session.commit()          # 提交
    print(f"  张三的年龄改为 {student.age}")

# ============================================================
# 第九步：删除（Delete）
# ============================================================

print("\n=== 6. 删除 ===")
# 之前：cur.execute("DELETE FROM students WHERE id = ?", (3,))
# 现在：
student = session.get(Student, 3)
if student:
    session.delete(student)
    session.commit()
    print("  王五被删除了")

# ============================================================
# 第十步：验证最终结果
# ============================================================

print("\n=== 最终数据库内容 ===")
for s in session.query(Student).all():
    print(f"  {s}")

# 用完关闭
session.close()
print("\n[OK] Day4 完成：SQLAlchemy ORM 入门")
