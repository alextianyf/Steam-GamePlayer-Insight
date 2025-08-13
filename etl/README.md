# ETL Pipeline — Steam Game Player Insight

This ETL pipeline serves as the foundational phase of a broader data science project that focuses on analyzing and modeling player behavior in Steam games. By leveraging public and semi-public Steam APIs, the pipeline collects structured gameplay data that supports both exploratory insights and predictive modeling.

**ETL** stands for **Extract, Transform, Load** — a common data pipeline process where you:

- **Extract** data from source systems (e.g., Steam APIs),
- **Transform** it into a clean, usable format (e.g., filter, convert timestamps),
- **Load** it into storage or databases for analysis.

This ETL ensures we turn raw player data into structured datasets ready for machine learning and analytics.

---

## ETL Workflow Summary

### Step 1: Extract Player IDs

- Download the base dataset from Kaggle: [Steam Achievement Stats Ranking](https://www.kaggle.com/datasets/patrickgendotti/steam-achievementstatscom-rankings)

- This file provides over 200,000 Steam user IDs ranked by achievement count. These IDs are ready for data fetching, but we do not yet know which games these players are playing.

- Cleaned CSV path: `data/players/amended_first_200k_players.csv`

### Step 2: Filter Usable SteamIDs

- Run: `extract_user_ids_from_csv.py`

- Filters for 20,000 users with public profiles

- Keep only numeric IDs since there are some invalid character usernames(e.g., non-ASCII usernames)

- Output file: `data/intermediate/user_ids.txt`

### Step 3: Game-Specific Data Extraction(demonstrate with game *7DTD*)

> Steam Web API details can be found at [Steam Web API Documentation](https://steamcommunity.com/dev).  
> As the project expands, similar fetch scripts can be added for other titles (e.g., `fetch_csgo_data.py`) using the same modular ETL structure. All you need to do is to modify the game ID.

- Run the script `fetch_7DTD_data.py`

- Filter the valid user IDs from `data/intermediate/user_ids.txt`, as many users have no playtime in the desired game. The filtered results will be saved to `data/intermediate/7dtd_valid_users.txt`.

- Collect gameplay data and achievement statistics for valid players.
  
  - playtime (must exceed 30 minutes), saved to `data/raw/7dtd_players.csv`
  
  - Achievement unlock status and timestamps (converted to Vancouver time), saved to `data/raw/7dtd_players.csv`
  
  - Global unlock rates for each achievement, saved to `data/raw/7dtd_players.csv`
  
  - Achievement description, saved to `data/raw/7dtd_achievement_schema.csv`

- Raw player data and achievement metadata will be saved to the `data/raw/` directory.

### Step 4: Data Preparation in PostgreSQL

> The following manipulations are based on 7 Days to Die. Different games may require different features and should be adjusted accordingly.

- upload fetched data into SQL(a SQL setup guideline is provided below)

- Create a new table in the database called `player_summary`. After processing, this table will include the following features:
  
  - **steamid**

  - **playtime_forever** — total playtime (in minutes)

  - **achievement_count** — total achievements unlocked

  - ***_count** — number of unlocked achievements in each category

  - **max_*** — highest achievement unlocked in each category
  
  - **efficiency_score** - $achievement_count / playtime_forever$

### Step 5: Data Loading and Start Analyzing

At this stage, the structured `player_summary` are ready to be:

- Loaded as dataframe

- Used for exploratory data analysis (EDA)  

- Passed into machine learning pipelines  

- Visualized through dashboards or reports  

---

## Setting Up PostgreSQL Database

### 1. Start the PostgreSQL Service(PostgreSQL17)  

This step is required only the first time (or after reboot) to ensure the PostgreSQL server is running:

```bash
brew services start postgresql@17
```

### 2. Create the steamdb Database

Use the createdb command to initialize the database (only needed once):

```bash
createdb -U alextian steamdb
```

> Replace alextian with your PostgreSQL username if different.  
> You can also replace steamdb to any other database naming.

### 3. Upload CSV Data to PostgreSQL

Run the script to load `.csv` files (such as `7dtd_players.csv`, `7dtd_achievement_schema.csv`) into PostgreSQL tables:

```bash
python upload_to_psql.py
```

> Make sure the script uses the correct credentials and table names (e.g., `players_7dtd`, `achievement_schema_7dtd`).

### 4. Connect to steamdb via Terminal

To manually inspect or query the database using the PostgreSQL CLI:

```bash
psql -U alextian -d steamdb
```

At this point, your data is uploaded into the PostgreSQL, and you are ready to restructure or load for further analysis.

> Once connected, you can run SQL commands directly from the terminal.  
> Alternatively, you can use **pgAdmin 4**, a GUI-based PostgreSQL management tool, for more user-friendly database interaction.