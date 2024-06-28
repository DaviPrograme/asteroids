-- Inserindo dados na tabela players
INSERT INTO players (id, player_name)
SELECT
    JSONExtractUInt(_airbyte_data, 'id') AS id,
    JSONExtractString(_airbyte_data, 'player_name') AS player_name
FROM airbyte_raw.default_raw__stream_players
WHERE JSONHas(_airbyte_data, 'player_name');

-- Inserindo dados na tabela high_scores
INSERT INTO high_scores (id, player_id, score, date)
SELECT 
    JSONExtractUInt(_airbyte_data, 'id') AS id,
    JSONExtractUInt(_airbyte_data, 'player_id') AS player_id,
    JSONExtractUInt(_airbyte_data, 'score') AS score,
    toDate(JSONExtractString(_airbyte_data, 'date')) AS date
FROM airbyte_raw.default_raw__stream_high_scores 
WHERE JSONHas(_airbyte_data, 'score') AND JSONHas(_airbyte_data, 'player_id');


-- Inserindo dados na tabela score_history
INSERT INTO score_history (id, player_id, score, date)
SELECT
    JSONExtractUInt(_airbyte_data, 'id') AS id,
    JSONExtractUInt(_airbyte_data, 'player_id') AS player_id,
    JSONExtractUInt(_airbyte_data, 'score') AS score,
    toDate(JSONExtractString(_airbyte_data, 'date')) AS date
FROM airbyte_raw.default_raw__stream_score_history
WHERE JSONHas(_airbyte_data, 'score') AND JSONHas(_airbyte_data, 'player_id');

-- Inserindo dados na tabela achievements
INSERT INTO achievements (id, achievement_name, description)
SELECT
    JSONExtractUInt(_airbyte_data, 'id') AS id,
    JSONExtractString(_airbyte_data, 'achievement_name') AS achievement_name,
    JSONExtractString(_airbyte_data, 'description') AS description
FROM airbyte_raw.default_raw__stream_achievements 
WHERE JSONHas(_airbyte_data, 'achievement_name');

-- Inserindo dados na tabela player_achievements
INSERT INTO player_achievements (player_id, achievement_id, date_earned)
SELECT
    JSONExtractUInt(_airbyte_data, 'player_id') AS player_id,
    JSONExtractUInt(_airbyte_data, 'achievement_id') AS achievement_id,
    toDate(JSONExtractString(_airbyte_data, 'date')) AS date_earned
FROM airbyte_raw.default_raw__stream_player_achievements 
WHERE JSONHas(_airbyte_data, 'achievement_id') AND JSONHas(_airbyte_data, 'player_id');
