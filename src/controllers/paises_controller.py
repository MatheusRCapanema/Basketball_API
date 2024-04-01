import requests
from flask import Blueprint, jsonify

countries = Blueprint('countries', __name__)


@countries.route('/country/<country_id>', methods=['GET'])
def get_country(country_id):
    headers = {
        'Authorization': '1234567890'
    }

    response = requests.get(
        f'https://virtserver.swaggerhub.com/PI_IESB_2024/API_Olimpiadas/0.0.2/paises?_id={country_id}', headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Não foi possível obter informações do país'}), response.status_code
