from infra.configs.connection import DBConnectionHandler
from infra.entities.carta import Carta

class CartaRepository: #vai ser como a interface para a tabela Carta
    def select_all(self):
        with DBConnectionHandler() as db: #as instanciar o objeto assim:
            #chama o método enter: retorna self, que vai estar em db
            data = db.session.query(Carta).all()
            return data
            #chama o método exit
            
        