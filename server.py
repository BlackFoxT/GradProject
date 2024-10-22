from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

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
            return "Hatalı email veya şifre", 401

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])  
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home_page'))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
