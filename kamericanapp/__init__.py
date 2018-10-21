from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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
from kamericanapp import routes, models


