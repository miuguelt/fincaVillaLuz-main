from app import create_app

# Crear la aplicación Flask
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Permitir que Gunicorn ejecute la aplicación
    app.run()
