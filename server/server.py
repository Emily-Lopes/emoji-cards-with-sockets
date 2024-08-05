"""
O servidor recebe o nome do client e o cumprimenta.
A biblioteca `tqdm` foi usada única e exclusivamente para mostrar
que é possível colocar dependências diferentes no requirements.txt
de cada parte do sistema, ela não cumpre nenhum propósito funcional aqui.

Referências:
- [Biblioteca de sockets](https://docs.python.org/3/library/socket.html)
"""
from random import randint
from sys import argv
import socket
import threading
import time
import tqdm


def send_response(conn: socket.socket):
    with conn:
        msg = conn.recv(1024)
        name = msg.decode("utf8")
        s = 0
        for _ in tqdm.tqdm(range(5)):
            s += randint(1, 100)
            time.sleep(0.25)
        conn.sendall(f"Hello, {name}! Your number is: {s}".encode("utf8"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 4242))
        s.listen()
        while True:
            conn, addr = s.accept()
            print(f"Connected with {addr}")
            thread = threading.Thread(target=send_response, args=(conn,))
            thread.start()


if __name__ == "__main__":
    # main(*argv[1:])
    main()
