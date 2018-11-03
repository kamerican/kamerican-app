import os
from kamericanapp import celery, create_app

#print(os.getenv('FLASK_CONFIG'))
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app()
app.app_context().push()