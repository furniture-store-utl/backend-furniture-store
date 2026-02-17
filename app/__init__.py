from flask import Flask

from config import Config
from .exceptions import register_error_handlers
from .extensions import db, migrate


def create_app():
    """
    Factory de la aplicación Flask.

    Crea y configura la instancia de la aplicación Flask,
    inicializa extensiones y registra blueprints.

    Returns:
        Flask: Instancia configurada de la aplicación
    """
    # Create Flask application
    app = Flask(__name__)

    # Initialize environment variables
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to register them with SQLAlchemy
    from app import models

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    # from .catalogs.colors import colors_bp
    # app.register_blueprint(colors_bp, url_prefix='/api/v1/colors')

    return app
