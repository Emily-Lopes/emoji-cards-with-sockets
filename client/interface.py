class Interface:
    def __init__(self, cliente):
        self.cliente = cliente
        self.username = None
        self.cliente.set_convite(self.manipular_convite)


    def manipular_convite(self, host, id_partida):
        print(f"Convite de partida do usuario: {host}")
        return f'resposta_convite,{self.username},{id_partida},aceito'

    def simula(self, username, senha):
        self.username = username
        condicao, response = self.cliente.criar_conta(username, senha)
        print(f"{condicao}\n{response}\n")

        condicao, response = self.cliente.login(username, senha)
        print(f"{condicao}\n{response}\n")

        # condicao, response = self.cliente.logout()
        # print(f"{condicao}\n{response}\n")

        condicao, response = self.cliente.exibir_perfil()
        print(f"{condicao}\n{response}\n")

        baralho = 'emocao1,emocao2,emocao3'
        condicao, response = self.cliente.adicionar_baralho(baralho)
        print(f"{condicao}\n{response}\n")

        condicao, response = self.cliente.excluir_baralho(0)
        print(f"{condicao}\n{response}\n")

    def criar_partida(self, username1, username2):
        resposta = self.cliente.criar_partida(username1, username2)
        print(f"{resposta}")