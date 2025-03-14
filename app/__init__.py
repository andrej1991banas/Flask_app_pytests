from flask import Flask

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'testing':
        app.config['TESTING'] = True
    else:
        app.config['TESTING'] = False
    
    # Register routes
    from .routes import init_routes
    init_routes(app)
    
    return app