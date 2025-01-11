from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from flask_cors import cross_origin

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])

@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@bp.route('/status', methods=['GET'])
def get_user_status():
    status_counts = db.session.query(
        User.status, db.func.count(User.status)
    ).group_by(User.status).all()
    status_data = [{"status": status, "count": count} for status, count in status_counts]
    return jsonify(status_data)


@bp.route('/roles', methods=['GET'])
def get_user_roles():
    roles = db.session.query(
        User.role, db.func.count(User.role)
    ).group_by(User.role).all()
    roles_data = [{"role": role.value , "count": count} for role, count in roles]
    return jsonify(roles_data)

@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
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
