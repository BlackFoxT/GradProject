from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat_history.id'), nullable=False)
    note_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

## Bunu henüz kullanmadık hata varsa değişebiliriz