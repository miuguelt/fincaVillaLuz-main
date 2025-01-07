from app import create_app
from flask_cors import CORS
import os
import json

# Crear la aplicación Flask
app = create_app()

#CORS(app, supports_credentials=True, origins=["https://mifinca.isladigital.xyz"], methods=["GET", "POST", "PUT", "DELETE"], headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"], expose_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"], allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"], max_age=3600)
cors_config_str = os.environ.get('CORS_CONFIG')
cors_config = json.loads(cors_config_str)  # Convert string to dictionary
print(cors_config)
print(cors_config_str)
CORS(app, **cors_config)

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
