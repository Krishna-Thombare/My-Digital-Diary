from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_no = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
    message = TextAreaField("Write your questions/queries...", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Submit")
    