from flask import Blueprint

bp = Blueprint('database', __name__, url_prefix = '/database')

from . import routes, models