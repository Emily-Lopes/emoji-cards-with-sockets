import socket
import threading
from collections import Counter
import json

class Cliente:
    def __init__(self, server_ip="127.0.0.1", server_porta=5000):
        self.__server_ip = server_ip
        self.__server_porta = server_porta
        self.__buffer = 1024
        self.__username = None

        self.mensagem_servidor = None
    
    def get_username(self):
        return self.__username

    # Funções para manipular o recebimento de convite de uma partida
    def set_convite(self, convite):
        self.convite = convite

    def __ouvir_mensagem_convite(self, client_ip, client_port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', int(client_port)))
            server.listen(1)

            print(f"Cliente escutando em {client_ip}:{client_port}\n")

            while True:
                try:
                    server_socket, addr = server.accept()
                    print(f"Conexão recebida de {addr}")
                    request = server_socket.recv(self.__buffer).decode('utf-8')
                    if request:
                        thread = threading.Thread(target=self.__manipular_mensagem_convite, args=(request,))
                        thread.start()    
                    
                except Exception as e:
                    print(f"Erro ao ouvir mensagem de convite: \n{e}\n")
        except Exception as e:
                    print(f"Erro ao tentar escutar servidor {client_ip}:{client_port} \n{e}")


    def __manipular_mensagem_convite(self, request):
        if request.startswith('convite_partida'):
            _, username_dono, id_partida = request.split(',')
            self.mensagem_servidor = f"convite,{username_dono},{id_partida}"
        
        if request.startswith('partida_criada'):
            self.mensagem_servidor = f"partida_criada,{username_dono},{id_partida}"

    def responder_convite(self, resposta, id_partida): 
        server_socket =  self.__criar_conexao_servidor()
        request = f'resposta_convite,{self.__username},{id_partida},{resposta}'
        server_socket.send(request.encode('utf-8'))

    def __criar_conexao_servidor(self):
        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.__server_ip, self.__server_porta))
            return client
        except Exception as e:
            print(f"Erro ao criar conexao com o servidor:\n{e}")
            return None
    
    def __fechar_conexao_servidor(self, client):
        try: 
            client.close()
        except Exception as e:
            print(f"Erro ao fechar conexao como o servidor:\n{e}")


    def __enviar_dados(self, client, request):
        try:
            client.send(request.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar dados:\n{e}")


    def __receber_dados(self, client):
        try:
            response = client.recv(self.__buffer).decode('utf-8')
            return response
        except Exception as e:
            print("Erro ao receber dados do socket")
            return None
    

    def __verificar_condicao_baralho(self, baralho):
        if len(baralho) != 9:
            return False, "Baralho deve ter 9 cartas"
        contagem = Counter(baralho)
        for count in contagem.values():
            if count > 3:
                return False, "Teve ter no máximo 3 cartas da mesma emoção"
        return True, None
    

    def __adicionar_caminho_cartas(self, cartas):
        cartas = cartas.split(',')
        for i in range(len(cartas)):
            caminho_carta = f"./emocoes/{cartas[i]}.png" # Tem que verificar depois corretamente esse caminho
            cartas[i] = caminho_carta
        return cartas


    def __adicionar_caminho_baralhos(self, baralhos):
        lista_baralho = []
        if baralhos == '':
            return lista_baralho
        if '-' in baralhos:
            baralhos_aux = baralhos.split('-')
        else:
            baralhos_aux = [baralhos]
        baralhos_aux = baralhos.split('-')
        for baralho in baralhos_aux:
            lista_baralho.append(self.__adicionar_caminho_cartas(baralho))
        return lista_baralho

    # Funções a serem usadas pela interface
    def criar_conta(self, username, senha):
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"criar_conta,{username},{senha}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
            if response == "Usuário adicionado com sucesso!":
                self.__username = username
                return True, response
            return False, response
        except Exception as e:
            return False, f"Erro ao criar conta:{str(e)}"
        finally:
            if client:
                self.__fechar_conexao_servidor(client)


    def login(self, username, senha):
        print(username,senha)
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"login,{username},{senha}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
            port, response = response.split(",")
            print(response)
            if response == "Login feito com sucesso!":
                self.__username = username
                client_ip, client_port = client.getsockname()
                client_port = port
                client.close()
                listen_thread = threading.Thread(target=self.__ouvir_mensagem_convite, args=(client_ip, client_port))
                listen_thread.daemon = True
                listen_thread.start()
                return True, response
            return False, response
        except Exception as e:
            return False, f"Erro ao realizar login:{str(e)}"

    def logout(self):
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"logout,{self.__username}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
            if response == 'Logout feito com sucesso!':
                return True, response
            return False, response
        
        except Exception as e:
            print(f"Erro  ao realizar logout:\n{e}")
            return False, None
        finally:
            if client:
                self.__fechar_conexao_servidor(client)


    def exibir_perfil(self):
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"exibir_perfil,{self.__username}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
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
            colecao_cartas = self.__adicionar_caminho_cartas(response.get('colecao_cartas'))
            baralhos = self.__adicionar_caminho_baralhos(response.get('baralhos'))
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
                self.__fechar_conexao_servidor(client)


    def adicionar_baralho(self, baralho):
        confirmacao, mensagem = self.__verificar_condicao_baralho(baralho)
        if not confirmacao:
            return confirmacao, mensagem
        client = None
        try:
            client = self.__criar_conexao_servidor()
            baralho = ",".join(baralho)
            request = f"adicionar_baralho,{self.__username},{baralho}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
            if response == "Baralho adicionado com sucesso":
                return True, response
            return False, response
        except Exception as e:
            print(f"Erro  ao adicionar baralho:\n{e}")
            return False, None
        finally:
            if client:
                self.__fechar_conexao_servidor(client)


    def excluir_baralho(self, indice):
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"excluir_baralho,{self.__username},{indice}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
            if response == "Baralho excluído com sucesso":
                return True, response
            return False, response

        except Exception as e:
            print(f"Erro  ao excluir baralho:\n{e}")
            return False, None
        finally:
            if client:
                self.__fechar_conexao_servidor(client)


    def montar_baralho(self):
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"montar_baralho,{self.__username}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)

            if response not in ("Usuário Não Existe", ""):
                colecao_cartas = self.__adicionar_caminho_cartas(response)
                return True, colecao_cartas
            return False, response
        except Exception as e:
            print(f"Erro  ao adicionar baralho:\n{e}")
            return False, None
        finally:
            if client:
                self.__fechar_conexao_servidor(client)


    def exibir_baralhos(self):
        client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"exibir_baralhos,{self.__username}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client)
            if response not in ("Usuário ainda não tem baralhos", "Usuário não encontrado."):
                baralhos = self.__adicionar_caminho_baralhos(response)
                return True, baralhos
            return False, response
        except Exception as e:
            print(f"Erro  ao exibir baralhos:\n{e}")
            return None
        finally:
            if client:
                self.__fechar_conexao_servidor(client)


    def criar_partida(self, username2, username3):
        # client = None
        try:
            client = self.__criar_conexao_servidor()
            request = f"criar_partida,{self.__username},{username2},{username3}"
            self.__enviar_dados(client, request)
            response = self.__receber_dados(client) #por enquanto criar partida não retorna nada
            # print(response)
            # if response == "True":
            #     return True
            # return False
        except Exception as e:
            print(f"Erro ao tentar criar partida:\n{e}")
            return False
        finally:
            if client:
                self.__fechar_conexao_servidor(client)
