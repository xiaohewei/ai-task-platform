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

## Day 4 — 2026-06-08：SQLAlchemy ORM 入门

### 学了什么

| 知识点 | 说明 |
|--------|------|
| 什么是 ORM | 用 Python 类代替 SQL 语句操作数据库，不用手写 INSERT/SELECT |
| Engine | `create_engine("sqlite:///xxx.db")` — 数据库引擎，负责跟数据库文件通信 |
| DeclarativeBase | 所有 ORM 模型的基类，`class Base(DeclarativeBase): pass` |
| Column | 定义数据库列：`name = Column(String)`、`age = Column(Integer)` |
| primary_key | 主键，唯一标识一行 |
| `__tablename__` | 指定对应的数据库表名（前后各两个下划线） |
| `Base.metadata.create_all(engine)` | 把所有继承 Base 的模型在数据库里建表 |
| Session | 数据库会话，增删改查的中间人：`db.add()`、`db.delete()`、`db.query()`、`db.commit()` |
| `unique=True` | 列约束，不允许重复值 |

### 核心概念——老师讲过的三个对应关系

```
1 个 Engine    →  1 个数据库文件
1 个 Base      →  1 组表模型
1 个 Session   →  1 次数据库对话
```

### 代码文件

- [main.py](days/day4-orm/main.py) — ORM CRUD 完整示例

### 运行方式

```bash
cd days/day4-orm/
python main.py
```

### 踩坑

- ⚠️ **`__tablename__` 是双下划线**：前后各两个，写成单下划线 SQLAlchemy 不认识
- ⚠️ **忘记 `db.commit()`**：增删改之后不 commit 等于白做，数据不会写入磁盘

### 解决了的疑惑

- [x] ORM 和原始 SQL 有什么区别？—— ORM 让你用 Python 对象操作数据库，不用拼 SQL 字符串。速度稍慢但开发效率高很多
- [x] `DeclarativeBase` 是什么？—— SQLAlchemy 2.0 的新写法，统一的基类声明方式

---

## Day 5 — 2026-06-10：FastAPI + ORM 集成

### 学了什么

| 知识点 | 说明 |
|--------|------|
| `Depends` | FastAPI 依赖注入，自动给函数参数赋值 |
| `get_db()` + `yield` | 数据库连接管理：进来开工，`yield` 交出连接，用完自动关 |
| `finally: db.close()` | 保证无论成功还是报错，连接一定会关闭 |
| Pydantic 请求模型 | `StudentCreate` 定义 POST body 格式，`StudentUpdate` 用 `str \| None = None` 表示可选 |
| ORM 增删改查 | `db.add()` + `db.commit()`（增）、`db.query().all()`（查全部）、`db.get(Student, id)`（查一个）、`db.delete()`（删） |
| 部分更新 | 只改用户填了的字段：`if data.name is not None: obj.name = data.name` |

### 代码文件

- [main.py](days/day5-fastapi-orm/main.py) — FastAPI + ORM 完整 CRUD API

### 运行方式

```bash
cd days/day5-fastapi-orm/
uvicorn main:app --reload --port 8002
# 浏览器打开 http://127.0.0.1:8002/docs
```

### 踩坑

- ⚠️ **依赖注入参数位置**：`Depends(get_db)` 必须放在函数参数里，FastAPI 会自动处理
- ⚠️ **`query(Student)` 只按主键查**：按主键用 `db.get()`，按其他字段用 `db.query().filter()`

### 解决了的疑惑

- [x] 为什么不用手动 `conn.close()` 了？—— `yield` + `finally` 保证了自动关闭，比 Day 1-3 的原始 SQL 方式安全
- [x] `StudentUpdate` 为什么要每个字段都 `None`？—— 让前端可以只传想改的字段，没传的不动

---

## Day 5-alt — 2026-06-11：数据库迁移 + 标准项目结构

### 学了什么

