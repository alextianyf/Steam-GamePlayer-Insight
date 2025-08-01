import pandas as pd

csv_path = "../data/players/amended_first_200k_players.csv"
output_path = "../user_ids.txt"

# 读取 CSV，忽略 dtype 警告
df = pd.read_csv(csv_path, low_memory=False)

# 使用 'Player Id' 列
id_col = "Player Id"

# 提取前 300 位玩家 ID（根据你需要的数量修改）
sample_ids = df[id_col].dropna().astype(str).head(1000)

# 写入 user_ids.txt，每行一个 ID
with open(output_path, "w") as f:
    for sid in sample_ids:
        f.write(f"{sid}\n")

print(f"✅ 成功写入 {len(sample_ids)} 个用户 ID 至 {output_path}")
