from datetime import datetime

from flask import request, Response, json, Blueprint, jsonify

from src import db
from src.models.match_model import Match

matches = Blueprint("matches", __name__)


@matches.route('/create', methods=['POST'])
def create_match():
    try:
        data = request.get_json()
        if not all(key in data for key in ('date', 'location_id', 'team_a_id', 'team_b_id', 'stage', 'status')):
            return Response(
                response=json.dumps({'status': 'error', 'message': 'All fields are required'}),
                status=400,
                mimetype='application/json'
            )

        new_match = Match(
            date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'),
            location_id=data['location_id'],
            team_a_id=data['team_a_id'],
            team_b_id=data['team_b_id'],
            stage=data['stage'],
            status=data['status']
        )

        db.session.add(new_match)
        db.session.commit()

        return Response(
            response=json.dumps({'status': 'success', 'message': 'Match created successfully'}),
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

        matches_query = Match.query.paginate(page=page, per_page=per_page, error_out=False)

        matches_list = []
        for match in matches_query.items:
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
            'page': matches_query.page,
            'pages': matches_query.pages,
            'total': matches_query.total,
            'has_next': matches_query.has_next,
            'has_prev': matches_query.has_prev,
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
