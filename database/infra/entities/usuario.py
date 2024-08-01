from infra.configs.base import Base
from sqlalchemy import Column, Integer, String

class Usuario(Base):
    __tablename__ = 'usuario'
    username = Column(String, primary_key=True)
    senha = Column(String)
    status = Column(String) #jogando - online - offline
    colecao_cartas = Column(String) #string simulado um vetor com nome das cartas: ['carta1', 'carta2',..]
    qtd_baralhos = Column(Integer)
    baralhos = Column(String) #string simulando um vetor de vetores: [['baralho1'],['baralho2'],['baralho3']]
