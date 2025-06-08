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
    set_access_cookies(response, access_token, domain="finca.isladigital.xyz") 
    set_refresh_cookies(response, refresh_token, domain="finca.isladigital.xyz")
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
    set_access_cookies(response, new_access_token, domain="finca.isladigital.xyz")
    print("-------fin2-------------------------", response, flush=True)
    print("refresh token generado:", new_access_token, flush=True)
    return response

# En tu backend Flask, agrega estos debugs:

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    print("-------entra a protected-------", flush=True)
    
    # Debug: verificar el token crudo
    from flask import request
    print("Cookies recibidas:", request.cookies, flush=True)
    
    # Debug: verificar el token JWT
    try:
        from flask_jwt_extended import get_jwt
        current_token = get_jwt()
        print("Token JWT decodificado:", current_token, flush=True)
    except Exception as token_error:
        print("Error al decodificar token:", token_error, flush=True)
    
    try:
        current_user = get_jwt_identity()
        print("Usuario actual:", current_user, flush=True)
        return jsonify(logged_in_as=current_user), 200
    except Exception as e:
        print("Error en protected:", str(e), flush=True)
        print("Tipo de error:", type(e).__name__, flush=True)
        return jsonify(error=str(e)), 401

# También verifica tu configuración JWT:
@bp.route('/debug-jwt-config', methods=['GET'])
def debug_jwt_config():
    from flask import current_app
    return jsonify({
        'jwt_secret_key_set': bool(current_app.config.get('JWT_SECRET_KEY')),
        'jwt_token_location': current_app.config.get('JWT_TOKEN_LOCATION'),
        'jwt_cookie_secure': current_app.config.get('JWT_COOKIE_SECURE'),
        'jwt_cookie_csrf_protect': current_app.config.get('JWT_COOKIE_CSRF_PROTECT'),
        'jwt_access_cookie_name': current_app.config.get('JWT_ACCESS_COOKIE_NAME'),
        'jwt_refresh_cookie_name': current_app.config.get('JWT_REFRESH_COOKIE_NAME'),
    })

# Y un endpoint para verificar si las cookies se están enviando correctamente:
@bp.route('/debug-cookies', methods=['GET'])
def debug_cookies():
    from flask import request
    cookies = dict(request.cookies)
    print("Todas las cookies:", cookies, flush=True)
    
    # Intentar decodificar el access token manualmente
    access_cookie = cookies.get('access_token_cookie')
    if access_cookie:
        try:
            import jwt
            from flask import current_app
            # Decodificar sin verificar (solo para debug)
            decoded = jwt.decode(access_cookie, options={"verify_signature": False})
            print("Token decodificado (sin verificar):", decoded, flush=True)
            
            # Ahora intentar verificar la firma
            try:
                verified = jwt.decode(access_cookie, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                print("Token verificado exitosamente:", verified, flush=True)
            except jwt.InvalidSignatureError:
                print("ERROR: Firma del token inválida", flush=True)
            except Exception as verify_error:
                print("ERROR en verificación:", verify_error, flush=True)
            
        except Exception as decode_error:
            print("ERROR al decodificar token:", decode_error, flush=True)
    
    return jsonify({
        'cookies_received': list(cookies.keys()),
        'access_token_present': 'access_token_cookie' in cookies,
        'refresh_token_present': 'refresh_token_cookie' in cookies
    })