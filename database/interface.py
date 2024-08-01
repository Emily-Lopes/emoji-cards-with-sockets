from schema import Usuario, Carta
from config import Session

def insert_data():
    session = Session() # criando uma sessao basica
    carta1 = Carta(emocao='autoestima', tempo='anos', impacto_social='positivo', efeito_cognitivo='certeza', qtd_emocoes_opostas=1, qtd_emocoes_relacionadas=1, intensidade=5)
    carta2 = Carta(emocao='raiva', tempo='minutos', impacto_social='negativo', efeito_cognitivo='confusão', qtd_emocoes_opostas=2, qtd_emocoes_relacionadas=6, intensidade=5)
    
    usuario_admin = Usuario(username='admin', senha='admin123', status='offline', colecao_cartas='["autoestima","raiva"]', qtd_baralhos=0, baralhos='')

    session.add_all([carta1, carta2, usuario_admin])
    session.commit()
    session.close()

# insert_data()

# SQL
session = Session()
# -> select
data = session.query(Carta).all()
for d in data:
    print(d.emocao)
session.close()