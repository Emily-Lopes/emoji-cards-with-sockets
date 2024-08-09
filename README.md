# emoji-cards

###
Para facilitar a execução do sistema distribuído foi utilizando docker. Portanto, antes de excutar é preciso ter Docker configurado na máquina e é recomendado que o sistema operacional seja Linux.

O arquivo docker-compose.yml tem um conteiner para o servidor de banco de dados, um conteiner para o servidor de aplicação e três conteiners para três clientes, já que para jogar uma partida é preciso ter no mínimo três jogadores.


> No Linux, primeiramente, é preciso executar o comando abaixo antes de
> executar os containers para liberar o acesso do seu display ao Docker:
```
$ xhost +local:*
```

> Se for a primeira execução,  é preciso usar o comando abaixo para preparar as imagens remotas:
```
$ docker compose build
```

> Em seguida, basta utilizar o comando abaixo para inicar os containers descritos no `docker-compose.yml`:
```
$ docker compose up
```

> Para interromper e destuir os containers basta utilizar o comando:
```
$ docker compose down
```

>Observações: No banco de dados já existem três usuários cadatrados:
```
|--------------|--------------|
|   username   |    senha     |
|--------------|--------------|
|    thais     |   12345678   |
|   henrique   |   12345678   |
|    aluno     |   12345678   |
|--------------|--------------|

```
