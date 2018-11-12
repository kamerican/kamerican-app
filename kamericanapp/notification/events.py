from kamericanapp.notification import bp_notification
from rq import Queue
from redis import Redis
from rq.job import Job
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from kamericanapp import socketio

from threading import Thread
import time
# consider using threading.Event to control
notification_thread = Thread()

def GetJobProgress():
    redis = Redis()
    queue = Queue(connection=redis)
    showing_running_job_bar = False
    toggle_on_running_job_bar = False
    toggle_off_running_job_bar = False

    running_registry = StartedJobRegistry(queue=queue)
    finished_registry = FinishedJobRegistry(queue=queue)

    while True:
        time.sleep(2)
        running_msg = "Currently running jobs:"
        running_job_id_list = running_registry.get_job_ids()
        #print(running_job_id_list)

        if running_job_id_list:
            # Get all job progress and emit update
            for job_id in running_job_id_list:
                running_msg += "<br>Job ID: {}".format(job_id)
                job = Job.fetch(id=job_id, connection=redis)
                #print(job)
                #print("meta: ", job.meta)
                if 'progress' in job.meta:
                    #print(job.meta['progress'])
                    running_msg += "...progress = {}".format(job.meta['progress'])


            #print('Server: Emitting: ' + running_msg)
            socketio.emit('update job progress', {'progress': running_msg})
            
            toggle_on_running_job_bar = True


        else:
            # Check for completed jobs and emit result to completed alert bar
            toggle_off_running_job_bar = True



        if showing_running_job_bar and toggle_off_running_job_bar:
            toggle_off_running_job_bar = False
            toggle_on_running_job_bar = False
            showing_running_job_bar = False
            print('Server: Hide running job bar')
            socketio.emit('hide running job bar')
        elif not showing_running_job_bar and toggle_on_running_job_bar:
            toggle_off_running_job_bar = False
            toggle_on_running_job_bar = False
            showing_running_job_bar = True
            print('Server: Show running job bar')
            socketio.emit('show running job bar')

@socketio.on('message')
def receive_message(message):
    print("Client: " + message)

@socketio.on('json')
def handle_json(json):
    pass

@socketio.on('connect')
def connect_response():
    print('Server: Client connected')
    global notification_thread
    if notification_thread.is_alive():
        print('Server: Notification thread is still running')
    else:
        print('Server: Starting notification thread')
        notification_thread = socketio.start_background_task(GetJobProgress)
    
    registry = StartedJobRegistry(queue=Queue(connection=Redis()))
    if registry:
        socketio.emit('show job progress notification bar')

@socketio.on('disconnect')
def disconnect_response():
    print('Server: Client disconnected')


    

#print('@@@@@@@@@@@@@2 loading context processor @@@@@@@@@@@@@@@')
# this doesn't work rofl, jinja2 doesn't find get_running_job_ids
'''
@bp_notification.context_processor
def utility_processor():
    def get_running_job_ids():
        registry = StartedJobRegistry(queue=Queue(connection=Redis()))
        #if not registry:
        return registry.get_job_ids()
    print(get_running_job_ids)
    return dict(get_running_job_ids=get_running_job_ids)
'''