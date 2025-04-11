from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models import User

bp = Blueprint('auth',__name__)


def authenticate(identificationDTO, passwordDTO):
    udata = User.query.all()
    for user_data in udata:
        identification = user_data.identification
        password = user_data.password
        if identification == identificationDTO and password == passwordDTO:
            return user_data
    return None

@bp.route('/login', methods=['POST', 'OPTIONS'], strict_slashes=False)
def login():
   identificationDto = request.json.get('identification', None)
   passwordDto = request.json.get('password', None)

   if identificationDto is None or passwordDto is None:
      return jsonify({"error": "Identificacion y contraseña son requeridos"}), 400

   user = authenticate(identificationDto, passwordDto)
   print(user)
   if not user:
      return jsonify({"error": "Identificacion o contraseña incorecta"}), 401

   access_token = create_access_token(identity={"identification": user.identification, "role": user.role.value, "fullname": user.fullname, "email": user.email, "phone": user.phone, "address": user.address})
   return jsonify(access_token=access_token), 200
   

@bp.route('/protected', methods=['GET'], strict_slashes=False)
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200