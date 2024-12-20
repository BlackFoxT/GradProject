from . import db
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    information = db.relationship('Information', backref='user', lazy=True)
    chats = db.relationship('ChatHistory', backref='user', lazy=True)

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
    chats = db.Column(MutableList.as_mutable(db.JSON), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
