
from app import create_app, db
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()

from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException

@app.errorhandler(JWTExtendedException)
def handle_jwt_errors(e):
    return jsonify({"error": str(e)}), 401