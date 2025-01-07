from app import create_app

# Crear la aplicación Flask
app = create_app()

if __name__ == "__main__":
    # Permitir que Gunicorn ejecute la aplicación
    app.run(ssl_context='adhoc')
