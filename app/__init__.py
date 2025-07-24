from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="default"):
    app = Flask(__name__)

    # Load configuration
    from app.config import config

    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models import user, inspection

    return app
