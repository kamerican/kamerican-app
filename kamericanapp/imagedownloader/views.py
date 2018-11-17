from flask import render_template, redirect, url_for
from kamericanapp.imagedownloader import bp_imagedownloader
from kamericanapp.imagedownloader.forms import LinksForm
from kamericanapp.imagedownloader.logic import ImageDownloader

from rq import Queue
from redis import Redis

@bp_imagedownloader.route('/imagedownloader', methods=['GET', 'POST'])
def route_imagedownloader():
    form = LinksForm()
    if form.validate_on_submit():
        twitter_URL_list = form.links.data.splitlines()
        run_local = form.run_local.data
        
        redis = Redis()
        queue = Queue(connection=redis)
        '''
        if run_local:
            queue = Queue(is_async=False, connection=redis)
        else:
            queue = Queue(connection=redis)
        '''
        queue.enqueue_call(
            func=async_download,
            args=(twitter_URL_list,),
        )
        return redirect(url_for('dashboard.route_index'))
    else:
        return render_template('imagedownloader.html', form=form)
    
def async_download(twitter_URL_list):
    image_downloader = ImageDownloader()
    result = image_downloader.DownloadFromListOfTwitterURLs(twitter_URL_list)
    return result



    
    
    
    