from client.client import Client
import threading
import random
import time

class Interface:
    def __init__(self, client: Client):
        self.client = client
        self.username = None

        self.listen_thread = threading.Thread(target=self.verificar_mensagem, daemon=True)
        self.listen_thread.start()
        

    def verificar_mensagem(self):
        while True:
            if self.client.mensagem_servidor is not None:
                request = self.client.mensagem_servidor
                print(f"\nMensagem recebida: \n{request}")

                if request.startswith('convite'):
                    _, username_dono, id_partida = request.split(',')
                    resposta = "aceito"
                    self.client.responder_convite(resposta, id_partida)
                
                elif request.startswith('partida_criada'):
                    _, id_partida, baralhos = request.split(',', 2)
                    self.client.responder_partida_criada(id_partida, baralhos)

                elif request.startswith('atributo_turno'):
                    emocoes = ['autoestima', 'raiva', 'alegria', 'tristeza', 'medo', 'amor', 'desgosto', 'surpresa', 'desprezo', 'gratidao']
                    emocao = random.choice(emocoes)
                    print(f'Fiz minha jogada: {emocao}')
                    _, atributo, id_partida = request.split(',')
                    self.client.responder_jogada_turno(emocao, id_partida)
                
                elif request.startswith('fim_turno'):
                    emocoes = ['autoestima', 'raiva', 'alegria', 'tristeza', 'medo', 'amor', 'desgosto', 'surpresa', 'desprezo', 'gratidao']
                    emocao = random.choice(emocoes)
                    print(f'Fiz minha jogada: {emocao}')
                    _, vencedor, carta_vencedor, atributo, id_partida = request.split(',')
                    self.client.responder_jogada_turno(emocao, id_partida)
                
                elif request.startswith('fim_partida'):
                    _, vencedor, carta_adicionada = request.split(',')
                    print(f'recebi do server: fim_partida, vencedor: {vencedor}, carta ganha: {carta_adicionada}')
                    print(f'PARTIDA ACABOU: vencedor: {vencedor}')

                elif request.startswith('fim_partida_empate'):
                    _, vencedor, carta_adicionada = request.split(',')
                    print(f'recebi do server: fim_partida, vencedor: {vencedor}, carta ganha: {carta_adicionada}')
                    print(f'PARTIDA ACABOU: vencedor: {vencedor}')

                elif request.startswith('Erro ao gerenciar a partida'):
                    print(request)


                self.client.mensagem_servidor = None
            time.sleep(1)


    def criar_conta(self):
        username = input("Username: ")
        senha = input("Senha: ")
        condicao, response = self.client.criar_conta(username, senha)
        print(f"{condicao}\n{response}\n")
    
    def login(self):
        username = input("Username: ")
        senha = input("Senha: ")
        condicao, response = self.client.login(username, senha)
        print(f"{condicao}\n{response}\n")

    def logout(self):
        condicao, response = self.client.logout()
        print(f"{condicao}\n{response}\n")

    def exibir_perfil(self):
        condicao, response = self.client.exibir_perfil()
        print(f"{condicao}\n{response}\n")


    def adicionar_baralho(self):
        #baralho = 'autoestima,raiva,alegria,tristeza,medo,amor,desgosto,surpresa,desprezo'
        baralho = ["autoestima","raiva","alegria","tristeza","medo","amor","desgosto","surpresa","desprezo"]
        condicao, response = self.client.adicionar_baralho(baralho)
        print(f"{condicao}\n{response}\n")
    
    def excluir_baralho(self):
        indice = 0
        indice = int(input("Indice do baralho para excluir: "))
        condicao, response = self.client.excluir_baralho(indice)
        print(f"{condicao}\n{response}\n")

    def exibir_colecao(self):
        condicao, response = self.client.montar_baralho()
        print(f"{condicao}\n{response}\n")

    def exibir_baralhos(self):
        condicao, response = self.client.exibir_baralhos()
        print(f"{condicao}\n{response}\n")
    
    def montar_baralho(self):
        condicao, response = self.client.montar_baralho()
        print(f"{condicao}\n{response}\n")

    def criar_partida(self):
        username1 = input("username1: ")
        username2 = input("username2: ")
        resposta = self.client.criar_partida(username1, username2)
        print(f"{resposta}")

