from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config

# Initialize SQLAlchemy extension
db = SQLAlchemy()

def create_app(config_name):
    # Create application instance with relative instance path configuration
    app = Flask(__name__, instance_relative_config=True)
    
    # Load environment configuration
    app.config.from_object(app_config[config_name])
    
    # Load sensitive credentials from instance/config.py
    app.config.from_pyfile('config.py')
    
    # Initialize database connection binding
    db.init_app(app)
    
    migrate = Migrate(app, db)

    
    # Register blueprint and mount under /html prefix
    from .html import html as html_blueprint
    app.register_blueprint(html_blueprint, url_prefix='/html')

    # Register blueprint and mount under /api prefix
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .health import health as health_blueprint
    app.register_blueprint(health_blueprint)

    from .metrics import metrics as metrics_blueprint
    app.register_blueprint(metrics_blueprint)
    
    return app