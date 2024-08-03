FROM python:3.10

RUN apt-get update
# && apt-get install -y 

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#especificar o comando que ele vai rodar
CMD python3 db-server.py