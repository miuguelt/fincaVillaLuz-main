# Usamos la imagen más ligera de Python basada en Alpine
FROM python:3.12-alpine

WORKDIR /app/fincaBack-main

COPY requirements.txt /app/fincaBack-main
RUN pip install -r requirements.txt

# Expone el puerto que usará la aplicación
EXPOSE 8081

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]