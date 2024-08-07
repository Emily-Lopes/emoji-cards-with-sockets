import socket

def send_login(username, senha) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 5000))
        request = f"login,{username},{senha}"
        s.sendall(request.encode("utf8"))
        response = s.recv(1024)
        return f"Server said: {response.decode('utf8')}"
    
def send_login(username, senha) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 5000))
        request = f"login,{username},{senha}"
        s.sendall(request.encode("utf8"))
        response = s.recv(1024)
        return f"Server said: {response.decode('utf8')}"