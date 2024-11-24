from flask import Blueprint, request, jsonify
from app.models import Fields
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('fields', __name__, url_prefix='/fields')

@bp.route('/', methods=['GET'])
def get_fields():
    fields = Fields.query.all()
    return jsonify([field.to_json() for field in fields])


@bp.route('/<int:id>', methods=['GET'])
def get_field(id):
    field = Fields.query.get(id)
    return jsonify(field.to_json())


@bp.route('/', methods=['POST'])
def create_field():
    data = request.get_json()
    field = Fields(**data)
    try:
        db.session.add(field)
        db.session.commit()
        return jsonify(field.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_field(id):
    field = Fields.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(field, key, value)
        db.session.commit()
        return jsonify(field.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

