# import requests
# import time
# import pandas as pd
# import os
# from datetime import datetime, timezone, timedelta
# from tqdm import tqdm  # 添加进度条支持


# # Your Steam Web API key
# API_KEY = "38FDE82053BED10CE4B5B9F588DF1C85"

# # File path to user ID list (one SteamID per line)
# USER_IDS_PATH = "../data/intermediate/user_ids.txt"

# # Directory to save output CSV files
# SAVE_DIR = "../data/raw/"
# os.makedirs(SAVE_DIR, exist_ok=True)

# # Target game(s) and their Steam AppIDs
# GAMES = {
#     "7dtd": 251570  # 7 Days to Die
# }

# # Number of valid players to collect per game
# NUM_PLAYERS_PER_GAME = 100
# FILTER_MIN_PLAY_TIME = 30

# # Define the timezone offset for Vancouver (UTC-7)
# VANCOUVER_OFFSET = timedelta(hours=-7)

# # Load list of SteamIDs from file
# def load_user_ids(path):
#     with open(path, 'r') as f:
#         return [line.strip() for line in f if line.strip().isdigit()]

# # Query whether a user owns a specific game and return playtime in minutes if available
# def get_playtime_if_owned(steamid, appid):
#     url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
#     params = {"key": API_KEY, "steamid": steamid, "include_appinfo": False}
#     try:
#         resp = requests.get(url, params=params).json()
#         games = resp.get("response", {}).get("games", [])
#         for game in games:
#             if str(game.get("appid")) == str(appid):
#                 return game.get("playtime_forever", 0)
#         return None
#     except Exception as e:
#         print(f"[ERROR] checking owned games for {steamid}: {e}")
#         return None

# # Retrieve the achievement schema (meta info) for a given game
# def get_achievement_schema(appid):
#     url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
#     params = {"key": API_KEY, "appid": appid}
#     try:
#         resp = requests.get(url, params=params).json()
#         achievements = resp.get("game", {}).get("availableGameStats", {}).get("achievements", [])
#         schema = {}
#         for item in achievements:
#             schema[item["name"]] = {
#                 "displayName": item.get("displayName"),
#                 "description": item.get("description"),
#                 "hidden": item.get("hidden"),
#                 "icon": item.get("icon"),
#                 "icongray": item.get("icongray"),
#                 "defaultvalue": item.get("defaultvalue", 0)  # global unlock rate (percentage)
#             }
#         return schema
#     except Exception as e:
#         print(f"[ERROR] fetching schema for appid {appid}: {e}")
#         return {}

# # Convert Unix timestamp into ISO 8601 format in Vancouver local time (UTC-7)
# def convert_to_vancouver_time(unix_ts):
#     if unix_ts and unix_ts > 0:
#         dt = datetime.fromtimestamp(unix_ts, timezone.utc) + VANCOUVER_OFFSET
#         return dt.isoformat()
#     return None

# # Get player achievement progress, unlock times, and global unlock rate
# def get_achievements_with_unlocktime(steamid, appid, schema):
#     url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
#     params = {"key": API_KEY, "steamid": steamid, "appid": appid}
#     try:
#         resp = requests.get(url, params=params).json()
#         achievements = resp.get("playerstats", {}).get("achievements", [])
#         result = {}
#         for item in achievements:
#             apiname = item["apiname"]
#             result[f"{apiname}"] = item.get("achieved", 0)  # 0 or 1
#             if item.get("achieved", 0) == 1:
#                 unlocktime = item.get("unlocktime", 0)
#                 result[f"{apiname}_unlocktime"] = convert_to_vancouver_time(unlocktime)
#             # Add global unlock rate (from schema)
#             if apiname in schema:
#                 result[f"{apiname}_global_unlock_rate"] = schema[apiname].get("defaultvalue", 0)
#         return result
#     except Exception as e:
#         print(f"[ERROR] getting achievements for {steamid}: {e}")
#         return {}

