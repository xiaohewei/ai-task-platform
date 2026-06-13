from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import DeclarativeBase, Session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

# 密码加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#写数据库引擎
engine = create_engine("sqlite:///users.db", echo = True)

#创建一个鸡肋,记得后面加冒号
class Base(DeclarativeBase):
    pass

'''创建用户表,同样是一个类'''
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True)
    hashed_password = Column(String)   

Base.metadata.create_all(engine)

# JWT 配置
SECRET_KEY = "my-secret-key-keep-it-safe"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

def create_token(user: Users) -> str:
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.get(Users, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
class UsersCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: UsersCreate, db=Depends(get_db)):
    # 1. 检查用户名是否已存在
    existing = db.query(Users).filter(Users.username == user.username).first()
    if existing:
        return {"error": "用户名已被注册"}

    # 2. 加密密码
    hashed = pwd_context.hash(user.password)

    # 3. 创建用户对象
    new_user = Users(username=user.username, hashed_password=hashed)

    # 4. 存进数据库
    db.add(new_user)
    db.commit()

    return {"message": "注册成功", "username": new_user.username}    
@app.post("/login")
async def login(user: UsersCreate, db=Depends(get_db)):
    # 1. 查用户
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if not db_user:
        return {"error": "用户名或密码错误"}

    # 2. 验证密码
    if not pwd_context.verify(user.password, db_user.hashed_password):
        return {"error": "用户名或密码错误"}

    # 3. 生成令牌
    token = create_token(db_user)

    return {"access_token": token, "token_type": "bearer"}

# ============================================================
# 受保护的路由：必须登录才能访问
# ============================================================
@app.get("/me")
async def whoami(user: Users = Depends(get_current_user)):
    return {"id": user.id, "username": user.username}

        




