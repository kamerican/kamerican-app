from flask import Blueprint

bp_imagedownloader = Blueprint('imagedownloader', __name__, template_folder='templates')

from kamericanapp.imagedownloader import views
