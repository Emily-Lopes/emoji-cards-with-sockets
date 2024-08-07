import arcade
from constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, AGRANDIR

class Aguardar(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(AZUL)
    
    def on_draw(self):
        # to-do: lógica para chamar a função, esperar a resposta e depois mudar de tela
        arcade.draw_text("Preparando Partida...", LARGURA_TELA//2, ALTURA_TELA//2, AMARELO, 
                         font_size=40, font_name=AGRANDIR, anchor_x="center")

if __name__ == "__main__":
    app = Aguardar()
    app.setup() 
    arcade.run()