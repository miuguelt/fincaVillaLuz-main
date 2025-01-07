from app import create_app
from flask_cors import CORS


# Crear la aplicación Flask
app = create_app()

CORS(app, supports_credentials=True, origins=["https://mifinca.isladigital.xyz"])


if __name__ == "__main__":
    # Permitir que Gunicorn ejecute la aplicación
    app.run()
