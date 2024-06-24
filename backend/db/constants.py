
CREATE_PLAYERS_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL
    );
'''

CREATE_HIGH_SCORES_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS high_scores (
        id SERIAL PRIMARY KEY,
        player_id INTEGER UNIQUE REFERENCES players(id),
        score INTEGER,
        date TIMESTAMP
    );
'''


CREATE_SCORE_HISTORY_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS score_history (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        date TIMESTAMP
    );
'''


CREATE_ACHIEVEMENTS_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS achievements (
        id SERIAL PRIMARY KEY,
        achievement_name VARCHAR(100),
        description TEXT
    );
'''


CREATE_PLAYERS_ACHIEVEMENTS_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS player_achievements (
        player_id INTEGER REFERENCES players(id),
        achievement_id INTEGER REFERENCES achievements(id),
        date_earned TIMESTAMP
    );
'''

CREATE_PROCEDURE_UPDATE_DB = '''
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
'''

CREATE_PROCEDURE_INSERT_PLAYERS = '''
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
'''


CREATE_PROCEDURE_INSERT_SCORE_HISTORY = '''
    CREATE OR REPLACE PROCEDURE insert_score_history(play_id INT, new_score INT)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        INSERT INTO score_history (player_id, score, date) VALUES (play_id, new_score, CURRENT_TIMESTAMP);
        COMMIT;
    END;
    $$;
'''

CREATE_PROCEDURE_UPDATE_HIGH_SCORE = '''
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
 '''


CREATE_TRIGGER_UPDATE_HIGH_SCORE = '''
    CREATE TRIGGER trigger_update_high_score
    AFTER INSERT ON score_history
    FOR EACH ROW
    EXECUTE FUNCTION update_high_score();
 '''


CREATE_PROCEDURE_GET_HIGHEST_SCORE_PLAYER = '''
    CREATE OR REPLACE FUNCTION get_highest_score_player(play_name TEXT)
    RETURNS INTEGER
    LANGUAGE plpgsql
    AS $$
    DECLARE
        play_id INTEGER;
        last_game_date TIMESTAMP;
        high_score_date TIMESTAMP;
        high_score_player INTEGER;
        count_games INTEGER;
    BEGIN
        -- Obtém o id do jogador
        SELECT id INTO play_id FROM players WHERE player_name = play_name;

        -- Obtém a data do último jogo
        SELECT date INTO last_game_date 
        FROM score_history 
        WHERE player_id = play_id 
        ORDER BY date DESC 
        LIMIT 1;

        -- Obtém a data do high score
        SELECT date INTO high_score_date 
        FROM high_scores 
        WHERE player_id = play_id 
        ORDER BY date DESC
        LIMIT 1;

        -- Obtém a contagem de jogos do jogador
        SELECT get_count_games_player(play_name) INTO count_games;

        -- Condicional baseado nas datas e na contagem de jogos
        IF high_score_date = last_game_date AND count_games > 1 THEN
            SELECT score INTO high_score_player 
            FROM score_history 
            WHERE player_id = play_id 
            ORDER BY date DESC 
            OFFSET 1 LIMIT 1;
        ELSIF count_games = 1 THEN
            high_score_player := 0;
        ELSE
            SELECT score INTO high_score_player 
            FROM high_scores 
            WHERE player_id = play_id;
        END IF;

        RETURN high_score_player;
    END;
    $$;
'''


CREATE_PROCEDURE_GET_COUNT_GAMES_PLAYER = '''
    CREATE OR REPLACE FUNCTION get_count_games_player(play_name TEXT)
    RETURNS INTEGER
    AS $$
    DECLARE
        play_id INTEGER;
        count_games INTEGER;
    BEGIN
        SELECT id INTO play_id FROM players WHERE player_name = play_name;
        SELECT count(*) INTO count_games FROM score_history WHERE player_id = play_id;
        RETURN count_games;
    END;
    $$ LANGUAGE plpgsql;
'''