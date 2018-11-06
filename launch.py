from kamericanapp import create_app, db, socketio
from kamericanapp.database.models import Users

app = create_app()

if __name__ == '__main__':
    socketio.run(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users}
