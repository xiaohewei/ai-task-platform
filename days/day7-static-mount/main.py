"""
Day 7 — 静态文件 / 文件下载 / 子应用挂载

三大知识点：
1. 静态文件：让 FastAPI 直接返回图片、CSS、JS 等文件
2. 文件下载：用 FileResponse 让用户下载文件
3. 子应用挂载：把多个 FastAPI 应用拼在一起，前缀自动裁剪
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# ============================================================
# 一、主应用
# ============================================================
app = FastAPI(title="Day7 — 静态文件与子应用")


@app.get("/")
async def home():
    return {"message": "首页"}


@app.get("/hello")
async def hello():
    return {"hello": "world"}


# ============================================================
# 二、文件下载（FileResponse）
# ============================================================
@app.get("/download")
async def download():
    """访问 /download 下载 report.txt 文件"""
    return FileResponse(
        "files/report.txt",
        filename="我的报告.txt",   # 下载时浏览器显示的文件名
        media_type="text/plain",
    )


# ============================================================
# 三、子应用（admin_app）
# ============================================================
admin_app = FastAPI(title="Admin 管理后台")


@admin_app.get("/")
async def admin_home():
    return {"data": "管理后台首页"}


@admin_app.get("/logs")
async def admin_logs():
    return {"data": "操作日志"}


# ============================================================
# 四、孙子应用（grand_son_app）
# ============================================================
grand_son_app = FastAPI()


@grand_son_app.get("/deep")
async def deep_route():
    return {"data": "这是三层嵌套的最深处！"}


# ============================================================
# 挂载关系（先挂载低层，再挂载高层）
# 实际 URL 对照：
#   /admin                → admin_app 的 "/"
#   /admin/logs           → admin_app 的 "/logs"
#   /admin/sub/deep       → grand_son_app 的 "/deep"
#   /static/logo.png      → static/ 目录下的文件
# ============================================================

# 孙子 → 挂到儿子上
admin_app.mount("/sub", grand_son_app)

# 儿子 → 挂到主应用上（grand_son_app 的前缀变成 /admin/sub）
app.mount("/admin", admin_app)

# 静态文件 → 挂到主应用上
app.mount("/static", StaticFiles(directory="static"), name="static")
