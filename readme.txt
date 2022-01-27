# HOW TO BUILD
docker-compose build --pull
docker-compose up -d --quiet-pull --build

# MYSQL
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=shilohcentro2022 -d mysql:latest
docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=104da04a0895b21318d2b2d3600ce2c61231 -d mysql:latest