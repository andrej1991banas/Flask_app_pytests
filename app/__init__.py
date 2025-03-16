from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['DEBUG_MODE'] = True  #  Enable debug in testing
    else:
        app.config['TESTING'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['DEBUG_MODE'] = False  # Disable debug in production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'a-very-secret-key-12345'

    db.init_app(app)

    from .routes import init_routes
    init_routes(app)

    if config_name != 'testing':
        with app.app_context():
            db.create_all()

    return app