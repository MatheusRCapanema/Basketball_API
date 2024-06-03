from flask import Blueprint

from src.controllers.match_controller import matches
from src.controllers.processamento_csv import load_data_blueprint
from src.controllers.user_controller import users
from src.controllers.paises_controller import countries
from src.controllers.location_controller import locations
from src.controllers.arbiter_controller import arbiter


api = Blueprint('api', __name__)

api.register_blueprint(users, url_prefix="/users")

api.register_blueprint(load_data_blueprint, url_prefix="/load_data")

api.register_blueprint(matches, url_prefix="/matches")

api.register_blueprint(countries, url_prefix="/countries")

api.register_blueprint(locations, url_prefix="/locations")

api.register_blueprint(arbiter, url_prefix="/arbiter")
