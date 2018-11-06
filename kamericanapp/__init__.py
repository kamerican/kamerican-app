import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config
from flask_socketio import SocketIO
from redis import Redis
from rq import Queue



db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        

        # Redis, unnecessary now
        #app.redis = Redis.from_url(app.config['REDIS_URL'])
        #app.queue = Queue(connection=app.redis)
        
        # Register blueprints
        from kamericanapp.errors import bp_errors
        app.register_blueprint(bp_errors)

        from kamericanapp.dashboard import bp_dashboard
        app.register_blueprint(bp_dashboard)

        from kamericanapp.imagedownloader import bp_imagedownloader
        app.register_blueprint(bp_imagedownloader)

        db.init_app(app)
        migrate.init_app(app, db)
        bootstrap.init_app(app)
        socketio.init_app(app)

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
