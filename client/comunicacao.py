import socket

def send_message(client_name: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 4242))
        s.sendall(client_name.encode("utf8"))
        msg = s.recv(1024)
        return f"Server said: {msg.decode('utf8')}"

def send_login(client_name: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 4242))
        s.sendall(client_name.encode("utf8"))
        msg = s.recv(1024)
        return f"Server said: {msg.decode('utf8')}"