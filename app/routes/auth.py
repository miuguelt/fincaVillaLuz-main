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
    identificationDto = request.json.get('identification', None)
    passwordDto = request.json.get('password', None)
    print("-------login-------------------------", identificationDto, passwordDto, flush=True)
    if not identificationDto or not passwordDto:
        return jsonify({"error": "Identificación y contraseña son requeridos"}), 400

    user = authenticate(identificationDto, passwordDto)
    if not user:
        return jsonify({"error": "Identificación o contraseña incorrecta"}), 401

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
    print("Token generado:", access_token, flush=True)
    response = jsonify({
        "login": True,
        "logged_in_as": identity  # Incluye los datos del usuario
    })

    response = jsonify({"login": True, "logged_in_as": identity})
    set_access_cookies(response, access_token, domain="mifinca.isladigital.xyz")
    set_refresh_cookies(response, refresh_token, domain="mifinca.isladigital.xyz")
    print("inicio de sesion", flush=True)
    return response

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_identity = get_jwt_identity() 
    new_access_token = create_access_token(identity=current_user_identity)
    print("-------fin refichs-------------------------", current_user_identity, flush=True)
    response = jsonify({
        'refresh': True,    
        'logged_in_as': current_user_identity # <-- This is still missing in your provided code
    })
    set_access_cookies(response, new_access_token)
    print("-------fin2-------------------------", response, flush=True)
    print("refresh token generado:", new_access_token, flush=True)
    return response

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    print("-------entra a protected-------", flush=True)
    try:
        current_user = get_jwt_identity()
        print("-------fin2- protected------------------------", current_user, flush=True)
        return jsonify(logged_in_as=current_user), 200
    except Exception as e:
        print("-------fin2 error-------------------------", e, flush=True)
        return jsonify(error=str(e)), 401