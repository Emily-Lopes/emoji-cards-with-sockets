import socket
import threading
import os
import random
import json
import time

# {username: {ip: <endereço_ip>, porta: <porta>}}
online_users = {}

db_host = os.getenv('DB_SERVER_HOST', 'localhost')  # db-server
db_port = int(os.getenv('DB_SERVER_PORT', 6000))   # 6000

# {id_parida: {username1: <resposta>, username2: <resposta>}}
partidas = {}
id_partida = -1

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"received request: {request}")

        if request.startswith('criar_conta'):
            _, username, senha = request.split(',')
            confirmation = criar_conta(username, senha)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('login'):
            _, username, senha = request.split(',')
            client_ip, client_port = client_socket.getpeername()
            confirmation = login(username, senha, client_ip, client_port)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('logout'):
            _, username = request.split(',')
            confirmation = logout(username)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('adicionar_baralho'):
            _, username, baralho = request.split(',', 2)
            confirmation = adicionar_baralho(username, baralho)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('excluir_baralho'):
            _, username, indice = request.split(',')
            confirmation = excluir_baralho(username, indice)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('adicionar_carta'):
            _, username, carta = request.split(',')
            confirmation = adicionar_carta_colecao(username, carta)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('exibir_perfil'):
            _, username = request.split(',')
            confirmation = exibir_perfil(username)
            
            if isinstance(confirmation, dict):
                confirmation = json.dumps(confirmation) 

            client_socket.send(confirmation.encode('utf-8')) 

        if request.startswith('montar_baralho'):
            _, username = request.split(',')
            confirmation = montar_baralho(username)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('exibir_baralhos'):
            _, username = request.split(',')
            confirmation = exibir_baralhos(username)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('criar_partida'):
            _, username_dono, username2, username3 = request.split(',')
            confirmation = criar_partida(username_dono, username2, username3)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('resposta_convite'):
            #resposta_convite,username,id_partida,aceito
            _, username, id_partida, resposta = request.split(',')
            partidas[int(id_partida)][username] = resposta

    except Exception as e:
        print(f"error handling client: {e}")
    finally:
        client_socket.close()

# GERENCIAMENTO DAS REQUISIÇÕES
def criar_conta(username, senha):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"verificar_username {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

        if response == 'Username está disponível!':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                bd_client.send("cartas_disponiveis".encode('utf-8'))
                cartas_response = bd_client.recv(1024).decode('utf-8')

            if cartas_response != "Nenhuma Carta Cadastrada":
                vetor_nome_emocoes = cartas_response.split(',')

                if len(vetor_nome_emocoes) >= 9:
                    cartas_sorteadas = random.sample(vetor_nome_emocoes, 9)
                    cartas = ','.join(cartas_sorteadas) 
                else:
                    return "Não há cartas suficientes para criar a conta."
            else:
                return "Nenhuma carta disponível para sortear."

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                request = f"adicionar_usuario {username} {senha} {cartas}"  
                bd_client.send(request.encode('utf-8'))
                response = bd_client.recv(1024).decode('utf-8')
    
    return response

