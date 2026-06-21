from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="何伟 — 个人主页")

# 静态文件（CSS、图片等）
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home():
    return FileResponse("index.html")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
