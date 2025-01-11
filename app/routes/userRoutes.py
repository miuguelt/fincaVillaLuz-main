from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from flask_cors import cross_origin

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'], strict_slashes=False, strict_slashes=False)
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False, strict_slashes=False)
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@bp.route('/status', methods=['GET'], strict_slashes=False)
def get_user_status():
    status_counts = db.session.query(
        User.status, db.func.count(User.status)
    ).group_by(User.status).all()
    status_data = [{"status": status, "count": count} for status, count in status_counts]
    return jsonify(status_data)


@bp.route('/roles', methods=['GET'], strict_slashes=False)
def get_user_roles():
    roles = db.session.query(
        User.role, db.func.count(User.role)
    ).group_by(User.role).all()
    roles_data = [{"role": role.value , "count": count} for role, count in roles]
    return jsonify(roles_data)


@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Verifica que todos los campos requeridos estén presentes
    required_fields = ["fullname", "email", "password", "phone", "address", "identification", "role", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
    
    # Crea el usuario
    user = User(**data)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        # Devuelve un mensaje de error más específico
        error_info = str(e.orig)
        if "duplicate key" in error_info.lower():
            return jsonify({"error": "El correo electrónico ya está en uso"}), 400
        elif "null value" in error_info.lower():
            return jsonify({"error": "Faltan campos requeridos"}), 400
        else:
            return jsonify({"error": error_info}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
