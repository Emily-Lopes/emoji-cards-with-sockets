import arcade 
from views import MainView, LoginView

def main(client_name: str):
    # cria uma instância da janela com 800x600 pixels, o título configurado para incluir o nome do cliente, e permite que a janela seja redimensionada.
    window = arcade.Window(800, 600,f"Client - {client_name}", resizable=True)
    # window = Window(fullscreen=True, resizable=False) #
    
    # cria uma instância da visão principal MainView, passando o nome do cliente como argumento.
    # main_view = MainView(client_name)
    main_view = LoginView()
    
    #Define a main_view como a visão que deve ser exibida na janela.
    window.show_view(main_view)
    
    #inicia o loop principal do arcade, que mantém a aplicação em execução e atualiza a tela.
    arcade.run()

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])