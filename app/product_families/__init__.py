from flask import Blueprint

bp = Blueprint('product_families', __name__)

from app.product_families import routes
