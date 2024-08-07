import arcade
from constantes import AZUL, LARGURA_TELA, ALTURA_TELA

class CriarPartida(arcade.View):
    def __init__(self):
        super().__init__()
        
        arcade.set_background_color(AZUL)

    def setup(self):

        pass

    def on_show(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Tela Criar Partida", LARGURA_TELA // 2, ALTURA_TELA // 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

if __name__ == "__main__":
    app = CriarPartida()
    app.setup()
    arcade.run()