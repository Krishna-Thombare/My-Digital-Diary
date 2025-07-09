from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NoteForm(FlaskForm):
    note_name = StringField("Topic Name", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[DataRequired()])
    source_links = TextAreaField("Source Links: ")
    submit = SubmitField("Add Note")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")