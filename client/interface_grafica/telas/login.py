import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading

from ..telas.criar_conta import CriarConta
from ..telas.criar_partida import CriarPartida

# define a classe LoginView que herda de arcade.View. Cada classe View representa uma tela ou seção da aplicação.
class Login(arcade.View): 
    def __init__(self, cliente):
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        self.manager = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        self.logo = arcade.load_texture(f"interface_grafica/resources/widgets/logo.png")
        self.cliente = cliente
        self.login_thread = None
        self.login_result = None
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        
        # campo de texto para mostrar mensagem
        self.username = arcade.gui.UITextArea(
            text="username", width=100, height=40, font_size=14, font_name=POPPINS
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.username)

        self.username_input = arcade.gui.UIInputText(
            text="", width=300, height=40, font_size=14, font_name=POPPINS, text_color=(255,255,255,255)
        )
        vbox.add(self.username_input)
        
        # campo de texto para mostrar mensagem
        self.password = arcade.gui.UITextArea(
            text="senha", width=100, height=40, font_size=14, font_name=POPPINS
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.password)

        # Campo de entrar com password
        self.password_input = arcade.gui.UIInputText(
            text="", width=300, height=40, font_size=14, font_name=POPPINS, text_color=(255,255,255,255)
        )
        vbox.add(self.password_input)

        # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        self.msg = arcade.gui.UITextArea(
            text="", width=450, height=40, font_size=8
        )
        vbox.add(self.msg)
        
        login_button = arcade.gui.UIFlatButton(
            text="LOGIN", width=100, style={
                                            "font_name": AGRANDIR,
                                            "font_size": 14,
                                            "font_color": AZUL,
                                            "border_width": 3,
                                            "border_color": arcade.color.WHITE,
                                            "bg_color": AMARELO
                                        }
        )

        # login_button = arcade.gui.UIFlatButton(text="Login", width=300)
        @login_button.event
        def on_click(event):
            threading.Thread(target=self.confirmar_dados).start()
            
        vbox.add(login_button)
        
        criar_conta_button = arcade.gui.UIFlatButton(
            text="criar conta", width=100, style={
                                            "font_name": POPPINS,
                                            "font_size": 12,
                                            "font_color": AMARELO,
                                            "border_width": 1,
                                            "border_color": AZUL,
                                            "bg_color": AZUL
                                        }
        )

        @criar_conta_button.event
        def on_click(event):
            self.window.show_view(CriarConta(self.cliente))
            
        vbox.add(criar_conta_button)
        
        # Adiciona o layout à interface do usuário
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right", anchor_y="center_y", child=vbox
            )
        )
    
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.login_result:
            if self.login_result == 'Login feito com sucesso!':
                self.window.show_view(CriarPartida(self.cliente))
            else:
                self.msg.text = self.login_result
                self.login_result = None

    # define o método on_show_view, chamado quando a visão é exibida.
    def on_show_view(self):
        # define a cor de fundo da janela.
        arcade.set_background_color(AZUL)
        # habilita o gerenciador de interface, tornando os widgets interativos.
        self.manager.enable()
        
    # define o método on_hide_view, chamado quando a visão é escondida. Desativa o gerenciador de interface.
    def on_hide_view(self):
        # desativa o gerenciador de interface, tornando os widgets não interativos.
        self.manager.disable()

    # define o método on_draw, chamado a cada atualização da tela. Limpa a tela e desenha os widgets.
    def on_draw(self):
        # limpa o conteúdo da tela.
        self.clear()
                
        arcade.draw_texture_rectangle(300, ALTURA_TELA // 2, self.logo.width,
                                          self.logo.height, self.logo)
            
        self.manager.draw()
    
    def confirmar_dados(self):
        username = self.username_input.text
        password = self.password_input.text       
        if username != "" and password != "":
            s, msg = self.cliente.login(username, password)
            self.login_result = msg
        else:
            self.login_result = "Preencha os Campos!"