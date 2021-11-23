# HOW TO BUILD
docker-compose build --pull
docker-compose up -d --quiet-pull --build

# MYSQL
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest