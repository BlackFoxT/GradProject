from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    # Flask instance
    app = Flask(__name__)

    # Application configuration
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change to a secure key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Use your DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Flask-Login config
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from .routes import main_routes
    from .auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes, url_prefix='/auth')

    # Create database tables if not exists
    with app.app_context():
        db.create_all()

    return app
