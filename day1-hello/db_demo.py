import sqlite3

conn = sqlite3.connect("test.db")

print("创建成功了喵")

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS student")


cur.execute("""
    CREATE TABLE IF NOT EXISTS student(
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
    )
""")
print("表创建好了！")

cur.execute("""
    INSERT INTO student (id, name, age)
    VALUES (1, '张三', 20)
""")
conn.commit()
print("插入了一个学生！")

# 5. 查询数据
cur.execute("SELECT * FROM student")
result = cur.fetchall()
print("查询结果：", result)

# 6. 更新数据
cur.execute("""
    UPDATE student
    SET age = 21
    WHERE name = '张三'
""")
conn.commit()

# 再查一次确认
cur.execute("SELECT * FROM student")
print("更新后：", cur.fetchall())

cur.execute("""
    DELETE FROM student
    WHERE name = '张三'
""")
conn.commit()

# 再查一次确认
cur.execute("SELECT * FROM student")
print("删除后：", cur.fetchall())

# 用完关闭连接
conn.close()
