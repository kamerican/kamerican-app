from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

from kamericanapp.auth import views
