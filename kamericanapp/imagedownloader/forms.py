from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LinksForm(FlaskForm):
    links = TextAreaField(label="Links to download images from:", validators=[DataRequired()])
    run_local = BooleanField(label="Run using localhost (Note: not working, likely because of eventlet incompatibility with python 3.7)")
    submit = SubmitField(label="Submit")