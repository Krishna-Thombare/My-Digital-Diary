from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class FolderForm(FlaskForm):
    name = StringField("Folder name", validators=[DataRequired()])
    submit = SubmitField("Create")

class UploadImageForm(FlaskForm):
    image = FileField("Images", render_kw={"multiple" : True})
    submit = SubmitField("Upload")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
