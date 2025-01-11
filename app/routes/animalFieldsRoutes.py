from flask import Blueprint, request, jsonify
from app.models import AnimalFields
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('animalFields', __name__, url_prefix='/animalFields')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_animalFields():
    animalFields = AnimalFields.query.all()
    return jsonify([animalField.to_json() for animalField in animalFields])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_animalField(id):
    animalFields = AnimalFields.query.get_or_404(id)
    return jsonify(animalFields.to_json())


@bp.route('/', methods=['POST'])
def create_animalFields():
    data = request.get_json()
    animalField = AnimalFields(**data)
    try:
        db.session.add(animalField)
        db.session.commit()
        return jsonify(animalField.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_animalFields(id):
    animalFields = AnimalFields.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(animalFields, key, value)
        db.session.commit()
        return jsonify(animalFields.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400



