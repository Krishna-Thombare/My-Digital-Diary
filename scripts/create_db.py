import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from app.models import UserJournal
from app.models import UserNotes
from app.models import UserQuotes
from app.models import UserIdeas
from app.models import UserTodoList

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully.")
