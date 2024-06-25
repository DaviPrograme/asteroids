USER_DB=postgres
PASSWORD_DB=abcXecole42
NAME_DB=asteroid
NAME_CONTAINER=asteroids_postgres

all:
	docker-compose up -d
# sleep 3
# python3 ./backend/backend.py

run:
	python ./frontend/frontend.py

access_db:
	docker exec -it $(NAME_CONTAINER) psql -U $(USER_DB) -d $(NAME_DB)

clean:
	docker stop $(NAME_CONTAINER)

fclean: 
	docker-compose down -v
	docker rmi $(docker images -q)


re: fclean all

.PHONY: all run access_db clean fclean re