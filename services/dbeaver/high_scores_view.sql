-- airbyte_internal.high_scores_view source

CREATE VIEW airbyte_internal.high_scores_view
(

    `id` UInt64,

    `player_id` UInt64,

    `score` UInt64,

    `date` Date
)
AS SELECT
    JSONExtractUInt(_airbyte_data,
 'id') AS id,

    JSONExtractUInt(_airbyte_data,
 'player_id') AS player_id,

    JSONExtractUInt(_airbyte_data,
 'score') AS score,

    toDate(JSONExtractString(_airbyte_data,
 'date')) AS date
FROM airbyte_internal.default_raw__stream_high_scores
WHERE JSONHas(_airbyte_data,
 'score') AND JSONHas(_airbyte_data,
 'player_id');