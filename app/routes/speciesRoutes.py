from flask import Blueprint, request, jsonify
from app.models import Species
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('species', __name__, url_prefix='/species')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_species():
    species = Species.query.all()
    return jsonify([specie.to_json() for specie in species])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_specie(id):
    specie = Species.query.get_or_404(id)
    return jsonify(specie.to_json())


@bp.route('/', methods=['POST'])
def create_specie():
    data = request.get_json()
    specie = Species(**data)
    try:
        db.session.add(specie)
        db.session.commit()
        return jsonify(specie.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_specie(id):
    specie = Species.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(specie, key, value)
        db.session.commit()
        return jsonify(specie.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


