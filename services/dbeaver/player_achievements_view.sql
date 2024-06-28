-- airbyte_internal.player_achievements_view source

CREATE VIEW airbyte_internal.player_achievements_view
(

    `player_id` UInt64,

    `achievement_id` UInt64,

    `date_earned` Date
)
AS SELECT
    JSONExtractUInt(_airbyte_data,
 'player_id') AS player_id,

    JSONExtractUInt(_airbyte_data,
 'achievement_id') AS achievement_id,

    toDate(JSONExtractString(_airbyte_data,
 'date')) AS date_earned
FROM airbyte_internal.default_raw__stream_player_achievements
WHERE JSONHas(_airbyte_data,
 'achievement_id') AND JSONHas(_airbyte_data,
 'player_id');