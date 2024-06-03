from datetime import datetime
from src import db

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    team_a_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team_b_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    referee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    stage = db.Column(db.String(50))
    status = db.Column(db.String(20))
    score_team_a = db.Column(db.Integer, default=0)  # Novo campo para o placar
    score_team_b = db.Column(db.Integer, default=0)  # Novo campo para o placar

    location = db.relationship('Location', backref=db.backref('matches', lazy=True))
    team_a = db.relationship('Team', foreign_keys=[team_a_id], backref=db.backref('matches_as_team_a', lazy=True))
    team_b = db.relationship('Team', foreign_keys=[team_b_id], backref=db.backref('matches_as_team_b', lazy=True))
    referee = db.relationship('User', backref=db.backref('matches', lazy=True))
