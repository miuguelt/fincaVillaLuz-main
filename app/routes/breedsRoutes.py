from flask import Blueprint, request, jsonify
from app.models import Breeds
from app.models import Species
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('breeds', __name__, url_prefix='/breeds')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_breeds():
    breeds = Breeds.query.all()
    return jsonify([breed.to_json() for breed in breeds])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_breed(id):
    breeds = Breeds.query.get_or_404(id)
    return jsonify(breeds.to_json())


@bp.route('/', methods=['POST'])
def create_breeds():
    data = request.get_json()
    breed = Breeds(**data)
    try:
        db.session.add(breed)
        db.session.commit()
        return jsonify(breed.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_breeds(id):
    breeds = Breeds.query.get_or_404(id)
    data = request.get_json()
    try:
        # Manejar campos no relacionados
        for key, value in data.items():
            if key == 'species_id':  # Manejo de la clave foránea
                species = Species.query.get(value)
                if species:
                    breeds.species = species
            else:
                setattr(breeds, key, value)
                
        db.session.commit()
        return jsonify(breeds.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

