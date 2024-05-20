from src import db


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    iso_code = db.Column(db.String(3), nullable=False, unique=True)
    continent = db.Column(db.String(50), nullable=False)
    gold_medals = db.Column(db.Integer, default=0)
    silver_medals = db.Column(db.Integer, default=0)
    bronze_medals = db.Column(db.Integer, default=0)
    teams = db.relationship('Team', backref='country', lazy=True)
