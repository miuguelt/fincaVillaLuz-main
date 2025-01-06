from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('config.Config')
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    jwt = JWTManager(app)

    Talisman(app, content_security_policy=None)
    db.init_app(app)


    from app.routes import (
        userRoutes, animalDiseasesRoutes, animalFieldsRoutes, animalsRoutes, breedsRoutes, controlRoutes, diseasesRoutes, fieldsRoutes, foodTypesRoutes, geneticImprovementsRoutes, medicationsRoutes, speciesRoutes, treatmentMedicationsRoutes, treatmentsRoutes, treatmentVaccinesRoutes, vaccinesRoutes, vaccinationsRoutes, auth
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

    return app