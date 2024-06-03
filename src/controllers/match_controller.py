from datetime import datetime

from flask import request, Response, json, Blueprint, jsonify

from src import db
from src.models import Team, Country, Player
from src.models.location_model import Location
from src.models.match_model import Match

matches = Blueprint("matches", __name__)


@matches.route('/create', methods=['POST'])
def create_match():
    try:
        data = request.get_json()
        if not all(key in data for key in ('date', 'location_id', 'country_a', 'country_b', 'stage', 'status')):
            return Response(
                response=json.dumps({'status': 'error', 'message': 'All fields are required'}),
                status=400,
                mimetype='application/json'
            )

        # Verificar se os países existem
        country_a = Country.query.filter_by(name=data['country_a']).first()
        country_b = Country.query.filter_by(name=data['country_b']).first()
        location = Location.query.get(data['location_id'])

        if not country_a or not country_b:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'One or both countries do not exist'}),
                status=400,
                mimetype='application/json'
            )

        if not location:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Location does not exist'}),
                status=400,
                mimetype='application/json'
            )

        # Verificar se os times existem para os países
        team_a = Team.query.filter_by(country_id=country_a.id).first()
        team_b = Team.query.filter_by(country_id=country_b.id).first()

        if not team_a or not team_b:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'One or both teams do not exist for the given countries'}),
                status=400,
                mimetype='application/json'
            )

        new_match = Match(
            date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'),
            location_id=data['location_id'],
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            stage=data['stage'],
            status=data['status'],
            referee_id=None,  # Inicialmente nulo
            score_team_a=0,  # Inicialmente 0
            score_team_b=0  # Inicialmente 0
        )

        db.session.add(new_match)
        db.session.commit()

        # Buscar jogadores das equipes A e B
        team_a_players = Player.query.filter_by(team_id=team_a.id).all()
        team_b_players = Player.query.filter_by(team_id=team_b.id).all()

        # Construir a resposta com detalhes da partida e jogadores
        response_data = {
            'id': new_match.id,
            'date': new_match.date.strftime('%Y-%m-%d %H:%M:%S'),
            'location': new_match.location.stadium_name,
            'team_a': {
                'id': new_match.team_a.id,
                'name': new_match.team_a.name,
                'score': new_match.score_team_a,  # Placar da equipe A
                'players': [{'id': player.id, 'name': player.name, 'position': player.position, 'number': player.number} for player in team_a_players]
            },
            'team_b': {
                'id': new_match.team_b.id,
                'name': new_match.team_b.name,
                'score': new_match.score_team_b,  # Placar da equipe B
                'players': [{'id': player.id, 'name': player.name, 'position': player.position, 'number': player.number} for player in team_b_players]
            },
            'stage': new_match.stage,
            'status': new_match.status,
            'referee': new_match.referee_id
        }

        return Response(
            response=json.dumps({'status': 'success', 'match': response_data}),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': 'An error occurred', 'error': str(e)}),
            status=500,
            mimetype='application/json'
        )


@matches.route('/list', methods=['GET'])
def list_matches():
    try:

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        matches_query = Match.query.all()

        matches_list = []
        for match in matches_query:
            matches_list.append({
                'id': match.id,
                'date': match.date.strftime('%Y-%m-%d %H:%M:%S'),
                'location': match.location.stadium_name,
                'team_a': match.team_a.name,
                'team_b': match.team_b.name,
                'stage': match.stage,
                'status': match.status
            })

        return jsonify({
            'status': 'success',
            'matches': matches_list,
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred',
            'error': str(e)
        }), 500


@matches.route('/delete/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    try:
        match = Match.query.get(match_id)
        if not match:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Match not found'}),
                status=404,
                mimetype='application/json'
            )

        db.session.delete(match)
        db.session.commit()

        return Response(
            response=json.dumps({'status': 'success', 'message': 'Match deleted successfully'}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': 'An error occurred', 'error': str(e)}),
            status=500,
            mimetype='application/json'
        )
