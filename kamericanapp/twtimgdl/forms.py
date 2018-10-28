from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm


class LinksForm(FlaskForm):
    links = TextAreaField('Links to download images from:', validators=[DataRequired()])
    submit = SubmitField('Submit')