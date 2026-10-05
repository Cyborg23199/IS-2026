from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
    
    # Register temporary test route
    @app.route("/")
    def prueba():
        return "¡Hola Flask con MariaDB!"
        
    return app