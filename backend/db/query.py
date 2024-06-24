import psycopg as psycopg
import backend.db.constants as const

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
    cursor.execute(const.CREATE_PLAYERS_TABLE_QUERY)
    print("Tabela 'players' criada com sucesso.")


def build_high_scores_table(cursor):
    """build_high_scores_table
        Método que cria a tabela de pontuações
        :param cursor: Cursor
    """
    cursor.execute(const.CREATE_HIGH_SCORES_TABLE_QUERY)
    print("Tabela 'high_scores' criada com sucesso.")


def build_score_history_table(cursor):
    """build_score_history_table
        Método que cria a tabela de histórico de pontuações
        :param cursor: Cursor
    """
    cursor.execute(const.CREATE_SCORE_HISTORY_TABLE_QUERY)
    print("Tabela 'score_history' criada com sucesso.")


def build_create_achievements_table(cursor):
    """build_create_achievements_table
        Método que cria a tabela de conquistas
        :param cursor: Cursor
    """
    cursor.execute(const.CREATE_ACHIEVEMENTS_TABLE_QUERY)
    print("Tabela 'achievements' criada com sucesso.")


def build_player_achievements_table(cursor):
    """build_player_achievements_table
        Método que cria a tabela de conquistas dos jogadores
        :param cursor: Cursor
    """
    cursor.execute(const.CREATE_PLAYERS_ACHIEVEMENTS_TABLE_QUERY)
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
    scores = score_achievement(player_name, score)
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
    count = get_count_games_player(player_name)
    return games_played.get(count, False)


def get_count_games_player(player_name):
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f"""SELECT get_count_games_player('{player_name}')"""
    cursor.execute(query)
    result = cursor.fetchone()
    count_games = 0 if len(result) == 0 else result[0]
    cursor.close()
    conn.close()
    return count_games


def get_highest_score_player(player_name):
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    query = f"""SELECT get_highest_score_player('{player_name}')"""
    cursor.execute(query)
    result = cursor.fetchone()
    highest_score = 0 if len(result) == 0 else result[0]
    cursor.close()
    conn.close()
    return highest_score


def score_achievement(player_name, score):
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
    highest_score = get_highest_score_player(player_name)
    result = [key for key in score_achieved.keys() if key <= score and key > highest_score]
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
        {const.CREATE_PROCEDURE_UPDATE_DB}
        {const.CREATE_PROCEDURE_INSERT_PLAYERS}
        {const.CREATE_PROCEDURE_INSERT_SCORE_HISTORY}
        {const.CREATE_PROCEDURE_UPDATE_HIGH_SCORE}
        {const.CREATE_TRIGGER_UPDATE_HIGH_SCORE}
        {const.CREATE_PROCEDURE_GET_HIGHEST_SCORE_PLAYER}
        {const.CREATE_PROCEDURE_GET_COUNT_GAMES_PLAYER}
    '''
    cursor.execute(query)
    cursor.close()
    conn.close()
