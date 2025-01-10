from app import create_app
from flask_cors import CORS
import os
import json
from flask import jsonify

# Crear la aplicación Flask
app = create_app()

# Configuración detallada de CORS
CORS(app)

# Hook para capturar el encabezado Access-Control-Allow-Origin
@app.after_request
def log_cors_headers(response):
    # Imprimir el valor del encabezado Access-Control-Allow-Origin
    cors_header = response.headers.get('Access-Control-Allow-Origin')
    if cors_header:
        print(f"Access-Control-Allow-Origin: {cors_header}")
    return response

# Ruta de ejemplo
@app.route('/example', methods=['GET'])
def example():
    return jsonify({"message": "Hello, world!"}), 200

if __name__ == "__main__":
    # Permitir que Gunicorn ejecute la aplicación
    app.run()