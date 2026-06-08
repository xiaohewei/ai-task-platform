# FastAPI 学习日志

> 💡 **为什么要写学习日志？**
> 学过的内容如果不记录，一个月后全忘了。这个日志就是你自己的"知识银行"——
> 每学一天，存一笔；以后忘了随时回来取。

---

## Day 1 — 2026-06-05：Hello World + SQLite CRUD

### 学了什么

| 知识点 | 说明 |
|--------|------|
| FastAPI 最小应用 | `FastAPI()` 创建 app，`@app.get()` 装饰器绑定路由 |
| 异步处理 | `async def` 让 FastAPI 能同时处理多个请求 |
| SQLite 建表 | `CREATE TABLE IF NOT EXISTS` |
| CRUD 四操作 | INSERT / SELECT / UPDATE / DELETE |
| 提交事务 | `conn.commit()` —— 忘了数据不保存！ |
| 参数化查询 | 用 `?` 占位符防 SQL 注入 |

### 代码文件

- [fastapi1.py](fastapi1.py) — 第一个 FastAPI 应用（两个路由）
- [db_demo.py](db_demo.py) — SQLite 增删改查全流程

### 运行方式

```bash
uvicorn fastapi1:app --reload
python db_demo.py
```

### 踩坑

- ⚠️ **SQLite 记得 commit**：不 commit 数据不会写入磁盘
- ⚠️ **关闭连接**：用完 `conn.close()` 避免资源泄露

---

## Day 2 — 2026-06-06：路径参数

### 学了什么

| 知识点 | 说明 |
|--------|------|
| 路径参数 | URL 里 `{变量名}` 不是固定字符串，是变量 |
| 类型转换 | `student_id: int` → FastAPI 自动把 "1" 转成 1 |
| 数据校验 | 传 `abc` 到 int 参数 → 自动返回 422 错误 |
| 字典查表 | 用 `in` 判断 key 是否存在，做简单"数据库" |

### 代码文件

- [fastapi2.py](fastapi2.py) — 路径参数 + 假数据库查询

### 运行方式

```bash
uvicorn fastapi2:app --reload
# 访问 http://127.0.0.1:8000/students/1
# 访问 http://127.0.0.1:8000/students/999  (看报错处理)
```

### 解决了的疑惑

- [x] Pydantic 模型是什么？跟 dict 有什么区别？—— Pydantic 是数据的"模具"，定义字段 + 类型，FastAPI 用它自动校验。dict 只是存数据用的
- [x] 查询参数和路径参数什么时候用哪个？—— 路径参数定位资源（/students/1），查询参数筛选/搜索（?respon=代码）

### 仍不理解

- [ ] `str | None = None` 这语法什么意思？（留到 Day 4）

---

## Day 3 — 2026-06-07：FastAPI + SQLite 完整 CRUD API

### 学了什么

| 知识点 | 说明 |
|--------|------|
| 接口 + 数据库联通 | 前端发请求 → FastAPI → SQL → 数据库 → 返回 |
| AUTOINCREMENT | 数据库自动编号，不用手动指定 id |
| `?` 占位符 | 防 SQL 注入，不直接拼字符串 |
| `cur.lastrowid` | 插入后拿回数据库自动生成的 id |
| Pydantic 可选字段 | `str \| None = None` 表示可以不填 |
| HTTP 方法 | POST(增)、GET(查)、PUT(改)、DELETE(删) |
| `/docs` 测试页面 | FastAPI 自动生成的接口调试工具 |
| NOT NULL | 数据库列的约束，不允许空值 |

### 代码文件

- [fastapi4.py](fastapi4.py) — 完整的学生管理 API（5 个接口 + SQLite）

### 运行方式

```bash
uvicorn FastAPI.fastapi4:app --reload --port 8002
# 浏览器打开 http://127.0.0.1:8002/docs
```

### 踩坑

- ⚠️ **多终端残留**：两个 uvicorn 同时跑在 8000 端口，浏览器访问到旧的。杀进程 `taskkill /F /IM python.exe`
- ⚠️ **拼写错误**：`BaseModel` 写成 `BaseMode1`（数字1），`TRXT` 写成 `TEXT`，编辑器有红色波浪线要注意看

---

## 学习进度

```
Day 1  ████████░░  Hello World + SQLite
Day 2  ██████░░░░  路径参数 / 查询参数 / POST
Day 3  ██████░░░░  FastAPI + SQLite 联调 CRUD
```

---

> 📝 **给自己**: 坚持每天学一个概念 + 写一段代码 + 记一条日志。
> 一个月后回头看，你会感谢现在的自己。

*最后更新：2026-06-07*
