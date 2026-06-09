"""
main.py —— 项目入口
====================
只做三件事：
1. 创建 FastAPI 应用
2. 挂载路由
3. 启动时自动建表

就这几行，都在这了。
"""

from fastapi import FastAPI
from app.db import engine, Base
from app.api import router

# 创建应用
app = FastAPI(title="Day5 — 标准项目结构")

# 挂载路由（所有 /students 开头的接口都在 api.py 里）
app.include_router(router)

# 启动时自动建表（表不存在才建，不会覆盖数据）
Base.metadata.create_all(bind=engine)
print("数据库就绪")


# 运行方式：
#   cd day5-migration
#   uvicorn main:app --reload --port 8003
#   浏览器打开 http://127.0.0.1:8003/docs
