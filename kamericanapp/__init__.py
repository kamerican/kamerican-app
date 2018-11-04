import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config

from redis import Redis
from rq import Queue


#os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        bootstrap.init_app(app)

        # Redis
        app.redis = Redis.from_url(app.config['REDIS_URL'])
        app.queue = Queue(connection=app.redis)
        
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
