from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_refresh_cookies, set_access_cookies

from app.models import User

bp = Blueprint('auth',__name__)

def authenticate(identificationDTO, passwordDTO):
    user = User.query.filter_by(identification=identificationDTO).first()
    if user and user.password == passwordDTO:
        return user
    return None
@bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    print("Antes de data", flush=True)
    # Imprimir el contenido bruto de la petición
    print("Request data raw:", request.data, flush=True)

    # Parse the JSON and store it in a variable
    data = request.get_json()
    print("Request JSON:", data, flush=True)

    if not data:
        return jsonify({"error": "Petición no contiene JSON"}), 400

    identificationDto = data.get('identification', None)
    passwordDto = data.get('password', None)
    
    print(f"Valores extraidos - Identificacion: {identificationDto}, Contraseña: {passwordDto}", flush=True)

    if not identificationDto or not passwordDto:
        return jsonify({"error": "Identificacion y contraseña son requeridos"}), 400

    user = authenticate(identificationDto, passwordDto)
    print(user)
    if not user:
        return jsonify({"error": "Identificacion o contraseña incorecta"}), 401

    identity = {"identification": user.identification, "role": user.role.value, "fullname": user.fullname, "email": user.email, "phone": user.phone, "address": user.address}
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({"login": True})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    response = jsonify({'refresh': True})
    set_access_cookies(response, new_token)
    return response

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200