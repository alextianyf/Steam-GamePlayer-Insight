-- 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    country TEXT,
    join_date TIMESTAMP,
    last_online TIMESTAMP
);

-- 游戏表（可后期补 genre 等）
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY,
    name TEXT,
    genre TEXT
);

-- 用户-游戏关系
CREATE TABLE IF NOT EXISTS user_game (
    user_id BIGINT,
    game_id INTEGER,
    total_playtime INTEGER,
    first_played TIMESTAMP,
    last_played TIMESTAMP,
    PRIMARY KEY (user_id, game_id)
);

-- 成就表
CREATE TABLE IF NOT EXISTS achievements (
    user_id BIGINT,
    game_id INTEGER,
    achievement_id TEXT,
    unlocked BOOLEAN,
    unlock_time TIMESTAMP,
    PRIMARY KEY (user_id, game_id, achievement_id)
);
