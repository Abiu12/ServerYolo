FROM python:3.8.10

# Crea el directorio de la aplicación
RUN mkdir -p /home/app

# Copia los archivos de la aplicación al directorio
COPY . /home/app

RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install flask flask-cors
RUN pip install waitress
RUN pip install ultralytics 

# Expone el puerto 5000
EXPOSE 5000

CMD ["python" ,"/home/app/run.py"]
