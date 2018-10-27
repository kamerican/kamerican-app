from kamericanapp import create_app, db
from kamericanapp.database.models import Users

app = create_app()
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': Users}
