from flask import Blueprint

ideas_bp = Blueprint("ideas", __name__, url_prefix="/ideas", template_folder="templates")

from . import routes