#docker exec -it asteroids_postgres psql -U postgres -d asteroid
all:
	docker volume create asteroids_data
	docker run --name asteroids_postgres -e POSTGRES_PASSWORD=abcXecole42 -e POSTGRES_DB=asteroid -p 9090:5432 -v asteroids_data:/var/lib/postgresql/data -d postgres

clean:
	docker stop asteroids_postgres

fclean: clean
	docker rm asteroids_postgres
	docker volume rm asteroids_data
	docker rmi postgres

re: fclean all

.PHONY: all clean fclean re