import os
import csv
import psycopg2
from psycopg2.extras import execute_values

# ✅ 数据库连接配置
DB_PARAMS = {
    "dbname": "steamdb",
    "user": "alextian",
    "password": "alextian",
    "host": "localhost",
    "port": 5432
}

# ✅ 原始数据文件夹
RAW_DATA_DIR = "../data/raw"

def upload_user_games(conn):
    print("📥 上传用户游戏数据 user_game ...")
    rows = []
    for file in os.listdir(RAW_DATA_DIR):
        if file.endswith("_games.csv"):
            user_id = file.split("_")[0]
            path = os.path.join(RAW_DATA_DIR, file)
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append((
                        int(user_id),
                        int(row["appid"]),
                        float(row["playtime_hours"])
                    ))

    with conn.cursor() as cur:
        execute_values(cur,
            """INSERT INTO user_game (user_id, game_id, total_playtime)
               VALUES %s
               ON CONFLICT (user_id, game_id) DO NOTHING""",
            rows
        )
        conn.commit()
    print("✅ 上传完成 user_game")

def upload_achievements(conn):
    print("📥 上传成就数据 achievements ...")
    rows = []
    for file in os.listdir(RAW_DATA_DIR):
        if file.endswith("_achievements.csv"):
            try:
                # 解析 appid 和 game_name
                appid, *game_name_parts = file.replace("_achievements.csv", "").split("_")
                game_name = " ".join(game_name_parts)
                game_id = int(appid)
            except Exception:
                print(f"⚠️ 文件名解析失败：{file}，跳过。")
                continue

            # 找到匹配 user_id（从 game 文件中推断）
            user_id = None
            for filename in os.listdir(RAW_DATA_DIR):
                if filename.endswith("_games.csv"):
                    path = os.path.join(RAW_DATA_DIR, filename)
                    with open(path, encoding="utf-8") as f:
                        if str(game_id) in f.read():
                            user_id = filename.split("_")[0]
                            break
            if user_id is None:
                continue

            # 读取成就内容
            path = os.path.join(RAW_DATA_DIR, file)
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append((
                        int(user_id),
                        int(game_id),
                        row["apiname"],  # ⚠️ 字段名必须是 apiname
                        bool(int(row["achieved"])),
                        int(row["unlock_time"]) if row["unlock_time"] else None
                    ))

    with conn.cursor() as cur:
        execute_values(cur,
            """INSERT INTO achievements (user_id, game_id, apiname, achieved, unlock_time)
               VALUES %s
               ON CONFLICT DO NOTHING""",
            rows
        )
        conn.commit()
    print("✅ 上传完成 achievements")

def main():
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        upload_user_games(conn)
        upload_achievements(conn)
    finally:
        conn.close()
        print("📁 数据库连接已关闭")

if __name__ == "__main__":
    main()
