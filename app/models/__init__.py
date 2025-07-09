from app import db
from datetime import date

# -------------------- USERS TABLE --------------------
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    # Relationships
    journals = db.relationship('UserJournal', backref='user', lazy=True)
    notes = db.relationship('UserNotes', backref='user', lazy=True)
    quotes = db.relationship('UserQuotes', backref='user', lazy=True)
    ideas = db.relationship('UserIdeas', backref='user', lazy=True)
    todos = db.relationship('UserTodoList', backref='user', lazy=True)

# -------------------- JOURNAL TABLE --------------------
class UserJournal(db.Model):
    __tablename__ = 'user_journal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    topic_name = db.Column(db.String(100), nullable=False)
    journal_texts = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today)

# -------------------- NOTES TABLE --------------------
class UserNotes(db.Model):
    __tablename__ = 'user_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    note_name = db.Column(db.String(70), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    source_links = db.Column(db.Text)
    date = db.Column(db.Date, default=date.today)

# -------------------- QUOTES TABLE --------------------
class UserQuotes(db.Model):
    __tablename__ = 'user_quotes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    quotes = db.Column(db.Text)
    date = db.Column(db.Date, default=date.today)

# -------------------- IDEAS TABLE --------------------
class UserIdeas(db.Model):
    __tablename__ = 'user_ideas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    ideas = db.Column(db.Text)
    date = db.Column(db.Date, default=date.today)

# -------------------- TO-DO LIST TABLE --------------------
class UserTodoList(db.Model):
    __tablename__ = 'user_todo_list'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    tasks = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, default=date.today)
