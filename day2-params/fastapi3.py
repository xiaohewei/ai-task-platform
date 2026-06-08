from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


# ============================================================
# Pydantic 模型 —— 数据的"模具"，定义新增设计师需要哪些字段
# ============================================================
class DesignerCreate(BaseModel):
    name: str
    age: int
    respon: str


# ============================================================
# 设计师数据库（列表）
# ============================================================
designer_database = [
    {"id": 1, "name": "筱柇薇", "respon": "主策划，代码，剧本"},
    {"id": 2, "name": "高志",   "respon": "副策划，代码，运维"},
    {"id": 3, "name": "吴地区", "respon": "音乐,bgm,音效"},
    {"id": 4, "name": "郑义航", "respon": "程序，代码，素材生成"},
    {"id": 5, "name": "龚天成", "respon": "测试"},
]


# ============================================================
# 接口3：POST —— 新增一个设计师
# ============================================================
@app.post("/designers")
async def create_designer(new_designer: DesignerCreate):
    # 第一步：Pydantic 对象 → 普通字典
    designer_dict = new_designer.model_dump()

    # 第二步：生成新 id（找出当前最大 id，+1）
    new_id = max(d["id"] for d in designer_database) + 1 if designer_database else 1

    # 第三步：补上 id，追加到数据库
    designer_dict["id"] = new_id
    designer_database.append(designer_dict)

    # 第四步：返回创建结果
    return {"message": "创建成功！", "id": new_id, "信息": designer_dict}


# ============================================================
# 接口1：路径参数 —— 按 id 找具体某个人
# ============================================================
@app.get("/designers/{designer_id}")
async def get_designer(designer_id: int):
    for d in designer_database:
        if d["id"] == designer_id:
            return {"id": designer_id, "信息": d}
    return {"error": f"找不到id为{designer_id}的设计师"}


# ============================================================
# 接口2：查询参数 —— 按职责筛选一批人
# ============================================================
@app.get("/designers")
async def list_designers(respon: str | None = None):
    if respon is None:
        return {"count": len(designer_database), "designers": designer_database}

    result = []
    for d in designer_database:
        if respon in d["respon"]:
            result.append(d)

    return {"count": len(result), "designers": result}


# ============================================================
# 启动入口 —— 让这个文件可以右键直接运行
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi3:app", host="127.0.0.1", port=8001, reload=True)
