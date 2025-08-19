from flask import Blueprint, request, jsonify
from app.models import Animals
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

bp = Blueprint('animals', __name__, url_prefix='/animals')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_animals():
    animals = Animals.query.all()
    return jsonify([animal.to_json() for animal in animals])

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_animal(id):
    animals = Animals.query.get_or_404(id)
    return jsonify(animals.to_json())

@bp.route('/status', methods=['GET'], strict_slashes=False)
def get_animal_status():
    # Consultar la base de datos para contar la cantidad de animales en cada estado
    status_counts = db.session.query(
        Animals.status, db.func.count(Animals.status)
    ).group_by(Animals.status).all()

    # Formatear los resultados en un JSON
    status_data = [{"status": status.value, "count": count} for status, count in status_counts]

    # Devolver el JSON como respuesta
    return jsonify(status_data)

@bp.route('/', methods=['POST'])
def create_animals():
    data = request.get_json()
    animal = Animals(**data)
    try:
        db.session.add(animal)
        db.session.commit()
        return jsonify(animal.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
    
@bp.route('/<int:id>', methods=['PUT'])
def update_animals(id):
    animals = Animals.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(animals, key, value)
        db.session.commit()
        return jsonify(animals.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


