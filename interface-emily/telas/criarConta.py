import arcade
from constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS
from telas.criarPartida import CriarPartida

class CriarConta(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(AZUL)

        self.logo = None
        self.botoes = []
        self.fundo_campo_nome = None
        self.fundo_campo_senha = None

        self.gerencia_entrada = arcade.gui.UIManager()
        self.gerencia_entrada.enable()

        self.campo_nome = arcade.gui.UIInputText(
            text = '',
            width = 270,
            text_color = arcade.color.WHITE,
            font_name = POPPINS
        )
        
        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=635,
                align_y=313,
                child=self.campo_nome
            )
        )

        self.campo_senha = arcade.gui.UIInputText(
            text='',
            width=270,
            text_color = arcade.color.WHITE,
            font_name = POPPINS
        )

        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=635,
                align_y=213,
                child=self.campo_senha
            )
        )

    def setup(self):
        self.logo = arcade.load_texture("./imagens/logo.png")
        self.b_conta = arcade.load_texture("./imagens/botoes/b-conta.png")
        self.campo_nome = arcade.load_texture("./imagens/campo.png")
        self.campo_senha = arcade.load_texture("./imagens/campo.png")

        self.botoes.append({
            'texture': self.b_conta,
            'x': 780,
            'y': 180,
            'width': 200,
            'height': 75,
            'action': self.confirmar_dados
        })

    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()

        if self.logo:
            arcade.draw_texture_rectangle(300, ALTURA_TELA // 2, self.logo.width, 
                                          self.logo.height, self.logo)

        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], 
                                              botao['texture'])

        if self.campo_nome:
            arcade.draw_texture_rectangle(770, 355, 350, 
                                          60, self.campo_nome)
        if self.campo_senha:
            arcade.draw_texture_rectangle(770, 255, 350, 
                                          60, self.campo_senha)
            
        arcade.draw_text("username", 770, 395,
                         arcade.color.WHITE, font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text("senha", 770, 295,
                         arcade.color.WHITE, font_size=15, font_name=POPPINS, anchor_x="center")

        self.gerencia_entrada.draw()
                
    def on_mouse_press(self, x, y, button, modifiers):
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break

    def confirmar_dados(self):
        nome = self.campo_nome.text
        senha = self.campo_senha.text
        print(f"Username: {nome}")
        print(f"Senha: {senha}")

        tela_criar_partida = CriarPartida() 
        self.window.show_view(tela_criar_partida) 

if __name__ == "__main__":
    app = CriarConta()
    app.setup() 
    arcade.run()