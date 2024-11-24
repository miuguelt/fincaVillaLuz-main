# Usamos la imagen más ligera de Python basada en Alpine
FROM python:3.12-alpine

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de requisitos y el proyecto
COPY requirements.txt /app/
COPY . /app/

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará la aplicación
EXPOSE 8081

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]