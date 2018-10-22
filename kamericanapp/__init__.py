from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize web server gateway interface (WSGI) web framework
app = Flask(__name__)

# Load flask configuration
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login
login = LoginManager(app)
login.login_view = 'login'

# Load python application modules
from kamericanapp import routes, models, errors

# Logging errors
if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/kamericanapp.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # Different logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('kamerican app startup')
