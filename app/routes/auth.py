from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_refresh_cookies, set_access_cookies
from datetime import timezone, datetime, timedelta
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
    
        # SOLO CAMBIAR ESTAS LÍNEAS:
    now_utc = datetime.now(timezone.utc)  # NUEVA LÍNEA
    

    identity = {
        "identification": user.identification,
        "role": user.role.value,
        "fullname": user.fullname,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "login_time_utc": now_utc.isoformat()
    }

    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    print("Token generado:", access_token, flush=True)
    response = jsonify({
        "login": True,
        "logged_in_as": identity  # Incluye los datos del usuario
    })

    set_access_cookies(response, access_token, domain="finca.isladigital.xyz") 
    set_refresh_cookies(response, refresh_token, domain="finca.isladigital.xyz")
    print("inicio de sesion", flush=True)
        # LOG MÍNIMO PARA DEBUG
    expires_at_utc = now_utc + timedelta(hours=1)  # Ajusta según tu config
    print(f"=== LOGIN DEBUG ===")
    print(f"Login UTC: {now_utc.isoformat()}")
    print(f"Expires UTC: {expires_at_utc.isoformat()}")
    print(f"User: {identity.get('identification', 'unknown')}")
    print("=================")
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
# Agrega este endpoint a tu Flask backend para debugging detallado

@bp.route('/debug-token-detailed', methods=['GET'])
def debug_token_detailed():
    from flask import request, current_app
    import jwt
    from datetime import datetime
    
    print("=== DEBUG TOKEN DETAILED ===", flush=True)
    
    # Obtener cookies
    cookies = dict(request.cookies)
    access_cookie = cookies.get('access_token_cookie')
    refresh_cookie = cookies.get('refresh_token_cookie')
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'cookies_received': list(cookies.keys()),
        'access_token_present': bool(access_cookie),
        'refresh_token_present': bool(refresh_cookie),
        'request_origin': request.headers.get('Origin'),
        'request_host': request.headers.get('Host'),
        'user_agent': request.headers.get('User-Agent'),
        'errors': []
    }
    
    if access_cookie:
        try:
            # Decodificar sin verificar firma
            decoded_unverified = jwt.decode(access_cookie, options={"verify_signature": False})
            result['token_payload_unverified'] = decoded_unverified
            
            # Verificar expiración
            exp_timestamp = decoded_unverified.get('exp', 0)
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            is_expired = datetime.now() > exp_datetime
            
            result['token_expires_at'] = exp_datetime.isoformat()
            result['token_is_expired'] = is_expired
            
            print(f"Token expira en: {exp_datetime}", flush=True)
            print(f"Token expirado: {is_expired}", flush=True)
            
            # Intentar verificar firma
            try:
                secret_key = current_app.config['JWT_SECRET_KEY']
                decoded_verified = jwt.decode(access_cookie, secret_key, algorithms=['HS256'])
                result['token_signature_valid'] = True
                result['token_payload_verified'] = decoded_verified
                print("Firma del token VÁLIDA", flush=True)
                
            except jwt.ExpiredSignatureError:
                result['errors'].append('Token expired')
                result['token_signature_valid'] = False
                print("ERROR: Token expirado", flush=True)
                
            except jwt.InvalidSignatureError:
                result['errors'].append('Invalid signature')
                result['token_signature_valid'] = False
                print("ERROR: Firma inválida", flush=True)
                
            except Exception as verify_error:
                result['errors'].append(f'Verification error: {str(verify_error)}')
                result['token_signature_valid'] = False
                print(f"ERROR en verificación: {verify_error}", flush=True)
                
        except Exception as decode_error:
            result['errors'].append(f'Decode error: {str(decode_error)}')
            print(f"ERROR al decodificar: {decode_error}", flush=True)
    
    # Intentar usar Flask-JWT-Extended para verificar el token
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
        
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        current_jwt = get_jwt()
        
        result['flask_jwt_verification'] = {
            'success': True,
            'current_user': current_user,
            'jwt_claims': current_jwt
        }
        print(f"Flask-JWT-Extended verificación EXITOSA: {current_user}", flush=True)
        
    except Exception as flask_jwt_error:
        result['flask_jwt_verification'] = {
            'success': False,
            'error': str(flask_jwt_error)
        }
        print(f"Flask-JWT-Extended ERROR: {flask_jwt_error}", flush=True)
    
    print("=== FIN DEBUG ===", flush=True)
    return jsonify(result)

# También modifica tu endpoint protected para más debugging:
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    print("=== PROTECTED ENDPOINT ===", flush=True)
    
    try:
        # Debug detallado
        from flask import request
        print(f"Headers: {dict(request.headers)}", flush=True)
        print(f"Cookies: {dict(request.cookies)}", flush=True)
        
        current_user = get_jwt_identity()
        current_jwt = get_jwt()
        
        print(f"Usuario: {current_user}", flush=True)
        print(f"JWT Claims: {current_jwt}", flush=True)
        
        return jsonify(
            logged_in_as=current_user,
            jwt_claims=current_jwt,
            message="Protected endpoint accessed successfully"
        ), 200
        
    except Exception as e:
        print(f"ERROR en protected: {str(e)}", flush=True)
        print(f"Tipo de error: {type(e).__name__}", flush=True)
        
        # Más información del error
        import traceback
        print(f"Traceback: {traceback.format_exc()}", flush=True)
        
        return jsonify(error=str(e), error_type=type(e).__name__), 401
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

@bp.route('/debug-time', methods=['GET'])
def debug_time():
    now_utc = datetime.now(timezone.utc)
    return jsonify({
        'server_utc': now_utc.isoformat(),
        'server_timestamp': int(now_utc.timestamp()),
        'timezone': 'UTC'
    })