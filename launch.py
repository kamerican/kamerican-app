from kamericanapp import create_app, db, socketio
from kamericanapp.database.models import RQJob, Person, Image, Face, Identity

app = create_app()
#app.app_context().push()
print("Launching server on host url: http://127.0.0.1:5000/")
#socketio.run(app)
#socketio.run(app, debug=True)
#socketio.run(app, log_output=True)


def remove_jobs():
    for rq_job in RQJob().query.all():
        print("Removing RQ job:", rq_job)
        db.session.delete(rq_job)
    db.session.commit()
    return

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'RQJob': RQJob,
        'Person': Person,
        'Image': Image,
        'Face': Face,
        'Identity': Identity,
        'remove_jobs': remove_jobs,
    }
