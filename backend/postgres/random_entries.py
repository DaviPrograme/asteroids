import random
from db.query import update_db, dbname, user, password, host, port
import psycopg


names_list = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
def random_entries(plays):
    """random_entries
        Método que insere valores aleatórios nas tabelas
        :param plays: numero de jogadas
    """
    for _ in range(plays):
        random_score = random.randint(0, 10000)
        random_name = random.choice(names_list)
        update_db(random_name, random_score)


def change_date(day):
    """change_date
        Método que atualiza a data
        :param name: Nome do jogador
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
    date = f"2024-06-{day} 14:37:39.776"
    id = random.randint(1, 9)

    cursor.execute(f'''
    WITH rows AS (
        SELECT id
        FROM score_history
        WHERE player_id = {id}
        LIMIT 10
    )
    UPDATE score_history
    SET date = '{date}'
    WHERE id IN (SELECT id FROM rows);
    ''')
    cursor.close()
    conn.close()


if __name__ == "__main__":

    for day in range(26, 30):
        random_entries(30)
        for _ in range(30):
            print(f"Changing date to 2024-06-{day}")
            change_date(day)