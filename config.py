import os
from datetime import timedelta
import secrets

class Config:
    # Database Configuration
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')  
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_NAME')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    # JWT Configuration - VERSIÓN CORREGIDA
    # =====================================
    
    # Clave secreta JWT (CRÍTICO: debe ser la misma siempre)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))  # Valor por defecto solo para desarrollo
    
    # Ubicación del token (solo cookies para tu caso)
    JWT_TOKEN_LOCATION = ['cookies']
    
    # Nombres de las cookies
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    
    # Tiempos de expiración
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)      # 1 hora (antes tenías 15 min)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)     # 30 días
    
    # Configuración de cookies
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'False').lower() == 'true'  # False para desarrollo, True para producción
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN', 'finca.isladigital.xyz')   # Tu dominio
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_SAMESITE = 'Lax'  # 'Lax' es mejor para cross-site requests
    
    # Paths específicos para cada tipo de token
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/refresh'  # Cambiado de '/refresh' a '/' para mayor flexibilidad
    
    # CSRF Protection (DESHABILITADO para simplificar debugging)
    JWT_COOKIE_CSRF_PROTECT = False  # Cambiado a False temporalmente
    JWT_CSRF_IN_COOKIES = False
    
    # Refresh token habilitado
    JWT_REFRESH_TOKEN_ENABLED = True
    
    # Headers (para uso futuro si decides usar headers además de cookies)
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

class DevelopmentConfig(Config):
    """Configuración específica para desarrollo"""
    DEBUG = True
    JWT_COOKIE_SECURE = False  # HTTP permitido en desarrollo
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)  # Tokens más largos en desarrollo

class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Validar JWT_SECRET_KEY antes de asignarlo
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret:
        raise ValueError("JWT_SECRET_KEY debe estar definida en producción")
    
    JWT_SECRET_KEY = jwt_secret  # Asignar después de validar

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}