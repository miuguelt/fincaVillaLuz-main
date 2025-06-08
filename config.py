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
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    _jwt_secret_from_env = os.getenv('JWT_SECRET_KEY')
    if not _jwt_secret_from_env:
        print("ADVERTENCIA: JWT_SECRET_KEY no definida. Se usará una clave temporal (solo desarrollo).", flush=True)
        JWT_SECRET_KEY = secrets.token_urlsafe(32)
    else:
        JWT_SECRET_KEY = _jwt_secret_from_env
    print(f"DEBUG: JWT_SECRET_KEY cargada (inicio): {JWT_SECRET_KEY[:5]}...", flush=True)

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'True').lower() == 'true'
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN') or '.isladigital.xyz'
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_IN_COOKIES = True
    JWT_REFRESH_TOKEN_ENABLED = True
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        jwt_domain = os.getenv('JWT_COOKIE_DOMAIN')

        if not jwt_secret:
            raise RuntimeError("❌ JWT_SECRET_KEY debe estar definida en entorno de producción.")
        if not jwt_domain:
            raise RuntimeError("❌ JWT_COOKIE_DOMAIN debe estar definida en entorno de producción.")

        cls.JWT_SECRET_KEY = jwt_secret
        cls.JWT_COOKIE_DOMAIN = jwt_domain
        cls.JWT_COOKIE_SECURE = True
        cls.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
        print("✅ ProductionConfig correctamente inicializada con variables críticas.", flush=True)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
