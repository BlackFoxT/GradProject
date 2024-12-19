from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import db, User, Information, ChatHistory
from application import llm
from datetime import datetime
from flask_babel import _, gettext

# Initialize Blueprint
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/change_language/<lang_code>')
def change_language(lang_code):
    # Save language preference in session or cookie
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

@main_bp.route('/')
def home_page():
    return render_template('index.html')

@main_bp.route("/chatl")
def chatl():
    chat_id = request.args.get('id', type=int)
    if chat_id:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=chat_id).first()
        current_user.currentChatID = chat_id
    return redirect(url_for('main_bp.home_page'))

@main_bp.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer)

@main_bp.route('/login', methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main_bp.home_page'))
        else:
            flash("Email or password is incorrect", "error")
            return redirect(url_for('main_bp.login_page'))

    return render_template("login.html")

@main_bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This email is already registered", "error")
            return redirect(url_for('main_bp.signup_page'))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('main_bp.login_page'))

    return render_template("signup.html")

@main_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main_bp.home_page'))

@main_bp.route("/profile")
def profile_page():
    if current_user.is_authenticated:
        user_information = Information.query.filter_by(user_id=current_user.id).first()
        return render_template("profile.html", info=user_information)
    else:
        return redirect(url_for('main_bp.login_page'))

@main_bp.route('/update_information', methods=['POST'])
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
        return redirect(url_for('main_bp.home_page'))
    else:
        flash("You must be logged in to update your information.", "error")
        return redirect(url_for('main_bp.login_page'))

@main_bp.route("/get-chat-history", methods=["GET"])
def get_chat_history():
    topic = request.args.get("topic", "General")

    if current_user.is_authenticated:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id).first()
        if chat_history:
            return jsonify({
                "contentVisible": True,
                "chats": chat_history.chats,
                "isUser": True
            })
        else:
            return jsonify({"contentVisible": False, "chats": [], "isUser": True})
    else:
        chat_history = session.get("chat_history", {})
        return jsonify({
            "contentVisible": bool(chat_history),
            "chats": chat_history,
            "isUser": False
        })

@main_bp.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get('message')
    topic = request.json.get('topic', 'General')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    if user_message.startswith('!'):
        command = user_message[1:].lower()
        response = ""

        if command == 'help':
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
            response = f"Today's date is: {datetime.now().strftime('%Y-%m-%d')}",
        elif command == 'tarih':
            response = f"Bugünün tarihi: {datetime.now().strftime('%Y-%m-%d')}"
        elif command == 'about':
            response = (
            "I am an educational bot designed to assist you with various topics.\n"
            "My purpose is to provide helpful information, guide you through lessons, and answer your questions on a variety of subjects.\n"
            "You can ask me anything related to your learning journey, and I'll do my best to provide accurate and insightful responses.\n"
            "I am constantly evolving to better serve your educational needs, so feel free to explore!\n"
            "I can help with coding, quizzes, general knowledge, and much more!\n"
            "I am here to support you in your learning process. Let's start learning together!"
            )
        elif command == 'hakkında':    
            response = (
                "Ben bir eğitim botuyum, çeşitli konularda size yardımcı olmak için tasarlandım.\n"
                "Amacım, size faydalı bilgiler sunmak, derslerde rehberlik yapmak ve birçok konuda sorularınızı cevaplamak.\n"
                "Öğrenme yolculuğunuzla ilgili bana her türlü soruyu sorabilirsiniz ve ben elimden gelenin en iyisini yaparak yanıt vermeye çalışırım.\n"
                "Sürekli olarak gelişiyorum, böylece eğitim ihtiyaçlarınıza daha iyi hizmet verebilirim. O yüzden keşfetmekten çekinmeyin!\n"
                "Kodlama, sınavlar, genel bilgiler ve daha birçok konuda yardımcı olabilirim!\n"
                "Öğrenme sürecinizde sizi desteklemek için buradayım. Haydi, birlikte öğrenmeye başlayalım!"
            )
        elif command == 'userinfo' or command == 'kullanıcıbilgisi':
            if command == 'userinfo':
                if current_user.is_authenticated:
                    response = "Redirecting you to your profile page..."
                else:
                    response = "You need to be logged in to view your profile."
            else:
                if current_user.is_authenticated:
                    response = "Profil sayfasına yönlendiriliyorsunuz..."
                else:
                    response = "Profilinizi görüntülemek için giriş yapmanız gerekmektedir."
        elif command == 'quiz':
            response = "Redirecting you to the quiz page..."
        elif command == 'sınav':
            response = "Sınav sayfasına yönlendiriliyorsunuz..."
            
        '''
        elif command == 'clearhistory' or command == 'temizle':
            if current_user.is_authenticated:
                chat_history = ChatHistory.query.filter_by(user_id=current_user.id).first()
                if chat_history:
                    chat_history.chats = []
                    db.session.commit()
                response = "Your chat history has been cleared."
            else:
                response = "You need to be logged in to clear chat history."
        '''
        if not response:
            response = "Command cannot be found! Type !help or !yardım to see the available commands."

    else:
        response = llm.invoke(user_message)

    chat_entry = {
        "question": user_message,
        "response": response,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if current_user.is_authenticated:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id).first()

        if not chat_history:
            chat_history = ChatHistory(user_id=current_user.id, topic=topic, chats=[])

        chat_history.chats.append(chat_entry)
        db.session.add(chat_history)
        db.session.commit()

        return jsonify({
            "topic": chat_history.topic,
            "chats": chat_history.chats,
            "isUser": True
        })
    else:
        return jsonify({
            "message": "Unauthenticated user, storing chat in localStorage temporarily.",
            "chat_entry": chat_entry,
            "isUser": False
        })

@main_bp.route("/quiz_start")
def quiz_start():
    return render_template("quiz_start.html")

@main_bp.route("/quiz")
def quiz():
    return render_template("quiz.html")

@main_bp.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")
