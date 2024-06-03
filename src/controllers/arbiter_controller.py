from flask import Blueprint, request, jsonify, Response, json
from src import db
from src.models.match_model import Match
from src.models.team_model import Team
from src.models.player_model import Player
from src.models.location_model import Location
from src.models.user_model import User
from datetime import datetime

arbiter = Blueprint('arbiter_controller', __name__)


@arbiter.route('/started_match/<int:match_id>', methods=['POST'])
def iniciar_partida(match_id):
    try:
        data = request.get_json()
        referee_id = data.get('referee_id')

        if not referee_id:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Referee ID is required'}),
                status=400,
                mimetype='application/json'
            )

        # Buscar a partida pelo ID
        match = Match.query.get(match_id)
        if not match:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Match not found'}),
                status=404,
                mimetype='application/json'
            )

        # Verificar se a partida já está "em andamento"
        if match.status == 'Em andamento':
            if match.referee_id != referee_id:
                return Response(
                    response=json.dumps(
                        {'status': 'error', 'message': 'Esta partida já está sendo arbitrada por outro juíz.'}),
                    status=403,
                    mimetype='application/json'
                )

        # Atualizar o status da partida para "Em andamento" e definir o árbitro
        match.status = 'Em andamento'
        match.referee_id = referee_id
        db.session.commit()

        # Buscar jogadores das equipes A e B
        team_a_players = Player.query.filter_by(team_id=match.team_a_id).all()
        team_b_players = Player.query.filter_by(team_id=match.team_b_id).all()

        # Construir a resposta com detalhes da partida e jogadores

        response_data = {
            'id': match.id,
            'date': match.date.strftime('%Y-%m-%d %H:%M:%S'),
            'location': match.location.stadium_name,
            'team_a': {
                'id': match.team_a.id,
                'name': match.team_a.country.iso_code,
                'score': match.score_team_a,  # Placar da equipe A
                'players': [{'id': player.id, 'name': player.name, 'position': player.position, 'number': player.number}
                            for player in team_a_players]
            },
            'team_b': {
                'id': match.team_b.id,
                'name': match.team_b.country.iso_code,
                'score': match.score_team_b,  # Placar da equipe B
                'players': [{'id': player.id, 'name': player.name, 'position': player.position, 'number': player.number}
                            for player in team_b_players]
            },
            'stage': match.stage,
            'status': match.status,
            'referee': match.referee_id
        }
        return Response(
            response=json.dumps({'status': 'success', 'match': response_data}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': 'An error occurred', 'error': str(e)}),
            status=500,
            mimetype='application/json'
        )


@arbiter.route('/points', methods=['POST'])
def marcar_ponto():
    try:
        data = request.get_json()
        if not all(key in data for key in ('match_id', 'player_id', 'points')):
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Match ID, Player ID, and Points are required'}),
                status=400,
                mimetype='application/json'
            )

        match = Match.query.get(data['match_id'])
        player = Player.query.get(data['player_id'])

        if not match or not player:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Match or Player not found'}),
                status=404,
                mimetype='application/json'
            )

        # Atualizar a pontuação do jogador
        player.points += data['points']

        # Atualizar a pontuação do time na partida
        if player.team_id == match.team_a_id:
            match.score_team_a += data['points']
        elif player.team_id == match.team_b_id:
            match.score_team_b += data['points']
        else:
            return Response(
                response=json.dumps(
                    {'status': 'error', 'message': 'Player does not belong to either team in the match'}),
                status=400,
                mimetype='application/json'
            )

        db.session.commit()

        # Construir a resposta com detalhes atualizados da partida
        team_a_players = Player.query.filter_by(team_id=match.team_a_id).all()
        team_b_players = Player.query.filter_by(team_id=match.team_b_id).all()

        response_data = {
            'id': match.id,
            'date': match.date.strftime('%Y-%m-%d %H:%M:%S'),
            'location': match.location.stadium_name,
            'team_a': {
                'id': match.team_a.id,
                'name': match.team_a.country.iso_code,
                'score': match.score_team_a,  # Placar da equipe A
                'players': [{'id': player.id, 'name': player.name, 'position': player.position, 'number': player.number,
                             'points': player.points} for player in team_a_players]
            },
            'team_b': {
                'id': match.team_b.id,
                'name': match.team_b.country.iso_code,
                'score': match.score_team_b,  # Placar da equipe B
                'players': [{'id': player.id, 'name': player.name, 'position': player.position, 'number': player.number,
                             'points': player.points} for player in team_b_players]
            },
            'stage': match.stage,
            'status': match.status,
            'referee': match.referee_id
        }

        return Response(
            response=json.dumps({'status': 'success', 'match': response_data}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': 'An error occurred', 'error': str(e)}),
            status=500,
            mimetype='application/json'
        )


@arbiter.route('/fault', methods=['POST'])
def marcar_falta():
    try:
        data = request.get_json()
        if not all(key in data for key in ('match_id', 'player_id')):
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Match ID and Player ID are required'}),
                status=400,
                mimetype='application/json'
            )

        match = Match.query.get(data['match_id'])
        player = Player.query.get(data['player_id'])

        if not match or not player:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Match or Player not found'}),
                status=404,
                mimetype='application/json'
            )

        # Incrementar a falta do jogador
        player.faults += 1

        db.session.commit()

        return Response(
            response=json.dumps({'status': 'success', 'message': 'Fault recorded successfully'}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': 'An error occurred', 'error': str(e)}),
            status=500,
            mimetype='application/json'
        )