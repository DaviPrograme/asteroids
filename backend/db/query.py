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
    cursor.close()
    conn.close()

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
    cursor.close()
    conn.close()


def is_player_highest_score(player_name, score):
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f"""SELECT * FROM score_history as s JOIN players as p ON (p.id = s.player_id) WHERE player_name = '{player_name}' AND score > {score}"""
    cursor.execute(query)
    rows = cursor.fetchall()
    # ret = False if len(rows) > 0 else True
    cursor.close()
    conn.close()
    return False if len(rows) > 0 else True


def insert_new_player_highest_score(player_name, score):
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query_identify = f"""select * from players as p join high_scores as h on (p.id = h.player_id) where player_name = '{player_name}'"""
    cursor.execute(query_identify)
    rows = cursor.fetchall()
    if len(rows) == 0 :
        query = f"""
        INSERT INTO high_scores (player_id, score, date)
        VALUES ((select id from players where player_name = %s order by id desc limit 1), %s, CURRENT_TIMESTAMP)
        """
    else:
        _id = rows[0][2]
        query = f"""
        UPDATE high_scores 
        SET player_id = (SELECT id FROM players WHERE player_name = %s ORDER BY id DESC LIMIT 1), score = %s, date = CURRENT_TIMESTAMP 
        WHERE id = {_id}
        """
    cursor.execute(query, (player_name, score))
    cursor.close()
    conn.close()
