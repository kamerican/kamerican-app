from kamericanapp import create_app, db, socketio
from kamericanapp.database.models import RQJob

app = create_app()
print("Launching server")
#socketio.run(app)
#socketio.run(app, debug=True)
#socketio.run(app, log_output=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'RQJob': RQJob}
