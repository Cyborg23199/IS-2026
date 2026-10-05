# Configuration environments for the application
class Config:
    """Base configuration class"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False

# Mapping configuration names to classes
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}