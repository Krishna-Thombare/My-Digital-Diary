from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class JournalForm(FlaskForm):
    topic_name = StringField("Topic Name", validators=[DataRequired()])
    journal_texts = TextAreaField("Journal Entry", validators=[DataRequired()])
    submit = SubmitField("Save Journal")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")