-- airbyte_internal.achievements_view source

CREATE VIEW airbyte_internal.achievements_view
(

    `id` UInt64,

    `achievement_name` String,

    `description` String
)
AS SELECT
    JSONExtractUInt(_airbyte_data,
 'id') AS id,

    JSONExtractString(_airbyte_data,
 'achievement_name') AS achievement_name,

    JSONExtractString(_airbyte_data,
 'description') AS description
FROM airbyte_internal.default_raw__stream_achievements
WHERE JSONHas(_airbyte_data,
 'achievement_name');