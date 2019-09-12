from flask import Blueprint

bp = Blueprint('production_lines', __name__)

from app.production_lines import routes
