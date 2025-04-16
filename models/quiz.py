from . import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat_history.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade="all, delete-orphan")

# Burada difficulty eklemek zor değil ama diğer functionların tekrar düzeltilmesi lazım