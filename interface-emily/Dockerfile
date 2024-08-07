FROM python:3.9

RUN apt-get update

RUN apt-get install -y -qq --no-install-recommends \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libgl1-mesa-glx \
    libgles2-mesa-dev \
    libglfw3 \
    libglfw3-dev \
    freeglut3-dev \
    x11-apps

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "main.py"]