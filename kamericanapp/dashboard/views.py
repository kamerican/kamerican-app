from datetime import datetime
from flask import render_template, flash, redirect, url_for, current_app, Response
from kamericanapp import db
from kamericanapp.database.models import Users
from kamericanapp.dashboard import bp
import time

from rq import Queue
from redis import Redis

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
        print(queue)
        print(queue.jobs)
        message = ""
        # Update image downloader progress
        for job in queue.jobs:
            job.refresh()
            
            message = job.id
            print('message: ' + message)
        
        print("data: {}\n\n".format(message))
        yield "data: {}\n\n".format(message)
        # Refresh every 3 seconds
        time.sleep(3)

    return Response(eventStream(), mimetype="text/event-stream")


