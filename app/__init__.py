from flask import Flask

from config import Config
from .extensions import db


def create_app():
    # Create Flask application
    app = Flask(__name__)

    # Initialize environment variables
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    # app.register_blueprint(main)

    return app
