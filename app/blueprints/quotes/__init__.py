from flask import Blueprint

quotes_bp = Blueprint("quotes", __name__, url_prefix="/quotes", template_folder="templates")

from . import routes

