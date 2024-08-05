"""
O cliente envia seu nome e mostra a resposta do servidor.
Essa não é necessariamente a melhor implementação de como lidar com as comunicações
com o servidor, serve apenas para ilustrar que isso é possível.
Inclusive, não é necessário usar as mesmas bibliotecas.

Referências:
- [Biblioteca de sockets](https://docs.python.org/3/library/socket.html)
- [Biblioteca arcade](https://api.arcade.academy/en/latest/)
"""

from sys import argv
import arcade
import arcade.gui
import threading
import socket


class MainView(arcade.View):

    def __init__(self, client_name: str):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.client_name = client_name
        self.current_message = None

        vbox = arcade.gui.UIBoxLayout()
        self.label = arcade.gui.UITextArea(
            text="", width=450, height=40, font_size=14
        )
        vbox.add(self.label)

        button = arcade.gui.UIFlatButton(text="Talk", width=250)

        @button.event
        def on_click(event):
            threading.Thread(target=self.talk_to_server).start()

        vbox.add(button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vbox
            )
        )

    def on_update(self, delta_time: float):
        if self.current_message is not None:
            self.label.text = self.current_message
            self.current_message = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def talk_to_server(self) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("0.0.0.0", 4242))
            self.current_message = "..."
            s.sendall(self.client_name.encode("utf8"))
            msg = s.recv(1024)
            self.current_message = f"Server said: {msg.decode('utf8')}"


def main(client_name: str):
    window = arcade.Window(800, 600, f"Client - {client_name}", resizable=True)
    main_view = MainView(client_name)
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main(*argv[1:])

