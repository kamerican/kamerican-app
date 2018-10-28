from flask import Blueprint

bp = Blueprint('twtimgdl', __name__, template_folder='templates')

from kamericanapp.twtimgdl import views
