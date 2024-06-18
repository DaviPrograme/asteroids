import psycopg
from db.query import build_create_achievements_table, build_high_scores_table, build_player_table, build_player_achievements_table, build_score_history_table

# Dados de conexão
host = "localhost"
port = "9090"
dbname = "asteroid"
user = "postgres"
password = "abcXecole42"


if __name__ == "__main__":
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
        build_player_table(cursor)
        build_high_scores_table(cursor)
        build_score_history_table(cursor)
        build_create_achievements_table(cursor)
        build_player_achievements_table(cursor)
        cursor.close()
        conn.close()
        print("Conexão ao PostgreSQL fechada.")
    except psycopg.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
