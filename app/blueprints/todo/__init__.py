from flask import Blueprint

todo_bp = Blueprint('todo', __name__, url_prefix="/todo", template_folder='templates')

from . import routes
