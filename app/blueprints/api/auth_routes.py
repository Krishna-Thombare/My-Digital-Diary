from flask import jsonify, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from . import api_bp
from app.models import User


@api_bp.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({
            "message": "Already logged in.",
            "user": {
                "id": current_user.id,
                "username": current_user.username,
            },
        })

    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password."}), 401

    login_user(user)

    return jsonify({
        "message": "Logged in successfully.",
        "user": {
            "id": user.id,
            "username": user.username,
        },
    })


@api_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."})
