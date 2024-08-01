from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

# configuracoes
engine = create_engine('sqlite:///database2.db')
Base = declarative_base()
Session = sessionmaker(bind=engine) # vincular uma sessao na engine
session = Session() # criando uma sessao basica

# entidades
class Usuario(Base):
    __tablename__ = 'usuario'
    username = Column(String, primary_key=True)
    senha = Column(String)
    status = Column(String) #jogando - online - offline
    colecao_cartas = Column(String) #string simulado um vetor com nome das cartas: ['carta1', 'carta2',..]
    qtd_baralhos = Column(Integer)
    baralhos = Column(String) #string simulando um vetor de vetores: [['baralho1'],['baralho2'],['baralho3']]

class Carta(Base):
    __tablename__ = 'carta'
    emocao = Column(String, primary_key=True)
    tempo = Column(String)
    impacto_social = Column(String)
    efeito_cognitivo = Column(String) 
    qtd_emocoes_opostas = Column(Integer) #pro sistema não importa quais, só importa quantas
    qtd_emocoes_relacionadas = Column(Integer) #pro sistema não importa quais, só importa quantas
    intensidade = Column(Integer)

Base.metadata.create_all(engine)

def insert_data():
    carta1 = Carta(emocao='autoestima', tempo='anos', impacto_social='positivo', efeito_cognitivo='certeza', qtd_emocoes_opostas=1, qtd_emocoes_relacionadas=1, intensidade=5)
    carta2 = Carta(emocao='raiva', tempo='minutos', impacto_social='negativo', efeito_cognitivo='confusão', qtd_emocoes_opostas=2, qtd_emocoes_relacionadas=6, intensidade=5)
    
    usuario_admin = Usuario(username='admin', senha='admin123', status='offline', colecao_cartas='["autoestima","raiva"]', qtd_baralhos=0, baralhos='')

    session.add_all([carta1, carta2, usuario_admin])
    session.commit()

insert_data()

# SQL
# -> select
data = session.query(Carta).all()
for d in data:
    print(d.emocao)

    
    