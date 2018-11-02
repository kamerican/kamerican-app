from flask import Blueprint

bp = Blueprint('imagedownloader', __name__, template_folder='templates')

from kamericanapp.imagedownloader import views
