import pandas as pd
import os
import zipfile

# Paths
zip_path = "../data/players/amended_first_200k_players.zip"
extracted_csv_path = "../data/players/amended_first_200k_players.csv"
output_path = "../data/intermediate/user_ids.txt"

# Ensure intermediate output folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Unzip if CSV does not exist yet
if not os.path.exists(extracted_csv_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(extracted_csv_path))
    print(f"📂 Extracted CSV to {extracted_csv_path}")

# Read CSV
df = pd.read_csv(extracted_csv_path, low_memory=False)

# Use 'Player Id' column
id_col = "Player Id"
sample_ids = df[id_col].dropna().astype(str).head(1000)

# Write to user_ids.txt
with open(output_path, "w") as f:
    for sid in sample_ids:
        f.write(f"{sid}\n")

print(f"✅ Successfully wrote {len(sample_ids)} user IDs to {output_path}")
