import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR, AGRANDIR_BOLD

import threading
# from ..telas.turno import Turno

class VencedorTurno(arcade.View):
    def __init__(self, cliente, atributo, vencedor, escolhas, pontuacao, id_partida, atributo_novo_turno, criar_partida_view, back_to_login):
        super().__init__()

        arcade.set_background_color(AZUL)
        
        self.cliente = cliente
        self.atributo = atributo
        self.vencedor = vencedor
        self.escolhas = escolhas
        self.pontuacao = pontuacao
        self.id_partida = id_partida
        self.atributo_novo_turno = atributo_novo_turno
         
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login

        self.centro = None
        self.esquerda = None
        self.direita = None
        
        self.resultado = None
        
        print(self.pontuacao.keys(), self.escolhas.keys())
        
        self.usernames = [username for username in self.pontuacao.keys()] #usernamedono, username2, username3
        print(self.usernames)
        
        if self.vencedor == "empate":
            
            self.resultado = "Resultado: Empate"

            self.username_1 = self.usernames[1]
            self.username_2 = self.usernames[0] # dono ficar no meio
            self.username_3 = self.usernames[2]
        
        else:            
            self.resultado = f"Resultado: {self.vencedor} venceu com a carta {self.escolhas[self.vencedor]}!"
            self.username_2 = self.vencedor
            
            # Remove o vencedor da lista para posicionar os outros dois
            outros_jogadores = [username for username in self.usernames if username != self.vencedor]

            self.username_1 = outros_jogadores[0]
            self.username_3 = outros_jogadores[1]
            
            

        self.pontuacao_1 = str(self.pontuacao[self.username_1])
        self.pontuacao_2 = str(self.pontuacao[self.username_2])
        self.pontuacao_3 = str(self.pontuacao[self.username_3])
        
        self.escolha_1 = str(self.escolhas[self.username_1])
        self.escolha_2 = str(self.escolhas[self.username_2])
        self.escolha_3 = str(self.escolhas[self.username_3])       
              

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
        self.centro = arcade.load_texture(f"interface_grafica/resources/cartas/{self.escolha_1}.png")
        self.esquerda = arcade.load_texture(f"interface_grafica/resources/cartas/{self.escolha_2}.png")
        self.direita = arcade.load_texture(f"interface_grafica/resources/cartas/{self.escolha_2}.png")
        
    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA // 2 - 50, 250, 280, self.centro)
        arcade.draw_text(self.username_1, LARGURA_TELA//2, 100, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        arcade.draw_texture_rectangle(LARGURA_TELA//2 - 200, ALTURA_TELA // 2 - 50, 210, 230, self.esquerda)
        arcade.draw_text(self.username_2, LARGURA_TELA//2 - 200, 120, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        arcade.draw_texture_rectangle(LARGURA_TELA//2 + 200, ALTURA_TELA // 2 - 50, 210, 230, self.direita)
        arcade.draw_text(self.username_3, LARGURA_TELA//2 + 200, 120, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")

        # if self.username_1 and self.pontuacao_1:
        arcade.draw_text(self.username_1, LARGURA_TELA//2, 570, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(self.pontuacao_1, LARGURA_TELA//2, 530, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
            
        # if self.username_2 and self.pontuacao_2:
        arcade.draw_text(self.username_2, LARGURA_TELA//2 - 180, 570, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(self.pontuacao_2, LARGURA_TELA//2 - 180, 530, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
            
        # if self.username_3 and self.pontuacao_3:
        arcade.draw_text(self.username_3, LARGURA_TELA//2 + 180, 570, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(self.pontuacao_3, LARGURA_TELA//2 + 180, 530, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
            
        if self.fundo_atributo and self.atributo:
            arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA// 2 + 150, 350, 60, self.fundo_atributo)
            arcade.draw_text(self.atributo, LARGURA_TELA//2, ALTURA_TELA// 2 + 143, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        arcade.draw_text(self.resultado, LARGURA_TELA//2,  ALTURA_TELA// 2 + 130, arcade.color.WHITE, 
                font_size=15, font_name=POPPINS, anchor_x="center")
        
        # for botao in self.botoes:
        #     if 'texture' in botao:
        #         arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], botao['texture'])
            
    # def on_mouse_press(self, x, y, button, modifiers):
    #     for botao in self.botoes:
    #         if 'texture' in botao:
    #             if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
    #                     botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
    #                 botao['action']()
    #                 break

    # def mudar_tela(self):
    #     prox_tela = ExibirVencedorPartida() 
    #     self.window.show_view(prox_tela) 
