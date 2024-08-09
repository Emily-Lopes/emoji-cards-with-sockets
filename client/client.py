import threading
from collections import Counter
import json
from listenServer import ListenServer
import ast

class Client(ListenServer):
    def __init__(self, server_ip="127.0.0.1", server_porta=5000):
        super().__init__(server_ip, server_porta)
        #self.username = None

    def get_username(self):
        return self.username


    def __verificar_condicao_baralho(self, baralho):
        if len(baralho) != 9:
            return False, "Baralho deve ter 9 cartas"
        contagem = Counter(baralho)
        for count in contagem.values():
            if count > 3:
                return False, "Teve ter no máximo 3 cartas da mesma emoção"
        return True, None
    

    def __manipular_baralhos(self, baralhos):
        lista_baralho = []
        if baralhos == '':
            return lista_baralho
        if '-' in baralhos:
            baralhos_aux = baralhos.split('-')
        else:
            baralhos_aux = [baralhos]
        baralhos_aux = baralhos.split('-')
        for baralho in baralhos_aux:
            #lista_baralho.append(self.__adicionar_caminho_cartas(baralho))
            lista_baralho.append(baralho.split(','))
        return lista_baralho


    def criar_conta(self, username, senha):
        try:
            client = self.criar_conexao()
            request = f"criar_conta,{username},{senha}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response == "Usuário adicionado com sucesso!":
                return True, response
            return False, response
        except Exception as e:
            print(f"Erro ao criar conta: {e}")
            return False, None
        finally:
            if client:
                self.fechar_conexao(client)


    def login(self, username, senha):
        try:
            client = self.criar_conexao()
            request = f"login,{username},{senha}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            port, response = response.split(",")
            if response == "Login feito com sucesso!":
                self.username = username
                client_ip, client_port = client.getsockname()
                client_port = port
                client.close()
                #self.fechar_conexao(client)                 
                listen_thread = threading.Thread(target=self.handle_server, args=(client_ip, client_port))
                listen_thread.daemon = True
                listen_thread.start()
                return True, response
            return False, response
        except Exception as e:
            self.fechar_conexao(client)
            print(f"Erro ao realizar login:\n{e}")
            return False, None


    def logout(self):
        try:
            client = self.criar_conexao()
            request = f"logout,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response == 'Logout feito com sucesso!':
                return True, response
            return False, response
        
        except Exception as e:
            print(f"Erro  ao realizar logout:\n{e}")
            return False, None
        finally:
            if client:
                self.fechar_conexao(client)


    def exibir_perfil(self):
        try:
            client = self.criar_conexao()
            request = f"exibir_perfil,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            try:
                data = json.loads(response)
                if isinstance(data, dict):
                    response = data
                else:
                    return False, response
            except json.JSONDecodeError:
                # Se não for JSON, trata como string
                return False, response
            qtd_baralhos = int(response.get('qtd_baralhos'))
            colecao_cartas = response.get('colecao_cartas').split(',')
            baralhos = self.__manipular_baralhos(response.get('baralhos'))
            perfil = {
                'colecao_cartas': colecao_cartas,
                'baralhos': baralhos,
                'qtd_baralhos': qtd_baralhos
            }
            return True, perfil
        except Exception as e:
            print(f"Erro  ao exibir o perfil do usuário:\n{e}")
            return False, None
        finally:
            if client:
                self.fechar_conexao(client)


    def adicionar_baralho(self, baralho):
        confirmacao, mensagem = self.__verificar_condicao_baralho(baralho)
        if not confirmacao:
            return confirmacao, mensagem
        try:
            client = self.criar_conexao()
            baralho = ",".join(baralho)
            request = f"adicionar_baralho,{self.username},{baralho}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response == "Baralho adicionado com sucesso":
                return True, response
            return False, response
        except Exception as e:
            print(f"Erro  ao adicionar baralho:\n{e}")
            return False, None
        finally:
            if client:
                self.fechar_conexao(client)


    def excluir_baralho(self, indice):
        try:
            client = self.criar_conexao()
            request = f"excluir_baralho,{self.username},{indice}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if ',' not in response:
                return False, response

            resposta, perfil = response.split(',', 1)

            perfil = ast.literal_eval(perfil)
            qtd_baralhos = int(perfil.get('qtd_baralhos'))
            colecao_cartas = perfil.get('colecao_cartas').split(',')
            baralhos = self.__manipular_baralhos(perfil.get('baralhos'))
            perfil = {
                'colecao_cartas': colecao_cartas,
                'baralhos': baralhos,
                'qtd_baralhos': qtd_baralhos
            }

            if resposta == "excluido":
                return True, perfil
            return False, perfil

        except Exception as e:
            print(f"Erro  ao excluir baralho: {e}")
            return False, None
        finally:
            if client:
                self.fechar_conexao(client)

    #Talvez mudar o nome da função para: exibir_colecao; Mais facil identificar
    def montar_baralho(self):
        try:
            client = self.criar_conexao()
            request = f"montar_baralho,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)

            if response not in ("Usuário Não Existe", ""):
                colecao_cartas = response.split(',')
                return True, colecao_cartas
            return False, response
        except Exception as e:
            print(f"Erro  ao adicionar baralho:\n{e}")
            return False, None
        finally:
            if client:
                self.fechar_conexao(client)


    def exibir_baralhos(self):
        try:
            client = self.criar_conexao()
            request = f"exibir_baralhos,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response not in ("Usuário ainda não tem baralhos", "Usuário não encontrado."):
                baralhos = self.__manipular_baralhos(response)
                return True, baralhos
            return False, response
        except Exception as e:
            print(f"Erro  ao exibir baralhos:\n{e}")
            return None
        finally:
            if client:
                self.fechar_conexao(client)


    def criar_partida(self, username2, username3):
        try:
            client = self.criar_conexao()
            request = f"criar_partida,{self.username},{username2},{username3}"
            self.enviar_dados(client, request)
            #response = self.receber_dados(client)
            # if response == "True":
            #     return True
            # return False
        except Exception as e:
            print(f"Erro ao tentar criar partida:\n{e}")
            return False
        finally:
            if client:
                self.fechar_conexao(client)

