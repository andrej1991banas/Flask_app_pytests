from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name='development'):
    app = Flask(__name__)

    # Configuration
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for tests
    else:
        app.config['TESTING'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # File-based DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'  # Required for forms

    # Initialize database
    db.init_app(app)

    # Register routes
    from .routes import init_routes
    init_routes(app)

    # Create database tables (only needed for development)
    if config_name != 'testing':
        with app.app_context():
            db.create_all()

    return app