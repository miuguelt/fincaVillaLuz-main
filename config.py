import os
from datetime import timedelta
import secrets # Se mantiene para el fallback en desarrollo, pero no se usa en producción directa

class Config:
    # --- Configuración de Base de Datos (asumida como correcta) ---
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')  
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_NAME')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # DEBUG dependerá de la variable de entorno FLASK_ENV
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    # --- Configuración JWT - Valores por Defecto / Desarrollo ---
    # ========================================================
    
    # JWT_SECRET_KEY: Se cargará desde ENV. En producción, se forzará su existencia.
    # Para desarrollo local, si no está en ENV, se generará una temporal (¡NO para producción!)
    _jwt_secret_from_env = os.getenv('JWT_SECRET_KEY')
    if not _jwt_secret_from_env:
        # Esto solo se ejecuta si JWT_SECRET_KEY no está en las variables de entorno.
        # Es útil para desarrollo local rápido, pero peligroso en producción.
        print("ADVERTENCIA: JWT_SECRET_KEY no definida en el entorno. Se generará una clave temporal (SOLO para desarrollo).", flush=True)
        JWT_SECRET_KEY = secrets.token_urlsafe(32)
    else:
        JWT_SECRET_KEY = _jwt_secret_from_env
    
    print(f"DEBUG: JWT_SECRET_KEY cargada (longitud: {len(JWT_SECRET_KEY) if JWT_SECRET_KEY else 'N/A'}): {JWT_SECRET_KEY[:5]}...", flush=True) # Muestra los primeros 5 caracteres para depuración

    # Ubicación del token (solo cookies para tu caso)
    JWT_TOKEN_LOCATION = ['cookies']
    
    # Nombres de las cookies (se recomienda mantener estos valores por defecto de Flask-JWT-Extended)
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    
    # Tiempos de expiración (valores por defecto)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) 
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configuración de cookies
    # JWT_COOKIE_SECURE: True para HTTPS en producción, False para HTTP en desarrollo
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'False').lower() == 'true' 
    
    # JWT_COOKIE_DOMAIN: Debe ser el dominio de tu aplicación (ej. finca.isladigital.xyz)
    # En desarrollo, puede ser 'localhost' o None.
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN') 
    if not JWT_COOKIE_DOMAIN and DEBUG: # Si no está definida en desarrollo, usa localhost
        print("ADVERTENCIA: JWT_COOKIE_DOMAIN no definida en desarrollo. Usando 'localhost'.", flush=True)
        JWT_COOKIE_DOMAIN = 'localhost'
    elif not JWT_COOKIE_DOMAIN and not DEBUG:
        # En producción, si no está definida, debería fallar.
        print("ERROR: JWT_COOKIE_DOMAIN debe estar definida en el entorno de producción.", flush=True)
        # Una aplicación real lanzaría un error aquí. Para este ejemplo, podemos dejarlo,
        # pero es una señal de que la ENV no está configurada.
        pass

    JWT_COOKIE_PATH = '/'
    # 'Lax' es el valor recomendado para la mayoría de las SPAs con backends en diferentes dominios/subdominios
    JWT_COOKIE_SAMESITE = 'Lax' 
    
    # Paths específicos para cada tipo de token (si ambos son '/', son accesibles desde cualquier ruta)
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/' # Más flexible, accessible desde cualquier ruta para el refresco

    # CSRF Protection (DESHABILITADO: CAMBIAR A TRUE EN PRODUCCIÓN CON SOPORTE DEL FRONTEND)
    JWT_COOKIE_CSRF_PROTECT = False 
    JWT_CSRF_IN_COOKIES = False # Relevante si JWT_COOKIE_CSRF_PROTECT es True
    
    # Refresh token habilitado
    JWT_REFRESH_TOKEN_ENABLED = True
    
    # Headers (para uso futuro si decides usar headers además de cookies)
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

class DevelopmentConfig(Config):
    """Configuración específica para desarrollo"""
    DEBUG = True
    JWT_COOKIE_SECURE = False  # HTTP permitido en desarrollo
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2) # Tokens más largos en desarrollo para no refrescar tanto
    # JWT_COOKIE_DOMAIN heredará el 'localhost' o el valor de ENV

class ProductionConfig(Config):
    """Configuración específica para producción"""
    DEBUG = False # Asegura que el modo depuración está desactivado

    # --- ¡CRÍTICO EN PRODUCCIÓN! ---
    # Forzar que JWT_SECRET_KEY SIEMPRE venga del entorno.
    # Si no está definida, la aplicación NO debe iniciar.
    _production_jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not _production_jwt_secret:
        raise ValueError("JWT_SECRET_KEY environment variable MUST be set in production for security.")
    JWT_SECRET_KEY = _production_jwt_secret # Asignar la clave validada

    # Forzar cookies seguras en producción (HTTPS)
    JWT_COOKIE_SECURE = True

    # Expiración de token de acceso más corta para seguridad en producción
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Forzar que el dominio de la cookie SIEMPRE venga del entorno en producción
    _production_jwt_cookie_domain = os.getenv('JWT_COOKIE_DOMAIN')
    if not _production_jwt_cookie_domain:
        raise ValueError("JWT_COOKIE_DOMAIN environment variable MUST be set in production for cookie security.")
    JWT_COOKIE_DOMAIN = _production_jwt_cookie_domain

    # Considerar habilitar CSRF en producción SI tu frontend lo soporta.
    # Si tu frontend no envía el token CSRF, establecerlo a True aquí romperá el login/refresh.
    # JWT_COOKIE_CSRF_PROTECT = True 
    # JWT_CSRF_IN_COOKIES = True


# Configuración de mapeo para usar en tu aplicación principal
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # Fallback por si FLASK_ENV no está definido
}