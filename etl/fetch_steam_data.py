import os
import requests
import csv
from datetime import datetime

API_KEY = "38FDE82053BED10CE4B5B9F588DF1C85"
STEAM_ID = "76561199467017934"
APP_IDS = [500, 550, 242760, 397540, 1599340]  # 你玩过的游戏

url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
params = {
    'key': API_KEY,
    'steamid': STEAM_ID,
    'include_appinfo': True,  # Include name
    'include_played_free_games': True
}

response = requests.get(url, params=params)
games = response.json()

for game in games["response"].get("games", []):
    print(f"{game['appid']} - {game['name']} - {game['playtime_forever'] / 60:.1f} Hour(s)")



#------------------------------------------------------------------------------------#
#--------------------------------Scripy Data------------------------------------#

SAVE_DIR = "../data/raw/"  # 相对于 etl/ 文件夹
os.makedirs(SAVE_DIR, exist_ok=True)


def fetch_player_achievements(steamid, appid):
    """获取某个玩家在某个游戏的成就数据"""
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        'key': API_KEY,
        'steamid': steamid,
        'appid': appid
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "playerstats" in data and "achievements" in data["playerstats"]:
        return data["playerstats"]["gameName"], data["playerstats"]["achievements"]
    else:
        return None, []


def save_achievements_to_csv(game_name, appid, achievements):
    """将成就信息保存为 CSV"""
    filename = os.path.join(SAVE_DIR, f"{appid}_{game_name.replace(' ', '_')}_achievements.csv")

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["apiname", "achieved", "unlock_time"])

        for ach in achievements:
            writer.writerow([ach["apiname"], ach["achieved"], ach.get("unlocktime", "")])

    print(f"[✔] 成就数据已保存：{filename}")


def main():
    for appid in APP_IDS:
        print(f"⏳ 正在抓取 appid={appid} ...")
        game_name, achievements = fetch_player_achievements(STEAM_ID, appid)

        if achievements:
            save_achievements_to_csv(game_name, appid, achievements)
        else:
            print(f"[✘] 无法获取 appid={appid} 的成就（可能是无成就或未公开）")
        
        user_info = fetch_user_info(STEAM_ID)
        if user_info:
            save_user_info_to_csv(user_info)
        else:
            print(f"[✘] 无法获取 appid={appid} 的userinfo（可能是无成就或未公开）")



def fetch_user_info(steamid):
    """获取玩家基本信息（国家、注册时间、最后上线）"""
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        'key': API_KEY,
        'steamids': steamid
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"] and len(data["response"]["players"]) > 0:
        player = data["response"]["players"][0]
        user_info = {
            "user_id": int(player.get("steamid", 0)),
            "country": player.get("loccountrycode", "Unknown"),
            "join_date": datetime.utcfromtimestamp(player.get("timecreated", 0)).strftime("%Y-%m-%d %H:%M:%S") if player.get("timecreated") else "N/A",
            "last_online": datetime.utcfromtimestamp(player.get("lastlogoff", 0)).strftime("%Y-%m-%d %H:%M:%S") if player.get("lastlogoff") else "N/A"
        }
        return user_info
    else:
        print("⚠️ 无法获取用户信息。")
        return None


def save_user_info_to_csv(user_info):
    """保存用户信息到 users.csv"""
    filename = os.path.join(SAVE_DIR, "users.csv")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "country", "join_date", "last_online"])
        writer.writeheader()
        writer.writerow(user_info)
    print(f"[✔] 用户信息已保存：{filename}")


if __name__ == "__main__":
    main()

