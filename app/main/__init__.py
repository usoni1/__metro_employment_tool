from flask import Blueprint
main = Blueprint('main', __name__, static_folder='static', template_folder='templates', static_url_path='/main/static')
from . import automation_features