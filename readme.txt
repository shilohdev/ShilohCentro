# HOW TO BUILD
docker-compose build --pull
docker-compose up -d --quiet-pull --build

# MYSQL
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=104da04a0895b21318d2b2d3600ce2c61231 -d mysql:latest
docker run --name some-mysql -p 3306:3306 -e

MYSQL_ROOT_PASSWORD=104da04a0895b21318d2b2d3600ce2c61231 -d mysql:latest

# PASSOS PARA ATUALIZAR O PROJETO.
Zip o projeto C:\projects\shiloh
Entre no SSH Google, clique na engrenagem, clique em Fazer upload do arquivo, dê upload no projeto.zip e copie o texto upload.txt e cole no ssh.
