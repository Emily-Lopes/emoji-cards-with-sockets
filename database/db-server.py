import socket
from  infra.repository.carta_repository import CartaRepository
from  infra.repository.usuario_repository import UsuarioRepository

repoCarta = CartaRepository()
repoUsuario = UsuarioRepository()


def run_server():
    # your code will go here
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    port = 8520
    
    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")
    
    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    # receive data from the client
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert bytes to string
        
        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        print(f"Received: {request.lower()}")
        
        if request.lower() == "carta":
            data = repoCarta.select_all()
            resposta = 'emocoes cadastradas:\n '
            for d in data:
                resposta += d.emocao + '\n'
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send(resposta.encode("utf-8"))
        
        else:
            response = "accepted".encode("utf-8") # convert string to bytes
            # convert and send accept response to the client
            client_socket.send(response)
    
    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()

run_server()
