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
    JWT_COOKIE_CSRF_PROTECT = False  # Puedes activar CSRF token si deseas
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(24))  
    JWT_ACCESS_TOKEN_EXPIRES = 900   # Ejemplo: 15 minutos
    JWT_REFRESH_TOKEN_EXPIRES = 2592000 
    JWT_COOKIE_SAMESITE = os.getenv('JWT_COOKIE_SAMESITE', "Lax")  # Puede ser 'Lax', 'Strict' o 'None'
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', True)
    JWT_COOKIE_PATH = '/'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/refresh' 


    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_ENV') == 'development'