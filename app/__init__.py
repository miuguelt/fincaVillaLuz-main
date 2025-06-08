from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS 
from datetime import timezone, datetime
from config import config

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt = JWTManager(app) 
    def expired_token_callback(jwt_header, jwt_payload):
        """Solo para mostrar tiempos UTC en errores de JWT"""
        exp_timestamp = jwt_payload['exp']
        exp_utc = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now_utc = datetime.now(timezone.utc)
        
        print(f"=== JWT EXPIRED DEBUG ===", flush=)
        print(f"Token expired at UTC: {exp_utc.isoformat()}")
        print(f"Current time UTC: {now_utc.isoformat()}", flush=True)
        print(f"Expired {int((now_utc - exp_utc).total_seconds())} seconds ago", flush=True)
        print("========================")
        
        return {
            'msg': 'Token has expired',
            'expired_at_utc': exp_utc.isoformat(),
            'current_time_utc': now_utc.isoformat()
        }, 401

    db.init_app(app)

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
    
    # ¡CONFIGURACIÓN DE CORS ESENCIAL!
    # ESTO DEBE SER LA LISTA DE ORÍGENES EXPLÍCITOS.
    # El *NO FUNCIONA* con supports_credentials=True.
    CORS(
        app,
        origins=[
            "http://localhost:5173",    # Frontend local (HTTP) - Temporal, ver Paso 2
            "https://localhost:5173",   # Frontend local (HTTPS) - PREFERIDO
            "https://mifinca.isladigital.xyz" # Tu dominio de frontend en producción
        ],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials",
                    "X-Requested-With", "Origin", "Accept", "Access-Control-Request-Method", "Access-Control-Request-Headers"],
        expose_headers=["Content-Type", "Authorization"], 
        supports_credentials=True
    ).init_app(app)

    return app
