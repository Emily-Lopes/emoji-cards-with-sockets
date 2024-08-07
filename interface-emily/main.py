import arcade
from constantes import LARGURA_TELA, ALTURA_TELA, TITULO
from telas.login import Login

def main():
    window = arcade.Window(LARGURA_TELA, ALTURA_TELA, TITULO)
    funcao = Login()
    funcao.setup()
    window.show_view(funcao)
    arcade.run()

if __name__ == "__main__":
    main()