from flask import Blueprint

bp_dashboard = Blueprint('dashboard', __name__, template_folder='templates')

from kamericanapp.dashboard import views, events
