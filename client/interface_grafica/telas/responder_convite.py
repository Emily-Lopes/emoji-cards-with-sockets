import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

from ..telas.aguardar_jogadores import AguardarJogadores
from ..telas.perfil import Perfil


import threading

# define a classe LoginView que herda de arcade.View. Cada classe View representa uma tela ou seção da aplicação.
class ResponderConvite(arcade.View): 
    def __init__(self, cliente, username_dono, id_partida,criar_partida_view, back_to_login):
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        self.manager = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        self.logo = arcade.load_texture(f"interface_grafica/resources/widgets/logo.png")
        
        self.cliente = cliente
        self.username_dono = username_dono
        self.id_partida = id_partida   
        
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login
        
        self.resposta = None
        
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        
        # campo de texto para mostrar mensagem
        self.titulo = arcade.gui.UITextArea(
            text="Bora Jogar?", width=400, height=40, font_size=25, font_name=AGRANDIR, text_color=AMARELO
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.titulo)

        # campo de texto para mostrar mensagem
        self.descricao = arcade.gui.UITextArea(
            text=f"{self.username_dono} convidou você para jogar.", width=400, height=40, font_size=14, font_name=POPPINS
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.descricao)

        # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        self.msg = arcade.gui.UITextArea(
            text="", width=450, height=40, font_size=14
        )
        vbox.add(self.msg)
        
        aceitar_button = arcade.gui.UIFlatButton(
            text="ACEITAR", width=100, style={
                                            "font_name": POPPINS,
                                            "font_size": 14,
                                            "font_color": AZUL,
                                            "border_width": 3,
                                            "border_color": arcade.color.WHITE,
                                            "bg_color": AMARELO
                                        }
        )

        @aceitar_button.event
        def on_click(event):
            self.resposta = "aceito"
            threading.Thread(target=self.enviar_resposta).start()
                        
        vbox.add(aceitar_button)
        
        recusar_button = arcade.gui.UIFlatButton(
            text="RECUSAR", width=100, style={
                                            "font_name": POPPINS,
                                            "font_size": 14,
                                            "font_color": AZUL,
                                            "border_width": 3,
                                            "border_color": arcade.color.WHITE,
                                            "bg_color": AMARELO
                                        }
        )

        @recusar_button.event
        def on_click(event):
            self.resposta = "recuso"
            threading.Thread(target=self.enviar_resposta).start()
            
        vbox.add(recusar_button)
        
        # Adiciona o layout à interface do usuário
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vbox
            )
        )
    
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.resposta:
            if self.resposta == "aceito":
                self.resposta = None
                self.window.show_view(AguardarJogadores(self.cliente, self.criar_partida_view, self.back_to_login))
                
            else:
                #se recusou: volta pra criar partida
                self.resposta = None
                self.window.show_view(self.criar_partida_view(self.cliente, self.back_to_login)) 
                     

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
                
        arcade.draw_texture_rectangle(0, 0, self.logo.width//100,
                                          self.logo.height//100, self.logo)
            
        self.manager.draw()
    
    def enviar_resposta(self):
        self.cliente.responder_convite(self.resposta, self.id_partida)

