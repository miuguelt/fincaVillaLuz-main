from flask import Blueprint, request, jsonify
from app.models import Vaccinations
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('vaccinations', __name__, url_prefix='/vaccinations')

@bp.route('/', methods=['GET'])
def get_vaccinations():
    vaccinations = Vaccinations.query.all()
    return jsonify([vaccination.to_json() for vaccination in vaccinations])


@bp.route('/<int:id>', methods=['GET'])
def get_vaccination(id):
    vaccination = Vaccinations.query.get_or_404(id)
    return jsonify(vaccination.to_json())


@bp.route('/', methods=['POST'])
def create_vaccination():
    data = request.get_json()
    vaccination = Vaccinations(**data)
    try:
        db.session.add(vaccination)
        db.session.commit()
        return jsonify(vaccination.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_vaccination(id):
    vaccination = Vaccinations.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(vaccination, key, value)
        db.session.commit()
        return jsonify(vaccination.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
