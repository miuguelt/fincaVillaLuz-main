from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timezone, datetime
from config import config
import logging
import sys

db = SQLAlchemy()

def create_app(config_name='production'):
    app = Flask(__name__)
    app_config = config[config_name]
    app.config.from_object(app_config)

    # Configurar logging detallado
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('jwt_debug.log')
        ]
    )
    
    logger = logging.getLogger(__name__)

    # Inicialización específica (como validación en producción)
    if hasattr(app_config, 'init_app'):
        app_config.init_app(app)

    jwt = JWTManager(app)

    # DEBUG: Imprimir configuración JWT crítica al inicio
    print("=" * 50, flush=True)
    print("JWT CONFIGURATION DEBUG", flush=True)
    print("=" * 50, flush=True)
    print(f"Config name: {config_name}", flush=True)
    print(f"JWT_SECRET_KEY length: {len(app.config.get('JWT_SECRET_KEY', ''))}", flush=True)
    print(f"JWT_SECRET_KEY starts with: {app.config.get('JWT_SECRET_KEY', '')[:10]}...", flush=True)
    print(f"JWT_ACCESS_TOKEN_EXPIRES: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}", flush=True)
    print(f"JWT_REFRESH_TOKEN_EXPIRES: {app.config.get('JWT_REFRESH_TOKEN_EXPIRES')}", flush=True)
    print(f"JWT_TOKEN_LOCATION: {app.config.get('JWT_TOKEN_LOCATION')}", flush=True)
    print(f"JWT_COOKIE_DOMAIN: {app.config.get('JWT_COOKIE_DOMAIN')}", flush=True)
    print(f"JWT_COOKIE_SECURE: {app.config.get('JWT_COOKIE_SECURE')}", flush=True)
    print(f"JWT_COOKIE_CSRF_PROTECT: {app.config.get('JWT_COOKIE_CSRF_PROTECT')}", flush=True)
    print(f"JWT_ACCESS_COOKIE_NAME: {app.config.get('JWT_ACCESS_COOKIE_NAME')}", flush=True)
    print(f"JWT_REFRESH_COOKIE_NAME: {app.config.get('JWT_REFRESH_COOKIE_NAME')}", flush=True)
    print(f"JWT_COOKIE_SAMESITE: {app.config.get('JWT_COOKIE_SAMESITE')}", flush=True)
    print("=" * 50, flush=True)

    # Handlers JWT con debugging detallado
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        exp_timestamp = jwt_payload['exp']
        exp_utc = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now_utc = datetime.now(timezone.utc)
        seconds_ago = int((now_utc - exp_utc).total_seconds())

        print("=" * 40, flush=True)
        print("JWT EXPIRED TOKEN DEBUG", flush=True)
        print("=" * 40, flush=True)
        print(f"Token expired at UTC: {exp_utc.isoformat()}", flush=True)
        print(f"Current time UTC: {now_utc.isoformat()}", flush=True)
        print(f"Expired {seconds_ago} seconds ago ({seconds_ago/60:.1f} minutes)", flush=True)
        print(f"JWT Header: {jwt_header}", flush=True)
        print(f"JWT Payload: {jwt_payload}", flush=True)
        print("=" * 40, flush=True)

        logger.error(f"Expired token: expired {seconds_ago} seconds ago")

        return {
            'msg': 'Token has expired',
            'expired_at_utc': exp_utc.isoformat(),
            'current_time_utc': now_utc.isoformat(),
            'seconds_expired': seconds_ago
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print("=" * 40, flush=True)
        print("JWT INVALID TOKEN DEBUG", flush=True)
        print("=" * 40, flush=True)
        print(f"Invalid token error: {error}", flush=True)
        print(f"Error type: {type(error).__name__}", flush=True)
        print("=" * 40, flush=True)
        
        logger.error(f"Invalid token: {error}")
        
        return {
            'msg': f'Invalid token: {error}',
            'error_type': type(error).__name__
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print("=" * 40, flush=True)
        print("JWT MISSING TOKEN DEBUG", flush=True)
        print("=" * 40, flush=True)
        print(f"Missing token error: {error}", flush=True)
        print("=" * 40, flush=True)
        
        logger.warning(f"Missing token: {error}")
        
        return {
            'msg': 'Missing token in request',
            'error': str(error)
        }, 401

    # Nuevo handler para errores de verificación de firma
    @jwt.decode_complete_token_loader
    def decode_complete_token_callback(encoded_token):
        """Handler personalizado para debugging de decodificación de tokens"""
        import jwt as pyjwt
        
        try:
            # Intentar decodificar sin verificar firma (solo para debug)
            unverified = pyjwt.decode(encoded_token, options={"verify_signature": False})
            
            print("=" * 40, flush=True)
            print("JWT DECODE DEBUG", flush=True)
            print("=" * 40, flush=True)
            print(f"Token payload (unverified): {unverified}", flush=True)
            
            # Verificar si está expirado
            exp_timestamp = unverified.get('exp', 0)
            if exp_timestamp:
                exp_utc = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                now_utc = datetime.now(timezone.utc)
                is_expired = now_utc > exp_utc
                print(f"Token expiry check: {exp_utc.isoformat()} (expired: {is_expired})", flush=True)
            
            print("=" * 40, flush=True)
            
        except Exception as decode_error:
            print(f"Error in decode debug: {decode_error}", flush=True)
        
        # Retornar None para que Flask-JWT-Extended use su decodificación normal
        return None

    # Handler para errores generales de JWT
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Agregar claims adicionales para debugging"""
        return {
            'server_time_utc': datetime.now(timezone.utc).isoformat(),
            'config_name': config_name
        }

    # Middleware para debugging de requests
    @app.before_request
    def log_request_info():
        from flask import request
        
        # Solo loggear requests a endpoints JWT
        if any(path in request.path for path in ['/login', '/refresh', '/protected', '/debug']):
            print("=" * 30, flush=True)
            print(f"REQUEST DEBUG: {request.method} {request.path}", flush=True)
            print(f"Headers: {dict(request.headers)}", flush=True)
            
            cookies = dict(request.cookies)
            if cookies:
                # Mostrar solo nombres de cookies para seguridad
                cookie_names = list(cookies.keys())
                print(f"Cookies present: {cookie_names}", flush=True)
                
                # Mostrar longitud de tokens JWT si existen
                if 'access_token_cookie' in cookies:
                    token_length = len(cookies['access_token_cookie'])
                    print(f"Access token length: {token_length}", flush=True)
                
                if 'refresh_token_cookie' in cookies:
                    token_length = len(cookies['refresh_token_cookie'])
                    print(f"Refresh token length: {token_length}", flush=True)
            
            print("=" * 30, flush=True)

    db.init_app(app)

    # Registrar blueprints
    from app.routes import (
        userRoutes, animalDiseasesRoutes, animalFieldsRoutes, animalsRoutes, breedsRoutes,
        controlRoutes, diseasesRoutes, fieldsRoutes, foodTypesRoutes, geneticImprovementsRoutes,
        medicationsRoutes, speciesRoutes, treatmentMedicationsRoutes, treatmentsRoutes,
        treatmentVaccinesRoutes, vaccinesRoutes, vaccinationsRoutes, auth
    )

    app.register_blueprint(userRoutes.bp)
    app.register_blueprint(animalDiseasesRoutes.bp)
    app.register_blueprint(animalFieldsRoutes.bp)
    app.register_blueprint(animalsRoutes.bp)
    app.register_blueprint(breedsRoutes.bp)
    app.register_blueprint(controlRoutes.bp)
    app.register_blueprint(diseasesRoutes.bp)
    app.register_blueprint(fieldsRoutes.bp)
    app.register_blueprint(foodTypesRoutes.bp)
    app.register_blueprint(geneticImprovementsRoutes.bp)
    app.register_blueprint(medicationsRoutes.bp)
    app.register_blueprint(speciesRoutes.bp)
    app.register_blueprint(treatmentMedicationsRoutes.bp)
    app.register_blueprint(treatmentsRoutes.bp)
    app.register_blueprint(treatmentVaccinesRoutes.bp)
    app.register_blueprint(vaccinesRoutes.bp)
    app.register_blueprint(vaccinationsRoutes.bp)
    app.register_blueprint(auth.bp)

    # Configurar CORS con debugging
    print("=" * 30, flush=True)
    print("CORS CONFIGURATION", flush=True)
    print("=" * 30, flush=True)
    
    cors_origins = [
        "http://localhost:5173",
        "https://localhost:5173", 
        "https://mifinca.isladigital.xyz"
    ]
    print(f"CORS Origins: {cors_origins}", flush=True)
    print("=" * 30, flush=True)

    CORS(
        app,
        origins=cors_origins,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials",
                       "X-Requested-With", "Origin", "Accept", "Access-Control-Request-Method",
                       "Access-Control-Request-Headers"],
        expose_headers=["Content-Type", "Authorization"],
        supports_credentials=True
    ).init_app(app)

    # Endpoint adicional para debugging completo
    @app.route('/debug-complete', methods=['GET'])
    def debug_complete():
        from flask import request
        import jwt as pyjwt
        
        result = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'config': {
                'JWT_SECRET_KEY_length': len(app.config.get('JWT_SECRET_KEY', '')),
                'JWT_ACCESS_TOKEN_EXPIRES': str(app.config.get('JWT_ACCESS_TOKEN_EXPIRES')),
                'JWT_COOKIE_DOMAIN': app.config.get('JWT_COOKIE_DOMAIN'),
                'JWT_COOKIE_SECURE': app.config.get('JWT_COOKIE_SECURE'),
                'JWT_COOKIE_CSRF_PROTECT': app.config.get('JWT_COOKIE_CSRF_PROTECT'),
            },
            'request': {
                'cookies': list(request.cookies.keys()),
                'headers': dict(request.headers),
                'origin': request.headers.get('Origin'),
                'host': request.headers.get('Host')
            }
        }
        
        # Análisis del token si existe
        access_token = request.cookies.get('access_token_cookie')
        if access_token:
            try:
                # Decodificar sin verificar
                unverified = pyjwt.decode(access_token, options={"verify_signature": False})
                result['token_analysis'] = {
                    'payload': unverified,
                    'is_expired': datetime.now(timezone.utc) > datetime.fromtimestamp(unverified.get('exp', 0), tz=timezone.utc),
                    'expires_at': datetime.fromtimestamp(unverified.get('exp', 0), tz=timezone.utc).isoformat()
                }
                
                # Intentar verificar firma
                try:
                    verified = pyjwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                    result['token_analysis']['signature_valid'] = True
                except pyjwt.InvalidSignatureError:
                    result['token_analysis']['signature_valid'] = False
                    result['token_analysis']['signature_error'] = 'Invalid signature'
                except Exception as e:
                    result['token_analysis']['signature_valid'] = False
                    result['token_analysis']['signature_error'] = str(e)
                    
            except Exception as e:
                result['token_analysis'] = {'error': str(e)}
        
        return result

    print("=" * 50, flush=True)
    print("APP INITIALIZATION COMPLETE", flush=True)
    print("=" * 50, flush=True)

    return app