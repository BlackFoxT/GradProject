from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from langchain_community.llms.ollama import Ollama
from application.models import User

# db burada tanımlanabilir ancak başka modüllerde kullanmak için create_app fonksiyonu ile ilişkilendirilir
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
llm = Ollama(model="llama3.2")

babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

# Helper functions
def get_locale():
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in ['en', 'tr']:
            session['lang'] = lang
            return session['lang']
    elif 'lang' in session:
        return session.get('lang')
    return request.accept_languages.best_match(['en', 'tr'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
    
# Kullanıcıyı yüklemek için user_loader fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Kullanıcıyı id'ye göre yükler

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config.from_object('application.config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    # Register blueprints or routes
    with app.app_context():
        from application.routes import main_bp
        app.register_blueprint(main_bp)

    return app
