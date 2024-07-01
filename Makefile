USER_DB=postgres
PASSWORD_DB=abcXecole42
NAME_DB=asteroid
NAME_CONTAINER=asteroids_postgres

all:
	docker-compose up -d
	sleep 3

# python3 ./backend/postgres/backend.py
	./services/airbyte/src/run-ab-platform.sh

init:
	git submodule init
	git submodule update
	python3 -m venv venv
# source ./venv/bin/activate
# pip3 install -r requirements.txt

run:
	python ./frontend/frontend.py

access_db:
	docker exec -it $(NAME_CONTAINER) psql -U $(USER_DB) -d $(NAME_DB)

clean:
	docker-compose down
	(cd ./services/airbyte/src ; docker-compose down)

fclean: clean
	docker container prune -f
	@docker rmi -f $(shell docker images -q)
	@docker volume rm -f $(shell docker volume ls -q)

re: fclean all

.PHONY: all init run access_db clean fclean re