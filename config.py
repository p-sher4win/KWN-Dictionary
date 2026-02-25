import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    # FLASK APP CONFIGURATIONS
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # DATABASE CONFIGURATIONS
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # PIXAZO API KEY
    PIXAZO_API_KEY=os.environ.get('PIXAZO_API_KEY')