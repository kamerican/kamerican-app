from flask import Blueprint

bp_notification = Blueprint('notification', __name__, template_folder='templates')

from kamericanapp.notification import views