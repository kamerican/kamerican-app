from flask import Blueprint

bp = Blueprint('errors', __name__)

from kamericanapp.errors import handlers
