# 🔄 ETL Pipeline — Steam Game Player Insight

This ETL pipeline is the first step in a larger project to analyze and model player behavior in Steam games using public and semi-public data.

---

## 🎯 Project Objectives

This project focuses on three main objectives:

1. **🧑‍💻 Player Insight**  
   Understand what kinds of players exist (e.g. achievers, explorers, casuals) by analyzing game ownership, playtime, and achievement profiles.

2. **🏆 Achievement Prediction**  
   Given a user’s gameplay history, can we predict which achievements they’re likely to unlock next?

3. **📈 Retention Modeling**  
   Estimate which factors contribute to whether a player continues playing a game or churns early.

---

## 📦 Data Sources

### 1. **Kaggle Dataset: Achievement Rankings**
We began with:

**[📎 Steam Achievement Stats Ranking (Kaggle)](https://www.kaggle.com/datasets/patrickgendotti/steam-achievementstatscom-rankings)**

- Contains over **200,000+ Steam players**, ranked by number of achievements.
- Our source file:
  ```text
  📄 data/players/amended_first_200k_players.csv
  ```
- From this we extracted SteamIDs of players with public profiles.

## 🏗️ Execution Pipeline (Extract)

### ✅ Step 1: Extract User IDs

```bash
python3 etl/extract_user_ids_from_csv.py
```

- Parses the Kaggle file: [`players/amended_first_200k.csv`](https://www.kaggle.com/datasets/patrickgendotti/steam-achievementstatscom-rankings)
- Filters out:
  - Invalid Steam IDs
  - Users with private profiles (which cause API errors)
- Saves valid public user IDs to: `user_ids.txt`

---

### ✅ Step 2: Fetch Game & Achievement Data

```bash
python3 etl/fetch_user_from_list.py
```

- For each user ID:
  - Calls Steam API:
    - `GetOwnedGames` → retrieves game list and playtime
    - `GetPlayerAchievements` → retrieves game-specific achievements
- Saves outputs to:
  ```
  📄 data/raw/{USER_ID}_games.csv
  📄 data/raw/{APPID}_{GAME_NAME}_achievements.csv
  ```

---

### ✅ Step 3: Upload Extracted Data to PostgreSQL

```bash
python3 etl/upload_to_pstgres.py
```

- Tables created:
  - `user_game(user_id, game_id, total_playtime)`
  - `achievements(user_id, game_id, apiname, achieved, unlock_time)`
- Insert method:
  - Efficient batch upload via `execute_values`
  - Duplicate records are skipped using `ON CONFLICT DO NOTHING`
- You can inspect the tables in pgAdmin after upload.

---

## 🧩 Major Challenges During Extract Phase

| Challenge | Description | Resolution |
|----------|-------------|------------|
| 🎯 Identifying High-Quality Users | Most randomly queried Steam users had no achievements or very sparse data, making them unsuitable for analysis | Used Kaggle dataset (`amended_first_200k.csv`) to locate active players, then manually filtered by profile visibility |
| 🔐 Private Profiles | Many user profiles from Kaggle were private or restricted, resulting in API failure | Filtered out dynamically during `GetOwnedGames` and `GetPlayerAchievements` calls |
| 🚫 Limited API Scope | Steam’s public API only exposes a few player-level features (e.g. playtime, achievements) | Narrowed project focus to only analyze those available features |
| 🔍 Validating User IDs | Kaggle dataset didn’t guarantee validity or accessibility of user IDs | Wrote scripts to validate each ID and skip unusable users |
| 📂 Filename Issues | Achievement data was saved as `{appid}_{game_name}_achievements.csv`, but many game names contained special characters or inconsistent formatting | Parsing logic was updated to extract only appid and sanitize file naming |
| ❗ Duplicate Data | When rerunning the data extraction and upload scripts, duplicate rows caused primary key violations in PostgreSQL | Added `ON CONFLICT DO NOTHING` to the insert logic to ensure idempotent uploads |
| 🧱 Schema Mismatches | Column mismatches (e.g., `api_name` vs `apiname`) caused PostgreSQL errors during insertions | Resolved by strictly aligning SQL schema and Python insert columns |

