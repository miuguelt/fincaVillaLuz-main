import os
from datetime import timedelta
import secrets
import logging

class Config:
    """Configuración base de la aplicación. Aplica a todos los entornos."""

    # Configuración de Base de Datos
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración base de JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_COOKIE_SAMESITE = 'None'
    JWT_COOKIE_CSRF_PROTECT = False

    # Configuración de CORS
    CORS_ORIGINS = ["http://localhost:5173", "https://mifinca.isladigital.xyz"]

    # Nivel de logging por defecto
    LOG_LEVEL = logging.INFO
    LOG_FILE_ENABLED = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo (localhost)."""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    
    # JWT - Atributos específicos de desarrollo
    # JWT_COOKIE_SECURE debe ser False para localhost
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    
    # JWT_COOKIE_DOMAIN debe ser None para que el navegador use 'localhost'
    JWT_COOKIE_DOMAIN = None
    
    # CORS - Orígenes de desarrollo
    CORS_ORIGINS = ["http://localhost:5173"]

class ProductionConfig(Config):
    """Configuración para producción (HTTPS)."""
    DEBUG = False
    LOG_LEVEL = logging.INFO
    
    # Validaciones de seguridad en producción
    if not os.getenv('JWT_SECRET_KEY'):
        raise ValueError("La variable JWT_SECRET_KEY DEBE estar definida en producción.")
    if not os.getenv('JWT_COOKIE_DOMAIN'):
        raise ValueError("La variable JWT_COOKIE_DOMAIN DEBE estar definida en producción.")

    # JWT - Atributos específicos de producción
    # JWT_COOKIE_SECURE debe ser True para HTTPS
    JWT_COOKIE_SECURE = True
    # El dominio de la cookie debe ser el dominio principal (con punto inicial)
    # para que sea válido en cualquier subdominio
    JWT_COOKIE_DOMAIN = "." + os.getenv('JWT_COOKIE_DOMAIN')
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # CORS - Orígenes de producción
    # Incluye el dominio y el subdominio si tu frontend está en un subdominio
    CORS_ORIGINS = ["https://isladigital.xyz", "https://mifinca.isladigital.xyz"]

# Diccionario de configuración final
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}