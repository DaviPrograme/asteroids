USER_DB=postgres
PASSWORD_DB=abcXecole42
NAME_DB=asteroid
NAME_CONTAINER=asteroids_postgres

all:
	docker volume create asteroids_data
	docker run --name $(NAME_CONTAINER) -e POSTGRES_PASSWORD=$(PASSWORD_DB) -e POSTGRES_DB=$(NAME_DB) -p 9090:5432 -v asteroids_data:/var/lib/postgresql/data -d postgres
	sleep 3
	python ./backend/backend.py

run:
	python ./frontend/frontend.py

access_db:
	docker exec -it $(NAME_CONTAINER) psql -U $(USER_DB) -d $(NAME_DB)

clean:
	docker stop $(NAME_CONTAINER)

fclean: clean
	docker rm $(NAME_CONTAINER)
	docker volume rm asteroids_data
	docker rmi postgres

re: fclean all

.PHONY: all run access_db clean fclean re