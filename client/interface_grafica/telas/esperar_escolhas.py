import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR, AGRANDIR_BOLD

import threading
from ..telas.montar_baralho import MontarBaralho

class EsperarEscolhas(arcade.View):
    def __init__(self, cliente, atributo_turno, pontuacao, id_partida, criar_partida_view, back_to_login):
        super().__init__()

        arcade.set_background_color(AZUL)
        
        self.cliente = cliente
        self.atributo = atributo_turno
        self.pontuacao = pontuacao
        self.id_partida = id_partida
         
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login

        self.centro = None
        self.esquerda = None
        self.direita = None
        
        self.usernames = [username for username in self.pontuacao.keys()] #usernamedono, username2, username3
        print(self.usernames)
        
        #mostrar pontuacao
        self.username_1 = self.usernames[1]
        self.username_2 = self.usernames[0] # dono ficar no meio
        self.username_3 = self.usernames[2]
        print(self.username_1)

        self.pontuacao_1 = self.pontuacao[self.username_1]
        self.pontuacao_2 = self.pontuacao[self.username_2]
        self.pontuacao_3 = self.pontuacao[self.username_3]
        print(self.pontuacao_1)

        self.fundo_atributo = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

        # self.botoes = []

        # self.b_provisorio = arcade.load_texture("./imagens/opcao.png")
        # self.botoes.append({
        #     'texture': self.b_provisorio,
        #     'x': LARGURA_TELA - 100,
        #     'y': 100,
        #     'width': 80,
        #     'height': 80,
        #     'action': self.mudar_tela
        # })

    def setup(self):
        self.centro = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        
    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA // 2 - 50, 180, 250, self.centro)
        arcade.draw_texture_rectangle(LARGURA_TELA//2 - 200, ALTURA_TELA // 2 - 50, 180, 250, self.esquerda)
        arcade.draw_texture_rectangle(LARGURA_TELA//2 + 200, ALTURA_TELA // 2 - 50, 180, 250, self.direita)
        
        if self.username_1 and self.pontuacao_1:
            arcade.draw_text(self.username_1, LARGURA_TELA//2, 570, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            arcade.draw_text(self.pontuacao_1, LARGURA_TELA//2, 530, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            
        if self.username_2 and self.pontuacao_2:
            arcade.draw_text(self.username_2, LARGURA_TELA//2 - 180, 570, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            arcade.draw_text(self.pontuacao_2, LARGURA_TELA//2 - 180, 530, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            
        if self.username_3 and self.pontuacao_3:
            arcade.draw_text(self.username_3, LARGURA_TELA//2 + 180, 570, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            arcade.draw_text(self.pontuacao_3, LARGURA_TELA//2 + 180, 530, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            
        if self.fundo_atributo and self.atributo:
            arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA// 2 + 150, 350, 60, self.fundo_atributo)
            arcade.draw_text(self.atributo, LARGURA_TELA//2, ALTURA_TELA// 2 + 143, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        # for botao in self.botoes:
        #     if 'texture' in botao:
        #         arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], botao['texture'])
    
    #
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.cliente.mensagem_servidor:
            if self.cliente.mensagem_servidor.startswith("fim_turno"):
                
                #pega a mensagem e libera a variável compartilhada
                _, vencedor, atributo, id_partida, escolhas_cada_jogador = self.cliente.mensagem_servidor.split(',', 4)
                self.cliente.mensagem_servidor = None
                escolhas = eval(escolhas_cada_jogador)
                print(vencedor)
                print(atributo)
                print(escolhas)
                print(escolhas.keys())
                
                
 
    
    # def on_mouse_press(self, x, y, button, modifiers):
    #     for botao in self.botoes:
    #         if 'texture' in botao:
    #             if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
    #                     botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
    #                 botao['action']()
    #                 break

    # # Só para testar as outras telas
    # def mudar_tela(self):
    #     prox_tela = ExibirVencedorTurno() 
    #     self.window.show_view(prox_tela) 
