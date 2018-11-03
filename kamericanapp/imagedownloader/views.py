from flask import render_template, flash, redirect, url_for, request, jsonify
from kamericanapp import db
from kamericanapp.imagedownloader import bp
from kamericanapp.imagedownloader.forms import LinksForm
from kamericanapp.imagedownloader.logic import ImageDownloader
import time

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
    image_downloader = ImageDownloader()
    task = image_downloader.long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@bp.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


