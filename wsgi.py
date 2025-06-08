
from app import create_app, db, jsonify
from flask_jwt_extended.exceptions import JWTExtendedException

app = create_app()

with app.app_context():
    db.create_all()

@app.errorhandler(JWTExtendedException)
def handle_jwt_errors(e):
    return jsonify({"error": str(e)}), 401
if __name__ == "__main__":
    app.run()