import os
import requests
import time
import csv
import re

API_KEY = "38FDE82053BED10CE4B5B9F588DF1C85"
USER_IDS_PATH = "../user_ids.txt"
SAVE_DIR = "../data/raw/"
os.makedirs(SAVE_DIR, exist_ok=True)

MAX_USERS = 30  # Target number of valid users to fetch
TOP_N_GAMES = 10  # Limit to top N games per user

def sanitize_filename(name):
    """Remove illegal characters from file names"""
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
        games = response.json().get("response", {}).get("games", [])
        return sorted(games, key=lambda g: g.get("playtime_forever", 0), reverse=True)[:TOP_N_GAMES]
    except Exception as e:
        print(f"Failed to fetch games for user {steamid}: {e}")
        return []

def fetch_achievements(steamid, appid):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        'key': API_KEY,
        'steamid': steamid,
        'appid': appid
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if "playerstats" in data and "achievements" in data["playerstats"]:
            name = data["playerstats"].get("gameName", str(appid))
            return name, data["playerstats"]["achievements"]
        return None, []
    except Exception:
        return None, []

def save_games_csv(steamid, games):
    path = os.path.join(SAVE_DIR, f"{steamid}_games.csv")
    try:
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["appid", "name", "playtime_hours"])
            for g in games:
                writer.writerow([g["appid"], g["name"], g["playtime_forever"] / 60])
        print(f"Saved game data for user {steamid}")
    except Exception as e:
        print(f"Failed to write game data: {e}")

def save_achievements_csv(steamid, appid, game_name, achievements):
    safe_name = sanitize_filename(game_name)
    filename = f"{appid}_{safe_name}_achievements.csv"
    path = os.path.join(SAVE_DIR, filename)
    try:
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["apiname", "achieved", "unlock_time"])
            for ach in achievements:
                writer.writerow([ach["apiname"], ach["achieved"], ach.get("unlocktime", "")])
        print(f"Saved achievements: {appid} - {game_name}")
    except Exception as e:
        print(f"Failed to write achievements: {e}")

def main():
    with open(USER_IDS_PATH) as f:
        user_ids = [line.strip() for line in f if line.strip()]

    successful_users = 0
    for steamid in user_ids:
        if successful_users >= MAX_USERS:
            break
        print(f"\nFetching user {steamid}")
        games = fetch_owned_games(steamid)
        if not games:
            print("No games found, skipping")
            continue

        save_games_csv(steamid, games)
        has_valid_game = False

        for g in games:
            game_name, achievements = fetch_achievements(steamid, g["appid"])
            if achievements:
                save_achievements_csv(steamid, g["appid"], game_name, achievements)
                has_valid_game = True
            else:
                print(f"No achievements or not public: {g['appid']} - {g['name']}")
            time.sleep(1.2)

        if has_valid_game:
            successful_users += 1
            print(f"Successfully fetched data for {successful_users} valid users")
        else:
            print("No achievement data, user skipped")

    print(f"\nDone. Successfully fetched {successful_users} users")

if __name__ == "__main__":
    main()
