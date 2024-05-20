import pandas as pd
from flask import Flask, Blueprint, request, jsonify
from src import db
from src.models.country_model import Country
from src.models.player_model import Player
from src.models.team_model import Team

load_data_blueprint = Blueprint('load_data', __name__)

@load_data_blueprint.route('/carregar', methods=['POST'])
def load_data():
    try:
        # Obtenha o caminho do arquivo CSV do corpo da requisição
        file_path = r'C:\Users\mathe\PycharmProjects\basketball-api\static\2020_Olympics_Dataset.csv'
        if not file_path:
            return jsonify({'status': 'error', 'message': 'File path is required'}), 400

        # Carregar o CSV
        data = pd.read_csv(file_path, encoding='ISO-8859-1')

        # Filtrar para jogadores de basquete masculino
        basketball_men = data[(data['Sport'] == 'Basketball') & (data['Event'] == 'Men Team')]

        # Obter lista de países únicos
        countries = basketball_men[['NOC', 'Country']].drop_duplicates().rename(
            columns={'Country': 'name', 'NOC': 'iso_code'})

        # Adicionar continentes (dados fictícios para exemplo)
        continent_mapping = {
            'USA': 'North America',
            'ESP': 'Europe',
            'ARG': 'South America',
            'FRA': 'Europe',
            'AUS': 'Oceania',
            'BRA': 'South America',
            'NGA': 'Africa',
            'CZE': 'Europe',  # Czech Republic
            'JPN': 'Asia',  # Japan
            'GER': 'Europe',  # Germany
            'SLO': 'Europe',  # Slovenia
            'IRN': 'Asia',  # Iran
            'ITA': 'Europe',  # Italy
        }

        countries['continent'] = countries['iso_code'].map(continent_mapping).fillna('Unknown')
        countries['gold_medals'] = 0
        countries['silver_medals'] = 0
        countries['bronze_medals'] = 0

        # Limpar tabelas existentes
        Player.query.delete()
        Team.query.delete()
        Country.query.delete()
        db.session.commit()

        # Adicionar países ao banco de dados
        for _, country_data in countries.iterrows():
            country = Country(
                name=country_data['name'],
                iso_code=country_data['iso_code'],
                continent=country_data['continent'],
                gold_medals=country_data['gold_medals'],
                silver_medals=country_data['silver_medals'],
                bronze_medals=country_data['bronze_medals']
            )
            db.session.add(country)

        db.session.commit()

        # Obter ID dos países inseridos
        country_id_mapping = {country.iso_code: country.id for country in Country.query.all()}

        # Adicionar equipes ao banco de dados
        teams = basketball_men[['NOC', 'Country']].drop_duplicates().rename(
            columns={'Country': 'name', 'NOC': 'iso_code'})
        for _, team_data in teams.iterrows():
            team = Team(
                name=f"Team {team_data['name']}",
                coach=None,  # Ajuste conforme necessário
                country_id=country_id_mapping.get(team_data['iso_code'])
            )
            db.session.add(team)

        db.session.commit()

        # Obter ID das equipes inseridas
        team_id_mapping = {team.country_id: team.id for team in Team.query.all()}

        # Adicionar jogadores ao banco de dados
        for _, player_data in basketball_men.iterrows():
            player = Player(
                team_id=team_id_mapping.get(country_id_mapping.get(player_data['NOC'])),  # Ajuste conforme necessário
                name=player_data['Name'],
                position=None,  # Ajuste conforme necessário
                number=None,  # Ajuste conforme necessário
                points=0,
                faults=0,
            )
            db.session.add(player)

        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Data loaded successfully!'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred', 'error': str(e)}), 500

# Configuração do aplicativo Flask
app = Flask(__name__)
app.register_blueprint(load_data_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
