from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)


    # IMPORT BLUEPRINT ROUTE
    from .routes import routes
    from .root import root
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(root, url_prefix='/')


    # CREATE CUSTOM ERROR PAGES
    # PAGE NOT FOUND
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    # INTERNAL SERVER ERROR
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500


    return app