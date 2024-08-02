import socket
import threading

import interface #arquivo interface.py vai funcionar como uma biblioteca

'''
possiveis mensagens para o servidor e respectivo retorno

'cartas_disponiveis' -> "emocao1,emocao2, ... ,emocaoN" #estão basta fazer .split(',') para ter um vetor de strings


'''
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')  # convert bytes to string
    print(f"Received request: {request}")

    if request.startswith('cartas_disponiveis'):
        mensagem = str(interface.get_emocoes_cadastradas()) #vetor string com as emocoes cadastradas
        client_socket.send(mensagem.encode('utf-8')) # convert string to bytes
    
    #finaliza thread
    client_socket.close()
       

def run_server():
    
    interface.iniciar_banco_dados()
    
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # bind the socket to a specific address and port
    server_ip = "127.0.0.1" #localhost
    port = 8520
    server.bind((server_ip, port)) 
    
    # listen for incoming connections
    server.listen()
    print(f"DB-Server listening on {server_ip}:{port}")
    
    # loop infinito pois servidor deve estar sempre disponível
    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        #para cada requisicao criar um thread para lidar com a requisao e deixar a porta 'de escuta' livre
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start() 
    
    # server.close() 

if __name__ == "__main__":
    run_server()
