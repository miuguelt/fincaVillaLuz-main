from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_refresh_cookies, set_access_cookies

from app.models import User

bp = Blueprint('auth',__name__)
def authenticate(identificationDTO, passwordDTO):
    # This logic should be optimized for production (e.g., query the database directly)
    # For now, it is functionally correct for the example.
    user_data = User.query.filter_by(identification=identificationDTO).first()
    if user_data and user_data.password == passwordDTO: # In a real app, use a password hashing library like Werkzeug or passlib
        return user_data
    return None

@bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    # 1. Get the JSON data from the request and store it in a variable.
    data = request.get_json()

    # 2. Check if JSON data was sent.
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    # 3. Get credentials from the stored 'data' variable.
    identificationDto = data.get('identification', None)
    passwordDto = data.get('password', None)

    if not identificationDto or not passwordDto:
        return jsonify({"error": "Identificacion y contraseña son requeridos"}), 400

    user = authenticate(str(identificationDto), passwordDto) # Ensure identification is a string

    if not user:
        return jsonify({"error": "Identificacion o contraseña incorecta"}), 401
    print("fin2", flush=True)

    # Create tokens and response
    identity = {
        "identification": user.identification, 
        "role": user.role.value, 
        "fullname": user.fullname, 
        "email": user.email, 
        "phone": user.phone, 
        "address": user.address
    }
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    print("fin 1", flush=True)

    response = jsonify({"login": True})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    print("fin", flush=True)
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