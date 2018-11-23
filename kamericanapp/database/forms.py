from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoadImagesForm(FlaskForm):
    """Submit button for loading images in load directory into database."""
    submit = SubmitField(label="Load into database")