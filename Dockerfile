FROM python:3.12-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copiar el resto del código
COPY . .

COPY /data/coolify/proxy/acme.json /app/proxy/acme.json
RUN python certificados.py

EXPOSE 8081

CMD ["python", "run.py"]
