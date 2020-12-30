from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_file=Config):
    app = Flask(__name__)
    app.config.from_object(config_file)

    db.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.home import bp as home_bp
    app.register_blueprint(home_bp)

    from .blueprints.database import bp as database_bp
    app.register_blueprint(database_bp)

    return app
