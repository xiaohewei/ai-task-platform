"""
AI 辅助个人任务管理平台 — 后端
FastAPI + SQLAlchemy + JWT + SQLite
部署：Render 免费托管，GitHub Push 自动部署
"""
import os
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import jwt
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship

# ============================================================
# 配置
# ============================================================
SECRET_KEY = "task-manager-secret-2026"
ALGORITHM = "HS256"
EXPIRE_HOURS = 24
engine = create_engine("sqlite:///taskmanager.db", echo=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class Base(DeclarativeBase):
    pass


# ============================================================
# 模型
# ============================================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    priority = Column(String, default="中")  # 高 / 中 / 低
    status = Column(String, default="待办")  # 待办 / 进行中 / 已完成
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")


Base.metadata.create_all(engine)

# ============================================================
# FastAPI
# ============================================================
app = FastAPI(title="AI 任务管理平台")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def create_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


# ============================================================
# Pydantic 模型
# ============================================================
class UserCreate(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "中"


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None


# ============================================================
# 认证接口
# ============================================================
@app.post("/api/register")
async def register(user: UserCreate, db=Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    hashed = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "注册成功"}


@app.post("/api/login")
async def login(user: UserCreate, db=Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token(db_user)
    return {"access_token": token, "token_type": "bearer", "username": db_user.username}


@app.get("/api/me")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "username": user.username}


# ============================================================
# 任务 CRUD
# ============================================================
@app.get("/api/tasks")
async def list_tasks(
    status_filter: str | None = None,
    priority_filter: str | None = None,
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    q = db.query(Task).filter(Task.user_id == user.id)
    if status_filter:
        q = q.filter(Task.status == status_filter)
    if priority_filter:
        q = q.filter(Task.priority == priority_filter)
    tasks = q.order_by(Task.created_at.desc()).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "status": t.status,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for t in tasks
    ]


@app.post("/api/tasks")
async def create_task(task: TaskCreate, user: User = Depends(get_current_user), db=Depends(get_db)):
    t = Task(title=task.title, description=task.description, priority=task.priority, user_id=user.id)
    db.add(t)
    db.commit()
    return {"message": "创建成功", "id": t.id}


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, data: TaskUpdate, user: User = Depends(get_current_user), db=Depends(get_db)):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")
    if data.title is not None:
        t.title = data.title
    if data.description is not None:
        t.description = data.description
    if data.priority is not None:
        t.priority = data.priority
    if data.status is not None:
        t.status = data.status
    db.commit()
    return {"message": "更新成功"}


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, user: User = Depends(get_current_user), db=Depends(get_db)):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")
    db.delete(t)
    db.commit()
    return {"message": "删除成功"}


# ============================================================
# 前端页面
# ============================================================
@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/app")
async def app_page():
    return FileResponse("static/app.html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
