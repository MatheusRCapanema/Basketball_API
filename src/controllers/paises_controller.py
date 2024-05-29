import requests
from flask import request, Response, json, Blueprint, jsonify

from src import db
from src.models.country_model import Country


countries = Blueprint('countries', __name__)


@countries.route('/list', methods=['GET'])
def listar_paises():
    try:
        countries = Country.query.all()
        country_names = [country.name for country in countries]
        return jsonify({'status': 'success', 'countries': country_names}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred', 'error': str(e)}), 500

