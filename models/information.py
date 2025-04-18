from . import db

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    telephone_number = db.Column(db.String(15))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    language = db.Column(db.String(20))
    profile_image = db.Column(db.String(200), nullable=True)