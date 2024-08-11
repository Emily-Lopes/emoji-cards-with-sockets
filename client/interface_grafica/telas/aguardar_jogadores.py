import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

from ..telas.aguardar_partida import AguardarPartida
from ..telas.escolher_baralho import EscolherBaralho


import threading

# define a classe LoginView que herda de arcade.View. Cada classe View representa uma tela ou seção da aplicação.
class AguardarJogadores(arcade.View): 
    def __init__(self, cliente, criar_partida_view, back_to_login):
        
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        
        self.manager = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        
        self.cliente = cliente
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login
        
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        
        # cria um layout vertical para organizar os widgets (elementos gráficos)
        vbox = arcade.gui.UIBoxLayout()
        
        # campo de texto para mostrar mensagem
        self.username = arcade.gui.UITextArea(
            text="Aguardando Jogadores ...", width=500, height=40, font_size=20, font_name=AGRANDIR, text_color=AMARELO
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
            if self.cliente.mensagem_servidor.startswith("partida_criada"):
                
                #pega a mensagem e libera a variável compartilhada
                _, id_partida, baralhos = self.cliente.mensagem_servidor.split(',', 2)
                self.cliente.mensagem_servidor = None
                
                baralhos = self.cliente.manipular_baralhos(baralhos)
                if len(baralhos)>0:
                    self.window.show_view(EscolherBaralho(self.cliente, baralhos,id_partida, self.criar_partida_view, self.back_to_login)) 
                else:
                    #escolher um baralho aleatorio
                    self.cliente.baralho_escolhido = self.cliente.gerar_baralho_aleatorio()
                    print("avisou_escolha")
                    self.cliente.responder_baralho_escolhido(id_partida)
                    self.window.show_view(AguardarPartida(self.cliente, self.criar_partida_view, self.back_to_login)) 
            
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