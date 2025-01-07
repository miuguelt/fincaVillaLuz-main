from app import create_app
from flask_cors import CORS


# Crear la aplicación Flask
app = create_app()

CORS(app, supports_credentials=True, origins=["https://mifinca.isladigital.xyz"], methods=["GET", "POST", "PUT", "DELETE"], headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"], expose_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"], allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"], max_age=3600)


if __name__ == "__main__":
    # Permitir que Gunicorn ejecute la aplicación
    app.run()
