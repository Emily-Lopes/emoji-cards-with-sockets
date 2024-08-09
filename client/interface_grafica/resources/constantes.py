import arcade
import os

LARGURA_TELA = 1000
ALTURA_TELA = 600
TITULO = "EmojiCards"
AZUL = arcade.color_from_hex_string("#2C346B")
AMARELO = arcade.color_from_hex_string("#F6BA2C")

POPPINS = os.path.join(os.path.dirname(__file__), 'fontes', 'Poppins.ttf')
arcade.load_font(POPPINS)

AGRANDIR = os.path.join(os.path.dirname(__file__), 'fontes', 'Agrandir.otf')
arcade.load_font(AGRANDIR)

AGRANDIR_BOLD = os.path.join(os.path.dirname(__file__), 'fontes', 'AgrandirBold.ttf')
arcade.load_font(AGRANDIR_BOLD)