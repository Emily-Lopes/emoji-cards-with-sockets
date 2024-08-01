from infra.configs.connection import DBConnectionHandler
from infra.entities.carta import Carta

class CartaRepository: #vai ser como a interface para a tabela Carta
    def select_all(self):
        with DBConnectionHandler() as db: #as instanciar o objeto assim:
            #chama o método enter: retorna self, que vai estar em db
            data = db.session.query(Carta).all()
            return data
            #chama o método exit
            
    #metodo para adicionar uma carta ao baralho, se ainda não existir carta com mesmo nome de emocao
    def add_carta(self, emocao, tempo, impacto_social, efeito_cognitivo, qtd_emocoes_opostas, qtd_emocoes_relacionadas, intensidade):
        try:
            with DBConnectionHandler() as db:
                if db.session.query(Carta).filter_by(emocao=emocao).first():
                    return False, 'Carta já existe!'
                
                nova_carta = Carta( emocao=emocao,
                                    tempo=tempo,
                                    impacto_social=impacto_social,
                                    efeito_cognitivo=efeito_cognitivo,
                                    qtd_emocoes_opostas=qtd_emocoes_opostas,
                                    qtd_emocoes_relacionadas=qtd_emocoes_relacionadas,
                                    intensidade=intensidade
                )
                db.session.add(nova_carta)
                db.session.commit()
                return True, 'Carta adicionada com sucesso!'
                
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao adicionar carta: {str(e)}"
    
    #metodo para buscar a emocao de todas as cartas cadastradas no banco de dados 
    def get_cartas(self):
        with DBConnectionHandler() as db:
            emocoes = db.session.query(Carta.emocao).all()
            return [emocao[0] for emocao in emocoes]
    
    #metodo para buscar informacoesd e uma carta atraves da emocao
    def get_carta(self, emocao):
        with DBConnectionHandler() as db:
            carta = db.session.query(Carta).filter_by(emocao=emocao).first()
            return carta #se retornar None: carta não existe no banco de dados  
        