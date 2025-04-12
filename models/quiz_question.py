from . import db
from sqlalchemy.ext.mutable import MutableList

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    options = db.Column(MutableList.as_mutable(db.JSON), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
