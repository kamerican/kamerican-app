import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config
#from celery import Celery

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
#print(Config.CELERY_RESULT_BACKEND)
#celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    #celery.conf.update(app.config)
    
    # Register blueprints
    from kamericanapp.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from kamericanapp.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from kamericanapp.imagedownloader import bp as imagedownloader_bp
    app.register_blueprint(imagedownloader_bp)

    '''
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/kamericanapp.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('kamericanapp startup')
    '''
    return app


from kamericanapp.database import models
