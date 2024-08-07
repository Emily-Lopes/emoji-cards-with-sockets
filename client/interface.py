from cliente import Client

class Interface:
    def __init__(self, client: Client):
        self.client = client
        self.username = None
        self.client.set_convite(self.manipular_convite)


    def manipular_convite(self, host, id_partida):
        print(f"Convite de partida do usuario: {host}")
        return f'resposta_convite,{self.username},{id_partida},aceito'

    def simula(self, username, senha):
        self.username = username
        condicao, response = self.client.criar_conta(username, senha)
        print(f"{condicao}\n{response}\n")

        # condicao, response = self.client.login(username, senha)
        # print(f"{condicao}\n{response}\n")

        # # condicao, response = self.client.logout()
        # # print(f"{condicao}\n{response}\n")

        # condicao, response = self.client.exibir_perfil()
        # print(f"{condicao}\n{response}\n")

        # baralho = 'emocao1,emocao2,emocao3'
        # condicao, response = self.client.adicionar_baralho(baralho)
        # print(f"{condicao}\n{response}\n")

        # condicao, response = self.client.excluir_baralho(0)
        # print(f"{condicao}\n{response}\n")

    def criar_partida(self, username1, username2):
        resposta = self.client.criar_partida(username1, username2)
        print(f"{resposta}")