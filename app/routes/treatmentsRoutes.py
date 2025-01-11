from flask import Blueprint, request, jsonify
from app.models import Treatments
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('treatments', __name__, url_prefix='/treatments')

@bp.route('/', methods=['GET'], strict_slashes=False)
def get_treatments():
    # treatments = Treatments.query.all()
    # return jsonify([treatment.to_json() for treatment in treatments])
    animal_id = request.args.get('animal_id')
    if animal_id:
        treatments = Treatments.query.filter_by(animal_id=animal_id).all()
    else:
        treatments = Treatments.query.all()
    return jsonify([treatment.to_json() for treatment in treatments])


@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_treatment(id):
    treatment = Treatments.query.get_or_404(id)
    return jsonify(treatment.to_json())


@bp.route('/', methods=['POST'])
def create_treatment():
    data = request.get_json()
    treatment = Treatments(**data)
    try:
        db.session.add(treatment)
        db.session.commit()
        return jsonify(treatment.to_json()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400


@bp.route('/<int:id>', methods=['PUT'])
def update_treatment(id):
    treatment = Treatments.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(treatment, key, value)
        db.session.commit()
        return jsonify(treatment.to_json())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