| 知识点 | 说明 |
|--------|------|
| 数据库迁移概念 | 旧表 → 备份 → 建新表 → 迁移数据 → 切换，四个步骤 |
| 标准项目结构 | `app/db.py`（数据库）、`app/models.py`（ORM 模型）、`app/schemas.py`（Pydantic 模型）、`app/api.py`（路由）、`main.py`（入口） |
| `sessionmaker` | 比直接 `Session(engine)` 更优雅的会话管理方式 |
| `APIRouter` | 把路由拆分到独立文件，再 `app.include_router()` 组装 |
| `response_model` | 声明接口返回的数据结构，FastAPI 自动过滤多余字段 |
| `from_attributes = True` | 让 Pydantic 能从 ORM 对象自动提取字段（替代旧版的 `orm_mode`） |
| `db.refresh()` | 提交后刷新对象，获取数据库自动生成的值（如 id、默认值） |

### 代码文件

- [01_what_is_migration.py](days/day5-migration/01_what_is_migration.py) — 迁移概念演示
- [main.py](days/day5-migration/main.py) — 入口文件
- [app/db.py](days/day5-migration/app/db.py) — 数据库配置 + get_db
- [app/models.py](days/day5-migration/app/models.py) — ORM 模型
- [app/schemas.py](days/day5-migration/app/schemas.py) — Pydantic 模型
- [app/api.py](days/day5-migration/app/api.py) — 路由

### 运行方式

```bash
cd days/day5-migration/
uvicorn main:app --reload --port 8003
```

### 踩坑

- ⚠️ **文件名不要用 `fastapi.py`**：会跟 `pip` 安装的 FastAPI 库冲突，导致 `ImportError`
- ⚠️ **目录里要有 `__init__.py`**：Python 才能把文件夹当作模块导入

---

## Day 6 — 2026-06-13：JWT 用户认证

### 学了什么

| 知识点 | 说明 |
|--------|------|
| JWT 概念 | JSON Web Token，登录后发的"令牌手环"，之后请求带着它证明身份 |
| 密码加密 | 用 `passlib` + `bcrypt` 把密码变成不可逆乱码再存，数据库被偷也看不到原密码 |
| `pwd_context.hash()` | 加密密码 |
| `pwd_context.verify()` | 验证密码（比对乱码是否一致） |
| JWT 结构 | payload（载荷：user_id + 过期时间）+ 签名（防伪造） |
| `jwt.encode()` | 生成令牌 |
| `jwt.decode()` | 解码验令牌 |
| `OAuth2PasswordBearer` | 告诉 FastAPI 从请求头 `Authorization: Bearer <token>` 取令牌 |
| `get_current_user` | 保护路由的依赖——验不过直接返回 401，验过了返回用户对象 |
| `HTTPException(401)` | 未授权时的标准响应 |

### 完整流程

```
注册 POST /register → 用户名+密码 → 加密存储
  ↓
登录 POST /login → 验证密码 → 返回 JWT 令牌
  ↓
访问 GET /me → 带令牌 → 解码验证 → 返回用户信息
```

### 代码文件

- [main.py](days/day6-auth/main.py) — 注册 / 登录 / 令牌 / 保护路由

### 运行方式

```bash
cd days/day6-auth/
uvicorn main:app --reload --port 8004
# 浏览器打开 http://127.0.0.1:8004/docs
```

### 踩坑

- ⚠️ **`UsersCreate` vs `UserCreate` 命名要一致**：类名和函数参数类型名必须一字不差，否则 `NameError`
- ⚠️ **`username` 不要写成 `usersname`**：多一个 s 就会字段对不上
- ⚠️ **`__tablename__` 是双下划线**：Day 4 的坑，Day 6 又踩了一次

### 解决了的疑惑

- [x] JWT 令牌为什么安全？—— 有密钥签名，别人改不了里面的内容。过了过期时间自动失效
- [x] 为什么登录和注册用同一个 Pydantic 模型？—— 字段一样（username + password），可以复用
- [x] `/docs` 页面怎么测试带令牌的接口？—— 点右上角 Authorize 按钮，粘贴 token，之后所有请求自动带令牌

---

## 学习进度

```
Day 1  ████████░░  Hello World + SQLite
Day 2  ██████░░░░  路径参数 / 查询参数 / POST
Day 3  ██████░░░░  FastAPI + SQLite 联调 CRUD
Day 4  ██████░░░░  SQLAlchemy ORM
Day 5  ██████░░░░  FastAPI + ORM 集成
Day 6  ██████░░░░  JWT 用户认证
```

---

> 📝 **给自己**: 坚持每天学一个概念 + 写一段代码 + 记一条日志。
> 一个月后回头看，你会感谢现在的自己。

*最后更新：2026-06-13*
