import os

DEBUG = True
SECRET_KEY = 'sdua98s798asuda98q98SD(A*as'
SQLALCHEMY_DATABASE_URI = os.environ.get('ENDORSE_URL')

if SQLALCHEMY_DATABASE_URI == None:
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/endorse"
SQLALCHEMY_TRACK_MODIFICATIONS = True