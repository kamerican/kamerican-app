import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # Server
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        os.urandom(16)

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'kamericanapp', 'database', 'production.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #print(SQLALCHEMY_DATABASE_URI)

    # Redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
