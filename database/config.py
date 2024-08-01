from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base

# configurações
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine) # vincular uma sessao na engine


# criando tabelas (caso ainda não existam)
Base.metadata.create_all(engine)