from app import create_app

app = create_app()

if __name__ == "__main__":
    cert_path = '/proxy/cert.pem'
    key_path = '/proxy/key.pem'
    app.run(ssl_context=(cert_path, key_path))