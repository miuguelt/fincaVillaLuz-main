FROM python:3.12-alpine

# Establecer el directorio de trabajo
WORKDIR /app/fincaBack-main

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN npm install -g npm@11.0.0
RUN pip install -r requirements.txt
RUN npm audit fix
# Copiar el resto del código
COPY . .

# Expone el puerto que usará la aplicación
EXPOSE 8081

CMD ["gunicorn", "--bind", "0.0.0.0:8081", "wsgi:app"]