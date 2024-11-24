from flask import Blueprint, request, jsonify
from app.models import AnimalDiseases
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('animalDiseases', __name__, url_prefix='/animalDiseases')

@bp.route('/', methods=['GET'])
def get_animalDiseases():
    animalDiseases = AnimalDiseases.query.all()
    return jsonify([animalDiseases.to_json() for animalDiseases in animalDiseases])

@bp.route('/<int:id>', methods=['GET'])
def get_animalDisease(id):
    animalDiseases = AnimalDiseases.query.get_or_404(id)
    return jsonify(animalDiseases.to_json())

@bp.route('/', methods=['POST'])
def create_animalDiseases():
    data = request.get_json()
    animalDiseases = AnimalDiseases(**data)
    try:
        db.session.add(animalDiseases)
        db.session.commit()
        return jsonify(animalDiseases.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
    

@bp.route('/<int:id>', methods=['PUT'])
def update_animalDiseases(id):
    animalDiseases = AnimalDiseases.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(animalDiseases, key, value)
        db.session.commit()
        return jsonify(animalDiseases.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
    