# # Main logic to collect valid player data for a specific game
# def collect_data_for_game(game_name, appid, user_ids):
#     schema = get_achievement_schema(appid)  # load achievement schema first

#     collected = []
#     for steamid in user_ids:
#         playtime = get_playtime_if_owned(steamid, appid)
#         if playtime is not None and playtime >= FILTER_MIN_PLAY_TIME:  # filter only active players (for example minimum 30 min)
#             print(f"[INFO] {steamid} owns {game_name.upper()} and played {playtime} min")
#             achievements = get_achievements_with_unlocktime(steamid, appid, schema)
#             if achievements:
#                 entry = {
#                     "steamid": steamid,
#                     "playtime_forever": playtime
#                 }
#                 entry.update(achievements)
#                 collected.append(entry)
#                 if len(collected) >= NUM_PLAYERS_PER_GAME:
#                     break
#             time.sleep(1)  # avoid rate limit
#         else:
#             print(f"[SKIP] {steamid} owns {game_name.upper()} but only played {playtime or 0} min")

#     # Save player data
#     df = pd.DataFrame(collected)
#     df.to_csv(os.path.join(SAVE_DIR, f"{game_name}_players.csv"), index=False)
#     print(f"[DONE] Saved {len(df)} players for {game_name.upper()}")

#     # Save achievement schema
#     if schema:
#         schema_df = pd.DataFrame.from_dict(schema, orient="index").reset_index().rename(columns={"index": "apiname"})
#         schema_df.to_csv(os.path.join(SAVE_DIR, f"{game_name}_achievement_schema.csv"), index=False)
#         print(f"[DONE] Saved achievement schema for {game_name.upper()}")

# # Run the collection process for all games
# def main():
#     user_ids = load_user_ids(USER_IDS_PATH)
#     for game_name, appid in GAMES.items():
#         print(f"\n[PROCESSING] {game_name.upper()} ({appid})")
#         collect_data_for_game(game_name, appid, user_ids)

# if __name__ == "__main__":
#     main()
import requests
import time
import pandas as pd
import os
from datetime import datetime, timezone, timedelta
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------- Config ---------
API_KEY = "83E7B436E900D4F8B0085F043D22BD23"
USER_IDS_PATH = "../data/intermediate/user_ids.txt"
VALID_USERS_PATH = "../data/intermediate/7dtd_valid_users.txt"
SAVE_DIR = "../data/raw/"
os.makedirs(SAVE_DIR, exist_ok=True)

GAME_NAME = "7dtd"
APPID = 251570  # 7 Days to Die
NUM_PLAYERS_PER_GAME = 5000
FILTER_MIN_PLAY_TIME = 30
VANCOUVER_OFFSET = timedelta(hours=-7)
MAX_THREADS = 10

# --------- Utilities ---------
def load_user_ids(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip().isdigit()]

def load_valid_user_cache():
    if os.path.exists(VALID_USERS_PATH):
        with open(VALID_USERS_PATH, "r") as f:
            return set(line.strip() for line in f)
    return set()

def save_valid_user_cache(valid_ids):
    with open(VALID_USERS_PATH, "w") as f:
        for uid in valid_ids:
            f.write(f"{uid}\n")

def safe_request(url, params, max_retries=3):
    for i in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            time.sleep(1 + i)
        except Exception as e:
            time.sleep(1 + i)
    return {}

# --------- Step 1: Get playtime ---------
def get_playtime_if_owned(steamid, appid):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {"key": API_KEY, "steamid": steamid, "include_appinfo": False}
    resp = safe_request(url, params)
    games = resp.get("response", {}).get("games", [])
    for game in games:
        if str(game.get("appid")) == str(appid):
            return game.get("playtime_forever", 0)
    return None

def try_get_valid_user(steamid):
    playtime = get_playtime_if_owned(steamid, APPID)
    if playtime is not None and playtime >= FILTER_MIN_PLAY_TIME:
        return (steamid, playtime)
    return None

