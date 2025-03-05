from flask import Flask, redirect, url_for, render_template, request, flash, jsonify, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_babel import Babel, _,lazy_gettext as _l, gettext
from langchain_community.llms.ollama import Ollama
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ChatHistory model (storing an array of chats for each topic)
from sqlalchemy.ext.mutable import MutableList

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ['en', 'tr']  # List of supported languages
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Initialize Ollama model
llm = Ollama(model="llama3.2" , system=("Sen bir eğitim asistanısın. Kullancılar sana bir konu hakkında danışacak ve sen de eğitim içerikleri sağlamaktan, sınavlara hazırlık yapmaktan ve konu anlatımı yapmaktan sorumlusun. Cevaplarını akademik bir dil ile ver, ancak karmaşık konuları basit ve anlaşılır bir şekilde anlat. Kısa ama öz yanıtlar vermeye çalış. Biraz konu anlattıktan sonra konu hakkında örnek soru sor eğer kullanıcı doğru bilemezse de doğrusunu açıkla."))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    information = db.relationship('Information', backref='user', lazy=True)
    chats = db.relationship('ChatHistory', backref='user', lazy=True)
    # Add currentChatID to store the ID of the current selected chat
    currentChatID = db.Column(db.Integer, nullable=True)

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    telephone_number = db.Column(db.String(15))

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    chats = db.Column(MutableList.as_mutable(db.JSON), nullable=True)  # Make the list mutable
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat_history.id'), nullable=False)  # Quiz'in ait olduğu chat
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade="all, delete-orphan")

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    options = db.Column(MutableList.as_mutable(db.JSON), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

selected_chat = None

def get_locale():
    # Check if the language query parameter is set and valid
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in ['en', 'tr']:
            session['lang'] = lang
            return session['lang']
    # If not set via query, check if we have it stored in the session
    elif 'lang' in session:
        return session.get('lang')
    # Otherwise, use the browser's preferred language
    return request.accept_languages.best_match(['en', 'tr'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/change_language/<lang_code>')
def change_language(lang_code):
    # Save language preference in session or cookie
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route("/")
def home_page():
    user_chats = None
    selected_chat = None

    if current_user.is_authenticated:
        # Fetch all chats for the current user
        user_chats = ChatHistory.query.filter_by(user_id=current_user.id).all()

    # Get the 'chat_id' from query parameters
    chat_id = request.args.get("chat_id", type=int)

    # Fetch the selected chat content, if chat_id is provided
    if chat_id:
        selected_chat = ChatHistory.query.filter_by(id=chat_id).first()
        
        # If no chat is found, flash an error message and redirect to home page
        if selected_chat is None:
            flash('Selected chat not found', 'error')
            return redirect(url_for('home_page'))  # Redirect to the homepage if no chat found
        else:
            # If a valid chat is found, update currentChatID and save to the database
            current_user.currentChatID = chat_id
            db.session.commit()
    else:
        # If no chat is selected, set currentChatID to None
        current_user.currentChatID = None
        db.session.commit()

    # Render the home page with the user's chats and the selected chat (if any)
    return render_template(
        "index.html",
        user_chats=user_chats,
        selected_chat=selected_chat
    )

@app.route("/chatl")
@login_required
def chatl():
    # Get the 'id' query parameter from the URL
    chat_id = request.args.get('id', type=int)
    if chat_id:
        # Fetch the chat history and ensure it belongs to the current user
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=chat_id).first()
        if chat_history:
            current_user.currentChatID = chat_id  # Store the current chat ID
            # Save the change to the database
            db.session.commit()

    # Redirect to home_page with the chat_id as a query parameter
    return redirect(url_for("home_page", chat_id=chat_id))



@app.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer)

@app.context_processor
def inject_babel():
    return dict(_=gettext)

@app.context_processor
def inject_locale():
    # This makes the function available directly, allowing you to call it in the template
    return {'get_locale': get_locale}

@app.route('/')
def home():
    return render_template('index.html', current_locale=get_locale())

@app.route('/js_translations')
def js_translations():
    translations = {
        'logoutText': gettext('Logout'),
        'accountText': gettext('Account'),
        'successTitle': gettext('Success!'),
        'successText': gettext('You are registered.'),
        'validEmail': gettext('Please enter a valid email address.')
    }
    return jsonify(translations)


@app.route("/login", methods=["GET", "POST"])
def login_page():

    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home_page'))
        else:
            flash("Email or password is incorrect", "error")
            return redirect(url_for('login_page'))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This email is already registered", "error")
            return redirect(url_for('signup_page'))

        # Hash the password before saving to the database
        hashed_password = generate_password_hash(password)

        # Create a new user with hashed password
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login_page'))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    current_user.currentChatID = None
    # Save the change to the database
    db.session.commit()
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/profile")
def profile_page():
    if current_user.is_authenticated:
        current_user.currentChatID = None
        # Save the change to the database
        db.session.commit()
        user_information = Information.query.filter_by(user_id=current_user.id).first()
        return render_template("profile.html", info=user_information)
    else:
        return redirect(url_for('login_page'))

@app.route('/update_information', methods=['POST'])
def update_information():
    if current_user.is_authenticated:
        name = request.form.get('name')
        surname = request.form.get('surname')
        telephone_number = request.form.get('telephone_number')

        user_information = Information.query.filter_by(user_id=current_user.id).first()
        if user_information:
            user_information.name = name
            user_information.surname = surname
            user_information.telephone_number = telephone_number
        else:
            user_information = Information(
                user_id=current_user.id,
                name=name,
                surname=surname,
                telephone_number=telephone_number
            )
            db.session.add(user_information)

        db.session.commit()
        flash("Information updated successfully!", "success")
        return redirect(url_for('home_page'))
    else:
        flash("You must be logged in to update your information.", "error")
        return redirect(url_for('login_page'))


@app.route("/get-chat-history", methods=["GET"])
def get_chat_history():
    topic = request.args.get("topic", "General")  # Default topic or fetch from user preference
    if current_user.is_authenticated:
        if current_user.currentChatID is None:
            return jsonify({"contentVisible": False, "chats": [],"isUser": True})
        # For authenticated users, fetch chat history from the database
        #print(current_user.id)
        chat_history = ChatHistory.query.filter_by(id=current_user.currentChatID).first()
        print(chat_history)
       # print(chat_history.chats)
        if chat_history:
           # print(chat_history.chats)
            return jsonify({
                "contentVisible": True,
                "chats": chat_history.chats,
                "isUser": True  # Assuming `chats` is JSON serializable
            })
        else:
            return jsonify({"contentVisible": False, "chats": [],"isUser": True})
    else:
        # For non-authenticated users, use localStorage or session to fetch chat history
        chat_history = session.get("chat_history", {})
       # print(chat_history)
        return jsonify({
            "contentVisible": bool(chat_history),  # Check if there are any chats for this topic
            "chats": chat_history,
            "isUser": False
        })

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get('message')
    topic = request.json.get('chatTopic')
    if topic is None:
        topic = request.json.get('topic', 'General')
    print(topic)
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = None
    redirect_url = None

    if user_message.startswith('!'):
        command = user_message[1:].lower()

        if command in ['userinfo', 'kullanıcıbilgisi']:
            if current_user.is_authenticated:
                redirect_url = url_for('profile_page')
                response = "Redirecting to your profile page..."
                #return redirect(redirect_url)
            else:
                response = "You need to be logged in to view your profile."

        elif command in ['quiz', 'sınav']:
            if current_user.is_authenticated:
                redirect_url = url_for('quiz_start')
                response = "Redirecting to the quiz page..."
            else:
                response = "You need to be logged in to access the quiz page."

        elif command == 'help':
            response = (
                "Here are the available commands:\n"
                "!time / !saat - Get the current server time\n"
                "!date / !tarih - Show today's date\n"
                "!userinfo / !kullanıcıbilgisi - Display your account information\n"
                "!quiz / !sınav - Directly open quiz page\n"
                "!clearhistory / !temizle - Clear your chat history\n"
                "!about / !hakkında - Learn more about me\n"
            )
        elif command == 'yardım':    
            response = (
                "Mevcut komutlar şunlardır:\n"
                "!time / !saat - Sunucunun mevcut saatini gösterir\n"
                "!date / !tarih - Bugünün tarihini gösterir\n"
                "!userinfo / !kullanıcıbilgisi - Kullanıcı bilgilerinizi gösterir\n"
                "!quiz / !sınav - Sınav sayfasına yönlendirir\n"
                "!clearhistory / !temizle - Sohbet geçmişinizi siler\n"
                "!about / !hakkında - Benim hakkımda bilgi verir\n"
            )
        elif command == 'time':
            response = f"The current server time is: {datetime.now().strftime('%H:%M:%S')}"
        elif command == 'saat':
            response = f"Sunucu saati: {datetime.now().strftime('%H:%M:%S')}"
        elif command == 'date':
            response = f"Today's date is: {datetime.now().strftime('%Y-%m-%d')}"
        elif command == 'tarih':
            response = f"Bugünün tarihi: {datetime.now().strftime('%Y-%m-%d')}"
        elif command == 'about':
            response = (
                "I am an educational bot designed to assist you with various topics.\n"
                "My purpose is to provide helpful information, guide you through lessons, and answer your questions on a variety of subjects.\n"
            )
        elif command == 'hakkında':    
            response = (
                "Ben bir eğitim botuyum, çeşitli konularda size yardımcı olmak için tasarlandım.\n"
                "Amacım, size faydalı bilgiler sunmak, derslerde rehberlik yapmak ve birçok konuda sorularınızı cevaplamak.\n"
            )
        else:
            response = "Command cannot be found! Type !help or !yardım to see the available commands."
    else:
        response = llm.invoke(user_message)
    chat_entry = {
        "question": user_message,
        "response": response,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if current_user.is_authenticated:
        #chat_history = ChatHistory.query.filter_by(user_id=current_user.id).first()
        if current_user.currentChatID is None:
            chat_history = ChatHistory(user_id=current_user.id, topic=topic, chats=[])
            
            ## refresh to the this chat
        else:
            chat_history = ChatHistory.query.filter_by(id=current_user.currentChatID).first()
       ## if not chat_history:
         ##   chat_history = ChatHistory(user_id=current_user.id, topic=topic, chats=[])
        chat_history.chats.append(chat_entry)
        db.session.add(chat_history)
        db.session.commit()
        print(chat_history.id)
        return jsonify({
                "topic": topic,
                "chats": chat_history.chats,
                "chatId": chat_history.id,
                "isUser": True  # Assuming `chats` is JSON serializable
            })

    #if redirect_url:
       # return redirect(redirect_url)

    return jsonify({
        "topic": topic,
        "chat_entry": chat_entry,
        "isUser": False
    })

@app.route("/quiz_start")
def quiz_start():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_page'))

    # Quiz'i veritabanından çek
    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_page'))

    # Quiz var, quiz sayfasına yönlendir
    return render_template("quiz_start.html", quiz=quiz)

@app.route("/quiz")
def quiz():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_page'))

    # Quiz'i ve soruları veritabanından çek
    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_page'))

    # Soruları al
    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()

    # Soruları JSON formatında frontend'e göndereceksek
    quiz_questions = []
    for question in questions:
        options = []  # Cevapları burada al
        answers = QuestionAnswer.query.filter_by(question_id=question.id).all()
        for answer in answers:
            options.append(answer.option_text)

        quiz_questions.append({
            'question': question.text,
            'options': options
        })

    return render_template("quiz.html", quiz=quiz, questions=quiz_questions)


@app.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



'''
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