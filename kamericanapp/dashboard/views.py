from datetime import datetime
from flask import render_template, flash, redirect, url_for, current_app, Response
from kamericanapp import db
from kamericanapp.database.models import Users
from kamericanapp.dashboard import bp
import time

from rq import Queue
from redis import Redis
from rq.registry import StartedJobRegistry

@bp.route('/')
def root():
    flash('Redirect to index!')
    return redirect(url_for('dashboard.index'))

@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@bp.route('/events', methods=['GET', 'POST'])
def events():
    def eventStream():
        print('@@@ ENTERING EVENT STREAM @@@')
        
        queue = Queue(connection=Redis())
        registry = StartedJobRegistry(queue=queue)
        print(queue)
        print(queue.jobs)
        print(registry)
        print(registry.get_job_ids())
        
        while True:
            message = ""
            # Update image downloader progress
            for job_id in registry.get_job_ids():
                # fix this if needed @@@ job.refresh()
                
                message = "Running job: " + job_id
                print('message to send to event source: ' + message)
            
            time.sleep(2)
            print("data: {}\n\n".format(message))
            yield "data: {}\n\n".format(message)
        

    return Response(eventStream(), mimetype="text/event-stream")


