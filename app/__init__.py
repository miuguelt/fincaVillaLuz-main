from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timezone, datetime
from config import config
import logging
import sys
import jwt as pyjwt # Usamos un alias para evitar conflictos con flask_jwt_extended

# ====================================================================
# 1. Inicialización de extensiones (sinlazarlas a la app aún)
# ====================================================================
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

# ====================================================================
# 2. Funciones de ayuda y configuración modular
# ====================================================================
def configure_logging(app):
    """Configura el sistema de logging de la aplicación."""
    # Accede al nivel de log definido en la configuración
    log_level = app.config.get('LOG_LEVEL', logging.INFO)
    
    # Define los handlers de log
    handlers = [
        logging.StreamHandler(sys.stdout)
    ]
    # Si la configuración lo permite, añade un FileHandler
    if app.config.get('LOG_FILE_ENABLED', False):
        log_file = app.config.get('LOG_FILE', 'app.log')
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    logging.getLogger('werkzeug').setLevel(logging.INFO) # Silencia logs de werkzeug si están muy bajos

def configure_jwt_handlers():
    """Configura los handlers para errores de JWT. Se llama después de jwt.init_app()."""
    
    logger = logging.getLogger(__name__)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        exp_timestamp = jwt_payload['exp']
        exp_utc = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now_utc = datetime.now(timezone.utc)
        seconds_ago = int((now_utc - exp_utc).total_seconds())

        logger.warning(f"Expired token: expired {seconds_ago} seconds ago. Payload: {jwt_payload}")

        return jsonify({
            'msg': 'Token has expired',
            'expired_at_utc': exp_utc.isoformat(),
            'current_time_utc': now_utc.isoformat(),
            'seconds_expired': seconds_ago
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.error(f"Invalid token: {error}")
        return jsonify({
            'msg': f'Invalid token: {error}',
            'error_type': type(error).__name__
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        logger.warning(f"Missing token: {error}")
        return jsonify({
            'msg': 'Missing token in request',
            'error': str(error)
        }), 401

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Agrega claims adicionales para debugging"""
        return {
            'server_time_utc': datetime.now(timezone.utc).isoformat(),
            'server_env': request.app.config.get('CONFIG_NAME')
        }

# ====================================================================
# 3. La función principal de creación de la aplicación
# ====================================================================
def create_app(config_name='production'):
    app = Flask(__name__)
    app_config = config.get(config_name, 'default')
    
    # 3.1. Carga la configuración desde el objeto
    app.config.from_object(app_config)
    app.config['CONFIG_NAME'] = config_name # Almacena el nombre para usarlo en los logs

    # 3.2. Configura el logging (antes de cualquier otra cosa)
    configure_logging(app)
    logger = logging.getLogger(__name__)

    logger.info("Initializing Flask app...")
    logger.debug(f"Using configuration: {config_name}")

    # 3.3. Inicializa y enlaza las extensiones con la app
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # 3.4. Configura los handlers de JWT de forma modular
    configure_jwt_handlers()

    # 3.5. Configura CORS
    # Las opciones de CORS ya están en la instancia de 'cors' si usas el método init_app
    # Por lo tanto, no es necesario llamar a CORS(app, ...).init_app(app)
    # Solo necesitas las opciones en la configuración o pasarlas al constructor
    
    # 3.6. Registra los blueprints
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
    
    # 3.7. Middleware para debugging (ahora con logging)
    @app.before_request
    def log_request_info():
        # Solo loggea si la configuración está en DEBUG
        if app.config.get('DEBUG', False):
            if any(path in request.path for path in ['/login', '/refresh', '/protected', '/debug']):
                logger.debug(f"REQUEST: {request.method} {request.path}")
                logger.debug(f"Headers: {dict(request.headers)}")
                if request.cookies:
                    logger.debug(f"Cookies present: {list(request.cookies.keys())}")
    
    # 3.8. Endpoint para debugging completo
    @app.route('/debug-complete', methods=['GET'])
    def debug_complete():
        access_token = request.cookies.get('access_token_cookie')
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
        if access_token:
            try:
                unverified = pyjwt.decode(access_token, options={"verify_signature": False})
                result['token_analysis'] = {
                    'payload': unverified,
                    'is_expired': datetime.now(timezone.utc) > datetime.fromtimestamp(unverified.get('exp', 0), tz=timezone.utc),
                    'expires_at': datetime.fromtimestamp(unverified.get('exp', 0), tz=timezone.utc).isoformat()
                }
                try:
                    pyjwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                    result['token_analysis']['signature_valid'] = True
                except pyjwt.InvalidSignatureError:
                    result['token_analysis']['signature_valid'] = False
                    result['token_analysis']['signature_error'] = 'Invalid signature'
                except Exception as e:
                    result['token_analysis']['signature_valid'] = False
                    result['token_analysis']['signature_error'] = str(e)
            except Exception as e:
                result['token_analysis'] = {'error': str(e)}
        
        return jsonify(result)

    logger.info("Flask app initialization complete.")
    return app