import os

class Config:
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')  
    PORT = os.getenv('DB_PORT')
    DATABASE = os.getenv('DB_USER')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False