from flask import Blueprint, request, jsonify
from app.models import FoodTypes
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('foodTypes', __name__, url_prefix='/foodTypes')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_foodTypes():
    foodTypes = FoodTypes.query.all()
    return jsonify([foodType.to_json() for foodType in foodTypes])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_foodType(id):
    foodTypes = FoodTypes.query.get_or_404(id)
    return jsonify(foodTypes.to_json())


@bp.route('/', methods=['POST'])
def create_foodTypes():
    data = request.get_json()
    foodType = FoodTypes(**data)
    try:
        db.session.add(foodType)
        db.session.commit()
        return jsonify(foodType.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_foodTypes(id):
    foodTypes = FoodTypes.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(foodTypes, key, value)
        db.session.commit()
        return jsonify(foodTypes.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

