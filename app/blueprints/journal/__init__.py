from flask import Blueprint

journal_bp = Blueprint("journal", __name__, url_prefix="/journal", template_folder="templates")

from . import routes

