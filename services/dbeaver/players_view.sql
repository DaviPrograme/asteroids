-- airbyte_internal.players_view source

CREATE VIEW airbyte_internal.players_view
(

    `id` UInt64,

    `player_name` String
)
AS SELECT
    JSONExtractUInt(_airbyte_data,
 'id') AS id,

    JSONExtractString(_airbyte_data,
 'player_name') AS player_name
FROM airbyte_internal.default_raw__stream_players
WHERE JSONHas(_airbyte_data,
 'player_name');