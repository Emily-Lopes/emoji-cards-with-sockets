FROM python:3.10
#Henrique: FROM ubuntu:22.04 pq ela já vai estar configurada com algumas coisas necessarias para abrir uma interface gráfica

RUN apt-get update
# RUN apt-get install -y #se precisar instalar lagumas dependências

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#especificar o comando que ele vai rodar
CMD python3 clientDB-simulation.py 

#da para passar um argumento:
# CMD python3 clientDB-simulation.py $CLIENTE_NAME