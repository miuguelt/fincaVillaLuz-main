from flask import Blueprint, request, jsonify
from app.models import GeneticImprovements
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('geneticImprovements', __name__, url_prefix='/geneticImprovements')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_geneticImprovements():
    geneticImprovements = GeneticImprovements.query.all()
    return jsonify([geneticImprovement.to_json() for geneticImprovement in geneticImprovements])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_geneticImprovement(id):
    geneticImprovements = GeneticImprovements.query.get_or_404(id)
    return jsonify(geneticImprovements.to_json())


@bp.route('/', methods=['POST'])
def create_geneticImprovements():
    data = request.get_json()
    geneticImprovement = GeneticImprovements(**data)
    try:
        db.session.add(geneticImprovement)
        db.session.commit()
        return jsonify(geneticImprovement.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_geneticImprovements(id):
    geneticImprovements = GeneticImprovements.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(geneticImprovements, key, value)
        db.session.commit()
        return jsonify(geneticImprovements.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
