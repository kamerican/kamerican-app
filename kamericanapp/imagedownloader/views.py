from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, Response
from kamericanapp import db
from kamericanapp.imagedownloader import bp_imagedownloader
from kamericanapp.imagedownloader.forms import LinksForm
from kamericanapp.imagedownloader.logic import ImageDownloader
import time

from rq import Queue
from redis import Redis
from rq.job import Job

@bp_imagedownloader.route('/imagedownloader', methods=['GET', 'POST'])
def imagedownloader():
    form = LinksForm()
    if form.validate_on_submit():
        queue = Queue(connection=Redis())
        
        twitter_URL_list = form.links.data.splitlines()
        image_downloader = ImageDownloader()
        #image_downloader.DownloadFromListOfTwitterURLs(twitter_URL_list)
        #job = queue.enqueue(image_downloader.DownloadFromListOfTwitterURLs, twitter_URL_list)
        job = queue.enqueue(image_downloader.tempfunc)
        

        return redirect(url_for('dashboard.index'))
    else:
        return render_template('imagedownloader.html', form=form)
    
