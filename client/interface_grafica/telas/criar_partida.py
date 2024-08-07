import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading

from ..telas.aguardar import Aguardar

#como é a tela que o cliente é direcionado quando faz login/cria conta, é onde vai lidar com convites
class CriarPartida(arcade.View): 
    def __init__(self, cliente):
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        self.manager = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        self.cliente = cliente
        self.thread = None
        self.response = None
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        
        # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        self.exibir_username = arcade.gui.UITextArea(
            text=self.cliente.get_username(), width=150, height=40, font_size=12, text_color=AMARELO
        )
        vbox.add(self.exibir_username)
        
        # campo de texto para mostrar mensagem
        self.username1 = arcade.gui.UITextArea(
            text="username_1", width=150, height=40, font_size=14, font_name=POPPINS
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.username1)

        self.username1_input = arcade.gui.UIInputText(
            text="", width=300, height=40, font_size=14, font_name=POPPINS, text_color=(255,255,255,255)
        )
        vbox.add(self.username1_input)
        
        self.username2 = arcade.gui.UITextArea(
            text="username_2", width=150, height=40, font_size=14, font_name=POPPINS
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.username2)

        self.username2_input = arcade.gui.UIInputText(
            text="", width=300, height=40, font_size=14, font_name=POPPINS, text_color=(255,255,255,255)
        )
        vbox.add(self.username2_input)

        # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        self.msg = arcade.gui.UITextArea(
            text="", width=450, height=40, font_size=8
        )
        vbox.add(self.msg)
        
        criar_conta_button = arcade.gui.UIFlatButton(
            text="CRIAR PARTIDA", width=300, style={
                                            "font_name": AGRANDIR,
                                            "font_size": 14,
                                            "font_color": AZUL,
                                            "border_width": 3,
                                            "border_color": arcade.color.WHITE,
                                            "bg_color": AMARELO
                                        }
        )

        # login_button = arcade.gui.UIFlatButton(text="Login", width=300)
        @criar_conta_button.event
        def on_click(event):
            #chamar funcao criar partida
            self.window.show_view(Aguardar(self.cliente))

            # self.start_thread()
            
        vbox.add(criar_conta_button)
        
        # Adiciona o layout à interface do usuário
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vbox
            )
        )
        
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        pass
        # if self.response:
        #     if self.response == '?':
        #         self.window.show_view(Aguardar(self.cliente))
        #     else:
        #         self.msg.text = self.response
        #         self.response = None
                
        # if self.cliente.convite:
        #     convite = self.cliente.convite
        #     self.cliente.convite = None  # Limpa o convite após processá-lo
        #     self.msg.text = f"receber convite {str(convite)}"
        #     # self.window.show_view(ResponderConvite(self.cliente, convite))

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
        #desenhar        
        self.manager.draw()
    
    # def start_thread(self):
    #     # if self.thread and self.thread.is_alive():
    #     #     return  # evita múltiplas threads ao mesmo tempo
    #     self.login_thread = threading.Thread(target=self.confirmar_dados)
    #     self.login_thread.start()
