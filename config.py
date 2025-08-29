import os
from datetime import timedelta
import secrets # Buena práctica para generar secretos si no existen

class Config:
    
    # --- Configuración de Base de Datos (Esto se ve bien) ---
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MEJORA: FLASK_ENV suele ser 'development' o 'production', no 'True'.
    # Es más seguro comparar con 'development'.
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    # --- Configuración de JWT (Aquí están los cambios importantes) ---
    
    # MEJORA: Genera una clave segura si no está en las variables de entorno para desarrollo.
    # Evita tener una clave fija quemada en el código.
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
    
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_HTTPONLY = True # ¡Excelente! Buena práctica de seguridad.
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1500) # Esto se sobrescribe en prod/dev
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # --- Configuración de Cookies (CAMBIO CRÍTICO AQUÍ) ---
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'True').lower() == 'true'
    
    # CORRECCIÓN PRINCIPAL: Debe ser 'None' para permitir cookies cross-site (React <-> Flask)
    JWT_COOKIE_SAMESITE = 'None' 
    
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN') # Es mejor no tener un default aquí y forzarlo en Prod/Dev.
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Para desarrollo en localhost (HTTP), SECURE debe ser False.
    # El navegador puede ser permisivo con SameSite='None' y Secure=False solo en localhost.
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    # Define explícitamente el dominio para desarrollo
    JWT_COOKIE_DOMAIN = None # Al ser None, el navegador usará el dominio actual (ej. localhost)


class ProductionConfig(Config):
    DEBUG = False 
    
    # Esta validación es una EXCELENTE práctica de seguridad. ¡Muy bien hecho!
    _production_jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not _production_jwt_secret:
        raise ValueError("La variable de entorno JWT_SECRET_KEY DEBE estar definida en producción.")
    JWT_SECRET_KEY = _production_jwt_secret

    # En producción, SIEMPRE debe ser True porque usarás HTTPS.
    JWT_COOKIE_SECURE = True
    
    # Esta validación también es excelente.
    _production_jwt_cookie_domain = os.getenv('JWT_COOKIE_DOMAIN')
    if not _production_jwt_cookie_domain:
        raise ValueError("La variable de entorno JWT_COOKIE_DOMAIN DEBE estar definida en producción.")
    JWT_COOKIE_DOMAIN = _production_jwt_cookie_domain

    # Tiempos de expiración más cortos y seguros para producción.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

# El diccionario de configuración se ve perfecto.
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}