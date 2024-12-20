from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from langchain_community.llms.ollama import Ollama

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()

# Initialize language model
llm = Ollama(model="llama3.2")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['LANGUAGES'] = ['en', 'tr']

    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    from .routes.routes import main_routes, auth_routes, chat_routes, profile_routes, quiz_routes
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(chat_routes.bp)
    app.register_blueprint(profile_routes.bp)
    app.register_blueprint(quiz_routes.bp)

    return app
