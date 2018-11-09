from flask_socketio import send, emit
from kamericanapp import socketio
import time
from rq import Queue
from redis import Redis
from rq.registry import StartedJobRegistry




@socketio.on('message')
def receive_message(message):
    print("message received: " + message)

@socketio.on('json')
def handle_json(json):
    pass

@socketio.on('connect')
def connect_response():
    print('Client connected')

@socketio.on('disconnect')
def disconnect_response():
    print('Client disconnected')

@socketio.on('start receiving notifications')
def stream_notifications():
    ### FIND A WAY TO ONLY CALL THIS ONCE, OR FIND A WAY TO BREAK OUT OF THE INFINITE LOOP
    print('@@@ ENTERING NOTIFICATION STREAM @@@')
    
    queue = Queue(connection=Redis())
    registry = StartedJobRegistry(queue=queue)
    print(queue)
    print(queue.jobs)
    print(registry)
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
        

