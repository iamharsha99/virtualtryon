from flask import Flask
from .routes import bp as routes_bp

def create_app():
    app = Flask(__name__)
    
    # Set a secret key for the session
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace this with a unique and secure key
    
    # Register Blueprints
    app.register_blueprint(routes_bp)
    
    return app
