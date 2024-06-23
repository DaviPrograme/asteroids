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


CREATE OR REPLACE FUNCTION get_highest_score_player(play_name TEXT)
RETURNS INTEGER
AS $$
DECLARE
    play_id INTEGER;
    last_game_date DATE;
    high_score_date DATE;
    high_score_player INTEGER;
BEGIN
    SELECT id INTO play_id FROM players WHERE player_name = play_name;
    SELECT date INTO last_game_date FROM score_history WHERE id = play_id ORDER BY date DESC LIMIT 1;
    SELECT date INTO  high_score_date FROM high_scores WHERE id = play_id LIMIT 1;

    IF high_score_date = last_game_date THEN
        SELECT id, score INTO play_id, high_score_player FROM score_history WHERE player_id = play_id ORDER BY id DESC OFFSET 1 LIMIT 1;
    ELSE
         SELECT score INTO high_score_player FROM high_scores WHERE player_id = play_id;
    END IF;
    RETURN high_score_player;
END;
$$ LANGUAGE plpgsql;


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

