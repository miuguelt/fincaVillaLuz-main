from flask import Blueprint, request, jsonify
from app.models import TreatmentVaccines
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('treatmentVaccines', __name__, url_prefix='/treatmentVaccines')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_treatmentVaccines():
    treatmentVaccines = TreatmentVaccines.query.all()
    return jsonify([treatmentVaccine.to_json() for treatmentVaccine in treatmentVaccines])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_treatmentVaccine(id):
    treatmentVaccine = TreatmentVaccines.query.get_or_404(id)
    return jsonify(treatmentVaccine.to_json())


@bp.route('/', methods=['POST'])
def create_treatmentVaccine():
    data = request.get_json()
    treatmentVaccine = TreatmentVaccines(**data)
    try:
        db.session.add(treatmentVaccine)
        db.session.commit()
        return jsonify(treatmentVaccine.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_treatmentVaccine(id):
    treatmentVaccine = TreatmentVaccines.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(treatmentVaccine, key, value)
        db.session.commit()
        return jsonify(treatmentVaccine.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

