import pandas as pd
import os
import zipfile

# Paths
zip_path = "../data/players/amended_first_200k_players.zip"
extracted_csv_path = "../data/players/amended_first_200k_players.csv"
output_path = "../data/intermediate/user_ids.txt"  

NUM_OF_IDS = 1000

# Ensure intermediate output folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Unzip if CSV does not exist yet
if not os.path.exists(extracted_csv_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(extracted_csv_path))
    print(f"Extracted CSV to {extracted_csv_path}")

# Read CSV
df = pd.read_csv(extracted_csv_path, low_memory=False)
print(f"amended_first_200k_players has feature: {df.columns}")

# Extract the 'Player Id' column
id_col = "Player Id"
player_ids = df[id_col].dropna().astype(str)

# Filter: Keep only numeric IDs
# This raw USER ID list may contain user IDs with limited API access or low activity(special Japanese character etc...); we will filter them before feature extraction.
numeric_ids = player_ids[player_ids.str.isnumeric()]

# Select top N IDs (adjust as needed)
sample_ids = numeric_ids.head(NUM_OF_IDS)

# Write to user_ids.txt
with open(output_path, "w") as f:
    for sid in sample_ids:
        f.write(f"{sid}\n")

print(f"Successfully wrote {len(sample_ids)} user IDs to {output_path}")
