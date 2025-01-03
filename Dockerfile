FROM python:3.12-alpine

# Establecer el directorio de trabajo
WORKDIR /app/fincaBack-main

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Expone el puerto que usará la aplicación
EXPOSE 8081

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]