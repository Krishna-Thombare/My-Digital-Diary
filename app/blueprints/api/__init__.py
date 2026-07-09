from flask import Blueprint, jsonify, request
from flask_login import current_user

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.before_request
def require_api_login():
    if request.endpoint == "api.login":
        return None

    if not current_user.is_authenticated:
        return jsonify({"error": "Authentication required."}), 401
