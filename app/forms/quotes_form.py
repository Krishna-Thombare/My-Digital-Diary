from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class QuoteForm(FlaskForm):
    quotes = TextAreaField("Write your quote...", validators=[DataRequired()])
    submit = SubmitField("Add Quote!")
    
class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")