from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    information = db.relationship('Information', backref='user', lazy=True)
    chats = db.relationship('ChatHistory', backref='user', lazy=True)
    currentChatID = db.Column(db.Integer, nullable=True)
