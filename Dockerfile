FROM python:3.12-alpine AS backend

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copiar el resto del código
COPY . .

EXPOSE 8081

RUN python certificados.py

#CMD ["gunicorn", "--bind", "0.0.0.0:8081", "--workers", "4", "--forwarded-allow-ips=*", "wsgi:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "--workers", "4", "--certfile=proxy/cert.pem", "--keyfile=proxy/key.pem", "wsgi:app"]
