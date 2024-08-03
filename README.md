# emoji-cards

###
para executar com docker:
primeiro:
```
$ docker compose build
```
que baixa as imagens do remoto e excuta os comandos dos arquivos DockerFile, ou seja, prepara as imagens pra gente mas não executa elas ainda


depois de ter elas 'compiladas':
```
$ docker compose up
```
que vai realmente ligar os processos e colocar eles em execução

e tem o 
```
$ docker compose down
```
que vai parar os processos e destruir os conteiners

