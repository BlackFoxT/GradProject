from flask import Flask, redirect, url_for, render_template, request, flash, jsonify, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_babel import Babel, _,lazy_gettext as _l, gettext
from models import db  # Import db from models/__init__.py
from routes import auth_routes, profile_routes  # Import route files
from routes.home_routes import home_routes  # Import the new routes
from bluePrint.language_bp import language_bp  # Import language-related routes
from processors.babel_processor import inject_babel, inject_locale  # Import context processors
from utils.language_utils import get_locale, get_timezone  # Import utility functions
from routes.chat_routes import chat_routes  # Import the chat blueprint
from routes.quiz_routes import quiz_routes  # Import quiz routes

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


# Import models after db initialization
from models.user import User  
from models.chat_history import ChatHistory
from models.quiz import Quiz
from models.information import Information 
from models.quiz_question import QuizQuestion

selected_chat = None

# Example usage in a route
@app.before_request
def before_request():
    g.locale = get_locale()  # Store locale in the global g object
    g.timezone = get_timezone()  # Store timezone in the global g object

babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register the blueprint
app.register_blueprint(language_bp)

# Register context processors
app.context_processor(inject_babel)
app.context_processor(inject_locale)


login_manager.login_view = "auth_routes.login_page"  # Redirect to the login page if not authenticated
# Register home_routes blueprint
app.register_blueprint(home_routes)


# Register routes
app.register_blueprint(auth_routes.auth_bp)  # Register the authentication blueprint
app.register_blueprint(profile_routes.profile_bp)  # Register the profile blueprint

# Register the blueprint
app.register_blueprint(chat_routes)

app.register_blueprint(quiz_routes)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




'''
Bu örnek soru ekleme sql kodu
# Kullanıcı ve chat ID
    user_id = 2   # Örnek kullanıcı ID'si
    chat_id = 5   # Örnek chat ID'si

    # Yeni quiz oluştur
    new_quiz = Quiz(user_id=user_id, chat_id=chat_id)
    db.session.add(new_quiz)
    db.session.commit()  # ID oluşması için önce commit et

    # 10 tane soru ekleyelim
    questions = [
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da listeleri tersine çevirmek için hangi yöntem kullanılır?",
            options=["list.reverse()", "list[::-1]", "reversed(list)", "Tümü"],
            correct_answer="Tümü"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da sözlük (dict) oluşturmak için hangi sembol kullanılır?",
            options=["{}", "[]", "()", "<>"],
            correct_answer="{}"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Lambda fonksiyonları ne için kullanılır?",
            options=["Anonim fonksiyonlar", "Global değişken tanımlama", "Modül yükleme", "Dosya açma"],
            correct_answer="Anonim fonksiyonlar"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da bir listeyi sıralamak için hangi metod kullanılır?",
            options=["sort()", "sorted()", "order()", "list.sort()"],
            correct_answer="sort()"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da fonksiyon içindeki bir değişkeni global olarak kullanmak için hangi anahtar kelime kullanılır?",
            options=["global", "var", "let", "static"],
            correct_answer="global"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da hangi veri tipi değiştirilemez (immutable)?",
            options=["List", "Dictionary", "Tuple", "Set"],
            correct_answer="Tuple"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da '==' ve 'is' operatörlerinin farkı nedir?",
            options=[
                "'==' değerleri karşılaştırır, 'is' bellek adreslerini karşılaştırır.",
                "'is' değerleri karşılaştırır, '==' bellek adreslerini karşılaştırır.",
                "İkisi de aynı anlama gelir.",
                "'==' sadece stringler için çalışır."
            ],
            correct_answer="'==' değerleri karşılaştırır, 'is' bellek adreslerini karşılaştırır."
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da bir modül nasıl içe aktarılır?",
            options=["import module_name", "require module_name", "using module_name", "include module_name"],
            correct_answer="import module_name"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da hata fırlatmak için hangi anahtar kelime kullanılır?",
            options=["throw", "raise", "error", "exception"],
            correct_answer="raise"
        ),
        QuizQuestion(
            quiz_id=new_quiz.id,
            text="Python'da hangi döngü yapısı belirli bir koşul sağlanana kadar çalışır?",
            options=["for", "while", "do-while", "foreach"],
            correct_answer="while"
        ),
    ]

    # Soruları veritabanına ekle
    db.session.add_all(questions)
    db.session.commit()

    print(f"Quiz oluşturuldu! Quiz ID: {new_quiz.id}, Chat ID: {chat_id}")
'''