from flask import Blueprint

bp = Blueprint('productions', __name__)

from app.productions import routes
