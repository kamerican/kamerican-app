from flask import Blueprint

bp = Blueprint('main', __name__)

from kamericanapp.main import routes
