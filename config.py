import os
from datetime import timedelta
import secrets

class Config:
    # ... [Configuración de Base de Datos] ...

    # JWT Configuration
    _jwt_secret_from_env = os.getenv('JWT_SECRET_KEY')
    if not _jwt_secret_from_env:
        print("ADVERTENCIA: JWT_SECRET_KEY no definida. Usando temporal (SOLO DESARROLLO).", flush=True)
        JWT_SECRET_KEY = secrets.token_urlsafe(32)
    else:
        JWT_SECRET_KEY = _jwt_secret_from_env

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Configuración crítica para producción
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'True').lower() == 'true'
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN')  # Debe estar definida en producción
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_SAMESITE = 'None'  # Permitir cross-site cookies con Secure
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

    @classmethod
    def init_app(cls, app):
        # Validar variables críticas en producción
        required_env = [
            ('JWT_SECRET_KEY', cls.JWT_SECRET_KEY),
            ('JWT_COOKIE_DOMAIN', cls.JWT_COOKIE_DOMAIN)
        ]
        for var, value in required_env:
            if not value:
                raise RuntimeError(f"❌ {var} no definida en entorno de producción.")

        # Forzar configuración segura
        cls.JWT_COOKIE_SECURE = True
        cls.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
        cls.JWT_COOKIE_SAMESITE = 'None'
        cls.JWT_COOKIE_DOMAIN = cls.JWT_COOKIE_DOMAIN.rstrip('.')  # Eliminar punto si existe

        print("✅ ProductionConfig inicializada correctamente.", flush=True)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}