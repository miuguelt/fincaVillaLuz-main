from flask import Blueprint, request, jsonify
from app.models import TreatmentMedications
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('treatmentMedications', __name__, url_prefix='/treatmentMedications')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_treatmentMedications():
    treatmentMedications = TreatmentMedications.query.all()
    return jsonify([treatmentMedication.to_json() for treatmentMedication in treatmentMedications])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_treatmentMedication(id):
    treatmentMedication = TreatmentMedications.query.get_or_404(id)
    return jsonify(treatmentMedication.to_json())


@bp.route('/', methods=['POST'])
def create_treatmentMedication():
    data = request.get_json()
    treatmentMedication = TreatmentMedications(**data)
    try:
        db.session.add(treatmentMedication)
        db.session.commit()
        return jsonify(treatmentMedication.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_treatmentMedication(id):
    treatmentMedication = TreatmentMedications.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(treatmentMedication, key, value)
        db.session.commit()
        return jsonify(treatmentMedication.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
