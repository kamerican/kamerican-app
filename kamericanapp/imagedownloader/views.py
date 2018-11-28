from flask import render_template, redirect, url_for
from kamericanapp.imagedownloader import bp_imagedownloader
from kamericanapp.imagedownloader.forms import LinksForm
from kamericanapp.imagedownloader.logic import ImageDownloader

from rq import Queue
from redis import Redis

def async_download(twitter_URL_list):
    """Initiate async download using redis queue worker."""
    image_downloader = ImageDownloader()
    result = image_downloader.download_from_list_of_twitter_urls(twitter_URL_list)
    return result
    
@bp_imagedownloader.route('/imagedownloader', methods=['GET', 'POST'])
def route_imagedownloader():
    """Route to Image Downloader page."""
    form = LinksForm()
    if form.validate_on_submit():
        twitter_URL_list = form.links.data.splitlines()
        
        redis = Redis()
        queue = Queue(connection=redis)

        queue.enqueue_call(
            func=async_download,
            args=(twitter_URL_list,),
        )
        return redirect(url_for('dashboard.route_index'))
    else:
        return render_template('imagedownloader.html', form=form)
    




    
    
    
    