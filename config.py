# import os

# class Config:
#     USER = os.getenv('MYSQL_USER', 'root')
#     PASSWORD = os.getenv('MYSQL_PASSWORD', '1234')
#     HOST = os.getenv('MYSQL_HOST', 'db')  # Aquí cambiamos localhost por 'db', el nombre del servicio
#     PORT = os.getenv('MYSQL_PORT', 3316)
#     DATABASE = os.getenv('MYSQL_DATABASE', 'finca')

#     SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    USER = os.getenv('MYSQL_USER', 'mysqlu')
    PASSWORD = os.getenv('MYSQL_PASSWORD', '1234567abc')
    HOST = os.getenv('MYSQL_HOST', 'dbmysql')  
    PORT = os.getenv('MYSQL_PORT', 3316)
    DATABASE = os.getenv('MYSQL_DATABASE', 'finca')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