def filter_valid_users(user_ids):
    valid_users = []
    seen = set()
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(try_get_valid_user, uid): uid for uid in user_ids}
        for future in tqdm(as_completed(futures), total=len(user_ids), desc="Filtering valid users"):
            result = future.result()
            if result and result[0] not in seen:
                valid_users.append(result)
                seen.add(result[0])
                if len(valid_users) >= NUM_PLAYERS_PER_GAME:
                    break
    return valid_users

# --------- Step 2: Achievement schema ---------
def get_achievement_schema(appid):
    url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params = {"key": API_KEY, "appid": appid}
    resp = safe_request(url, params)
    achievements = resp.get("game", {}).get("availableGameStats", {}).get("achievements", [])
    schema = {}
    for item in achievements:
        schema[item["name"]] = {
            "displayName": item.get("displayName"),
            "description": item.get("description"),
            "hidden": item.get("hidden"),
            "icon": item.get("icon"),
            "icongray": item.get("icongray"),
            "defaultvalue": item.get("defaultvalue", 0)
        }
    return schema

def convert_to_vancouver_time(unix_ts):
    if unix_ts and unix_ts > 0:
        dt = datetime.fromtimestamp(unix_ts, timezone.utc) + VANCOUVER_OFFSET
        return dt.isoformat()
    return None

# --------- Step 3: Get player achievements ---------
def get_achievements_with_unlocktime(steamid, appid, schema):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {"key": API_KEY, "steamid": steamid, "appid": appid}
    resp = safe_request(url, params)
    achievements = resp.get("playerstats", {}).get("achievements", [])
    result = {}
    for item in achievements:
        apiname = item["apiname"]
        result[f"{apiname}"] = item.get("achieved", 0)
        if item.get("achieved", 0) == 1:
            unlocktime = item.get("unlocktime", 0)
            result[f"{apiname}_unlocktime"] = convert_to_vancouver_time(unlocktime)
        if apiname in schema:
            result[f"{apiname}_global_unlock_rate"] = schema[apiname].get("defaultvalue", 0)
    return result

# --------- Main data collection ---------
def collect_data_for_valid_users(valid_users, schema):
    collected = []
    for steamid, playtime in tqdm(valid_users, desc="Fetching achievement data"):
        achievements = get_achievements_with_unlocktime(steamid, APPID, schema)
        if achievements:
            entry = {"steamid": steamid, "playtime_forever": playtime}
            entry.update(achievements)
            collected.append(entry)
    return collected

# --------- Main runner ---------
def main():
    user_ids = load_user_ids(USER_IDS_PATH)
    print(f"[INFO] Loaded {len(user_ids)} user ids")

    cached_valid = load_valid_user_cache()
    print(f"[INFO] Found {len(cached_valid)} cached valid users")

    needed = NUM_PLAYERS_PER_GAME - len(cached_valid)
    if needed > 0:
        new_valid_users = filter_valid_users(user_ids)
        new_ids = [uid for uid, _ in new_valid_users]
        save_valid_user_cache(cached_valid.union(new_ids))
        valid_users = new_valid_users
    else:
        valid_users = [(uid, get_playtime_if_owned(uid, APPID)) for uid in list(cached_valid)[:NUM_PLAYERS_PER_GAME]]

    print(f"[INFO] Start fetching achievements for {len(valid_users)} users")
    schema = get_achievement_schema(APPID)
    player_data = collect_data_for_valid_users(valid_users, schema)

    df = pd.DataFrame(player_data)
    df.to_csv(os.path.join(SAVE_DIR, f"{GAME_NAME}_players.csv"), index=False)
    print(f"[DONE] Saved {len(df)} players to CSV")

    if schema:
        schema_df = pd.DataFrame.from_dict(schema, orient="index").reset_index().rename(columns={"index": "apiname"})
        schema_df.to_csv(os.path.join(SAVE_DIR, f"{GAME_NAME}_achievement_schema.csv"), index=False)
        print(f"[DONE] Saved achievement schema")

if __name__ == "__main__":
    main()
