from flask import Blueprint

bp = Blueprint('home', __name__, url_prefix='/')

from . import routes, models