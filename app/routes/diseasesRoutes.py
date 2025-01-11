from flask import Blueprint, request, jsonify
from app.models import Diseases
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('diseases', __name__, url_prefix='/diseases')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_diseases():
    diseases = Diseases.query.all()
    return jsonify([disease.to_json() for disease in diseases])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_disease(id):
    diseases = Diseases.query.get_or_404(id)
    return jsonify(diseases.to_json())


@bp.route('/', methods=['POST'])
def create_diseases():
    data = request.get_json()
    disease = Diseases(**data)
    try:
        db.session.add(disease)
        db.session.commit()
        return jsonify(disease.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_diseases(id):
    diseases = Diseases.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(diseases, key, value)
        db.session.commit()
        return jsonify(diseases.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

