from flask import Blueprint, request, jsonify
from app.models import Control
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('control', __name__, url_prefix='/control')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_users():
    controls = Control.query.all()
    return jsonify([control.to_json() for control in controls])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_control(id):
    control = Control.query.get_or_404(id)
    return jsonify(control.to_json())


@bp.route('/', methods=['POST'])
def create_control():
    data = request.get_json()
    control = Control(**data)
    try:
        db.session.add(control)
        db.session.commit()
        return jsonify(control.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_control(id):
    control = Control.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(control, key, value)
        db.session.commit()
        return jsonify(control.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


