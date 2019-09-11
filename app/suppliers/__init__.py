from flask import Blueprint

bp = Blueprint('suppliers', __name__)

from app.suppliers import routes
