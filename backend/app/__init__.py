from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .routes import auth, image_processing, tabular_data, text_analysis
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    #register blueprints here
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(tabular_data.sales_data_bp)  # Register the tabular data blueprint
    app.register_blueprint(image_processing.image_processing_bp)
    app.register_blueprint(text_analysis.text_analysis_bp)

    return app
