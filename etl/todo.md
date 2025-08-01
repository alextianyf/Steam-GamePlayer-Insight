# Todo List

## 1. 使用 Python 自动执行 SQL 文件

> Note: 我们现在已经手动建立好steamdb了，我们应该让init_db.py自动化这个过程，并且检测是否已经拥有steamdb，如果有的话那就不用创建了。

我们用 psycopg2 或 SQLAlchemy 在 Python 脚本中运行 schema 文件，这样可以自动化整个流程。

安装依赖（如果未装）：
```bash
pip install psycopg2-binary
```

示例代码：etl/init_db.py

```python
import psycopg2

# 替换为你自己的 PostgreSQL 设置
DB_NAME = "steamdb"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = 5432

SCHEMA_PATH = "../sql/schema.sql"  # 相对路径（从 etl/ 运行）

def run_schema():
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ 数据库表结构已成功创建！")

if __name__ == "__main__":
    run_schema()
```

运行方法（从 etl/ 文件夹）：
```bash
python init_db.py
```

## 2. 了解terminal SQL启动过程

步骤目标

1️⃣	启动 PostgreSQL 服务

2️⃣	创建数据库用户（可选）与目标数据库（如 steamdb）

3️⃣	使用 init_db.py 运行你写好的 schema.sql

4️⃣	配置你的项目连接信息

5️⃣	写入数据测试（users.csv）

步骤 1：启动 PostgreSQL 服务

在 macOS 下你安装的是 postgresql@17，所以你要运行：

```bash
brew services start postgresql@17
```

如果你之前没执行过 initdb，你可能需要先运行一次：

```bash
initdb /usr/local/var/postgresql@17
```

## 3. 常用SQL Terminal指令

```bash
brew services start postgresql@17

brew services stop postgresql@17

brew services restart postgresql@17

```

