import os
import requests
import time
import csv
import re
import random
from datetime import datetime, timezone

# This file will obtain data of multiple random players, with each player of multiple games

# --- Configuration ---
API_KEY = "38FDE82053BED10CE4B5B9F588DF1C85"
USER_IDS_PATH = "../data/intermediate/user_ids.txt"
SAVE_DIR = "../data/raw/"
MAX_USERS = 2
MAX_GAMES_PER_USER = 30
RANDOM_SEED = 42

os.makedirs(SAVE_DIR, exist_ok=True)

# --- Helpers ---
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def fetch_owned_games(steamid):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        'key': API_KEY,
        'steamid': steamid,
        'include_appinfo': True,
        'include_played_free_games': True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        games = data.get("response", {}).get("games", [])

        if not games:
            return []

        played_games = [g for g in games if g.get("playtime_forever", 0) > 0]

        if not played_games:
            print(f"⚠️ All games have 0 playtime for user {steamid}")
            return []

        print(f"🧪 [Schema] Fields in game object for user {steamid}: {list(played_games[0].keys())}")
        query_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        for game in played_games:
            game["query_date"] = query_date

        random.seed(RANDOM_SEED)
        if len(played_games) > MAX_GAMES_PER_USER:
            played_games = random.sample(played_games, MAX_GAMES_PER_USER)

        return played_games

    except Exception as e:
        print(f"❌ Error fetching games for user {steamid}: {e}")
        return []

def fetch_achievements(steamid, appid):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        'key': API_KEY,
        'steamid': steamid,
        'appid': appid
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        stats = data.get("playerstats", {})

        if "achievements" in stats:
            game_name = stats.get("gameName", str(appid))
            achievements = stats["achievements"]
            if achievements:
                print(f"🧪 [Schema] Fields in achievements for app {appid}: {list(achievements[0].keys())}")
            return game_name, achievements

        return None, []

    except Exception:
        return None, []

def save_games_global_csv(rows):
    path = os.path.join(SAVE_DIR, "all_users_games.csv")
    try:
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "steamid", "appid", "name", "playtime_minutes", "query_date",
                "icon_url", "content_descriptorids"
            ])
            writer.writerows(rows)
        print(f"✅ Saved global games data to all_users_games.csv")
    except Exception as e:
        print(f"❌ Failed to write games: {e}")

def save_achievements_global_csv(rows):
    path = os.path.join(SAVE_DIR, "all_users_achievements.csv")
    try:
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["steamid", "appid", "game_name", "apiname", "achieved", "unlock_time"])
            writer.writerows(rows)
        print(f"📦 Saved global achievements to all_users_achievements.csv")
    except Exception as e:
        print(f"❌ Failed to write achievements: {e}")

# --- Main Driver ---
def main():
    with open(USER_IDS_PATH) as f:
        user_ids = [line.strip() for line in f if line.strip()]

    all_games_rows = []
    all_achievement_rows = []

    valid_user_count = 0
    for steamid in user_ids:
        if valid_user_count >= MAX_USERS:
            break

        print(f"\n🔍 Processing user {steamid}...")
        games = fetch_owned_games(steamid)
        if not games:
            print("⚠️ No games found or profile is private.")
            continue

        for g in games:
            appid = g["appid"]
            icon_hash = g.get("img_icon_url", "")
            icon_url = f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{icon_hash}.jpg" if icon_hash else ""

            content_ids = g.get("content_descriptorids", [])
            content_ids_str = ",".join(map(str, content_ids)) if isinstance(content_ids, list) else str(content_ids)

            all_games_rows.append([
                steamid,
                appid,
                g.get("name", ""),
                g.get("playtime_forever", 0),  # Minutes
                g["query_date"],
                icon_url,
                content_ids_str
            ])

        has_valid_achievement = False
        for g in games:
            game_name, achievements = fetch_achievements(steamid, g["appid"])
            if achievements:
                for ach in achievements:
                    all_achievement_rows.append([
                        steamid,
                        g["appid"],
                        game_name,
                        ach.get("apiname"),
                        ach.get("achieved"),
                        ach.get("unlocktime", "")
                    ])
                has_valid_achievement = True
            else:
                print(f"⚠️ No achievements or not public: {g['appid']} - {g['name']}")
            time.sleep(1.2)

        if has_valid_achievement:
            valid_user_count += 1
            print(f"✅ Accepted: {valid_user_count} valid users so far")
        else:
            print("⛔ No valid achievements found; skipping user")

    if all_games_rows:
        save_games_global_csv(all_games_rows)
    if all_achievement_rows:
        save_achievements_global_csv(all_achievement_rows)

    print(f"\n🏁 Extraction completed. {valid_user_count} valid users saved.")

if __name__ == "__main__":
    main()
