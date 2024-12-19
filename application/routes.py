from flask import Flask, redirect, url_for, render_template, request, flash, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from models import User, Information, ChatHistory
from flask_babel import gettext

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/chatl')
def chatl():
    chat_id = request.args.get('id', type=int)
    if chat_id:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=chat_id).first()
        current_user.currentChatID = chat_id
    return redirect(url_for('home_page'))

# More routes such as /login, /signup, etc.
