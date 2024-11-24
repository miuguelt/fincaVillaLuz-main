from flask import Blueprint, request, jsonify
from app.models import Medications
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('medications', __name__, url_prefix='/medications')

@bp.route('/', methods=['GET'])
def get_medications():
    medications = Medications.query.all()
    return jsonify([medication.to_json() for medication in medications])


@bp.route('/<int:id>', methods=['GET'])
def get_medication(id):
    medication = Medications.query.get_or_404(id)
    return jsonify(medication.to_json())


@bp.route('/', methods=['POST'])
def create_medication():
    data = request.get_json()
    medication = Medications(**data)
    try:
        db.session.add(medication)
        db.session.commit()
        return jsonify(medication.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_medication(id):
    medication = Medications.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(medication, key, value)
        db.session.commit()
        return jsonify(medication.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400

