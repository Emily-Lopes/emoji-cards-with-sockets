from cliente import Client
from interface import Interface

if __name__ == "__main__":
    client1 = Client()
    interface1 = Interface(client1)

    interface1.simula("ingred", "123")

    # interface1.criar_partida("leticia", "iury")
    
    while True:
        pass