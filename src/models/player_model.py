from src import db


class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))
    number = db.Column(db.Integer)
    points = db.Column(db.Integer)
    faults = db.Column(db.Integer)
