import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading

# define a classe LoginView que herda de arcade.View. Cada classe View representa uma tela ou seção da aplicação.
class AguardarPartida(arcade.View): 
    def __init__(self, cliente, criar_partida_view, back_to_login):
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        self.manager = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        self.cliente = cliente
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login
        print(self.cliente.baralho_escolhido)
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        
        # campo de texto para mostrar mensagem
        self.username = arcade.gui.UITextArea(
            text="Aguardando Partida ...", width=500, height=40, font_size=20, font_name=AGRANDIR, text_color=AMARELO
        )
        # adiciona o campo de texto ao layout vertical
        vbox.add(self.username)
        
        # Adiciona o layout à interface do usuário
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right", anchor_y="center_y", child=vbox
            )
        )
    
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.cliente.mensagem_servidor:
            if self.cliente.mensagem_servidor.startswith("atributo_turno"):
                
                _, atributo, id_partida = self.cliente.mensagem_servidor.split(',')
                
                self.cliente.mensagem_servidor = None
                
                print(atributo)
                
                

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
            
        self.manager.draw()