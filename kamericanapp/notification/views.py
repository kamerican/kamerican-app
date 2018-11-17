from kamericanapp import socketio
from kamericanapp.notification import bp_notification
from kamericanapp.database.models import RQJob
from threading import Thread
import time

from flask import has_app_context, current_app

from redis import Redis
from rq import Queue
from rq.job import Job
from rq.registry import StartedJobRegistry, FinishedJobRegistry

notification_thread = Thread()

def GetJobProgress(app):
    with app.app_context():
        redis = Redis()
        queue = Queue(connection=redis)
        running_registry = StartedJobRegistry(queue=queue)
        finished_registry = FinishedJobRegistry(queue=queue)

        showing_running_job_bar = False
        toggle_on_running_job_bar = False
        toggle_off_running_job_bar = False
        
        
        while True:
            time.sleep(2)
            running_msg = "Running jobs:"
            finished_msg = ""
            running_job_id_list = running_registry.get_job_ids()
            finished_job_id_list = finished_registry.get_job_ids()

            if running_job_id_list:
                # Get all job progress and emit update
                for job_id in running_job_id_list:
                    running_msg += "<br>Job ID: {}".format(job_id)
                    running_job = Job.fetch(id=job_id, connection=redis)
                    if 'process' in running_job.meta:
                        running_msg += "<UL><LI>Process: {}".format(running_job.meta['process'])
                    if 'progress' in running_job.meta:
                        running_msg += "<LI>Progress: {}</UL>".format(running_job.meta['progress'])
                socketio.emit('update job progress', {'data': running_msg})
                toggle_on_running_job_bar = True
            else:
                toggle_off_running_job_bar = True

            if finished_job_id_list:
                # Display finished job notification and save to db
                for job_id in finished_job_id_list:
                    finished_msg += "<br>Job ID: {}".format(job_id)
                    finished_job = Job.fetch(job_id, connection=redis)
                    if 'process' in finished_job.meta:
                        finished_msg += "<UL><LI>Process: {}".format(finished_job.meta['process'])
                    rq_job = RQJob()
                    rq_job.save_job(finished_job)
                    finished_registry.remove(finished_job)
                    finished_msg += "<LI>Result: {}".format(rq_job.get_result())
                    finished_msg += "<LI>Time elapsed: {} seconds</UL>".format(rq_job.get_elapsed_time())
                socketio.emit('update job finished', {'data': finished_msg})
                socketio.emit('show finished job bar')

            

            if showing_running_job_bar and toggle_off_running_job_bar:
                toggle_off_running_job_bar = False
                toggle_on_running_job_bar = False
                showing_running_job_bar = False
                print('---------Server: Hide running job bar')
                socketio.emit('hide running job bar')
            elif not showing_running_job_bar and toggle_on_running_job_bar:
                toggle_off_running_job_bar = False
                toggle_on_running_job_bar = False
                showing_running_job_bar = True
                print('---------Server: Show running job bar')
                socketio.emit('show running job bar')
    return
@socketio.on('message')
def receive_message(message):
    print("---------Client:", message)

@socketio.on('json')
def handle_json(json):
    print("---------Client:", json)


@socketio.on('connect')
def connect_response():
    print('---------Server: Client connected')

    # Start background thread for job updates only once
    global notification_thread
    if notification_thread.is_alive():
        print('---------Server: Notification thread already running')
    else:
        print('---------Server: Starting notification thread')
        notification_thread = socketio.start_background_task(GetJobProgress, current_app._get_current_object())
    
    # Show job bars if active
    redis = Redis()
    queue = Queue(connection=redis)
    running_registry = StartedJobRegistry(queue=queue)
    if running_registry.get_job_ids():
        socketio.emit('show running job bar')

@socketio.on('disconnect')
def disconnect_response():
    print('---------Server: Client disconnected')


    

