"""
Day5 — 数据库迁移 & 项目结构拆分
=======================================

今天两个目标：
1. 理解"迁移"是什么（手工模拟）
2. 把代码拆成 FastAPI 标准目录结构
"""

import sqlite3
import os

# ============================================================
# 核心问题：表结构会变
# ============================================================

print("""
=== 场景 ===

6月5号，你定义了一个 players 表：
  players(id, name)

6月9号，想加一个新字段：gold（金币）
  players(id, name, gold)

如果你直接改代码 → 旧数据库没 gold 列 → 程序崩溃！

100条玩家数据还在旧表里，不能丢。
这就是"迁移"要解决的问题。
""")

# ============================================================
# 演示
# ============================================================

DB = "game.db"
if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
cur = conn.cursor()
print("=== 6月5号：建旧表 ===")

# 旧版本的表结构——只有 id 和 name
cur.execute("""
    CREATE TABLE players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
""")

# 加两条玩家数据
cur.execute("INSERT INTO players (name) VALUES ('张三')")
cur.execute("INSERT INTO players (name) VALUES ('李四')")
conn.commit()

print("旧表数据：")
cur.execute("SELECT * FROM players")
for row in cur.fetchall():
    print(f"  id={row[0]}, name={row[1]}")

# ============================================================
# 模拟迁移：加 gold 和 level 字段
# ============================================================

print("\n=== 6月9号：迁移（加 gold 和 level 字段） ===")

# 步骤1：备份旧数据
cur.execute("SELECT id, name FROM players")
old_data = cur.fetchall()
print(f"1. 备份了 {len(old_data)} 条数据")

# 步骤2：建新表（新结构）
cur.execute("""
    CREATE TABLE players_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gold INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    )
""")
print("2. 新表建好（有 gold, level）")

# 步骤3：把旧数据搬过去
for row in old_data:
    cur.execute(
        "INSERT INTO players_new (id, name) VALUES (?, ?)",
        (row[0], row[1])
    )
print(f"3. {len(old_data)} 条数据搬移完成（gold 自动补 0，level 自动补 1）")

# 步骤4：切换表
cur.execute("DROP TABLE players")
cur.execute("ALTER TABLE players_new RENAME TO players")
conn.commit()
print("4. 旧表删除，新表改名")

# ============================================================
# 验证
# ============================================================

print("\n=== 迁移完成，新表数据 ===")
cur.execute("SELECT * FROM players")
for row in cur.fetchall():
    print(f"  id={row[0]}, name={row[1]}, gold={row[2]}, level={row[3]}")

conn.close()
os.remove(DB)

print(f"""
{'='*60}
核心理解：

  旧表 players(id, name)
       ↓ 迁移（备份→建新→搬数据→切换）
  新表 players(id, name, gold, level)

  旧数据的 gold 和 level 自动补了默认值。
  100条玩家数据一条没丢，新字段全加上了。

  Alembic 就是把这四步自动化：
  alembic revision → 生成迁移文件 → alembic upgrade → 执行
{'='*60}
""")
