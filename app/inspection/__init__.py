from flask import Blueprint

inspection_bp = Blueprint('inspection', __name__)

from . import routes