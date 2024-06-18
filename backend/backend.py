import psycopg

# Dados de conexão
host = "localhost"
port = "9090"
dbname = "asteroid"
user = "postgres"
password = "abcXecole42"

try:
    # Conectar ao banco de dados
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    print("Conexão ao PostgreSQL bem-sucedida!")

    # Criar um cursor
    cursor = conn.cursor()

    print("Conexão ao PostgreSQL bem-sucedida!")

    # Criar um cursor
    cursor = conn.cursor()
    
    # Comando SQL para criar a tabela players
    create_players_table_query = '''
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL
    );
    '''

    # Executar o comando SQL para criar a tabela players
    cursor.execute(create_players_table_query)
    print("Tabela 'players' criada com sucesso.")

    # Comando SQL para criar a tabela high_scores
    create_high_scores_table_query = '''
    CREATE TABLE IF NOT EXISTS high_scores (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        date TIMESTAMP
    );
    '''

    # Executar o comando SQL para criar a tabela high_scores
    cursor.execute(create_high_scores_table_query)
    print("Tabela 'high_scores' criada com sucesso.")

    # Comando SQL para criar a tabela score_history
    create_score_history_table_query = '''
    CREATE TABLE IF NOT EXISTS score_history (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        date TIMESTAMP
    );
    '''

    # Executar o comando SQL para criar a tabela score_history
    cursor.execute(create_score_history_table_query)
    print("Tabela 'score_history' criada com sucesso.")

    # Comando SQL para criar a tabela achievements
    create_achievements_table_query = '''
    CREATE TABLE IF NOT EXISTS achievements (
        id SERIAL PRIMARY KEY,
        achievement_name VARCHAR(100),
        description TEXT
    );
    '''

    # Executar o comando SQL para criar a tabela achievements
    cursor.execute(create_achievements_table_query)
    print("Tabela 'achievements' criada com sucesso.")

    # Comando SQL para criar a tabela player_achievements
    create_player_achievements_table_query = '''
    CREATE TABLE IF NOT EXISTS player_achievements (
        player_id INTEGER REFERENCES players(id),
        achievement_id INTEGER REFERENCES achievements(id),
        date_earned TIMESTAMP
    );
    '''

    # Executar o comando SQL para criar a tabela player_achievements
    cursor.execute(create_player_achievements_table_query)
    print("Tabela 'player_achievements' criada com sucesso.")

    cursor.close()
    conn.close()
    print("Conexão ao PostgreSQL fechada.")

except psycopg.Error as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")
