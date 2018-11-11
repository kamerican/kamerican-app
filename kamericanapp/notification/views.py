from kamericanapp.notification import bp_notification
from rq import Queue
from redis import Redis
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from kamericanapp import socketio

from threading import Thread
import time
# consider using threading.Event to control
notification_thread = Thread()

'''
class NotificationThread(Thread):
    def __init__(self):
        self.delay = 1
        super(NotificationThread, self).__init__()
    def run(self):
        self.GetJobProgress()
    def GetJobProgress(self):
        while True:
            time.sleep(self.delay)
            registry = StartedJobRegistry(queue=Queue(connection=Redis()))

            if registry:
                socketio.emit('newnumber', {'number': number}, namespace='/test')
            else:
                socketio.emit('hide job progress notification bar')
'''

#notification_thread = NotificationThread()
#notification_thread.is_alive()
#notification_thread.start()

def GetJobProgress():
    while True:
        time.sleep(2)

        running_registry = StartedJobRegistry(queue=Queue(connection=Redis()))
        running_msg = "Running job ids:"
        finished_registry = FinishedJobRegistry(queue=Queue(connection=Redis()))
        

        if running_registry:
            # Get all job progress and emit update
            for job_id in running_registry.get_job_ids():
                running_msg += "<br>{}".format(job_id)                    
            
            print('Server: Emitting: ' + running_msg)
            socketio.emit('update job progress', {'progress': running_msg})
            
            print('Server: Show job progress notification bar')
            socketio.emit('show job progress notification bar')
            
            #socketio.emit('newnumber', {'number': number}, namespace='/test')
        else:
            # Check for completed jobs and emit result to completed alert bar
            print('Server: Hide job progress notification bar')
            socketio.emit('hide job progress notification bar')
        
        

def stream_notifications():
    ### FIND A WAY TO ONLY CALL THIS ONCE, OR FIND A WAY TO BREAK OUT OF THE INFINITE LOOP
    print('@@@ ENTERING NOTIFICATION STREAM @@@')
    
    queue = Queue(connection=Redis())
    registry = StartedJobRegistry(queue=queue)
    #print(queue)
    print(queue.jobs)
    #print(registry)
    print(registry.get_job_ids())
    
    while True:
        message = ""
        # Update image downloader progress
        #for job_id in registry.get_job_ids():
            # fix this if needed @@@ job.refresh()
        job_id_list = registry.get_job_ids()
        
        if job_id_list:
            message = "RQ worker: " + job_id_list[0]
            print('message to send: ' + message)
            socketio.emit('notification', {'data': message})
        time.sleep(4)



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