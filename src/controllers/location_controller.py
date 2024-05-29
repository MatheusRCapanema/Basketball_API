import requests
from flask import request, Response, json, Blueprint, jsonify

from src import db
from src.models.location_model import Location


locations = Blueprint('locations', __name__)


@locations.route('/list', methods=['GET'])
def listar_paises():
    try:
        locations = Location.query.all()
        location_names = [location.stadium_name for location in locations]
        return jsonify({'status': 'success', 'countries': location_names}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred', 'error': str(e)}), 500