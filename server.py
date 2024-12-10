from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from langchain_community.llms.ollama import Ollama
from datetime import datetime
import bcrypt
# ChatHistory model (storing an array of chats for each topic)
from sqlalchemy.ext.mutable import MutableList

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Initialize Ollama model
llm = Ollama(model="llama3.2")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    information = db.relationship('Information', backref='user', lazy=True)
    chats = db.relationship('ChatHistory', backref='user', lazy=True)
    chat_links = db.relationship('ChatLink', backref='user', lazy=True)


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    telephone_number = db.Column(db.String(15))

class ChatLink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link = db.Column(db.String(255), nullable=False)



class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    chats = db.Column(MutableList.as_mutable(db.JSON), nullable=True)  # Make the list mutable
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home_page():
    print(current_user.is_authenticated)
    return render_template('index.html')

@app.route("/chatl")
def chatl():
    # Get the 'id' query parameter from the URL
    chat_id = request.args.get('id', type=int)
    if chat_id:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=chat_id).first()
        current_user.currentChatID = id
    # Pass the 'chat_id' to the template
    return redirect(url_for('home_page'))



@app.route("/login", methods=["GET", "POST"])
def login_page():

    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user with hashed password
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login_page'))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/profile")
def profile_page():
    if current_user.is_authenticated:
        user_information = Information.query.filter_by(user_id=current_user.id).first()
        user_chat_links = ChatLink.query.filter_by(user_id=current_user.id).all()
        return render_template("profile.html", info=user_information, chat_links=user_chat_links)
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

from flask import request, jsonify, session

@app.route("/get-chat-history", methods=["GET"])
def get_chat_history():
    topic = request.args.get("topic", "General")  # Default topic or fetch from user preference
    
    if current_user.is_authenticated:
        # For authenticated users, fetch chat history from the database
        print(current_user.id)
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id).first()
        print(chat_history.chats)
        if chat_history:
            print(chat_history.chats)
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
        print(chat_history)
        return jsonify({
            "contentVisible": bool(chat_history),  # Check if there are any chats for this topic
            "chats": chat_history,
            "isUser": False
        })




@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get('message')
    topic = request.json.get('topic', 'General')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Invoke the LLM with the user message
    response = llm.invoke(user_message)

    chat_entry = {
        "question": user_message,
        "response": response,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if current_user.is_authenticated:
        # If the user is authenticated, save chat history in the database
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
        # If the user is not authenticated, store the chat in localStorage on the frontend
        return jsonify({
            "message": "Unauthenticated user, storing chat in localStorage temporarily.",
            "chat_entry": chat_entry,
            "isUser": False
        })


@app.route("/quiz_start")
def quiz_start():
    return render_template("quiz_start.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
