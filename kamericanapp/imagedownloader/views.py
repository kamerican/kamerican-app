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
        download(twitter_URL_list)
        return redirect(url_for('dashboard.route_index'))
    else:
        return render_template('imagedownloader.html', form=form)
    
def download(twitter_URL_list):
    redis = Redis()
    queue = Queue(connection=redis)
    image_downloader = ImageDownloader()

    #image_downloader.DownloadFromListOfTwitterURLs(twitter_URL_list)
    #job = queue.enqueue(image_downloader.DownloadFromListOfTwitterURLs, twitter_URL_list)
    queue.enqueue_call(func=image_downloader.tempfunc)
    return




    
    
    
    