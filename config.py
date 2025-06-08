import os
from datetime import timedelta
import secrets

class Config:
    
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_ENV') == 'True'
    JWT_COOKIE_HTTPONLY = True

    # JWT Configuration
    _jwt_secret_from_env = os.getenv('JWT_SECRET_KEY', 'Tq8L0Rd9sXkZ2YpQ5mF7wN1vK3rL8jPb')
    if not _jwt_secret_from_env:
        print("ADVERTENCIA: JWT_SECRET_KEY no definida. Usando temporal (SOLO DESARROLLO).", flush=True)
        JWT_SECRET_KEY = "Tq8L0Rd9sXkZ2YpQ5mF7wN1vK3rL8jPb"
    else:
        JWT_SECRET_KEY = _jwt_secret_from_env

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1500)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Configuración crítica para producción
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'True').lower() == 'true'
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN', ".isladigital.xyz")  # Debe estar definida en producción
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_SAMESITE = 'Lax'  # Permitir cross-site cookies con Secure
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_IN_COOKIES = False
    JWT_REFRESH_TOKEN_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_COOKIE_DOMAIN = 'localhost'

class ProductionConfig(Config):
    DEBUG = False 

    _production_jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not _production_jwt_secret:
        # Esto es lo que debe pasar en producción si la ENV no está seteada.
        raise ValueError("JWT_SECRET_KEY environment variable MUST be set in production for security.")
    JWT_SECRET_KEY = _production_jwt_secret # Asignar la clave validada

    JWT_COOKIE_SECURE = True # Siempre True en producción (HTTPS)

    _production_jwt_cookie_domain = os.getenv('JWT_COOKIE_DOMAIN')
    if not _production_jwt_cookie_domain:
        raise ValueError("JWT_COOKIE_DOMAIN environment variable MUST be set in production for cookie security.")
    JWT_COOKIE_DOMAIN = _production_jwt_cookie_domain

    # JWT_ACCESS_TOKEN_EXPIRES y JWT_REFRESH_TOKEN_EXPIRES deberían estar aquí con valores de producción
    # (ej. 30 minutos y 7 días respectivamente).
    # Como tienes 1 día y 30 días, eso está bien.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}