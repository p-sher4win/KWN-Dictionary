from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    db.init_app(app)


    # IMPORT BLUEPRINT ROUTE
    from .routes import routes
    from .root import root
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(root, url_prefix='/')


    create_db_schema(app)


    return app


# CREATE TABLE SCHEMA IN DATABASE
def create_db_schema(app):
    with app.app_context():
        db.create_all()
        print("Created Schema")