import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    # FLASK APP CONFIGURATIONS
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # DATABASE CONFIGURATIONS
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_MASTER_DATABASE_URI')
    SQLALCHEMY_BINDS = {
        "konkani": os.environ.get("SQLALCHEMY_KONKANI_DATABASE_URI")
    }

    # MICROSOFT TRANSLATOR API CREDENTIALS
    MS_TRANSLATOR_KEY=os.environ.get('MS_TRANSLATOR_KEY')
    MS_TRANSLATOR_ENDPOINT=os.environ.get('MS_TRANSLATOR_ENDPOINT')
    MS_TRANSLATOR_REGION=os.environ.get('MS_TRANSLATOR_REGION')