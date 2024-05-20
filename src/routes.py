from flask import Blueprint

from src.controllers.match_controller import matches
from src.controllers.processamento_csv import load_data_blueprint
from src.controllers.user_controller import users

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(users, url_prefix="/users")

api.register_blueprint(load_data_blueprint, url_prefix="/load_data")

api.register_blueprint(matches, url_prefix="/matches")
