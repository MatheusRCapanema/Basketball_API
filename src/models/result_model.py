from src import db


class Result(db.Model):
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    score = db.Column(db.Integer)
    fouls = db.Column(db.Integer)
