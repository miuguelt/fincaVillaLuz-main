from app import create_app
from flask_cors import CORS

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}}, 
supports_credentials=True, 
methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],    
allow_headers=["Content-Type", "Authorization"])

if __name__ == "__main__":
    app.run()