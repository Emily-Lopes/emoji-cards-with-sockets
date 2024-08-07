import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.
import threading
from comunicacao import send_login

from cliente import Client

# from main import client

# define a classe MainView que herda de arcade.View. Cada classe View representa uma tela ou seção da aplicação.
class MainView(arcade.View):
    def __init__(self, client_name: str): #o construtor recebe o nome do cliente por parâmetro
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        self.manager = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        self.client_name = client_name
        self.current_message = None #  este atributo será usado para armazenar mensagens recebidas do servidor.
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        self.label = arcade.gui.UITextArea(
            text="", width=450, height=40, font_size=14
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.label)

        # cria um botão com o texto "Talk". Define a largura do botão.
        talk_button = arcade.gui.UIFlatButton(text="Talk", width=250)
        
        # define um evento para o botão. Quando clicado, o evento inicia uma nova thread para chamar self.talk_to_server
        @talk_button.event
        def on_click(event):
            threading.Thread(target=self.talk_to_server).start()
        # sdiciona o botão ao layout vertical
        vbox.add(talk_button)

        # cria um botão com o texto "Go to Another View". define a largura do botão.
        change_view_button = arcade.gui.UIFlatButton(text="Go to Another View", width=250)
        
        # define um evento para o botão. Quando clicado, muda a visão atual para AnotherView.
        @change_view_button.event
        def on_click(event):
            self.window.show_view(AnotherView())
        
        #adiciona o botão ao layout vertical.
        vbox.add(change_view_button)

        # adiciona o layout vertical (vbox) ao gerenciador de interface do usuário (UIManager), configurando a posição e o alinhamento na tela.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vbox
            )
        )

    # define o método on_update, chamado a cada atualização do quadro. Atualiza o texto do campo de texto se current_message não for None.
    def on_update(self, delta_time: float):
        # verifica se há uma mensagem atual para exibir.
        if self.current_message is not None:
            # atualiza o texto do campo de texto com a mensagem atual.
            self.label.text = self.current_message
            # limpa a mensagem atual após exibi-la.
            self.current_message = None

    # define o método on_show_view, chamado quando a visão é exibida.
    def on_show_view(self):
        # define a cor de fundo da janela.
        # arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        arcade.set_background_color((44,52,107))
        # dabilita o gerenciador de interface, tornando os widgets interativos.
        self.manager.enable()

    # define o método on_hide_view, chamado quando a visão é escondida. Desativa o gerenciador de interface.
    def on_hide_view(self):
        # desativa o gerenciador de interface, tornando os widgets não interativos.
        self.manager.disable()

    # define o método on_draw, chamado a cada atualização da tela. Limpa a tela e desenha os widgets.
    def on_draw(self):
        # limpa o conteúdo da tela.
        self.clear()
        #desenha
        self.manager.draw()

    #método que vai ser chamado com a thred do botao for iniciada
    def talk_to_server(self):
        self.current_message = send_message(self.client_name)

class AnotherView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        vbox = arcade.gui.UIBoxLayout()
        self.label = arcade.gui.UITextArea(
            text="This is another screen", width=450, height=40, font_size=14
        )
        vbox.add(self.label)

        #define um botao pra voltar pra tela principal
        button = arcade.gui.UIFlatButton(text="Back to Main", width=250)
        @button.event
        def on_click(event):
            self.window.show_view(MainView("Client"))
        vbox.add(button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vbox
            )
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

class LoginView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.username = ""
        self.password = ""
        self.client = Client()
        self.setup()

    def setup(self):
        # # Cria um layout horizontal
        # hbox = arcade.gui.UIBoxLayout(vertical=False)

        # # Adiciona a imagem como sprite
        # self.image_sprite = arcade.Sprite("/usr/local/ccf355/client/resources/logo.png", scale=0.5)  # Caminho relativo
        # self.image_sprite.center_x = 150
        # self.image_sprite.center_y = self.window.height // 2
        
        # # Adiciona o sprite à lista de sprites
        # self.sprite_list = arcade.SpriteList()
        # self.sprite_list.append(self.image_sprite)
        
        # adiciona o campo de texto ao layout vertical
        # hbox.add(self.sprite_list)
        
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        
        self.username_input = arcade.gui.UIInputText(
            text="", width=450, height=40, font_size=14, placeholder_text="Username"
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.username_input)

        self.password_input = arcade.gui.UIInputText(
            text="", width=300, height=40, font_size=14, placeholder_text="Password", is_password=True
        )
        vbox.add(self.password_input)
        
        # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        self.msg = arcade.gui.UITextArea(
            text="", width=450, height=40, font_size=14, placeholder_text="Username"
        )
        vbox.add(self.msg)
        
        login_button = arcade.gui.UIFlatButton(text="Login", width=300)
        @login_button.event
        def on_click(event):
            username = self.username_input.text
            password = self.password_input.text
            msg = send_login(username, password)
            self.msg.text = str(msg) #self.send_login_info()
            # threading.Thread(target=self.send_login_info).start()
        vbox.add(login_button)
        
        # hbox.add(vbox)

        # Adiciona o layout horizontal à interface do usuário
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vbox
            )
        )
        

    def on_update(self, delta_time: float):
        pass

    def on_show_view(self):
        # Define a cor de fundo usando valores RGB
        rgb_color = (44, 52, 107)  # RGB equivalente ao hexadecimal #2C346B
        arcade.set_background_color(rgb_color)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        # Desenha a lista de sprites
        # self.sprite_list.draw()
        self.manager.draw()

    def send_login_info(self):
        username = self.username_input.text
        password = self.password_input.text
        # Simulação de envio de login (substitua com a função real)
        return f" login info: {username}, {password}"
