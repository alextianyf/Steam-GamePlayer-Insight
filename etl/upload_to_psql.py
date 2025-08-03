import pandas as pd
from sqlalchemy import create_engine

# 配置数据库连接信息
DB_USER = "alextian"
DB_PASS = "alextian"
DB_NAME = "steamdb"
DB_HOST = "localhost"
DB_PORT = "5432"

# 建立连接
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 要上传的文件及其对应的目标表名
CSV_TABLE_MAP = {
    "../data/raw/7dtd_players.csv": "players_7dtd",
    "../data/raw/7dtd_achievement_schema.csv": "achievement_schema_7dtd"
}

for csv_path, table_name in CSV_TABLE_MAP.items():
    print(f"[INFO] Uploading {csv_path} to table `{table_name}`")
    df = pd.read_csv(csv_path)

    # 上传至数据库
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"[DONE] {table_name} uploaded successfully.")
