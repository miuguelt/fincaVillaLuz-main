import os
from datetime import timedelta
import secrets

class Config:
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')  
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_NAME')

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True  # Puedes activar CSRF token si deseas
    JWT_ACCESS_COOKIE_NAME = os.getenv('JWT_ACCESS_COOKIE_NAME', "access_token_cookie")
    JWT_REFRESH_COOKIE_NAME = os.getenv('JWT_REFRESH_COOKIE_NAME', "refresh_token_cookie")
    JWT_HEADER_NAME = os.getenv('JWT_HEADER_NAME', "Authorization")
    JWT_HEADER_TYPE = os.getenv('JWT_HEADER_TYPE', "Bearer")  # Por defecto es Bearer
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', False)
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN', "'.isladigital.xyz'")  # Puedes especificar un dominio si es necesario
    JWT_COOKIE_PATH = os.getenv('JWT_COOKIE_PATH', "/")
    JWT_CSRF_IN_COOKIES = os.getenv('JWT_CSRF_IN_COOKIES', True)  # Si deseas usar CSRF token en cookies
    JWT_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']  # Métodos que requieren CSRF token
    JWT_CSRF_COOKIE_NAME = os.getenv('JWT_CSRF_COOKIE_NAME', "csrf_token_cookie")
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(24))  
    JWT_COOKIE_SAMESITE = os.getenv('JWT_COOKIE_SAMESITE', "Lax")  # Puede ser 'Lax', 'Strict' o 'None'
    JWT_ACCESS_TOKEN_PATH = os.getenv('JWT_ACCESS_TOKEN_PATH', '/')
    JWT_REFRESH_TOKEN_PATH = os.getenv('JWT_REFRESH_TOKEN_PATH', '/refresh')    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # 15 minutos
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 días
    JWT_REFRESH_TOKEN_ENABLED = True # Genera una clave secreta si no está definida
    
    
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/refresh' 


    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_ENV') == 'development'