from src import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stadium_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    capacity = db.Column(db.Integer)