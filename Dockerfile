# Usamos la imagen más ligera de Python basada en Alpine
FROM python:3.12-alpine
# Continúa con la instalación de dependencias, si es necesario
WORKDIR /app/fincaBack-main
# Clona el repositorio público
RUN git clone https://github.com/miuguelt/fincaBack-main.git

COPY requirements.txt /app/fincaBack-main
RUN pip install -r requirements.txt

# Expone el puerto que usará la aplicación
EXPOSE 8081

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]