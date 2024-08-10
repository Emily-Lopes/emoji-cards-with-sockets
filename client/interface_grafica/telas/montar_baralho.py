import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading

from ..telas.escolher_baralho import EscolherBaralho

class MontarBaralho(arcade.View):
    def __init__(self, cliente, info_usuario, perfil_view, back_to_login, back_to_criar_partida):
        super().__init__()
        
        self.cliente = cliente
        self.colecao_usuario = info_usuario['colecao_cartas']
        
        # pra poder voltar para tela perfil:
        self.back_to_perfil = perfil_view
        self.login_view = back_to_login
        self.criar_partida_view = back_to_criar_partida

        arcade.set_background_color(AZUL)

        self.botoes = []

        # Carrossel da Coleção
        self.indice_inicial = 0
        self.cartas = []
        self.mapeamento_cartas = {}
        
        # Lista para armazenar os nomes dos emojis selecionados
        self.nomes_baralho = []

        for emocao in self.colecao_usuario:
            carta = arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png")
            self.cartas.append(carta)
            self.mapeamento_cartas[carta] = {
                'texture': arcade.load_texture(f"interface_grafica/resources/emojis/{emocao}.png"),
                'nome': emocao
            }

        self.seta_esquerda = arcade.load_texture("interface_grafica/resources/widgets/seta-esquerda.png")
        self.seta_direita = arcade.load_texture("interface_grafica/resources/widgets/seta-direita.png")
        self.fundo_colecao = arcade.load_texture("interface_grafica/resources/widgets/colecao2.png")
    
        # Carrossel do Baralho 
        self.fundo_baralho = arcade.load_texture("interface_grafica/resources/widgets/baralho.png")
        self.baralho = []

        self.b_montar = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-montar.png")
        self.botoes.append({
            'texture': self.b_montar,
            'x': LARGURA_TELA // 2,
            'y': 46,
            'width': 190,
            'height': 70,
            'action': self.salvar_baralho 
        })

    def setup(self):
        pass

    def ow_show(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()  

        # Carrossel da Coleção    
        arcade.draw_text("Coleção", 110, 560, AMARELO, font_size=24, font_name=AGRANDIR, anchor_x="center")
        arcade.draw_texture_rectangle(LARGURA_TELA // 2, 395, 950, 308, self.fundo_colecao)

        espacamento = 205
        largura_carta = 280
        altura_carta = 300
        cartas_visiveis = 4

        for i in range(cartas_visiveis):
            indice_carta = (self.indice_inicial + i) % len(self.cartas)
            carta = self.cartas[indice_carta]
            pos_x = 190 + i * espacamento
            pos_y = 396

            arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

        arcade.draw_texture_rectangle(68, 400, 50, 50, self.seta_esquerda)
        arcade.draw_texture_rectangle(LARGURA_TELA - 70, 400, 50, 50, self.seta_direita)

        # Carrossel do Baralho
        arcade.draw_text("Escolhas", 110, 210, AMARELO, font_size=24, font_name=AGRANDIR, anchor_x="center")
        arcade.draw_texture_rectangle(LARGURA_TELA // 2, 145, 950, 120, self.fundo_baralho)

        espacamento_baralho = 100
        largura_baralho = 70
        altura_baralho = 70
        pos_x_baralho = 90

        for carta in self.baralho:
            arcade.draw_texture_rectangle(pos_x_baralho, 145, largura_baralho, altura_baralho, carta['texture'])
            pos_x_baralho += espacamento_baralho

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

        # Setas para Coleção
        if 70 - 25 < x < 70 + 25 and 400 - 25 < y < 400 + 25:
            self.indice_inicial = (self.indice_inicial - 1) % len(self.cartas)

        elif LARGURA_TELA - 70 - 25 < x < LARGURA_TELA - 70 + 25 and 400 - 25 < y < 400 + 25:
            self.indice_inicial = (self.indice_inicial + 1) % len(self.cartas)

        espacamento = 205
        largura_carta = 280
        altura_carta = 300
        cartas_visiveis = 4

        for i in range(cartas_visiveis):
            pos_x = 200 + i * espacamento
            pos_y = 396

            if pos_x - largura_carta // 2 < x < pos_x + largura_carta // 2 and pos_y - altura_carta // 2 < y < pos_y + altura_carta // 2:
                indice_carta = (self.indice_inicial + i) % len(self.cartas)
                carta_selecionada = self.cartas[indice_carta]
                emoji_correspondente = self.mapeamento_cartas[carta_selecionada]

                if len(self.baralho) < 9: 
                    self.baralho.append(emoji_correspondente)
                    self.nomes_baralho.append(emoji_correspondente['nome'])

        espacamento_baralho = 100
        largura_carta_baralho = 60
        altura_carta_baralho = 60
        for i, carta in enumerate(self.baralho):
            pos_x = 90 + i * espacamento_baralho
            pos_y = 145

            if (pos_x - largura_carta_baralho / 2 < x < pos_x + largura_carta_baralho / 2 and
                    pos_y - altura_carta_baralho / 2 < y < pos_y + altura_carta_baralho / 2):
                self.baralho.pop(i)
                self.nomes_baralho.pop(i)
                break

        self.on_draw()

    def salvar_baralho(self):
        print(self.nomes_baralho)
