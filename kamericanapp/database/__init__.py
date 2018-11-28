from flask import Blueprint

bp_database = Blueprint('database', __name__, template_folder='templates')

from kamericanapp.database import views
