from clickhouse_driver import Client

# Configurações de conexão
host = 'localhost'
port = 9000  # Porta padrão para ClickHouse
username = 'default'
password = ''

permissions_queries = [
    "CREATE USER airbyte_user IDENTIFIED BY 'sua_senha_segura';",
    "GRANT CREATE ON *.* TO airbyte_user;",
    "GRANT CREATE ON default.* TO airbyte_user;",
    "GRANT DROP ON *.* TO airbyte_user;",
    "GRANT TRUNCATE ON *.* TO airbyte_user;",
    "GRANT INSERT ON *.* TO airbyte_user;",
    "GRANT SELECT ON *.* TO airbyte_user;",
    "GRANT CREATE DATABASE ON airbyte_internal.* TO airbyte_user;",
    "GRANT CREATE TABLE ON airbyte_internal.* TO airbyte_user;",
    "GRANT DROP ON airbyte_internal.* TO airbyte_user;",
    "GRANT TRUNCATE ON airbyte_internal.* TO airbyte_user;",
    "GRANT INSERT ON airbyte_internal.* TO airbyte_user;",
    "GRANT SELECT ON airbyte_internal.* TO airbyte_user;",
]

# Comando SQL para criar a tabela
create_table_queries = [
    '''
    CREATE VIEW players_view (
        `id` UInt64,
        `player_name` String
    )
    AS SELECT JSONExtractUInt(_airbyte_data,'id') AS id,
    JSONExtractString(_airbyte_data, 'player_name') AS player_name
    FROM airbyte_internal.default_raw__stream_players
    WHERE JSONHas(_airbyte_data, 'player_name');
    ''',
    
    '''
    CREATE VIEW high_scores_view (
        `id` UInt64,
        `player_id` UInt64,
        `score` UInt64,
        `date` Date
    )
    AS SELECT
    JSONExtractUInt(_airbyte_data, 'id') AS id,
    JSONExtractUInt(_airbyte_data, 'player_id') AS player_id,
    JSONExtractUInt(_airbyte_data, 'score') AS score,
    toDate(JSONExtractString(_airbyte_data, 'date')) AS date
    FROM airbyte_internal.default_raw__stream_high_scores
    WHERE JSONHas(_airbyte_data, 'score') AND JSONHas(_airbyte_data, 'player_id');
    ''',
    
    '''
    CREATE VIEW score_history_view AS
    SELECT
        JSONExtractUInt(_airbyte_data, 'id') AS id,
        JSONExtractUInt(_airbyte_data, 'player_id') AS player_id,
        JSONExtractUInt(_airbyte_data, 'score') AS score,
        toDate(JSONExtractString(_airbyte_data, 'date')) AS date
    FROM airbyte_internal.default_raw__stream_score_history
    WHERE JSONHas(_airbyte_data, 'score') AND JSONHas(_airbyte_data, 'player_id');
    ''',
    
    '''
    CREATE VIEW achievements_view (
        `id` UInt64,
        `achievement_name` String,
        `description` String
    )
    AS SELECT
    JSONExtractUInt(_airbyte_data, 'id') AS id,
    JSONExtractString(_airbyte_data, 'achievement_name') AS achievement_name,
    JSONExtractString(_airbyte_data, 'description') AS description
    FROM airbyte_internal.default_raw__stream_achievements
    WHERE JSONHas(_airbyte_data, 'achievement_name');
    ''',
    
    '''
    CREATE VIEW player_achievements_view(
        `player_id` UInt64,
        `achievement_id` UInt64,
        `date_earned` Date
    )
    AS SELECT
    JSONExtractUInt(_airbyte_data, 'player_id') AS player_id,
    JSONExtractUInt(_airbyte_data, 'achievement_id') AS achievement_id,
    toDate(JSONExtractString(_airbyte_data, 'date_earned')) AS date_earned
    FROM airbyte_internal.default_raw__stream_player_achievements
    WHERE JSONHas(_airbyte_data, 'achievement_id') AND JSONHas(_airbyte_data, 'player_id');
    '''
]

try:
    # Conectar ao ClickHouse
    client = Client(host=host, port=port, user=username, password=password)

    # for permission in permissions_queries:
    #     client.execute(permission)

    # Executar o comando para criar a tabela
    for create_table_query in create_table_queries:
        client.execute(create_table_query)

    # Verificar se a criação da tabela foi bem-sucedida
    print("Tabela 'players' criada com sucesso!")

except Exception as e:
    print(f"Erro ao criar tabela: {str(e)}")