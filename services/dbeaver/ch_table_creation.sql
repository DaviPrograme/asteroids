CREATE TABLE IF NOT EXISTS players (
    id UInt32,
    player_name String
) ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS high_scores (
    id UInt32,
    player_id UInt32,
    score UInt32,
    date DateTime
) ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS score_history (
    id UInt32,
    player_id UInt32,
    score UInt32,
    date DateTime
) ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS achievements (
    id UInt32,
    achievement_name String,
    description String
) ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS player_achievements (
    player_id UInt32,
    achievement_id UInt32,
    date_earned DateTime
) ENGINE = MergeTree()
ORDER BY (player_id, achievement_id);
