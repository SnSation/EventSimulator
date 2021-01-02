from flask import Blueprint

bp = Blueprint('modeler', __name__, url_prefix='/modeler')

from . import routes, models