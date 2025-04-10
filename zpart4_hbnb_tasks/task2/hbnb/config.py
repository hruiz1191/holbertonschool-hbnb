import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # ✅ Base de datos SQLite para desarrollo
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # ✅ Evita advertencias de SQLAlchemy

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://user:password@localhost/hbnb_prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # ✅ Recomendado para producción

# Diccionario para acceder a las configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # ✅ Default será DevelopmentConfig
}