def login(username, senha, client_ip, client_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"verificar_login {username} {senha}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

        if response == 'Login Correto!':
            online_users[username] = {'ip': client_ip, 'porta': client_port}

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                request = f"set_status {username} online"
                bd_client.send(request.encode('utf-8'))
                response = bd_client.recv(1024).decode('utf-8')
    
                response = f"{client_port},Login feito com sucesso!"

    print(online_users)
    return response

def logout(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"get_status {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

        if response != 'Usuário não encontrado':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                request = f"set_status {username} offline"
                bd_client.send(request.encode('utf-8'))
                response = bd_client.recv(1024).decode('utf-8')
                
                if username in online_users:
                    del online_users[username]
    
                response = 'Logout feito com sucesso!'

    print(online_users)
    return response

def adicionar_baralho(username, baralho):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"get_qtd_baralhos {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

        if response != 'Usuário não encontrado':
            qtd_baralhos = response

            if qtd_baralhos == 3:
                response = 'Quantidade máxima de baralhos atingida!'
                return response

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                request = f"adicionar_baralho {username} {baralho}"
                bd_client.send(request.encode('utf-8'))
                response = bd_client.recv(1024).decode('utf-8')

    return response

def excluir_baralho(username, indice):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"get_qtd_baralhos {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

        if response != 'Usuário não encontrado':
            qtd_baralhos = response

            if qtd_baralhos == 0:
                response = 'Não existem baralhos para excluir!'
                return response

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                request = f"excluir_baralho {username} {indice}"
                bd_client.send(request.encode('utf-8'))
                response = bd_client.recv(1024).decode('utf-8')

    return response

def adicionar_carta_colecao(username, carta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"adicionar_carta_na_colecao {username} {carta}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

    return response

def exibir_perfil(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"buscar_usuario {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

    if response == "Usuário não encontrado":
        return response
    
    try:
        user_data = eval(response)
        filtered_data = {
            'colecao_cartas': user_data.get('colecao_cartas'),
            'baralhos': user_data.get('baralhos'),
            'qtd_baralhos': user_data.get('qtd_baralhos')
        }
        return filtered_data
    
    except Exception as e:
        return f"erro ao processar a resposta: {str(e)}"
    
def montar_baralho(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"get_colecao {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

    return response

def exibir_baralhos(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"get_baralhos {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

    return response

def convidar_jogador(username, host, id_partida):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"buscar_usuario {username}"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

        if response != 'Usuário não encontrado':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                bd_client.connect((db_host, db_port))
                request = f"get_status {username}"
                bd_client.send(request.encode('utf-8'))
                response = bd_client.recv(1024).decode('utf-8')

                if response == 'online':
                    enviar_mensagem(username, f'convite_partida,{host},{id_partida}')

def criar_partida(username_dono, username2, username3):
    
    global id_partida
    id_partida += 1
    id = id_partida

    partidas[id] = {}
    def convidar_jogador_thread(username,username_dono,id):
        convidar_jogador(username,username_dono,id)

    threads = []
    for username in [username2, username3]:
        thread = threading.Thread(target=convidar_jogador_thread, args=(username,username_dono,id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    inicio = time.time()
    fim = inicio
    while(fim - inicio < 10):
        info_partida = partidas[id]

        if len(info_partida.keys()) == 2:
            if info_partida[username2] == 'aceito' and info_partida[username3] == 'aceito':
                mensagem = 'preparando'
                for username in [username_dono, username2, username3]:
                    enviar_mensagem(username, mensagem) # todos vão pra tela preparando e userdono envia uma requisição pro server pra preparar partida
                    jogador_jogando(username) # todos agora estao jogando
                return
            else:
                break

        fim = time.time()

    mensagem = 'nao foi possivel criar partida'
    enviar_mensagem(username_dono, mensagem) # sai da aguardando pro inicio

# FUNÇÕES AUXILIARES
def enviar_mensagem(username, mensagem):

    print(f'tentando mandar: {mensagem}')

    if username in online_users:
        ip = online_users[username]['ip']
        porta = online_users[username]['porta']
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, porta))
        client_socket.send(mensagem.encode('utf-8'))
        print('tudo certo enviando!')

def jogador_jogando(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
        bd_client.connect((db_host, db_port))
        request = f"set_status {username} jogando"
        bd_client.send(request.encode('utf-8'))
        response = bd_client.recv(1024).decode('utf-8')

    return response

def selecionar_atributo():
    emocoes = []

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
            bd_client.connect((db_host, db_port))
            bd_client.send("cartas_disponiveis".encode('utf-8'))
            cartas_response = bd_client.recv(1024).decode('utf-8')

            if cartas_response != "Nenhuma Carta Cadastrada":
                emocoes = cartas_response.split(',')

                emocao_aleatoria = random.choice(emocoes)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bd_client:
                    bd_client.connect((db_host, db_port))
                    request = f"atributos_carta {emocao_aleatoria}"
                    bd_client.send(request.encode('utf-8'))
                    response = bd_client.recv(1024).decode('utf-8')

                    if response != 'Carta não existe!':
                        dicionario_atributos = eval(response)
                        atributo_aleatorio = random.choice(list(dicionario_atributos.keys()))

                        return atributo_aleatorio

    except Exception as e:
        return f"erro na seleção de atributo: {str(e)}"
    

# SERVIDOR DE APLICAÇÃO
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen()
    print("servidor ouvindo na porta 5000...")

    while True:
        client_socket, addr = server.accept()
        print(f"conexão aceita de {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
