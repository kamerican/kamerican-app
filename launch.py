from kamericanapp import create_app, db, socketio
from kamericanapp.database.models import RQJob

app = create_app()
print("launching socketio")
#socketio.run(app)
#socketio.run(app, debug=True)
#socketio.run(app, log_output=True)
#app.run()
#if __name__ == '__main__':
#    socketio.run(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'RQJob': RQJob}
