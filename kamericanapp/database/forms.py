from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoadImagesForm(FlaskForm):
    """Submit button for loading images in original directory into database."""
    submit_load = SubmitField(label="Load new original images into the database")

class ResizeImagesForm(FlaskForm):
    """Submit button for creating resized images of images in the database without a resize_filepath. Resized image is saved in the resized directory."""
    submit_resize = SubmitField(label="Create new resized images")