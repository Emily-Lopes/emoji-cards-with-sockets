import socket

def run_client():
    
    db_server_ip = "0.0.0.0"  # replace with the server's IP address
    db_server_port = 39526  # replace with the server's port number

    while True:
        # create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # establish connection with server
        client.connect((db_server_ip, db_server_port))
    
        # input message and send it to the server
        msg = input("\nEnter message: ")
        client.send(msg.encode("utf-8")[:1024])

        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")

        print(f"Received: {response}")

if __name__ == "__main__":
    run_client()
