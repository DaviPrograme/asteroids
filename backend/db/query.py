import psycopg as psycopg

host = "localhost"
port = "9090"
dbname = "asteroid"
user = "postgres"
password = "abcXecole42"


def build_player_table(cursor):
    """build_player_table 
        Método que cria a tabela de jogadores
        :param cursor: Cursor
    """
    create_players_table_query = '''
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL
    );
    '''
    cursor.execute(create_players_table_query)
    print("Tabela 'players' criada com sucesso.")

def build_high_scores_table(cursor):
    """build_high_scores_table
        Método que cria a tabela de pontuações
        :param cursor: Cursor
    """
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
    """build_score_history_table
        Método que cria a tabela de histórico de pontuações
        :param cursor: Cursor
    """
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
    """build_create_achievements_table
        Método que cria a tabela de conquistas
        :param cursor: Cursor
    """
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
    """build_player_achievements_table
        Método que cria a tabela de conquistas dos jogadores
        :param cursor: Cursor
    """
    create_player_achievements_table_query = '''
    CREATE TABLE IF NOT EXISTS player_achievements (
        player_id INTEGER REFERENCES players(id),
        achievement_id INTEGER REFERENCES achievements(id),
        date_earned TIMESTAMP
    );
    '''
    cursor.execute(create_player_achievements_table_query)
    print("Tabela 'player_achievements' criada com sucesso.")


def update_db(player_name, score):
    """update_db 
        Método que atualiza o banco de dados
        :param player_name: Nome do jogador
        :param score: pontuação do jogador
    """
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f'''CALL update_db('{player_name}', {score});'''
    cursor.execute(query)
    cursor.close()
    conn.close()
    achievements_selection(player_name, score)


def table_insert(table_name, columns, values):
    """table_insert
        Método que insere valores em uma tabela
        :param table_name: Nome da tabela
        :param columns: Colunas
        :param values: Valores
    """
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


def count_games_player(player_name):
    """count_games_player
        Método que conta os jogos de um jogador
        :param player_name: Nome do jogador
    """
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f"""select count(*) from score_history as s join players as p on (s.player_id = p.id) where player_name = '{player_name}'"""
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0]


def highest_score_all(score):
    """highest_score_all
        Método que verifica se a pontuação é a maior
        :param score: Pontuação
    """
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f"""select count(*) from high_scores where score > {score}"""
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return True if len(row[0]) == 0 else False

def populate_achievements(cursor):
    """populate_achievements
        Método que popula a tabela de conquistas
        :param cursor: Cursor
    """
    achievements = [
        ("First Game", "First time playing the game"),
        ("First Score", "First time scoring points"),
        ("5 Games", "Played 5 games"),
        ("10 Games", "Played 10 games"),
        ("20 Games", "Played 20 games"),
        ("50 Games", "Played 50 games"),
        ("100 Points", "Scored 100 points"),
        ("500 Points", "Scored 500 points"),
        ("1000 Points", "Scored 1000 points"),
        ("5000 Points", "Scored 5000 points"),
        ("10000 Points", "Scored 10000 points"),

    ]
    for achievement in achievements:
        query = f"""INSERT INTO achievements (achievement_name, description) VALUES ('{achievement[0]}', '{achievement[1]}')"""
        cursor.execute(query)

def achievements_selection(player_name, score):
    """achievements_selection
        Método que seleciona as conquistas
        :param player_name: Nome do jogador
        :param score: Pontuação
    """
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    games = games_achievement(player_name)
    if games:
        table_insert("player_achievements", "player_id, achievement_id, date_earned", f"(SELECT id FROM players WHERE player_name = '{player_name}' ORDER BY id DESC LIMIT 1), (SELECT id FROM achievements WHERE achievement_name = '{games}'), CURRENT_TIMESTAMP")
    scores = score_achievement(score)
    for score in scores:
        print(f"Score: {score}")
        table_insert("player_achievements", "player_id, achievement_id, date_earned", f"(SELECT id FROM players WHERE player_name = '{player_name}' ORDER BY id DESC LIMIT 1), (SELECT id FROM achievements WHERE achievement_name = '{score}'), CURRENT_TIMESTAMP")


def games_achievement(player_name):
    """games_achievement
        Método que verifica a conquista de jogos
        :param player_name: Nome do jogador
    """
    games_played = {
        1: "First Game",
        5: "5 Games",
        10: "10 Games",
        20: "20 Games",
        50: "50 Games",
    }
    count = count_games_player(player_name)
    return games_played.get(count, False)

def score_achievement(score):
    """score_achievement
        Método que verifica a conquista de pontuação
        :param score: Pontuação
    """
    score_achieved = {
        1: "First Score",
        100: "100 Points",
        500: "500 Points",
        1000: "1000 Points",
        5000: "5000 Points",
        10000: "10000 Points",
    }
    result = [key for key in score_achieved.keys() if key <= score]
    if result:
        return [score_achieved[key] for key in result]
    return []


def create_procedures_db(cursor):
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
    CREATE OR REPLACE PROCEDURE update_db(name TEXT, new_score INT)
    LANGUAGE plpgsql
    AS $$
    DECLARE
        play_id INTEGER;
    BEGIN
        play_id := insert_players(name);
        call insert_score_history(play_id, new_score);
    END;
    $$;


    CREATE OR REPLACE FUNCTION insert_players(name TEXT)
    RETURNS INTEGER
    AS $$
    DECLARE
        player_id INTEGER;
    BEGIN
        SELECT id INTO player_id FROM players WHERE player_name = name;
        IF player_id IS NULL THEN
            INSERT INTO players (player_name) VALUES (name);
            SELECT id INTO player_id FROM players WHERE player_name = name;
        END IF;
        RETURN player_id;
    END;
    $$ LANGUAGE plpgsql;


    CREATE OR REPLACE PROCEDURE insert_score_history(play_id INT, new_score INT)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        INSERT INTO score_history (player_id, score, date) VALUES (play_id, new_score, CURRENT_TIMESTAMP);
        COMMIT;
    END;
    $$;


    CREATE OR REPLACE FUNCTION update_high_score()
    RETURNS TRIGGER AS $$
    DECLARE
        high_score_id INTEGER;
        high_score_now INTEGER;
    BEGIN
        SELECT id INTO high_score_id FROM high_scores WHERE player_id = NEW.player_id LIMIT 1;
        IF high_score_id IS NULL THEN
            INSERT INTO high_scores (player_id, score, date)
            VALUES (NEW.player_id, NEW.score, NEW.date);
        ELSE
            SELECT score INTO high_score_now FROM high_scores WHERE id = high_score_id LIMIT 1;
            IF high_score_now < NEW.score THEN
                UPDATE high_scores 
                SET player_id = NEW.player_id, score = NEW.score, date = NEW.date
                WHERE id = high_score_id;
            END IF;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;


    CREATE TRIGGER trigger_update_high_score
    AFTER INSERT ON score_history
    FOR EACH ROW
    EXECUTE FUNCTION update_high_score();
    '''
    cursor.execute(query)
    cursor.close()
    conn.close()
