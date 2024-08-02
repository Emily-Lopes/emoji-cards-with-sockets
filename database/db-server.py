import socket
import threading

import interface #arquivo interface.py vai funcionar como uma biblioteca

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')  # convert bytes to string
    print(f"Received request: {request}")

    if request.startswith('cartas_disponiveis'):
        try:
            _, response = interface.get_emocoes_cadastradas() 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        
    elif request.startswith('atributos_carta'):
        try:
            _, emocao = request.split(' ')
            _, response = interface.get_atributos_carta(emocao) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    
    elif request.startswith('adicionar_usuario'):
        try:
            _, username, senha, cartas = request.split(' ')
            _, response = interface.adicionar_usuario(username, senha, cartas) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('verificar_username'):
        try:
            _, username = request.split(' ')
            _, response = interface.verificar_username_existe(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('verificar_login'):
        try:
            _, username,senha = request.split(' ')
            _, response = interface.verificar_login(username,senha) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('buscar_usuario'):
        try:
            _, username = request.split(' ')
            _, response = interface.buscar_usuario(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_status'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_status(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('set_status'):
        try:
            _, username,status = request.split(' ')
            _, response = interface.set_status(username,status) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_colecao'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_colecao(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    
    elif request.startswith('adicionar_carta_na_colecao'):
        try:
            _, username,emocao = request.split(' ')
            _, response = interface.adicionar_carta_na_colecao(username, emocao)
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_baralhos'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_baralhos(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_qtd_baralhos'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_qtd_baralhos(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('adicionar_baralho'):
        try:
            _, username,baralho = request.split(' ')
            _, response = interface.adicionar_baralho(username, baralho)
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('excluir_baralho'):
        try:
            _, username,indice = request.split(' ')
            _, response = interface.excluir_baralho(username, indice)
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    else:
        response = f"erro: mensagem não foi combinada"
        client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    print(f"Response: {response}")
    
    #finaliza thread
    client_socket.close()
       

def run_server():
    
    interface.iniciar_banco_dados()
    
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # bind the socket to a specific address and port
    server_ip = "127.0.0.1" #localhost
    port = 39526
    server.bind((server_ip, port)) 
    
    # listen for incoming connections
    server.listen()
    print(f"DB-Server listening on {server_ip}:{port}")
    
    # loop infinito pois servidor deve estar sempre disponível
    while True:
        client_socket, client_address = server.accept()
        print(f"\nAccepted connection from {client_address[0]}:{client_address[1]}")

        #para cada requisicao criar um thread para lidar com a requisao e deixar a porta 'de escuta' livre
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start() 
    
    # server.close() 

if __name__ == "__main__":
    run_server()
