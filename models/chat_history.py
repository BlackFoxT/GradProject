from . import db
from sqlalchemy.ext.mutable import MutableList

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    chats = db.Column(MutableList.as_mutable(db.JSON), nullable=True)
    difficulty = db.Column(db.String(100), nullable=False, default="easy")
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    realchat_count = db.Column(db.Integer, nullable=False, default=0)
    extrachat = db.Column(db.Integer, nullable=False, default=0)
    is_sumbitted = db.Column(db.Boolean, nullable=False, default=False)
    is_quizstarted = db.Column(db.Boolean, nullable=False, default=False)
