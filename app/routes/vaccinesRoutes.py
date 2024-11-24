from flask import Blueprint, request, jsonify
from app.models import Vaccines
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('vaccines', __name__, url_prefix='/vaccines')

@bp.route('/', methods=['GET'])
def get_vaccines():
    vaccines = Vaccines.query.all()
    return jsonify([vaccine.to_json() for vaccine in vaccines])


@bp.route('/<int:id>', methods=['GET'])
def get_vaccine(id):
    vaccine = Vaccines.query.get(id)
    return jsonify(vaccine.to_json())


@bp.route('/', methods=['POST'])
def create_vaccine():
    data = request.get_json()
    vaccine = Vaccines(**data)
    try:
        db.session.add(vaccine)
        db.session.commit()
        return jsonify(vaccine.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_vaccine(id):
    vaccine = Vaccines.query.get(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(vaccine, key, value)
        db.session.commit()
        return jsonify(vaccine.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
