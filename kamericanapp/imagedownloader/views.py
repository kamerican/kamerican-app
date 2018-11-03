from flask import render_template, flash, redirect, url_for, request, jsonify
from kamericanapp import db
from kamericanapp.imagedownloader import bp
from kamericanapp.imagedownloader.forms import LinksForm
from kamericanapp.imagedownloader.logic import ImageDownloader
import time
#
#from kamericanapp import celery
from rq import Queue, get_current_job
from redis import Redis
from rq.job import Job


import random

@bp.route('/imagedownloader', methods=['GET', 'POST'])
def imagedownloader():
    form = LinksForm()
    if form.validate_on_submit():
        time_start = time.time()
        total_number_of_images = 0

        twitter_URL_list = form.links.data.splitlines()

        image_downloader = ImageDownloader()

        for twitter_URL in twitter_URL_list:
            image_downloader.Download(twitter_URL)
            total_number_of_images += 1
        

        
        time_end = time.time()
        print("Wrote " + str(total_number_of_images) + " images to disk.")
        print("Process took " + str(time_end - time_start) + " seconds.")
        return redirect(url_for('dashboard.index'))
    else:
        return render_template('imagedownloader.html', form=form)
    
@bp.route('/longtask', methods=['POST'])
def longtask():
    redis_conn = Redis()
    q = Queue(connection=redis_conn)



    #print('starting long_task!!! :)')
    task = q.enqueue(long_task)
    #print('finish starting the long_task...')
    #print(task)
    #print(jsonify({}), 202, {'Location': url_for('imagedownloader.taskstatus', task_id=task.id)})
    return jsonify({}), 202, {'Location': url_for('imagedownloader.taskstatus', task_id=task.id)}


@bp.route('/status/<task_id>')
def taskstatus(task_id):
    #print(task_id)

    redis_conn = Redis()
    #print(redis_conn)

    task = Job.fetch(task_id, connection=redis_conn)
    task.refresh()
    #print(task)
    #time.sleep(5)
    #print(task.meta)

    #state = task.meta['state']

    if 'state' not in task.meta or task.meta['state'] == 'PENDING':
        # job did not start yet
        response = {
            'state': 'PENDING',
            'current': 0,
            'total': 1,
            'status': 'Pending...',
        }
    elif task.meta['state'] != 'FAILURE':
        response = {
            'state': task.meta['state'],
            'current': task.meta['meta']['current'],
            'total': task.meta['meta']['total'],
            'status': task.meta['meta']['status'],
        }
        if task.is_finished:
            response = {
                'state': 'COMPLETE',
                'current': task.result['current'],
                'total': task.result['total'],
                'status': task.result['status'],
                'result': task.result['result'],
            }
    else:
        # something went wrong in the background job
        response = {
            'state': task.meta['state'],
            'current': 1,
            'total': 1,
            'status': task.meta['meta']['status'],  # this is the exception raised (?, changed)
        }
    print(response)
    return jsonify(response)


def long_task():
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(4, 20)

    task = get_current_job()
    print(task)
    if task is None:
        print('ERROR @@@ TASK NOT FOUND')

    print('ENTER FOR LOOP')

    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                            random.choice(adjective),
                                            random.choice(noun))
        task.meta['state'] = 'PROGRESS'
        task.meta['meta'] = {'current': i, 'total': total, 'status': message}
        task.save_meta()
        print(i, task.meta)
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}
