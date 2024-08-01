from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

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

    
    