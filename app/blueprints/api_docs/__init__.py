from flask import Blueprint

api_docs_bp = Blueprint('api_docs', __name__, template_folder="templates")

from . import routes
