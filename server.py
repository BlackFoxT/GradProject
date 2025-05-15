from flask import Flask, g
from flask_login import LoginManager
from flask_babel import Babel, _,lazy_gettext as _l
from models import db 
from routes import auth_routes, profile_routes 
from routes.home_routes import home_routes 
from bluePrint.language_bp import language_bp  
from processors.babel_processor import inject_babel, inject_locale 
from utils.language_utils import get_locale, get_timezone  
from routes.chat_routes import chat_routes  
from routes.quiz_routes import quiz_routes  
from routes.note_routes import note_routes  
from models.user import User  


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ['en', 'tr']

# Initialize db with the app
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager(app)



selected_chat = None

# Example usage in a route
@app.before_request
def before_request():
    g.locale = get_locale() 
    g.timezone = get_timezone() 

babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register the blueprint
app.register_blueprint(language_bp)

# Register context processors
app.context_processor(inject_babel)
app.context_processor(inject_locale)


login_manager.login_view = "auth_routes.login_page" 
# Register home_routes blueprint
app.register_blueprint(home_routes)


# Register routes
app.register_blueprint(auth_routes.auth_bp) 
app.register_blueprint(profile_routes.profile_bp)  

# Register the blueprint
app.register_blueprint(chat_routes)

app.register_blueprint(quiz_routes)
app.register_blueprint(note_routes)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)