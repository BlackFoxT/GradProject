from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models import db

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth_routes', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home_routes.home_page'))
        else:
            flash("Email or password is incorrect", "error")
            return redirect(url_for('auth_routes.login_page'))

    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for('auth_routes.signup_page'))

        # Hash the password before saving to the database
        hashed_password = generate_password_hash(password)

        # Create a new user with hashed password
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('auth_routes.login_page'))

    return render_template("signup.html")

@auth_bp.route("/logout")
def logout():
    current_user.currentChatID = None
    # Save the change to the database
    db.session.commit()
    logout_user()
    return redirect(url_for('home_routes.home_page'))
