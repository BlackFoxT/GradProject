from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    information = db.relationship('Information', backref='user', lazy=True)
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home_page():
    return render_template("index.html")

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

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This email is already registered", "error")
            return redirect(url_for('signup_page'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
