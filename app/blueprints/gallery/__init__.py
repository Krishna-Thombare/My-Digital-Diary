from flask import Blueprint

gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery", template_folder="templates")

from . import routes

