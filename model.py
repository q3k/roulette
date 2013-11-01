from app import app, db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(16), unique=True)
    level = db.Column(db.Integer)
    events = db.Column(db.Text)
    shots = db.Column(db.Integer)

