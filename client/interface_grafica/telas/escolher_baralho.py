import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR, AGRANDIR_BOLD

from ..telas.aguardar_partida import AguardarPartida

class EscolherBaralho(arcade.View):
    def __init__(self, cliente, baralhos, id_partida, criar_partida_view, back_to_login):
        super().__init__()
        
        self.cliente = cliente
        self.baralhos = baralhos
        self.id_partida = id_partida
        
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login

        arcade.set_background_color(AZUL)

        self.botoes = []
        self.indice_inicial = 0
        self.baralho_selecionado = None

        self.b_escolher = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-escolher.png")
        self.botoes.append({
            'texture': self.b_escolher,
            'x': LARGURA_TELA // 2,
            'y': 46,
            'width': 190,
            'height': 70,
            'action': self.confirmar_escolha
        })

        self.opcao = arcade.load_texture("interface_grafica/resources/widgets/opcao.png")
        
        self.baralho_1 = []
        self.baralho_2 = []
        self.baralho_3 = []

        # Preencher baralhos
        if len(self.baralhos) >= 1:
            for emocao in self.baralhos[0]:
                self.baralho_1.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))
        
        if len(self.baralhos) >= 2:
            for emocao in self.baralhos[1]:
                self.baralho_2.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))

        if len(self.baralhos) == 3:
            for emocao in self.baralhos[2]:
                self.baralho_3.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))


        if self.baralho_1:
            self.fundo_baralho_1 = arcade.load_texture("interface_grafica/resources/widgets/baralho.png")

        if self.baralho_2:
            self.fundo_baralho_2 = arcade.load_texture("interface_grafica/resources/widgets/baralho.png")

        if self.baralho_3:
            self.fundo_baralho_3 = arcade.load_texture("interface_grafica/resources/widgets/baralho.png")

    def setup(self):
        pass

    def ow_show(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()  

        espacamento = 85
        largura_carta = 100
        altura_carta = 118
        qtd_cartas = 9

        if self.baralho_1:
            arcade.draw_texture_rectangle(LARGURA_TELA // 2, 500, 850, 150, self.fundo_baralho_1)

            for i in range(qtd_cartas):
                indice_carta = (self.indice_inicial + i) % len(self.baralho_1)
                carta = self.baralho_1[indice_carta]
                pos_x = 160 + i * espacamento
                pos_y = 500

                arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

        if self.baralho_2:    
            arcade.draw_texture_rectangle(LARGURA_TELA // 2, 330, 850, 150, self.fundo_baralho_2)

            for i in range(qtd_cartas):
                indice_carta = (self.indice_inicial + i) % len(self.baralho_2)
                carta = self.baralho_2[indice_carta]
                pos_x = 160 + i * espacamento
                pos_y = 330

                arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)
        
        if self.baralho_3:
            arcade.draw_texture_rectangle(LARGURA_TELA // 2, 160, 850, 150, self.fundo_baralho_3)

            for i in range(qtd_cartas):
                indice_carta = (self.indice_inicial + i) % len(self.baralho_3)
                carta = self.baralho_3[indice_carta]
                pos_x = 160 + i * espacamento
                pos_y = 160

                arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

        if self.baralho_selecionado == 1:
            arcade.draw_texture_rectangle(LARGURA_TELA // 2 + 415, 500 + 65, 40, 40, self.opcao)
        elif self.baralho_selecionado == 2:
            arcade.draw_texture_rectangle(LARGURA_TELA // 2 + 415, 330 + 65, 40, 40, self.opcao)
        elif self.baralho_selecionado == 3:
            arcade.draw_texture_rectangle(LARGURA_TELA // 2 + 415, 160 + 65, 40, 40, self.opcao)

        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], botao['texture'])
            
    def on_mouse_press(self, x, y, button, modifiers):
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break

        if LARGURA_TELA // 2 - 425 < x < LARGURA_TELA // 2 + 425 and 425 < y < 575:
            self.baralho_selecionado = 1
        elif LARGURA_TELA // 2 - 425 < x < LARGURA_TELA // 2 + 425 and 255 < y < 405:
            self.baralho_selecionado = 2
        elif LARGURA_TELA // 2 - 425 < x < LARGURA_TELA // 2 + 425 and 85 < y < 235:
            self.baralho_selecionado = 3

        self.on_draw()

    def confirmar_escolha(self):
        if self.baralho_selecionado:
            self.cliente.baralho_escolhido = self.baralhos[self.baralho_selecionado-1]
            self.cliente.responder_baralho_escolhido(self.id_partida)
            self.window.show_view(AguardarPartida(self.cliente, self.criar_partida_view, self.back_to_login)) 
        else:
            print("Você precisa escolher um baralho")

