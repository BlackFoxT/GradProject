from . import db
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer)
    passed = db.Column(db.Boolean)
    userAnswers = db.Column(MutableList.as_mutable(db.JSON))
    correctAnswers = db.Column(MutableList.as_mutable(db.JSON))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)