from . import db
from sqlalchemy.ext.mutable import MutableList

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    chats = db.Column(MutableList.as_mutable(db.JSON), nullable=True)
    difficulty = db.Column(db.String(100), nullable=False, default="easy")
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
