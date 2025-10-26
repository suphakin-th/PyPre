"""
DataBoard Configuration
Centralized configuration for easy customization
"""
import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'data/uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Data Storage
    DATA_FOLDER = 'data'
    DATASETS_FOLDER = 'data/datasets'
    DASHBOARDS_FOLDER = 'data/dashboards'
    USERS_FILE = 'data/users.json'
    
    # Chart Configuration
    DEFAULT_CHART_LIMIT = 20
    MAX_CHART_LIMIT = 100
    
    # Performance
    CSV_CHUNK_SIZE = 10000  # Rows to process at a time
    PREVIEW_ROWS = 100  # Default rows for preview
    
    # UI Configuration
    APP_NAME = 'DataBoard'
    APP_TAGLINE = 'Lightweight Business Intelligence Platform'
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Ensure directories exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.DATASETS_FOLDER, exist_ok=True)
        os.makedirs(Config.DASHBOARDS_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.USERS_FILE), exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # Override with environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-must-set-a-secret-key'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific initialization
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/databoard.log',
            maxBytes=10240000,
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('DataBoard startup')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
