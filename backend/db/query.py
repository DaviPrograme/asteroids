import psycopg as psycopg

host = "localhost"
port = "9090"
dbname = "asteroid"
user = "postgres"
password = "abcXecole42"


def build_player_table(cursor):
    create_players_table_query = '''
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL
    );
    '''
    cursor.execute(create_players_table_query)
    print("Tabela 'players' criada com sucesso.")

def build_high_scores_table(cursor):
    create_high_scores_table_query = '''
    CREATE TABLE IF NOT EXISTS high_scores (
        id SERIAL PRIMARY KEY,
        player_id INTEGER UNIQUE REFERENCES players(id),
        score INTEGER,
        date TIMESTAMP
    );
    '''
    cursor.execute(create_high_scores_table_query)
    print("Tabela 'high_scores' criada com sucesso.")

def build_score_history_table(cursor):
    create_score_history_table_query = '''
    CREATE TABLE IF NOT EXISTS score_history (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        date TIMESTAMP
    );
    '''
    cursor.execute(create_score_history_table_query)
    print("Tabela 'score_history' criada com sucesso.")

def build_create_achievements_table(cursor):
    create_achievements_table_query = '''
    CREATE TABLE IF NOT EXISTS achievements (
        id SERIAL PRIMARY KEY,
        achievement_name VARCHAR(100),
        description TEXT
    );
    '''
    cursor.execute(create_achievements_table_query)
    print("Tabela 'achievements' criada com sucesso.")

def build_player_achievements_table(cursor):
    create_player_achievements_table_query = '''
    CREATE TABLE IF NOT EXISTS player_achievements (
        player_id INTEGER REFERENCES players(id),
        achievement_id INTEGER REFERENCES achievements(id),
        date_earned TIMESTAMP
    );
    '''
    cursor.execute(create_player_achievements_table_query)
    print("Tabela 'player_achievements' criada com sucesso.")

def table_insert(table_name, columns, values):
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f'''
    INSERT INTO {table_name} ({columns})
    VALUES ({values});
    '''
    cursor.execute(query)

def table_upsert(table_name, columns, values, conflict_target, updates):
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f"""
    INSERT INTO {table_name} ({columns}) VALUES ({values})
    ON CONFLICT ({conflict_target})
    DO UPDATE SET {updates}
    """
    cursor.execute(query)