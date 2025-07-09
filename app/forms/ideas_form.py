from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class IdeaForm(FlaskForm):
    ideas = TextAreaField("Write your idea...", validators=[DataRequired()])
    submit = SubmitField("Add Idea!")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
