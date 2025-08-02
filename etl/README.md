# ETL Pipeline — Steam Game Player Insight

This ETL pipeline serves as the foundational phase of a broader data science project that focuses on analyzing and modeling player behavior in Steam games. By leveraging public and semi-public Steam APIs, the pipeline collects structured gameplay data that supports both exploratory insights and predictive modeling.

**ETL** stands for **Extract, Transform, Load** — a common data pipeline process where you:

- **Extract** data from source systems (e.g., Steam APIs),
- **Transform** it into a clean, usable format (e.g., filter, convert timestamps),
- **Load** it into storage or databases for analysis.

This ETL ensures we turn raw player data into structured datasets ready for machine learning and analytics.

---

## Game Selection Rationale

To support a diverse range of player behaviors and game mechanics, the full project will eventually include several games across different genres, chosen based on:

- A large, active player base  
- A rich, structured achievement system  
- Distinct gameplay and progression mechanics  
- Compatibility with Steam's public API format  

However, this repository currently focuses on one title:

### 7 Days to Die

- **Genre**: Open-World Sandbox Survival (Crafting, Exploration, Combat)

- **Why Start Here?**  
  *7 Days to Die* features open-ended survival gameplay and a broad achievement system that reflects various player behaviors — from zombie combat to base-building. It provides strong analytical signals for clustering, prediction, and early-game survival studies.

- **Personal Connection**  
  I’ve followed this game’s development and community for years, and its strategic depth and variety make it a compelling case for player insight research.

- **Analytical Features**  
  The Steam achievement system tracks key behaviors like:
  - Crafting volume (e.g., tools, structures)
  - Combat milestones (e.g., zombie/player kills)
  - Exploration and survival (e.g., distance traveled, longest life lived)

  These data points enable us to:
  - Segment players by in-game behavior  
  - Predict future achievements  
  - Study early factors that influence retention  

---

## ETL Workflow Summary

### Step 1: Extract Player IDs

- Download the base dataset from Kaggle: [Steam Achievement Stats Ranking](https://www.kaggle.com/datasets/patrickgendotti/steam-achievementstatscom-rankings)

- Extracts over 200,000 Steam user IDs ranked by achievement count.

- Cleaned CSV path: `data/players/amended_first_200k_players.csv`

### Step 2: Filter Usable SteamIDs

- Run: `extract_user_ids_from_csv.py`

- Filters for 15,000 users with public profiles

- Removes entries with invalid characters (e.g., non-ASCII usernames)

- Output file: `data/intermediate/user_ids.txt`

### Step 3: Game-Specific Data Extraction

- Run the script `fetch_7DTD_data.py` to collect gameplay data and achievement statistics for *7 Days to Die*.
- The script fetches:
  - Verified player ownership and playtime (must exceed 30 minutes)
  - Achievement unlock status and timestamps (converted to Vancouver time)
  - Global unlock rates for each achievement
- Raw player data and achievement metadata will be saved to the `data/raw/` directory.
- Steam Web API details can be found at [Steam Web API Documentation](https://steamcommunity.com/dev).

As the project expands, similar fetch scripts will be added for other titles (e.g., `fetch_csgo_data.py`, `fetch_l4d2_data.py`) using the same modular ETL structure.

#### Data Collection Tips

- Exclude users with zero playtime in the target game  
- Avoid only sampling "high playtime" users — that introduces bias  
- Be mindful of special characters in game names or paths  
- Define and maintain a consistent output schema  
- Store achievement metadata (e.g., description, unlock rate) separately  

---

## Data Transfer

The ETL step outputs game-specific player data and metadata files:

- Player gameplay data: `data/raw/7dtd_players.csv`
- Achievement schema and global unlock rates: `data/raw/7dtd_achievement_schema.csv`

These outputs form the raw dataset foundation for downstream cleaning, feature engineering, and modeling.

---

## Data Load

At this stage, structured `.csv` outputs are ready to be:

- Loaded into databases or data lakes  
- Used for exploratory data analysis (EDA)  
- Passed to machine learning pipelines for modeling  
- Visualized via dashboards or reports  

### SQL Integration (PostgreSQL Example)

To support flexible queries and structured data modeling, we load the final datasets into a PostgreSQL database using Python (via `pandas` + `SQLAlchemy`).

- Script: `load_to_postgres.py`
- Target Tables:
  - `players_7dtd`: Stores player gameplay records
  - `achievement_schema_7dtd`: Stores achievement metadata with global unlock rates

**Benefits of SQL Layer**:
- Enables fast filtering (e.g., "players who unlocked 10+ combat achievements")
- Supports joins (e.g., combine achievement descriptions with player stats)
- Useful for downstream analytics dashboards or machine learning pipelines

---

## Major Challenges During Extract Phase

| Challenge | Description | Resolution |
|----------|-------------|------------|
| 🎯 Identifying High-Quality Users | Most randomly queried Steam users had no achievements or very sparse data, making them unsuitable for analysis | Used Kaggle dataset (`amended_first_200k.csv`) to locate active players, then manually filtered by profile visibility |
| 🔐 Private Profiles | Many user profiles from Kaggle were private or restricted, resulting in API failure | Filtered out dynamically during `GetOwnedGames` and `GetPlayerAchievements` calls |
| 🚫 Limited API Scope | Steam’s public API only exposes a few player-level features (e.g. playtime, achievements) | Narrowed project focus to only analyze those available features |
| 🔍 Validating User IDs | Kaggle dataset didn’t guarantee validity or accessibility of user IDs | Wrote scripts to validate each ID and skip unusable users |
| 📂 Filename Issues | Achievement data was saved as `{appid}_{game_name}_achievements.csv`, but many game names contained special characters or inconsistent formatting | Parsing logic was updated to extract only appid and sanitize file naming |
| ❗ Duplicate Data | When rerunning the data extraction and upload scripts, duplicate rows caused primary key violations in PostgreSQL | Added `ON CONFLICT DO NOTHING` to the insert logic to ensure idempotent uploads |
| 🧱 Schema Mismatches | Column mismatches (e.g., `api_name` vs `apiname`) caused PostgreSQL errors during insertions | Resolved by strictly aligning SQL schema and Python insert columns |

