from kamericanapp import create_app, db
from kamericanapp.models import User, Post

app = create_app()
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
