"""
app/db.py —— 数据库层
======================
这个文件只管一件事：连接数据库。

其他文件（api.py、models.py）需要数据库时，从这里拿。
不用自己重复写 create_engine。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 数据库文件路径
SQLALCHEMY_DATABASE_URL = "sqlite:///school.db"

# 引擎——所有数据库操作都通过它
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Session 工厂——不是单个 session，而是"生产线"
# 每个请求来了就生产一个新的 session 实例
SessionLocal = sessionmaker(bind=engine)


# 基类——所有模型都继承它
class Base(DeclarativeBase):
    pass


# 快捷方法：拿一个 session（用完要关掉）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
