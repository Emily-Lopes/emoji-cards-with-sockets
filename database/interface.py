from infra.configs.base import Base
from infra.configs.connection import DBConnectionHandler

from  infra.repository.carta_repository import CartaRepository
from  infra.repository.usuario_repository import UsuarioRepository

repoCarta = CartaRepository()
repoUsuario = UsuarioRepository()

# criando tabelas (caso ainda não existam)
Base.metadata.create_all(DBConnectionHandler().get_engine())

# def insert_data():
#     session = Session() # criando uma sessao basica
#     carta1 = Carta(emocao='autoestima', tempo='anos', impacto_social='positivo', efeito_cognitivo='certeza', qtd_emocoes_opostas=1, qtd_emocoes_relacionadas=1, intensidade=5)
#     carta2 = Carta(emocao='raiva', tempo='minutos', impacto_social='negativo', efeito_cognitivo='confusão', qtd_emocoes_opostas=2, qtd_emocoes_relacionadas=6, intensidade=5)
    
#     usuario_admin = Usuario(username='admin', senha='admin123', status='offline', colecao_cartas='["autoestima","raiva"]', qtd_baralhos=0, baralhos='')

#     session.add_all([carta1, carta2, usuario_admin])
#     session.commit()
#     session.close()

# # apenas na primeira vez que rodar:
# # insert_data()

data = repoCarta.select_all()
for d in data:
    print(d.emocao)

