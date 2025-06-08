from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS 


db = SQLAlchemy()
jwt = JWTManager() 
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    
    jwt.init_app(app)
    jwt._set_error_handler_callbacks(app)  # Configura los manejadores de errores de JWT
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
    )

    return app
