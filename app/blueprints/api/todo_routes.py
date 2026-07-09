from datetime import date
from flask import jsonify, request
from flask_login import current_user, login_required
from . import api_bp
from app.models import UserTodoList, db

def serialize_todo(todo):
    return {
        "id": todo.id,
        "task": todo.tasks,
        "completed": todo.status,
        "date": todo.date.isoformat() if todo.date else None,
    }

def get_current_user_todo_or_404(todo_id):
    return UserTodoList.query.filter_by(
        id=todo_id,
        user_id=current_user.id,
    ).first_or_404()

def parse_completed(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized_value = value.strip().lower()
        if normalized_value in {"true", "1", "yes"}:
            return True
        if normalized_value in {"false", "0", "no"}:
            return False

    return None

@api_bp.route("/todos", methods=["GET"])
@login_required
def get_todos():
    todos = UserTodoList.query.filter_by(
        user_id=current_user.id,
    ).order_by(UserTodoList.date.desc(), UserTodoList.id.desc()).all()

    return jsonify({"todos": [serialize_todo(todo) for todo in todos]})

@api_bp.route("/todos/<int:todo_id>", methods=["GET"])
@login_required
def get_todo(todo_id):
    todo = get_current_user_todo_or_404(todo_id)
    return jsonify({"todo": serialize_todo(todo)})

@api_bp.route("/todos", methods=["POST"])
@login_required
def create_todo():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()

    if not task:
        return jsonify({"error": "Task is required."}), 400

    completed = parse_completed(data.get("completed", False))
    if completed is None:
        return jsonify({"error": "Completed must be true or false."}), 400

    todo = UserTodoList(
        user_id=current_user.id,
        username=current_user.username,
        tasks=task,
        status=completed,
        date=date.today(),
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify({
        "message": "Todo created successfully.",
        "todo": serialize_todo(todo),
    }), 201

@api_bp.route("/todos/<int:todo_id>", methods=["PATCH"])
@login_required
def update_todo(todo_id):
    todo = get_current_user_todo_or_404(todo_id)
    data = request.get_json(silent=True) or {}

    if "task" in data:
        task = str(data.get("task", "")).strip()
        if not task:
            return jsonify({"error": "Task cannot be empty."}), 400
        todo.tasks = task

    if "completed" in data:
        completed = parse_completed(data["completed"])
        if completed is None:
            return jsonify({"error": "Completed must be true or false."}), 400
        todo.status = completed

    db.session.commit()

    return jsonify({
        "message": "Todo updated successfully.",
        "todo": serialize_todo(todo),
    })

@api_bp.route("/todos/<int:todo_id>", methods=["DELETE"])
@login_required
def delete_todo(todo_id):
    todo = get_current_user_todo_or_404(todo_id)

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo deleted successfully."})
