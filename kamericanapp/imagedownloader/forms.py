from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LinksForm(FlaskForm):
    """Form for image downloader page"""
    links = TextAreaField(label="Links to download images from:", validators=[DataRequired()])
    submit = SubmitField(label="Submit")